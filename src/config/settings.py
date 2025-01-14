import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LYRICS_BATCH_SIZE = int(os.getenv('LYRICS_BATCH_SIZE'))
if not LYRICS_BATCH_SIZE:
    print("LYRICS_BATCH_SIZE not found in environment variables. Using default value of 15.")
    LYRICS_BATCH_SIZE = 15

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

