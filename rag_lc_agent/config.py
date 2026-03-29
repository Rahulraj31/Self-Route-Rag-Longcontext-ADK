import os
from dotenv import load_dotenv

# Use absolute path so .env loads correctly from any working directory
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path)

_base_dir = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.abspath(os.path.join(_base_dir, os.getenv("DOCS_FOLDER", "./docs")))

AGENT_MODEL = os.getenv("AGENT_MODEL", "gemini-2.5-flash")
DATASTORE_RESOURCE = os.getenv("DATASTORE_RESOURCE")

MAX_RESULTS = int(os.getenv("MAX_RESULTS", 3))
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Ensure the Project ID is available to the Google SDK for authentication
if os.getenv("GOOGLE_CLOUD_PROJECT"):
    os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GOOGLE_CLOUD_PROJECT")

if not DATASTORE_RESOURCE and SEARCH_ENGINE_ID:
    raise ValueError("Any one DATASTORE_RESOURCE or SEARCH_ENGINE_ID should be present in .env. ")
