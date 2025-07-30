from dotenv import load_dotenv
import os
load_dotenv(override=True)  # Force override existing env vars

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"API key found, length: {len(api_key)}")
    print(f"First 10 chars: {api_key[:10]}")
    print(f"Last 10 chars: {api_key[-10:]}")
    print(f"Contains newlines: {'Yes' if '\n' in api_key else 'No'}")
else:
    print("No API key found")