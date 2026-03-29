from google.adk.agents import Agent
from ..instructions import RAG_AGENT_INSTRUCTION
from ..config import AGENT_MODEL

rag_answer_agent = Agent(
    name="rag_answer_agent",
    model=AGENT_MODEL,
    instruction=RAG_AGENT_INSTRUCTION,
    output_key="rag_answer"
)