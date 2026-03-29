from typing import AsyncGenerator
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import AgentTool

# Import sub-agents
from .config import AGENT_MODEL
from .subagents.rag import rag_answer_agent
from .subagents.evaluator import evaluator_agent
from .subagents.long_context import lc_agent
from .subagents.retreiver import retriever_agent
from .instructions import ROUTER_AGENT_INSTRUCTION


# -----------------------------
# Wrapping Agent as Tools
# -----------------------------
long_context_tool = AgentTool(agent=lc_agent)
retriever_tool = AgentTool(agent=retriever_agent)
rag_answer_tool = AgentTool(agent=rag_answer_agent)
evaluator_tool = AgentTool(agent=evaluator_agent)


# -----------------------------
# ROOT ROUTER: Conversational Agent
# -----------------------------

root_agent = Agent(
    name="self_route_main_agent",
    model=AGENT_MODEL,
    instruction=ROUTER_AGENT_INSTRUCTION,
    tools=[long_context_tool, retriever_tool, rag_answer_tool, evaluator_tool]
)