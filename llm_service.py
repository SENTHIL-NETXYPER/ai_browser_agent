import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
def decide_action(user_prompt):
    system_prompt = """
    You are an AI agent.
    Decide what tool should be used.

    Available tools:
    1. google_search
    2. open_website

    Always respond in JSON.

    Example:
    {
      "tool": "google_search",
      "query": "AI agents"
    }
    """
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    ) 
    print("--------------------------------")
    print(response.choices[0].message.content)
    return json.loads(response.choices[0].message.content)