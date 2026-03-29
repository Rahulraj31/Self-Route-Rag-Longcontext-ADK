import asyncio
import csv
import os
import uuid
from typing import Tuple, Optional

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ..agent import root_agent
from .eval_metrics import judge_agent, EvalMetrics
from .test_data import TEST_CASES


APP_NAME = "self_route_eval"
USER_ID = "eval_user"
SESSION_ID = "eval_session"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)


# -----------------------------
# Get final answer + route
# -----------------------------
async def get_final_answer_and_route(query: str) -> Tuple[str, Optional[str]]:

    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    final_answer = ""
    route_taken = None

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):

        # capture routing decision
        if event.actions and event.actions.state_delta:
            delta = event.actions.state_delta

            if "rag_eval" in delta:
                decision_obj = delta["rag_eval"]

                if isinstance(decision_obj, dict):
                    decision = decision_obj.get("decision")
                else:
                    decision = decision_obj.decision

                if decision == "answerable":
                    route_taken = "rag"
                else:
                    route_taken = "long_context"

        # capture final response
        if event.is_final_response():
            if event.content and event.content.parts:
                final_answer = event.content.parts[0].text

    return final_answer.strip(), route_taken


# -----------------------------
# Judge
# -----------------------------
async def judge_answer(
    query: str,
    ground_truth: str,
    candidate: str
) -> EvalMetrics:

    prompt = f"""
User Query:
{query}

Ground Truth:
{ground_truth}

Candidate Answer:
{candidate}
"""

    judge_session_id = f"judge_{uuid.uuid4()}"

    await session_service.create_session(
        app_name="judge",
        user_id="judge_user",
        session_id=judge_session_id
    )

    judge_runner = Runner(
        agent=judge_agent,
        app_name="judge",
        session_service=session_service
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    async for event in judge_runner.run_async(
        user_id="judge_user",
        session_id=judge_session_id,
        new_message=content
    ):

        if event.actions and event.actions.state_delta:
            delta = event.actions.state_delta

            if "eval_result" in delta:
                result = delta["eval_result"]

                if isinstance(result, dict):
                    return EvalMetrics(**result)

                return result

    raise RuntimeError("Judge failed")


# -----------------------------
# Main Eval Loop
# -----------------------------
async def run_evals():

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    test_dir = os.path.dirname(__file__)
    os.makedirs(test_dir, exist_ok=True)

    csv_file = os.path.join(test_dir, "evaluation_results.csv")

    print("\nStarting Self-Route Evaluation")
    print(f"Results will be saved to: {csv_file}")

    total = len(TEST_CASES)

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Category",
            "Query",
            "Ground Truth",
            "Expected Route",
            "Actual Route",
            "Route Correct",
            "Final Answer",
            "Correctness",
            "Faithfulness",
            "Completeness",
            "Judge Reasoning"
        ])

        file.flush()

        for idx, test in enumerate(TEST_CASES, start=1):

            print(f"\n[{idx}/{total}] {test['category']}")
            print("Query:", test["query"])

            final_answer, actual_route = await get_final_answer_and_route(
                test["query"]
            )

            expected_route = test["expected_route"]
            ground_truth = test["ground_truth"]

            route_correct = actual_route == expected_route

            metrics = await judge_answer(
                test["query"],
                ground_truth,
                final_answer
            )

            writer.writerow([
                test["category"],
                test["query"],
                ground_truth,
                expected_route,
                actual_route,
                route_correct,
                final_answer,
                metrics.correctness,
                metrics.faithfulness,
                metrics.completeness,
                metrics.reasoning
            ])

            file.flush()

            print("Expected Route:", expected_route)
            print("Actual Route:", actual_route)
            print("Route Correct:", route_correct)
            print("Scores:",
                  metrics.correctness,
                  metrics.faithfulness,
                  metrics.completeness
                  )


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    asyncio.run(run_evals())
