from neo4j import GraphDatabase


# uri = "bolt://localhost:7687"

uri = "bolt://shortline.proxy.rlwy.net:53207"

driver = GraphDatabase.driver(uri)

def fetch_graph_by_entity(tx, entity_name):
    query = """
    MATCH (a:Entity {name: $entity_name})-[r]->(b)
    RETURN a, r, b
    """
    result = tx.run(query, entity_name=entity_name)
    return result.data()

entity_name = "ЭКОНОМИЧЕСКОЕ_УПРАВЛЕНИЕ_ПРЕДПРИЯТИЯМИ_ТОПЛИВНО-ЭНЕРГЕТИЧЕСКОГО_КОМПЛЕКСА"

with driver.session() as session:
    graph_data = session.execute_read(fetch_graph_by_entity, entity_name)
    print(graph_data)
    for record in graph_data:
        source = record['a']['name']
        target = record['b']['name']
        relation_type = record['r']
        relation_description = record['r']
        print(f"Сущность: {source} -> {target} | Тип связи: {relation_type} | Описание: {relation_description}")

driver.close()