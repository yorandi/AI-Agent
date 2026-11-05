import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError("api key not found, please provide correct path")


parser = argparse.ArgumentParser(description="chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [
    {"role": "user", "content": args.user_prompt},
]

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
response = client.chat.completions.create(
    model="nvidia/nemotron-3.5-super-vl:free", messages=messages
)

prompt_tokens = response.usage.prompt_tokens
response_tokens = response.usage.completion_tokens
message = response.choices[0].message.content
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print("Prompt tokens:", prompt_tokens)
    print("Response tokens:", response_tokens)
    print(message)
else:
    print(message)
