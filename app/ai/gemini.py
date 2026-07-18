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
- Only one correct answer
- No duplicate questions
- Return ONLY JSON

Format:

[
  {{
    "question":"Question",
    "options":[
      "A",
      "B",
      "C",
      "D"
    ],
    "answer_index":0
  }}
]
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