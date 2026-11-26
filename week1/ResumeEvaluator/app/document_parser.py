"""
document_parser.py — File Reading (PDF & DOCX)
================================================

PURPOSE:
    Pure file I/O — reads bytes from disk and returns plain text.
    No AI, no Groq client, no business logic.

WHY A SEPARATE FILE?
    Separation of concerns: reading a PDF has nothing to do with
    calling an LLM. By isolating file I/O, you can:
      - Test PDF/DOCX extraction without mocking any AI service
      - Swap pypdf for another PDF library without touching AI code
      - Reuse these functions in completely different projects

IMPORTS FROM app/:
    Nothing — this module is fully self-contained.

EXPORTS:
    read_pdf, read_docx, read_resume
"""

from pathlib import Path
from pypdf import PdfReader
from docx import Document


def read_pdf(file_path):
    """Extract all text from a PDF file, page by page."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def read_docx(file_path):
    """Extract text from a DOCX file (paragraphs + table cells)."""
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"
    return text


def read_resume(file_path):
    """
    Router function: picks the correct reader based on file extension.

    Returns the extracted text, or None if the file type is unsupported.
    file_path should be a pathlib.Path object.
    """
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None
