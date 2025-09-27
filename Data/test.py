from neo4j import GraphDatabase

URI = "neo4j+s://d598a1e7.databases.neo4j.io"
USERNAME = "neo4j"
PASSWORD = "LgL2XKWqhZERu6KdDpmN1s6dDp1tuCPQZTwlWOfueJw"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

try:
    driver.verify_connectivity()
    print("✅ Connected to Neo4j Aura successfully!")
except Exception as e:
    print("❌ Connection failed:", e)
finally:
    driver.close()
