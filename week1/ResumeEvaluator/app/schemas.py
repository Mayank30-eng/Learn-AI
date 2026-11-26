"""
schemas.py — Pydantic Data Models
===================================

PURPOSE:
    Defines the shape (schema) of every data structure in the project.
    Pydantic models serve three roles:
      1. Validation — reject bad data automatically
      2. Serialization — convert to/from JSON for the LLM
      3. Documentation — anyone reading this file knows exactly
         what fields exist and what types they expect

WHY A SEPARATE FILE?
    Multiple modules need these models:
      - ai_service.py uses them to parse LLM responses
      - batch_processor.py uses them to access fields for display
    If schemas lived inside ai_service.py, batch_processor would
    have to import from ai_service just for type definitions —
    creating tight coupling. A dedicated schemas file keeps
    dependencies clean.

EXPORTS:
    JobD, Experience, Resume, MatchDetails, MatchResult
"""

from pydantic import BaseModel, Field


class JobD(BaseModel):
    """Structured representation of a parsed job description."""
    role: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience: float | None = None
    education_requirements: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class Experience(BaseModel):
    """A single work experience or internship entry from a resume."""
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    """Structured representation of a parsed resume."""
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = Field(default_factory=list)
    experiences: list[Experience] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class MatchDetails(BaseModel):
    """Detailed breakdown of how a resume matches a job description."""
    candidate_name: str | None = None
    matching_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    experience_requirement_met: bool | None = None
    final_verdict: str | None = None


class MatchResult(BaseModel):
    """Final evaluation result: a score plus detailed breakdown."""
    score: float
    details: MatchDetails
