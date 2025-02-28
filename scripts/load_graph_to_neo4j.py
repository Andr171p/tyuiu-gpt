import re
from pathlib import Path
from neo4j import GraphDatabase


BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "notebooks" / "ТИУ_Графовая_База_знаний.txt"

# uri = "bolt://localhost:7687"

uri = "bolt://shortline.proxy.rlwy.net:53207"

driver = GraphDatabase.driver(uri)

def clear_database(tx):
    tx.run("MATCH (n) DETACH DELETE n;")

with driver.session() as session:
    session.write_transaction(clear_database)
    print("Graph was cleared")

driver.close()


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
print(entities[1575])

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


def add_entity(tx, entity) -> None:
    print("+")
    tx.run(
        "CREATE (e:Entity {name: $name, type: $type, description: $description})",
        name=entity["name"], type=entity["type"], description=entity["description"]
    )


def add_relationship(tx, relation) -> None:
    tx.run("""
        MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
        CREATE (a)-[r:RELATION {type: $type, description: $description}]->(b)
        """,
        source=relation["source"],
        target=relation["target"],
        type=relation["type"],
        description=relation["description"]
    )


with driver.session() as session:
    for entity in entities:
        session.execute_write(add_entity, entity)

    for relation in relationships:
        session.execute_write(add_relationship, relation)

driver.close()
