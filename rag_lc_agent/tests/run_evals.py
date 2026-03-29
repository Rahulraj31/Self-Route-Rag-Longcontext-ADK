import asyncio
import csv
import sys
import os

# Append project root to path so we can cleanly import our agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rag_lc_agent.agent import root_agent
from rag_lc_agent.tests.eval_metrics import judge_agent
from rag_lc_agent.tests.test_data import TEST_CASES
from google.adk.agents import InvocationContext

async def run_evaluation():
    test_dir = os.path.dirname(__file__)
    os.makedirs(test_dir, exist_ok=True)
    csv_file = os.path.join(test_dir, "evaluation_results.csv")
    
    print(f"Starting Automated Pipeline. Results will be saved to: {csv_file}")
    
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Query", "Final Answer", "Correctness", "Faithfulness", "Completeness", "Judge Reasoning"])

        for i, test in enumerate(TEST_CASES):
            print(f"\n--- Running Test {i+1}/9: {test['category']} ---")
            print(f"Query: {test['query']}")
            
            # --- 1. Get Answer from Router ---
            ctx = InvocationContext()
            ctx.new_message = test["query"]
            
            final_answer_parts = []
            
            try:
                async for event in root_agent.run_async(ctx):
                    # In ADK, event.text contains the streaming message chunks
                    if hasattr(event, 'text') and event.text:
                        final_answer_parts.append(event.text)
                
                final_answer = "".join(final_answer_parts).strip()
                print(f"Answer Generated. Length: {len(final_answer)} characters.")
                
            except Exception as e:
                print(f"Error invoking root_agent: {e}")
                final_answer = f"ERROR: {str(e)}"

            # --- 2. Evaluate using LLM Judge ---
            judge_ctx = InvocationContext()
            judge_input = f"User Query: {test['query']}\nExpected Ground Truth: {test['ground_truth']}\nCandidate Answer: {final_answer}"
            judge_ctx.set_agent_state("llm_judge_agent", {"eval_input": judge_input})
            
            eval_result = None
            try:
                async for event in judge_agent.run_async(judge_ctx):
                    if getattr(event, 'actions', None) and getattr(event.actions, 'state_delta', None):
                        if "eval_result" in event.actions.state_delta:
                            eval_result = event.actions.state_delta["eval_result"]
            except Exception as e:
                print(f"Error running evaluator judge: {e}")
                
            if eval_result:
                print(f"Scores -> Correctness: {eval_result.correctness}/5 | Faithfulness: {eval_result.faithfulness}/5 | Completeness: {eval_result.completeness}/5")
                writer.writerow([
                    test["category"], 
                    test["query"], 
                    final_answer, 
                    eval_result.correctness, 
                    eval_result.faithfulness, 
                    eval_result.completeness, 
                    eval_result.reasoning
                ])
                # Flush the file buffer so we see results immediately during long runs
                file.flush()
            else:
                print("Evaluation failed to extract metrics.")
                writer.writerow([test["category"], test["query"], final_answer, 0, 0, 0, "Evaluation parsing failed."])
                file.flush()
                
    print("\n--- Evaluation Complete! ---")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
