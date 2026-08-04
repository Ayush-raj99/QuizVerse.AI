import json
import os
import time
from pathlib import Path

from dotenv import dotenv_values
from google import genai

# ============================================================
# Load API Key
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / ".env"

# Load local .env (works on your laptop)
env = dotenv_values(env_path)

# First try Render environment variable,
# then fall back to local .env
API_KEY = os.getenv("GEMINI_API_KEY") or env.get("GEMINI_API_KEY")

if not API_KEY:
    raise Exception(
        "❌ GEMINI_API_KEY not found. "
        "Add it to Render Environment Variables or your local .env file."
    )

print("✅ Gemini API Loaded")

client = genai.Client(api_key=API_KEY)

# ============================================================
# Model Priority
# ============================================================

MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest"
]


# ============================================================
# Generate Questions
# ============================================================

def generate_questions(subject, chapter, difficulty="Easy", number=5):

    prompt = f"""
You are an expert CBSE Class 10 Question Paper Setter.

Generate exactly {number} HIGH QUALITY Multiple Choice Questions.

Subject: {subject}
Chapter: {chapter}
Difficulty: {difficulty}

Rules:

- Latest NCERT only
- Board level quality
- Four options
- if the question level is medium then the 2 options are similar so that student confuse to answer
- if the question level is hard then the 3 options are similar to each other so the student confuse to answer
- if the question level is hard then the 1/3 of the number of is HOTS , conceptual and Repeated question in 10th board exam 
- if the question based on assertion and reason then change line to the output to the user is neat and clean 
  something like this Assertion:.
                    Reason:

Return ONLY valid JSON.

Each question must follow this format:

{
  "question": "Question text",
    "diagram_svg": "",
      "options": [
          "Option A",
              "Option B",
                  "Option C",
                      "Option D"
                        ],
                          "correct_answer": "A"
                          }

                          IMPORTANT:

                          If the question DOES NOT require a figure,

                          set

                          "diagram_svg":""

                          If the question REQUIRES a figure,

                          generate valid SVG code.

                          Example:

                          "diagram_svg":"<svg width='220' height='220'> ... </svg>"

                          The SVG must be complete and ready to insert into HTML.

                          Never explain the SVG.

                          Never wrap it inside markdown.

                          Return ONLY JSON.
"""
    last_error = None

    for model in MODELS:

        print(f"🔄 Trying {model}")

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            text = response.text.strip()

            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

            questions = json.loads(text)

            if not isinstance(questions, list):
                raise Exception("Invalid JSON")

            print(f"✅ Success using {model}")

            return questions

        except Exception as e:

            last_error = e

            print(f"❌ {model} failed")

            time.sleep(2)

    raise Exception(f"All Gemini models failed.\n\n{last_error}")