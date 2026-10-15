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
        "GEMINI_API_KEY not found. "
        "Add it to Render Environment Variables or your local .env file."
    )

print("Gemini API Loaded")

client = genai.Client(api_key=API_KEY)

# ============================================================
# Model Priority
# ============================================================

# Try the latest Flash model first, then fall back to other
# currently documented Flash models.
MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]


# ============================================================
# Generate Questions
# ============================================================

def generate_questions(subject, chapter, difficulty="Easy", number=5):
    prompt = f"""
You are an expert CBSE Class 10 Question Paper Setter.

Generate exactly {number} high-quality multiple-choice questions.

Subject: {subject}
Chapter: {chapter}
Difficulty: {difficulty}

Rules:
- Follow the latest relevant NCERT syllabus.
- Keep the questions at CBSE board-exam level.
- Give exactly four options for every question.
- For Medium questions, make two options plausibly similar.
- For Hard questions, make three options plausibly similar.
- For Hard difficulty, aim for about one-third HOTS, conceptual, or
  board-exam-style questions.
- For Assertion-Reason questions, format the question text neatly, for
  example:
  Assertion: ...
  Reason: ...

Return ONLY a valid JSON array. Do not include Markdown fences or any
explanation outside the JSON.

Each item in the array must follow this format:
{{
    "question": "Question text",
    "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
    ],
    "correct_answer": "A"
}}

The correct_answer value must be exactly "A", "B", "C", or "D".
"""

    last_error = None

    for model in MODELS:
        print(f"Trying Gemini model: {model}")

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            text = response.text.strip()
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

            questions = json.loads(text)

            if not isinstance(questions, list):
                raise ValueError("Gemini response was not a JSON list.")

            if len(questions) != number:
                raise ValueError(
                    f"Expected {number} questions, but received {len(questions)}."
                )

            for index, question in enumerate(questions, start=1):
                if not isinstance(question, dict):
                    raise ValueError(
                        f"Question {index} is not a JSON object."
                    )

                if not all(
                    key in question
                    for key in ("question", "options", "correct_answer")
                ):
                    raise ValueError(
                        f"Question {index} is missing a required field."
                    )

                if (
                    not isinstance(question["options"], list)
                    or len(question["options"]) != 4
                ):
                    raise ValueError(
                        f"Question {index} must have exactly four options."
                    )

                if question["correct_answer"] not in {"A", "B", "C", "D"}:
                    raise ValueError(
                        f"Question {index} has an invalid correct_answer."
                    )

            print(f"Success using {model}")
            return questions

        except Exception as e:
            last_error = e
            print(f"Model {model} failed: {e}")
            time.sleep(2)

    raise Exception(f"All Gemini models failed. Last error: {last_error}")
