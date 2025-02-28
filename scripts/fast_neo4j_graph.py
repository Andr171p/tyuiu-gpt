import re
from pathlib import Path
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "scripts" / "ТИУ_Entities_Relations_Passed_Scores.txt"

# uri = "bolt://localhost:7687"

uri = "bolt://shortline.proxy.rlwy.net:53207"

driver = GraphDatabase.driver(uri)

'''def clear_database(tx):
    tx.run("MATCH (n) DETACH DELETE n;")

with driver.session() as session:
    session.execute_write(clear_database)

driver.close()

print("Graph database cleared")'''


with open(FILE_PATH, mode="r", encoding="utf-8") as file:
    data = file.read()

print(f"---Size of file: {len(data)}---")


entity_pattern = re.compile(r'\(entity\|([^|]+)\|([^|]+)\|([^|]+)\)')
relationship_pattern = re.compile(r'\(relationship\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\)')


entities: list[dict] = []
for match in entity_pattern.finditer(data):
    entity_name, entity_type, entity_description = match.groups()
    entities.append({
        "name": entity_name.strip(),
        "type": entity_type.strip(),
        "description": entity_description.strip()
    })
print(f"---Count of entities: {len(entities)}---")
print(entities[15])

relationships: list[dict] = []
for match in relationship_pattern.finditer(data):
    source, target, relation_type, relation_description = match.groups()
    relationships.append({
        "source": source.strip(),
        "target": target.strip(),
        "type": relation_type.strip(),
        "description": relation_description.strip()
    })
print(f"---Count of relationships: {len(relationships)}---")


def create_entities(tx, entities) -> None:
    tx.run(
        """
        UNWIND $entities AS entity
        MERGE (e:Entity {name: entity.name})
        ON CREATE SET e.type = entity.type, e.description = entity.description
        """,
        entities=entities
    )


def create_relationships(tx, relationships) -> None:
    tx.run(
        """
        UNWIND $relationships AS rel
        MATCH (a:Entity {name: rel.source}), (b:Entity {name: rel.target})
        MERGE (a)-[r:RELATION {type: rel.type}]->(b)
        ON CREATE SET r.description = rel.description
        """,
        relationships=relationships
    )


def process_in_batches(session, data, batch_size=1000, func=None):
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        session.execute_write(func, batch)


with driver.session() as session:
    process_in_batches(session, entities, batch_size=1000, func=create_entities)
    process_in_batches(session, relationships, batch_size=1000, func=create_relationships)

driver.close()