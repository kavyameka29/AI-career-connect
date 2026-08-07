"""
AI Service — Mistral API Integration
-------------------------------------
Handles all communication with the Mistral AI API.
Provides specialized methods for career chat, resume review,
and interview question generation.
"""

import json
from flask import current_app
from mistralai import Mistral


def _get_client() -> Mistral:
    """Return a configured Mistral client."""
    api_key = current_app.config["MISTRAL_API_KEY"]
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set. Add it to your .env file.")
    return Mistral(api_key=api_key)


def _build_messages(system_prompt: str, history: list[dict]) -> list[dict]:
    """Build the messages array expected by the Mistral Chat API."""
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages


# ── Career Chat ──────────────────────────────────────────────────────

CAREER_SYSTEM_PROMPT = """You are an expert AI Career Advisor. You help users with:
- Career path guidance and planning
- Job search strategies
- Skill development recommendations
- Industry insights and trends
- Professional networking advice

Be encouraging, specific, and actionable in your advice. 
Always consider the user's background and goals."""


def get_career_response(conversation_history: list[dict]) -> str:
    """Send conversation history to Mistral and return the assistant reply."""
    client = _get_client()
    model = current_app.config["MISTRAL_MODEL"]

    messages = _build_messages(CAREER_SYSTEM_PROMPT, conversation_history)

    response = client.chat.complete(model=model, messages=messages)
    return response.choices[0].message.content


# ── Resume Review ────────────────────────────────────────────────────

RESUME_SYSTEM_PROMPT = """You are an expert Resume Reviewer. Analyze the resume and provide:
1. Overall impression (2-3 sentences)
2. Strengths (bullet points)
3. Areas for improvement (bullet points)
4. Specific suggestions for each section
5. ATS (Applicant Tracking System) compatibility tips

Format your response clearly with markdown headings."""


def get_resume_suggestions(resume_text: str) -> str:
    """Analyze resume text and return improvement suggestions."""
    client = _get_client()
    model = current_app.config["MISTRAL_MODEL"]

    messages = [
        {"role": "system", "content": RESUME_SYSTEM_PROMPT},
        {"role": "user", "content": f"Please review this resume:\n\n{resume_text}"},
    ]

    response = client.chat.complete(model=model, messages=messages)
    return response.choices[0].message.content


# ── Interview Question Generation ───────────────────────────────────

INTERVIEW_SYSTEM_PROMPT = """You are an expert Interview Coach. Generate realistic interview 
questions for the specified role. For each question, provide:
1. The question itself
2. Why the interviewer asks it
3. A brief tip on how to answer

Return the result as a JSON array of objects with keys: 
"question", "purpose", "tip".
Generate exactly 5 questions."""


def get_interview_questions(job_role: str, difficulty: str = "medium") -> list[dict]:
    """Generate interview questions for a specific role and difficulty."""
    client = _get_client()
    model = current_app.config["MISTRAL_MODEL"]

    messages = [
        {"role": "system", "content": INTERVIEW_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Generate {difficulty}-level interview questions "
                f"for the role: {job_role}"
            ),
        },
    ]

    response = client.chat.complete(model=model, messages=messages)
    raw = response.choices[0].message.content

    # Try to parse JSON from the response
    try:
        # Strip markdown code fences if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except (json.JSONDecodeError, IndexError):
        # Fallback: return raw text wrapped in a list
        return [{"question": raw, "purpose": "", "tip": ""}]
