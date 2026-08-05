from google import genai
import os

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

with open(".github/workflows/deploy.yml", "r") as f:
    pipeline = f.read()

prompt = f"""
You are a CI/CD expert.

Review the following pipeline.

Check:
1. Syntax issues
2. Invalid keywords
3. YAML formatting issues

Respond in this format:

STATUS: PASS

or

STATUS: FAIL

Then explain why.

Pipeline:

{pipeline}
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print(response.text)
