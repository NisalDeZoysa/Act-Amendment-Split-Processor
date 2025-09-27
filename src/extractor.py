import json
import time
import logging
from pathlib import Path
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFExtractor:
    def __init__(self, output_dir="output/extracted"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_text(self, pdf_path: str) -> str:
        """Extracts structured text from PDF using Docling."""
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        doc_converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)},
        )

        start_time = time.time()
        result = doc_converter.convert(pdf_path)
        logger.info(f"Converted {pdf_path} in {time.time() - start_time:.2f} sec")

        base_name = Path(pdf_path).stem
        txt_path = self.output_dir / f"{base_name}.txt"
        json_path = self.output_dir / f"{base_name}.json"
        md_path = self.output_dir / f"{base_name}.md"

        raw_text = result.document.export_to_text()
        txt_path.write_text(raw_text, encoding="utf-8")
        md_path.write_text(result.document.export_to_markdown(), encoding="utf-8")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result.document.export_to_dict(), f, indent=2)

        return raw_text
