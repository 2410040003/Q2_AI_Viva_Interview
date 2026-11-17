

\# AI-Based Viva Interview System



An AI-powered technical viva interview system developed using FastAPI and Groq LLM.



\## Features

\- Generates three technical viva questions.

\- Evaluates student answers using AI.

\- Provides scores and feedback.

\- Maintains interview session history.

\- Generates a final performance report.



\## Technologies

\- Python

\- FastAPI

\- Groq LLM API

\- Pytest

\- GitHub Actions

\- Docker



\## Run Locally



Install dependencies:



pip install -r requirements.txt



Start server:



uvicorn app.main:app --reload



Open:



http://127.0.0.1:8000/docs



\## Run Tests



pytest -v



\## Run with Docker



docker build -t ai-viva-interview .



docker run --rm -p 8000:8000 --env-file .env ai-viva-interview



