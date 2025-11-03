import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=OPENAI_API_KEY)

def call_openai_as_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Gọi OpenAI API (SDK 2.x) bằng Chat Completions, ép về JSON.
    """
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},  # GPT-5/4o hỗ trợ JSON mode
    )
    text = completion.choices[0].message.content
    return json.loads(text)
