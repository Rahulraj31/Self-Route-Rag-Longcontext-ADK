import asyncio
import csv
import sys
import os
import uuid

# Append project root to path so we can cleanly import our agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rag_lc_agent.agent import root_agent
from rag_lc_agent.tests.eval_metrics import judge_agent
from rag_lc_agent.tests.test_data import TEST_CASES

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

APP_NAME = "self_route_eval"
USER_ID = "eval_user"

import re

async def get_final_answer_and_eval(runner: Runner, session_id: str, query: str):
    """Invoke the root agent and collect both final text and the internal eval state."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_parts = []
    internal_eval = None
    
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content
    ):
        # 1. Collect text
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_parts.append(part.text)
        
        # 2. Capture internal rag_eval state delta if present
        if (getattr(event, 'actions', None)
                and getattr(event.actions, 'state_delta', None)
                and "rag_eval" in event.actions.state_delta):
            internal_eval = event.actions.state_delta["rag_eval"]
            
    full_text = "".join(final_parts).strip()
    # Remove internal JSON leakage from the text stream for the user-facing answer
    clean_text = re.sub(r'\{.*?"decision".*?\}', '', full_text, flags=re.DOTALL).strip()
    return clean_text, internal_eval

async def get_eval_scores(judge_runner: Runner, session_id: str, query: str, ground_truth: str, answer: str):
    """Invoke the LLM judge and return the EvalMetrics output."""
    judge_input = f"User Query: {query}\nExpected Ground Truth: {ground_truth}\nCandidate Answer: {answer}"
    content = types.Content(role="user", parts=[types.Part(text=judge_input)])
    async for event in judge_runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content
    ):
        if (getattr(event, 'actions', None)
                and getattr(event.actions, 'state_delta', None)
                and "eval_result" in event.actions.state_delta):
            return event.actions.state_delta["eval_result"]
    return None

async def run_evaluation():
    test_dir = os.path.dirname(__file__)
    os.makedirs(test_dir, exist_ok=True)
    csv_file = os.path.join(test_dir, "evaluation_results.csv")

    print(f"Starting Automated Pipeline. Results will be saved to: {csv_file}")

    session_service = InMemorySessionService()
    main_runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    judge_runner = Runner(agent=judge_agent, app_name=APP_NAME, session_service=session_service)

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Added 'Eval Agent Response' column per user request
        writer.writerow(["Category", "Query", "Final Answer", "Eval Agent Response", "Correctness", "Faithfulness", "Completeness", "Judge Reasoning"])

        for i, test in enumerate(TEST_CASES):
            print(f"\n--- Running Test {i+1}/9: {test['category']} ---")
            print(f"Query: {test['query']}")

            session_id = f"eval_session_{uuid.uuid4().hex}"
            await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)

            # --- 1. Get Answer and Internal Eval ---
            try:
                final_answer, internal_eval = await get_final_answer_and_eval(main_runner, session_id, test["query"])
                print(f"Answer Generated. Length: {len(final_answer)} chars.")
            except Exception as e:
                print(f"Error invoking root_agent: {e}")
                final_answer, internal_eval = f"ERROR: {str(e)}", None

            # --- 2. Evaluate using LLM Judge ---
            judge_session_id = f"judge_session_{uuid.uuid4().hex}"
            await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=judge_session_id)

            try:
                eval_result = await get_eval_scores(judge_runner, judge_session_id, test["query"], test["ground_truth"], final_answer)
            except Exception as e:
                print(f"Error running evaluator judge: {e}")
                eval_result = None

            if eval_result:
                c = eval_result.get("correctness", 0) if isinstance(eval_result, dict) else eval_result.correctness
                f = eval_result.get("faithfulness", 0) if isinstance(eval_result, dict) else eval_result.faithfulness
                comp = eval_result.get("completeness", 0) if isinstance(eval_result, dict) else eval_result.completeness
                reason = eval_result.get("reasoning", "") if isinstance(eval_result, dict) else eval_result.reasoning
                
                print(f"Scores -> Correctness: {c}/5 | Faithfulness: {f}/5 | Completeness: {comp}/5")
                writer.writerow([test["category"], test["query"], final_answer, str(internal_eval), c, f, comp, reason])
            else:
                print("Evaluation failed to extract metrics.")
                writer.writerow([test["category"], test["query"], final_answer, str(internal_eval), 0, 0, 0, "Evaluation parsing failed."])

            file.flush()

    print("\n--- Evaluation Complete! Results saved. ---")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
