from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri: str, username: str, password: str, database: str = "neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.database = database
        self.driver.verify_connectivity()
        print("✅ Connected to Neo4j Aura")

    def close(self):
        self.driver.close()
        print("✅ Neo4j connection closed")

    def insert_chapter_section(self, act_name: str, chapter: str, section: str, content: str):
        def _insert(tx, act_name, chapter, section, content):
            tx.run(
                """
                MERGE (a:Act {name: $act_name})
                MERGE (c:Chapter {name: $chapter})
                MERGE (s:Section {number: $section, content: $content})
                MERGE (a)-[:HAS_CHAPTER]->(c)
                MERGE (c)-[:HAS_SECTION]->(s)
                """,
                act_name=act_name,
                chapter=chapter,
                section=section,
                content=content
            )
        with self.driver.session(database=self.database) as session:
            session.execute_write(_insert, act_name, chapter, section, content)
