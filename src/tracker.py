import json
from pathlib import Path
from src.extractor import PDFExtractor
from src.ai_parser import generate_amendment_summary

class AIAmendmentTracker:
    def __init__(self, base_pdf: str, amendment_pdfs: list, output_dir="output/json"):
        self.base_pdf = base_pdf
        self.amendment_pdfs = amendment_pdfs
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extractor = PDFExtractor()

    def run(self):
        base_text = self.extractor.extract_text(self.base_pdf)
        results = []

        for amendment_pdf in self.amendment_pdfs:
            amendment_text = self.extractor.extract_text(amendment_pdf)
            summary = generate_amendment_summary(base_text, amendment_text)
            summary["base_act"] = Path(self.base_pdf).name
            summary["amendment"] = Path(amendment_pdf).name

            # Save JSON output
            output_path = self.output_dir / f"{Path(amendment_pdf).stem}_changes.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=4, ensure_ascii=False)

            results.append(summary)
        return results
