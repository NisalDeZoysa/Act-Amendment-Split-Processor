Act Amendment Tracker

A Python-based application that extracts, compares, and tracks amendments made to any legal Act using Docling for accurate PDF parsing.
The tool outputs a JSON summary showing what has changed in the Act over time, making it ideal for legal analytics, compliance, and building Graph-based RAG systems.

Features

✅ Generic Amendment Tracking
Works with any Act and any number of amendments.

✅ Accurate PDF Extraction
Uses Docling
to extract structured, clean text from PDFs.

✅ Structured JSON Output
Generates JSON files summarizing:

Amended sections, subsections, and clauses.

Old vs. new text.

Type of change (substitution, repeal, insert, etc.).

✅ Ready for Graph DB Integration
JSON outputs are designed to be stored directly in Neo4j for Graph-based RAG.

✅ Scalable Project Structure
Clean modular codebase designed for future integration into APIs, UIs, or knowledge graphs.

Project Structure
act-amendment-tracker/
│
├── data/ # Input files
│ ├── base_act.pdf # Base act (e.g., Civil Aviation Act 2010)
│ ├── amendment_1.pdf # First amendment (e.g., 2023 amendment)
│ └── amendment_2.pdf # (Optional) Additional amendments
│
├── output/
│ ├── extracted/ # Raw extracted text & metadata from Docling
│ └── json/ # Final tracked JSON changes
│
├── src/
│ ├── **init**.py
│ ├── extractor.py # Docling-powered PDF text extraction
│ ├── parser.py # Parses and identifies amendments
│ ├── tracker.py # Orchestrates extraction & comparison
│ ├── utils.py # Common helper functions (optional)
│
├── main.py # CLI entry point
├── requirements.txt # Dependencies
└── README.md # Project documentation

Installation

1. Clone the Repository
   git clone https://github.com/your-username/act-amendment-tracker.git
   cd act-amendment-tracker

2. Create Virtual Environment
   python -m venv venv
   source venv/bin/activate # Linux / Mac
   venv\Scripts\activate # Windows

3. Install Dependencies
   pip install -r requirements.txt
