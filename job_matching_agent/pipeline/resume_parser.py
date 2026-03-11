import pdfplumber
from typing import Union

class ResumeParser:
    @staticmethod
    def parse_text(text: str) -> str:
        return text.strip()

    @staticmethod
    def parse_pdf(pdf_path: str) -> str:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        return '\n'.join([p for p in pages if p])
