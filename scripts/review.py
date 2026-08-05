from google import genai
import os
import sys
import time

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

IGNORE_FILES = [
    ".github/workflows/ai-review.yml"
]

pipeline_files = []

with open("changed_files.txt", "r") as f:
    changed_files = [line.strip() for line in f.readlines()]

for file in changed_files:

    if file in IGNORE_FILES:
        continue

    is_pipeline_file = (
        file == "Jenkinsfile"
        or file == ".gitlab-ci.yml"
        or file == "azure-pipelines.yml"
        or file == "buildspec.yml"
        or file == "Dockerfile"
        or file.endswith(".tf")
        or file.startswith(".github/workflows/")
        or "helm" in file.lower()
        or "k8s" in file.lower()
        or "kubernetes" in file.lower()
    )

    if is_pipeline_file:
        pipeline_files.append(file)

print("\nDetected CI/CD Files:")
for file in pipeline_files:
    print(f" - {file}")

if not pipeline_files:
    print("\nNo CI/CD files found.")
    sys.exit(0)

review_failed = False

for file in pipeline_files:

    print(f"\n{'='*60}")
    print(f"Reviewing: {file}")
    print(f"{'='*60}\n")

    try:

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = f"""
You are a Senior DevOps Engineer.

Review this CI/CD file.

Check:
1. Syntax errors
2. Invalid keywords
3. YAML formatting issues
4. Common CI/CD mistakes

Respond ONLY in this format:

STATUS: PASS

or

STATUS: FAIL

Issue:
<issue>

Fix:
<fix>

File:

{content}
"""

        response = None

        for attempt in range(3):

            try:

                print(f"Gemini attempt {attempt + 1}")

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                break

            except Exception as e:

                print(f"Attempt {attempt + 1} failed: {str(e)}")

                if attempt < 2:
                    time.sleep(10)
                else:
                    raise

        result = response.text.strip()

        print(result)

        if "STATUS: FAIL" in result.upper():
            review_failed = True

    except Exception as e:

        print(f"\nERROR reviewing {file}")
        print(str(e))

        review_failed = True

if review_failed:

    print("\n❌ CI/CD Review Failed")
    sys.exit(1)

print("\n✅ CI/CD Review Passed")
