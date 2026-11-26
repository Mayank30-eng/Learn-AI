# Resume Evaluator

An AI-powered batch resume evaluator that uses Groq LLM to parse job descriptions, extract resume data from PDF/DOCX files, score candidates against job requirements, and rank them.

## Project Structure

```
ResumeEvaluator/
│
├── app/
│   ├── __init__.py          # Makes app/ a Python package
│   ├── config.py            # Loads .env, creates Groq client
│   ├── schemas.py           # All Pydantic data models
│   ├── document_parser.py   # PDF and DOCX text extraction
│   ├── ai_service.py        # All LLM interactions (parse JD, parse resume, score)
│   ├── batch_processor.py   # Orchestration, display, and ranking
│   └── main.py              # Entry point
│
├── resumes/                 # Place PDF/DOCX resume files here
├── .env                     # Your API keys (never commit this!)
├── requirements.txt         # Python dependencies
├── pyproject.toml           # uv project config
└── README.md
```

## Setup

1. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Place resume files (`.pdf` or `.docx`) in the `resumes/` folder.

## Usage

Run the batch evaluator from the `ResumeEvaluator/` directory:

```bash
python -m app.main
```

## How It Works

1. **Job Description Parsing** — The LLM extracts required skills, preferred skills, experience, education, and responsibilities from the JD.
2. **Resume Parsing** — Each resume is converted to text (PDF/DOCX) and then parsed by the LLM into structured data.
3. **Scoring** — The LLM compares each parsed resume against the parsed JD and assigns a match score (0–100).
4. **Ranking** — All candidates are sorted by score, and the top 2 and bottom 2 are displayed.
