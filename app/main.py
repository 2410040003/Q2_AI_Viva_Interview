
from fastapi import FastAPI, HTTPException

from app.models import (
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    InterviewReport
)

from app.interview import (
    start_interview,
    submit_answer,
    get_interview_report
)

app = FastAPI(
    title="AI Viva Interview System",
    description="AI-powered technical viva interview with three questions",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Viva Interview System is running"
    }


@app.post(
    "/start-interview",
    response_model=StartInterviewResponse
)
def start(request: StartInterviewRequest):
    try:
        return start_interview(
            request.student_name,
            request.subject,
            request.difficulty
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Could not start interview: {str(e)}"
        )


@app.post(
    "/submit-answer",
    response_model=SubmitAnswerResponse
)
def answer(request: SubmitAnswerRequest):
    try:
        return submit_answer(
            request.session_id,
            request.answer
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not evaluate answer"
        )


@app.get(
    "/report/{session_id}",
    response_model=InterviewReport
)
def report(session_id: str):
    try:
        return get_interview_report(session_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not generate report"
        )
