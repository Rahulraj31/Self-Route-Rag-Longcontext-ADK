from google.adk.agents import Agent

from ..config import DOCS_FOLDER, AGENT_MODEL
from ..tool import load_docs
from ..instructions import LC_AGENT_INSTRUCTION

lc_agent = Agent(
    name="long_context_agent",
    model=AGENT_MODEL,
    instruction=LC_AGENT_INSTRUCTION.format(full_context=load_docs(DOCS_FOLDER))
)
