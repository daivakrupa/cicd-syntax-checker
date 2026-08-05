# from google import genai
# import os

# client = genai.Client(
#     api_key=os.environ["GEMINI_API_KEY"]
# )

# with open(".github/workflows/deploy.yml") as f:
#     pipeline = f.read()

# prompt = f"""
# Review this CI/CD pipeline.

# Check:
# 1. Syntax issues
# 2. Invalid keywords
# 3. YAML formatting

# Return PASS or FAIL.

# Pipeline:

# {pipeline}
# """

# response = client.models.generate_content(
#     model="gemini-1.5-flash",
#     contents=prompt
# )

# print(response.text)

from google import genai
import os

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

for model in client.models.list():
    print(model.name)
