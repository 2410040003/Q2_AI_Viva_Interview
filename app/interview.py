
import uuid

from app.llm import (
    generate_question,
    evaluate_answer,
    generate_assessment
)

# Temporary in-memory session storage
sessions = {}


def start_interview(student_name, subject, difficulty):
    session_id = str(uuid.uuid4())

    first_question = generate_question(
        subject,
        difficulty,
        []
    )

    sessions[session_id] = {
        "student_name": student_name,
        "subject": subject,
        "difficulty": difficulty,
        "current_question": first_question,
        "results": []
    }

    return {
        "session_id": session_id,
        "question_number": 1,
        "question": first_question
    }


def submit_answer(session_id, answer):
    if session_id not in sessions:
        raise ValueError("Invalid session ID")

    session = sessions[session_id]
    results = session["results"]

    if len(results) >= 3:
        raise ValueError("Interview is already completed")

    current_question = session["current_question"]

    score, feedback = evaluate_answer(
        current_question,
        answer,
        session["subject"]
    )

    results.append({
        "question": current_question,
        "answer": answer,
        "score": score,
        "feedback": feedback
    })

    question_number = len(results)

    if question_number == 3:
        return {
            "session_id": session_id,
            "question_number": question_number,
            "score": score,
            "feedback": feedback,
            "next_question": None,
            "completed": True
        }

    previous_questions = [
        item["question"] for item in results
    ]

    next_question = generate_question(
        session["subject"],
        session["difficulty"],
        previous_questions
    )

    session["current_question"] = next_question

    return {
        "session_id": session_id,
        "question_number": question_number,
        "score": score,
        "feedback": feedback,
        "next_question": next_question,
        "completed": False
    }


def get_interview_report(session_id):
    if session_id not in sessions:
        raise ValueError("Invalid session ID")

    session = sessions[session_id]
    results = session["results"]

    if len(results) != 3:
        raise ValueError("Interview is not completed yet")

    average_score = round(
        sum(item["score"] for item in results) / 3,
        2
    )

    assessment = generate_assessment(
        session["student_name"],
        session["subject"],
        average_score,
        results
    )

    return {
        "session_id": session_id,
        "student_name": session["student_name"],
        "subject": session["subject"],
        "total_questions": 3,
        "average_score": average_score,
        "overall_assessment": assessment["overall_assessment"],
        "improvement_areas": assessment["improvement_areas"],
        "results": results
    }
