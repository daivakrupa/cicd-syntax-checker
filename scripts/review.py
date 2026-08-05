import os
import google.generativeai as genai

genai.configure(
    api_key=os.environ["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

with open(".github/workflows/deploy.yml", "r") as f:
    pipeline = f.read()

prompt = f"""
You are a CI/CD reviewer.

Review this pipeline.

Check:
1. Syntax issues
2. Invalid keywords
3. YAML indentation issues

Return only:

PASS

or

FAIL

with explanation.

Pipeline:

{pipeline}
"""

response = model.generate_content(prompt)

print(response.text)
