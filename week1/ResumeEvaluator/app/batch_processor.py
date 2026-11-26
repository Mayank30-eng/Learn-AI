"""
batch_processor.py — Orchestration, Display & Ranking
======================================================

PURPOSE:
    The "conductor" that ties everything together:
      1. Parse the job description (one LLM call)
      2. Iterate through a folder of resumes
      3. For each resume: extract text → parse via LLM → score via LLM
      4. Rank all candidates and display top/bottom results

WHY A SEPARATE FILE?
    The batch_processor knows the *workflow* (what order to do things,
    how to rank). It does NOT know how to read a PDF or call an LLM —
    it delegates those to document_parser and ai_service respectively.
    This means you can change the ranking logic without touching AI
    code, or change the LLM provider without touching orchestration.

IMPORTS FROM app/:
    ai_service      → parse_job_description, parse_resume, final_score
    document_parser → read_resume

EXPORTS:
    display_evaluation, process_batch
"""

import time
from pathlib import Path

from app.ai_service import parse_job_description, parse_resume, final_score
from app.document_parser import read_resume


def display_evaluation(result):
    """Print a formatted evaluation report for a single candidate."""
    details = result.details

    print("\n" + "=" * 50)
    print("         RESUME EVALUATION REPORT")
    print("=" * 50)

    print(f"Candidate: {details.candidate_name}")
    print(f"Match Score: {result.score:.1f}%")

    print("\nMatching Skills:")
    for skill in details.matching_skills:
        print(f"  + {skill}")

    print("\nMissing Skills:")
    for skill in details.missing_skills:
        print(f"  - {skill}")

    print("\nExperience Requirement:")

    if details.experience_requirement_met is True:
        print("  Met")
    elif details.experience_requirement_met is False:
        print("  Not Met")
    else:
        print("  Could Not Determine")

    print("\nFinal Verdict:")
    print(f"  {details.final_verdict}")

    print("=" * 50)


def process_batch(job_description, resume_folder_path):
    """
    Full batch-processing pipeline:
      1. Parse the job description via LLM
      2. Loop through every PDF/DOCX in the resume folder
      3. Parse each resume and score it against the job
      4. Rank candidates and display top 2 / bottom 2

    Parameters:
        job_description (str): The raw job description text.
        resume_folder_path (str or Path): Path to the folder containing resumes.

    The time.sleep(5) calls between LLM requests are preserved to
    respect Groq's rate limits on free-tier accounts.
    """
    # Step 1: Parse the job description into a structured object
    job = parse_job_description(job_description)
    print(f"Job parsed: {job.role}")
    print(f"Minimum experience: {job.minimum_experience}")
    print(f"Education requirements: {job.education_requirements}")

    # Step 2: Process each resume in the folder
    resume_folder = Path(resume_folder_path)
    all_results = []

    for file_path in resume_folder.iterdir():
        if file_path.suffix.lower() not in [".pdf", ".docx"]:
            continue

        print("\nProcessing:", file_path.name)

        # Extract text from the file
        resume_text = read_resume(file_path)
        if not resume_text or not resume_text.strip():
            print(f"Skipping {file_path.name}: No readable text found.")
            continue

        # LLM call 1: Parse the resume
        parsed_resume = parse_resume(resume_text)
        time.sleep(5)

        # LLM call 2: Score the resume against the job
        result = final_score(job, parsed_resume)
        time.sleep(5)

        # Display this candidate's evaluation
        display_evaluation(result)

        # Collect results for ranking
        all_results.append({
            "name": parsed_resume.name,
            "score": result.score,
            "details": result.details
        })

    # Step 3: Rank candidates by score (highest first)
    all_results.sort(
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    # Step 4: Display top 2 and bottom 2 candidates
    top_2 = all_results[:2]
    worst_2 = all_results[-2:]

    print("\nTOP 2 CANDIDATES")
    for candidate in top_2:
        print(
            candidate["name"],
            "-",
            candidate["score"],
            "%"
        )
        print(candidate["details"])

    print("\nLOWEST 2 CANDIDATES")
    for candidate in worst_2:
        print(
            candidate["name"],
            "-",
            candidate["score"],
            "%"
        )
        print(candidate["details"])
