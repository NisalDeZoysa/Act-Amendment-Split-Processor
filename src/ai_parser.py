import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch the API key
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_amendment_summary(base_text: str, amendment_text: str) -> dict:
    """
    Uses ChatGPT API to intelligently compare base act & amendment
    and return structured JSON of changes.
    """
    prompt = f"""
You are a legal AI assistant. Compare the following BASE ACT and AMENDMENT.
Extract all changes as a structured JSON.

BASE ACT:
\"\"\" 
{base_text[:20000]}  # limit token usage
\"\"\"

AMENDMENT:
\"\"\" 
{amendment_text[:15000]}
\"\"\"

Instructions:
1. Identify sections, subsections, clauses mentioned in the amendment.
2. Detect whether it’s a substitution, repeal, insertion, or modification.
3. Include both OLD TEXT (from base act) and NEW TEXT (from amendment) if applicable.
4. Output in **strict JSON** with this schema:

{{
  "base_act": "string",
  "amendment": "string",
  "changes": [
    {{
      "section": "number",
      "subsection": "number | null",
      "clause": "string | null",
      "change_type": "substitution | repeal | insertion | modification",
      "old_text": "string | null",
      "new_text": "string"
    }}
  ]
}}
    """

    response = client.responses.create(
        model="gpt-4.1",  # You can use gpt-4o-mini for cheaper calls
        input=prompt,
        temperature=0,
        max_output_tokens=2000
    )

    # Parse JSON safely
    try:
        json_output = json.loads(response.output_text)
    except Exception:
        json_output = {
            "error": "Failed to parse model output",
            "raw": response.output_text
        }

    return json_output
