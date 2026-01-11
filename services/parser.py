from io import BytesIO
from pdfminer.high_level import extract_text
from docx import Document

def parse_resume_text(content: bytes, content_type: str) -> str:
    if content_type == "application/pdf":
        bio = BytesIO(content)
        return extract_text(bio)
    if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        bio = BytesIO(content)
        doc = Document(bio)
        return "\n".join([p.text for p in doc.paragraphs])
    if content_type == "text/plain":
        return content.decode("utf-8")
    return ""
