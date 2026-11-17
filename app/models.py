
from pydantic import BaseModel, Field
from typing import List, Optional


class StartInterviewRequest(BaseModel):
    student_name: str = Field(min_length=2, max_length=100)
    subject: str = Field(min_length=2, max_length=100)
    difficulty: str = Field(
        default="medium",
        pattern="^(easy|medium|hard)$"
    )


class StartInterviewResponse(BaseModel):
    session_id: str
    question_number: int
    question: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str = Field(min_length=2, max_length=3000)


class SubmitAnswerResponse(BaseModel):
    session_id: str
    question_number: int
    score: int
    feedback: str
    next_question: Optional[str] = None
    completed: bool


class QuestionResult(BaseModel):
    question: str
    answer: str
    score: int
    feedback: str


class InterviewReport(BaseModel):
    session_id: str
    student_name: str
    subject: str
    total_questions: int
    average_score: float
    overall_assessment: str
    improvement_areas: List[str]
    results: List[QuestionResult]
