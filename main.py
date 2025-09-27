from pathlib import Path
from src.neo4j_utils import Neo4jHandler
from src.process_act import process_act

# Neo4j Aura credentials
URI = "neo4j+s://d598a1e7.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "LgL2XKWqhZERu6KdDpmN1s6dDp1tuCPQZTwlWOfueJw"

# Initialize Neo4j handler
neo4j_handler = Neo4jHandler(URI, USERNAME, PASSWORD)

# Root Acts folder
ACTS_DIR = Path("Acts")

# Process all Acts
for act_folder in ACTS_DIR.iterdir():
    if act_folder.is_dir():
        process_act(act_folder, neo4j_handler)

# Close Neo4j connection
neo4j_handler.close()
