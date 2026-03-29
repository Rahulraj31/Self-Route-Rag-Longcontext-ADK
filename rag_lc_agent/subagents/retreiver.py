from ..config import DATASTORE_RESOURCE, MAX_RESULTS, AGENT_MODEL, SEARCH_ENGINE_ID
from google.adk.agents import Agent
from google.adk.tools import VertexAiSearchTool
from ..instructions import RETRIEVER_AGENT_INSTRUCTION

retriever_agent = Agent(
    name="retriever_agent",
    model=AGENT_MODEL,
    tools=[
        VertexAiSearchTool(
            search_engine_id=SEARCH_ENGINE_ID,
            max_results=MAX_RESULTS
        )
    ],
    instruction=RETRIEVER_AGENT_INSTRUCTION,
    output_key="retrieved_chunks"
)