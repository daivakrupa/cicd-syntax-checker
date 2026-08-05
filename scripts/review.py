from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

with open(".github/workflows/deploy.yml", "r") as f:
    pipeline = f.read()

prompt = f"""
You are a CI/CD reviewer.

Review this pipeline.

Check:
1. Syntax issues
2. Invalid keywords
3. YAML mistakes

Return ONLY:

PASS

or

FAIL
with explanation.

Pipeline:

{pipeline}
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
