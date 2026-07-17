import json
import time
from pathlib import Path

from dotenv import dotenv_values
from google import genai

# ============================================================
# Load API Key
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / ".env"

env = dotenv_values(env_path)

API_KEY = env.get("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ GEMINI_API_KEY not found in .env")

print("✅ Gemini API Loaded")

client = genai.Client(api_key=API_KEY)

# ============================================================
# Model Priority
# ============================================================

MODELS = [
    "gemini-3.5-flash",
    "gemini-3.1-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-2.0-flash"
]


# ============================================================
# Generate Questions
# ============================================================

def generate_questions(subject, chapter, difficulty="Easy", number=5):

    prompt = f"""
You are an expert CBSE Class 10 Question Paper Setter.

Generate exactly {number} HIGH QUALITY Multiple Choice Questions.

Subject:
{subject}

Chapter:
{chapter}

Difficulty:
{difficulty}

==========================
IMPORTANT INSTRUCTIONS
==========================

1. Base every question on the latest NCERT textbook.

2. Use NCERT terminology.

3. Use NCERT keywords.

4. Use scientific words exactly as used in NCERT.

5. Questions should feel like Board Exam questions.

6. Mix Conceptual + Assertion Style + Application + Reasoning.

7. Wrong options should look believable.

8. Do NOT repeat questions.

9. Every question must have exactly four options.

10. Only ONE option should be correct.

11. Return ONLY JSON.

12. Never explain anything.

13. Never use Markdown.

14. Never use ```json.

15. answer_index must be:

0
1
2
or
3

NOT answer text.

==========================
FORMAT
==========================

[
  {{
    "question":"Question",

    "options":[
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],

    "answer_index":0
  }}
]
"""

    last_error = None

    for model in MODELS:

        print(f"\n🔄 Trying {model}")

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            if not response.text:
                raise Exception("Empty response")

            text = response.text.strip()

            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

            questions = json.loads(text)

            if not isinstance(questions, list):
                raise Exception("Response is not a list")

            if len(questions) == 0:
                raise Exception("No questions returned")

            print(f"✅ Success using {model}")

            return questions

        except Exception as e:

            last_error = e

            print(f"❌ {model} failed")
            print(e)

            # wait before trying next model
            time.sleep(2)

    raise Exception(
        f"""

❌ All Gemini Models Failed

Last Error:

{last_error}

"""
    )