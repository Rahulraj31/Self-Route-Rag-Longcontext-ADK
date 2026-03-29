from typing import AsyncGenerator
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import AgentTool

# Import sub-agents
from .config import AGENT_MODEL
from .subagents.rag import rag_agent
from .subagents.evaluator import evaluator_agent
from .subagents.long_context import lc_agent
from .instructions import ROUTER_AGENT_INSTRUCTION

# -----------------------------
# Workflow: Sequential RAG -> Eval
# -----------------------------
rag_pipeline = SequentialAgent(
    name="rag_pipeline",
    sub_agents=[rag_agent, evaluator_agent]
)

# -----------------------------
# ROOT ROUTER: Conversational Agent
# -----------------------------

rag_pipeline_tool = AgentTool(agent=rag_pipeline)
long_context_tool = AgentTool(agent=lc_agent)


root_agent = Agent(
    name="self_route_main_agent",
    model=AGENT_MODEL,
    instruction=ROUTER_AGENT_INSTRUCTION,
    tools=[rag_pipeline_tool, long_context_tool]
)