from google import genai
import os
import sys

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

# Read changed files
with open("changed_files.txt", "r") as f:
    changed_files = [line.strip() for line in f.readlines()]

# Detect CI/CD files
pipeline_files = []

for file in changed_files:

    if (
        file == "Jenkinsfile"
        or ".github/workflows/" in file
        or file.endswith(".gitlab-ci.yml")
        or file == "azure-pipelines.yml"
        or file == "buildspec.yml"
        or file.endswith(".tf")
        or file == "Dockerfile"
        or "helm" in file
        or "k8s" in file
    ):
        pipeline_files.append(file)

print(f"\nDetected files: {pipeline_files}\n")

if not pipeline_files:
    print("No CI/CD files changed.")
    sys.exit(0)

review_failed = False

for file in pipeline_files:

    print(f"\nReviewing: {file}\n")

    try:
        with open(file, "r") as f:
            content = f.read()

        prompt = f"""
You are a Senior DevOps Engineer.

Review this CI/CD file.

Check:
1. Syntax issues
2. Invalid keywords
3. YAML formatting issues
4. Pipeline logic mistakes

Respond ONLY in this format:

STATUS: PASS

or

STATUS: FAIL

Issue:
<issue>

Fix:
<fix>

File Content:

{content}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        result = response.text.strip()

        print(result)

        if "STATUS: FAIL" in result.upper():
            review_failed = True

    except Exception as e:
        print(f"ERROR reviewing {file}")
        print(str(e))
        review_failed = True

if review_failed:
    print("\nCI/CD Review Failed")
    sys.exit(1)

print("\nCI/CD Review Passed")
