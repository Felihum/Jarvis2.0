import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_MODEL_VERBOSITY = os.getenv("OPENAI_MODEL_VERBOSITY")
OPENAI_MODEL_REASONING = os.getenv("OPENAI_MODEL_REASONING")