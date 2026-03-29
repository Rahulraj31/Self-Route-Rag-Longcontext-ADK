from typing import Literal
from pydantic import BaseModel
from google.adk.agents import Agent

from ..config import AGENT_MODEL
from ..instructions import EVALUATOR_AGENT_INSTRUCTION

class EvalDecision(BaseModel):
    decision: Literal["answerable", "not_answerable"]

evaluator_agent = Agent(
    name="evaluator_agent",
    model=AGENT_MODEL,
    output_schema=EvalDecision,
    output_key="rag_eval",
    instruction=EVALUATOR_AGENT_INSTRUCTION
)
