from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool

from ..config import DATASTORE_RESOURCE, MAX_RESULTS, AGENT_MODEL
from ..instructions import RAG_AGENT_INSTRUCTION

rag_agent = Agent(
    name="rag_agent",
    model=AGENT_MODEL,
    tools=[VertexAiSearchTool(search_engine_id="projects/796681818226/locations/global/collections/default_collection/engines/rag-search_1774783605479", max_results=MAX_RESULTS)],
    instruction=RAG_AGENT_INSTRUCTION,
    output_key="rag_answer"
)
