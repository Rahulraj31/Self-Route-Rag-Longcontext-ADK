from pydantic import BaseModel
from google.adk.agents import Agent
from ..config import AGENT_MODEL

class EvalMetrics(BaseModel):
    correctness: int
    faithfulness: int
    completeness: int
    reasoning: str

judge_agent = Agent(
    name="llm_judge_agent",
    model=AGENT_MODEL,
    output_schema=EvalMetrics,
    output_key="eval_result",
    instruction="""You are an expert impartial AI evaluator grading a RAG-based QA system.
Your job is to evaluate the Candidate Answer against the original User Query.

You must assign a score from 1 to 5 for three metrics:
1. CORRECTNESS: (1=Completely wrong, 5=Perfectly accurate and addresses the core query)
2. FAITHFULNESS: (1=Hallucinated or made up facts, 5=Strictly relies on retrieved context or safely admits lack of info without fabricating)
3. COMPLETENESS: (1=Missed almost all parts of a multi-part question, 5=Answered every single detail asked)

Input Data:
{eval_input}

Output a strictly formatted JSON with the numerical scores and a brief reasoning justifying the grades.
"""
)
