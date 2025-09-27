import json
from neo4j import GraphDatabase

# -----------------------------
# Load structured JSON file
# -----------------------------
with open("Civil_Aviation_Act_structured.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# -----------------------------
# Neo4j Aura connection details
# -----------------------------
URI = "neo4j+s://d598a1e7.databases.neo4j.io"  # Replace with your Aura URI
USERNAME = "neo4j"          # Your Aura username
PASSWORD = "LgL2XKWqhZERu6KdDpmN1s6dDp1tuCPQZTwlWOfueJw"                     # Your Aura password

# Initialize driver
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

# Verify connectivity
driver.verify_connectivity()
print("✅ Connected to Neo4j Aura")

# -----------------------------
# Function to insert data
# -----------------------------
def insert_chapter_section(tx, chapter, section, content):
    tx.run(
        """
        MERGE (c:Chapter {name: $chapter})
        MERGE (s:Section {number: $section, content: $content})
        MERGE (c)-[:HAS_SECTION]->(s)
        """,
        chapter=chapter,
        section=section,
        content=content
    )

# -----------------------------
# Insert JSON data into Neo4j
# -----------------------------
with driver.session(database="neo4j") as session:
    for entry in data:
        session.execute_write(
            insert_chapter_section,
            entry["chapter"],
            entry["section"],
            entry["content"]
        )

# Close driver
driver.close()
print("✅ Data inserted into Neo4j Aura successfully!")
