import re
import networkx as nx


with open(
        file=r"C:\Users\andre\IdeaProjects\TyuiuNeuralChatAgent\notebooks\ТИУ Сущности База знаний.txt",
        mode="r",
        encoding="utf-8"
) as file:
    data = file.read()

print(len(data))

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

print(len(entities))

relationships: list[dict] = []
for match in relationship_pattern.finditer(data):
    source, target, relation_type, relation_description = match.groups()
    relationships.append({
        "source": source.strip(),
        "target": target.strip(),
        "type": relation_type.strip(),
        "description": relation_description.strip()
    })
print(len(relationships))

G = nx.DiGraph()

for entity in entities:
    G.add_node(
        entity["name"],
        type=entity["type"],
        description=entity["description"]
    )

for relation in relationships:
    G.add_edge(
        relation["source"],
        relation["target"],
        type=relation["type"],
        description=relation["description"]
    )


from py2neo import Graph

graph_db = Graph("bolt://localhost:7687")
graph_db.delete_all()

for node in G.nodes.data():
    name = node[0]
    properties = {
        'type': node[1].get('type'),
        'description': node[1].get('description')
    }
    graph_db.run(f"CREATE (:Entity {{name:'{name}', type:'{properties['type']}', description:'{properties['description']}'}})")

for edge in G.edges.data():
    source = edge[0]
    target = edge[1]
    properties = {
        'type': edge[2]['type'],
        'description': edge[2]['description']
    }
    query = f"MATCH (a:Entity {{name:'{source}'}}), (b:Entity {{name:'{target}'}}) CREATE (a)-[:RELATIONSHIP {{type:'{properties['type']}', description:'{properties['description']}'}}]->(b)"
    graph_db.run(query)