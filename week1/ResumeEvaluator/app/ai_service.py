"""
ai_service.py — All LLM Interactions
======================================

PURPOSE:
    Every function that calls the Groq API lives here.
    This isolates the "AI layer" — if you switch to OpenAI or Gemini
    tomorrow, you only change this file and config.py.

WHY A SEPARATE FILE?
    The batch_processor orchestrates the workflow (which resume next,
    how to rank). The ai_service just knows how to make one LLM call
    and return structured data. This is the Single Responsibility
    Principle: each module has one reason to change.

IMPORTS FROM app/:
    config  → client, model  (the Groq client and model name)
    schemas → JobD, Resume, MatchResult  (Pydantic models for parsing)

EXPORTS:
    parse_job_description, parse_resume, final_score
"""

import json

from app.config import client, model
from app.schemas import JobD, Resume, MatchResult


def parse_job_description(job_description_text):
    """
    Send a job description to the LLM and get back a structured JobD object.

    This was previously module-level code (lines 59-113 in evaluator.py).
    Wrapping it in a function means it only runs when explicitly called,
    not when you import this module.
    """
    jobd_schema = JobD.model_json_schema()

    system_prompt = f"""
    You are an expert HR assistant.

    Your job is to analyze job descriptions and extract
    structured information from them.

    Return ONLY valid JSON matching this schema:

    {jobd_schema}
    IMPORTANT:
    Do NOT return the schema itself.
    Do NOT return fields like "properties", "title" or "type".
    Fill the schema with actual information extracted from the job description.

    If minimum experience is not mentioned, return null.
    If information for a list is missing, return an empty list.
    Do not invent information.
    """

    user_prompt = f"""
    Analyze the following job description:

    {job_description_text}
    """

    message_system = {
        "role": "system",
        "content": system_prompt
    }
    message_user = {
        "role": "user",
        "content": user_prompt
    }
    response_format = {
        "type": "json_object"
    }

    messages = [message_system, message_user]

    response = client.chat.completions.create(
        model=model, messages=messages, response_format=response_format
    )

    answer = response.choices[0].message.content
    job_data = json.loads(answer)
    job = JobD(**job_data)
    return job


def parse_resume(resume_text):
    """
    Send resume text to the LLM and get back a structured Resume object.

    The LLM prompt instructs it to look for experience, skills, education
    etc. across various heading styles (e.g., "Work History", "Employment",
    "Professional Experience" are all treated as experience sections).
    """
    resume_schema = Resume.model_json_schema()

    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """

    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """

    message_system = {
        "role": "system",
        "content": system_prompt
    }
    message_user = {
        "role": "user",
        "content": user_prompt
    }
    messages = [message_system, message_user]
    response_format = {
        "type": "json_object"
    }

    response = client.chat.completions.create(
        model=model, messages=messages, response_format=response_format
    )

    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume


def final_score(job, resume):
    """
    Compare a parsed resume against a parsed job description via the LLM.
    Returns a MatchResult with a score (0-100) and detailed breakdown.
    """
    match_schema = MatchResult.model_json_schema()

    prompt = f"""
    You are an HR recruiter.

    Compare the candidate's resume with the job description.

    JOB DESCRIPTION:
    {job.model_dump_json(indent=2)}

    CANDIDATE RESUME:
    {resume.model_dump_json(indent=2)}

    Return JSON matching this schema:

    {match_schema}

    Evaluation instructions:

    1. Calculate an overall match score between 0 and 100.
    2. Identify the candidate's name.
    3. List all relevant matching skills.
    4. List important missing skills.
    5. Determine whether the experience requirement is met.
    6. Provide a short final verdict.

    Important:
    - Follow the provided JSON schema.
    - Keep the score between 0 and 100.
    - Do not invent candidate information.
    - Use an empty list when no matching or missing skills are identified.
    - Use null when experience cannot be determined.
    - Return only valid JSON.
    """

    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    response_format = {
        "type": "json_object"
    }

    response = client.chat.completions.create(
        model=model, messages=messages, response_format=response_format
    )

    data = json.loads(response.choices[0].message.content)
    return MatchResult(**data)
