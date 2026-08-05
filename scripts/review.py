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
comments = []
review_failed = False

# Read changed files
with open("changed_files.txt", "r") as f:
    changed_files = [line.strip() for line in f.readlines()]

# Detect CI/CD files
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

# No pipeline files changed
if not pipeline_files:

    with open("review_results.md", "w") as f:
        f.write("# 🤖 AI CI/CD Review\n\n")
        f.write("No CI/CD files were modified in this PR.\n")

    sys.exit(0)

# Review files
for file in pipeline_files:

    print("\n" + "=" * 60)
    print(f"Reviewing: {file}")
    print("=" * 60)

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

                print(f"Attempt {attempt +1} failed: {str(e)}")

                if attempt < 2:
                    time.sleep(10)
                else:
                    raise

        result = response.text.strip()

        print(result)

        comments.append(
            f"""
## 📄 `{file}`

{result}

---
"""
        )

        if "STATUS: FAIL" in result.upper():
            review_failed = True

    except Exception as e:

        error_msg = f"""
## 📄 `{file}`

STATUS: FAIL

Issue:
AI review execution failed.

Fix:
{str(e)}

---
"""

        comments.append(error_msg)

        review_failed = True

# Generate PR comment file
with open("review_results.md", "w", encoding="utf-8") as f:

    f.write("# 🤖 AI CI/CD Review Report\n\n")

    if review_failed:
        f.write("## ❌ Review Failed\n\n")
    else:
        f.write("## ✅ Review Passed\n\n")

    for comment in comments:
        f.write(comment)

# Create flag file if failed
if review_failed:

    with open("review_failed.flag", "w") as f:
        f.write("failed")

    print("\n❌ CI/CD Review Failed")

else:
    print("\n✅ CI/CD Review Passed")
