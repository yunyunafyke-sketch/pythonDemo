import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
print(os.environ.get("OPENAI_API_KEY"))


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model="gpt-5.3-codex",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)