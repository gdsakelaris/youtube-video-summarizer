import os
from dotenv import load_dotenv

print("=== Before load_dotenv ===")
print(f"OPENAI_API_KEY in os.environ: {'OPENAI_API_KEY' in os.environ}")
if 'OPENAI_API_KEY' in os.environ:
    print(f"Current value: {os.environ['OPENAI_API_KEY'][:10]}...")

print("\n=== Loading .env file ===")
result = load_dotenv(override=True)
print(f"load_dotenv returned: {result}")

print("\n=== After load_dotenv ===")
print(f"OPENAI_API_KEY in os.environ: {'OPENAI_API_KEY' in os.environ}")
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"API key found, length: {len(api_key)}")
    print(f"First 10 chars: {api_key[:10]}")
else:
    print("No API key found")

print(f"\n=== Direct file check ===")
try:
    with open('.env', 'r') as f:
        content = f.read()
        print(f"File content length: {len(content)}")
        print(f"File content: {repr(content[:100])}")
except Exception as e:
    print(f"Error reading .env file: {e}")