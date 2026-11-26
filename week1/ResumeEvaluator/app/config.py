"""
config.py — Configuration & Client Setup
=========================================

PURPOSE:
    This is the single source of truth for all configuration.
    It loads environment variables, validates that required secrets
    exist, and creates the shared Groq client that every AI function
    will reuse.

WHY A SEPARATE FILE?
    If you ever switch from Groq to OpenAI or Gemini, you only change
    this one file. No other module knows or cares how the client is
    created — they just import `client` and `model`.

EXPORTS:
    client  — the initialized Groq API client
    model   — the model identifier string
"""

import os
from dotenv import load_dotenv
from groq import Groq

# load_dotenv() searches from the current working directory upward.
# When you run `python -m app.main` from the ResumeEvaluator/ folder,
# it finds the .env file sitting right there.
load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

# One client shared across the entire application.
# Creating multiple clients wastes memory and connections.
client = Groq(api_key=my_api_key)

# The LLM model identifier. Change this single variable to switch models.
model = "openai/gpt-oss-120b"
