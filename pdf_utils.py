import pdfplumber
from typing import List, Dict

def extract_sections_from_pdfs(pdf_dir: str, documents: List[str]) -> List[Dict]:
    all_sections = []
    for doc in documents:
        path = f"{pdf_dir}/{doc}"
        with pdfplumber.open(path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text and text.strip():
                    lines = [line.strip() for line in text.split('\n') if line.strip()]
                    section_title = lines[0][:100] if lines else f"Page {page_num}"
                    all_sections.append({
                        'document': doc,
                        'page_number': page_num,
                        'section_title': section_title,
                        'text': text
                    })
    return all_sections 