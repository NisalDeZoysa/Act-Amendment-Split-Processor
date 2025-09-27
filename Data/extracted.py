import re
import json
from pathlib import Path
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path: str) -> str:
    """Extract text from PDF into a single string."""
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def split_by_chapters_and_sections(text: str):
    """
    Splits the Act into chapters and sections.
    Each section contains all its text until the next section begins.
    """
    # --- Split into chapters (CHAPTER I, II, III ...)
    chapters = re.split(r"(CHAPTER\s+[IVXLC]+\s+[^\n]*)", text)

    structured = []
    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i].strip()
        chapter_content = chapters[i+1] if (i+1) < len(chapters) else ""

        # --- Split by sections (a section begins with number + dot)
        matches = list(re.finditer(r"(?m)^(\d+)\.", chapter_content))

        for idx, match in enumerate(matches):
            section_num = match.group(1)
            start = match.end()

            if idx + 1 < len(matches):
                end = matches[idx + 1].start()
                section_text = chapter_content[start:end].strip()
            else:
                section_text = chapter_content[start:].strip()

            structured.append({
                "chapter": chapter_title,
                "section": section_num,
                "content": section_text
            })

    return structured


if __name__ == "__main__":
    pdf_file = "14-2010_E.pdf"

    # Extract full text
    raw_text = pdf_to_text(pdf_file)

    # Save full text
    Path("Civil_Aviation_Act.txt").write_text(raw_text, encoding="utf-8")

    # Split into chapters & sections
    structured_act = split_by_chapters_and_sections(raw_text)

    # Save structured JSON
    Path("Civil_Aviation_Act_structured.json").write_text(
        json.dumps(structured_act, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("✅ Done: JSON with chapter, section, and full section text")
