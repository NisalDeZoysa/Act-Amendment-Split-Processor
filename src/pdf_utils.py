import re
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path: str) -> str:
    """Extract text from PDF into a single string."""
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def split_by_chapters_and_sections(text: str):
    """
    Split Act text into chapters and sections.
    Returns a list of dicts: {"chapter": ..., "section": ..., "content": ...}
    """
    chapters = re.split(r"(CHAPTER\s+[IVXLC]+\s+[^\n]*)", text)
    structured = []

    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i].strip()
        chapter_content = chapters[i+1] if (i+1) < len(chapters) else ""

        matches = list(re.finditer(r"(?m)^(\d+)\.", chapter_content))
        for idx, match in enumerate(matches):
            section_num = match.group(1)
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(chapter_content)
            section_text = chapter_content[start:end].strip()

            structured.append({
                "chapter": chapter_title,
                "section": section_num,
                "content": section_text
            })

    return structured
