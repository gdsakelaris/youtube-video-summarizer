import os
from dotenv import load_dotenv

# Clear any existing API key from environment
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']
    print("Cleared old API key from environment")

# Force reload from .env file
load_dotenv(override=True)

# Check the new key
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"New API key loaded, length: {len(api_key)}")
    print(f"First 10 chars: {api_key[:10]}")
    print(f"Last 10 chars: {api_key[-10:]}")
else:
    print("No API key found")