import json
from pathlib import Path

from .pdf_utils import pdf_to_text, split_by_chapters_and_sections
from .neo4j_utils import Neo4jHandler


def process_act(act_folder: Path, neo4j_handler: Neo4jHandler):
    """
    Process a single Act folder:
    - extract base PDF
    - convert to text & structured JSON
    - insert into Neo4j
    """
    act_name = act_folder.name
    base_pdf_path = act_folder / "base"
    base_pdfs = list(base_pdf_path.glob("*.pdf"))

    if not base_pdfs:
        print(f"⚠️ No base PDF found for {act_name}, skipping...")
        return

    base_pdf = base_pdfs[0]
    print(f"📄 Processing Act: {act_name}, Base PDF: {base_pdf.name}")

    # Extract text
    raw_text = pdf_to_text(base_pdf)
    Path(act_folder / f"{act_name}.txt").write_text(raw_text, encoding="utf-8")

    # Split into structured JSON
    structured_act = split_by_chapters_and_sections(raw_text)
    Path(act_folder / f"{act_name}_structured.json").write_text(
        json.dumps(structured_act, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    # Insert into Neo4j
    for entry in structured_act:
        neo4j_handler.insert_chapter_section(
            act_name=act_name,
            chapter=entry["chapter"],
            section=entry["section"],
            content=entry["content"]
        )

    print(f"✅ Finished processing {act_name}")
