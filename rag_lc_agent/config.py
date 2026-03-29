import os
from dotenv import load_dotenv

# Load config
load_dotenv()

AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-2.5-flash")
DATASTORE_RESOURCE = os.getenv("DATASTORE_RESOURCE")
DOCS_FOLDER = os.getenv("DOCS_FOLDER", "./docs")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", 3))

if not DATASTORE_RESOURCE:
    raise ValueError("DATASTORE_RESOURCE missing in .env")
