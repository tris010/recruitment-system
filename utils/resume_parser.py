import os
import PyPDF2
from docx import Document

def parse_resume(file_path: str) -> str:
    """
    Extract text from a resume file (PDF, DOCX, or TXT).
    """
    if not os.path.exists(file_path):
        return ""

    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    try:
        if ext == ".pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        elif ext == ".docx":
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            # Assume plain text for other extensions
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
    except Exception as e:
        print(f"Error parsing resume {file_path}: {e}")
        return ""

    return text.strip()
