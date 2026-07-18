from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.ai.gemini import generate_questions

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# ----------------------------
# Temporary Quiz Storage
# (Later replace with database)
# ----------------------------

quiz_data = []


# ----------------------------
# Dashboard
# ----------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


# ----------------------------
# Generate Page
# ----------------------------

@app.get("/generate", response_class=HTMLResponse)
async def generate_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="generate_quiz.html",
        context={}
    )


# ----------------------------
# Loading Page
# ----------------------------

@app.get("/loading", response_class=HTMLResponse)
async def loading_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="loading.html",
        context={}
    )


# ----------------------------
# API Generate Quiz
# ----------------------------

@app.post("/api/generate")
async def api_generate_quiz(

    subject: str = Form(...),
    chapter: str = Form(...),
    difficulty: str = Form(...),
    number: int = Form(...)

):

    global quiz_data

    try:

        questions = generate_questions(

            subject=subject,
            chapter=chapter,
            difficulty=difficulty,
            number=number

        )

        quiz_data = questions

        return JSONResponse(

            {

                "success": True

            }

        )

    except Exception as e:

        return JSONResponse(

            {

                "success": False,

                "error": str(e)

            },

            status_code=500

        )


# ----------------------------
# Quiz Page
# ----------------------------

@app.get("/quiz", response_class=HTMLResponse)
async def quiz_page(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="quiz.html",

        context={

            "questions": quiz_data

        }

    )


# ----------------------------
# Submit Quiz
# ----------------------------

@app.post("/submit", response_class=HTMLResponse)
async def submit_quiz(request: Request):

    form = await request.form()

    score = 0

    total = len(quiz_data)

    results = []

    for i, question in enumerate(quiz_data):

        user_answer = form.get(f"q{i}")

        correct_answer = str(question["answer_index"])

        if user_answer == correct_answer:

            score += 1

            results.append(True)

        else:

            results.append(False)

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "score": score,

            "total": total,

            "results": results,

            "questions": quiz_data

        }

    )
@app.get("/health")
async def health():
    return {"status": "ok"}