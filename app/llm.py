
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client():
    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        raise ValueError("LLM_API_KEY is missing")

    return OpenAI(
        api_key=api_key,
        base_url=os.getenv(
            "LLM_BASE_URL",
            "https://api.groq.com/openai/v1"
        )
    )


def get_model():
    return os.getenv("LLM_MODEL", "openai/gpt-oss-120b")


def generate_question(subject, difficulty, previous_questions):
    client = get_client()

    prompt = f"""
    Generate exactly one technical viva question.
    Subject: {subject}
    Difficulty: {difficulty}
    Previous questions: {previous_questions}

    Do not repeat previous questions.
    Return only the question, without numbering or explanation.
    """

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a technical viva examiner."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


def evaluate_answer(question, answer, subject):
    client = get_client()

    prompt = f"""
    Evaluate this student's technical viva answer.

    Subject: {subject}
    Question: {question}
    Student answer: {answer}

    Give a score from 0 to 10 and short constructive feedback.

    Return valid JSON only:
    {{
        "score": 0,
        "feedback": "Your feedback here"
    }}
    """

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are a fair technical examiner. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    result = json.loads(response.choices[0].message.content)

    score = max(0, min(10, int(result["score"])))
    feedback = str(result["feedback"])

    return score, feedback


def generate_assessment(student_name, subject, average_score, results):
    client = get_client()

    prompt = f"""
    Prepare a concise viva performance report.

    Student: {student_name}
    Subject: {subject}
    Average score: {average_score}/10
    Results: {json.dumps(results)}

    Return valid JSON only:
    {{
        "overall_assessment": "Short assessment",
        "improvement_areas": ["Area 1", "Area 2"]
    }}
    """

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are an academic evaluator. Return valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)
