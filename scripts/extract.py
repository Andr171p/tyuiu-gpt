import py2neo
from py2neo import Graph, NodeMatcher

uri = "bolt://shortline.proxy.rlwy.net:53207"

# uri = "bolt://localhost:7687"

graph_db = Graph(uri)
matcher = NodeMatcher(graph_db)
print("Connected to neo4j successfully")

def get_subgraph_by_entity_name(entity_name):
    """
    Функция находит сущность в Neo4j по имени и возвращает подграф,
    содержащий данную сущность и все связанные с ней узлы и ребра.
    """
    # Поиск узла по имени сущности
    entity_node = matcher.match("Entity").where(f"_.name = '{entity_name}'").first()

    if not entity_node:
        print(f"Сущность с именем {entity_name} не найдена.")
        return None

    # Извлечение ID сущности
    entity_id = entity_node.identity

    # Запрос для получения всех связанных узлов и рёбер
    result = graph_db.run("""
        MATCH path = (n)-[*0..1]-(:Entity {name: $entity_name})
        RETURN nodes(path) AS nodes, relationships(path) AS rels
    """, {"entity_name": entity_name})

    # Сбор данных для построения подграфа
    subgraph_nodes = {}
    subgraph_rels = {}

    for record in result:
        for node in record["nodes"]:
            subgraph_nodes[node.identity] = dict(node.items())

        for rel in record["rels"]:
            subgraph_rels[(rel.start_node.identity, rel.end_node.identity)] = dict(rel.items())

    # Построение подграфа
    from networkx import MultiDiGraph
    nx_graph = MultiDiGraph()

    for node_id, props in subgraph_nodes.items():
        nx_graph.add_node(node_id, **props)

    for (start, end), props in subgraph_rels.items():
        nx_graph.add_edge(start, end, **props)

    return nx_graph


import py2neo
from py2neo import Graph, NodeMatcher

# Установите параметры соединения с вашей базой данных Neo4j
graph_db = Graph(uri)
matcher = NodeMatcher(graph_db)

def get_subgraph_by_entity_name(entity_name):
    """
    Функция находит сущность в Neo4j по имени и возвращает подграф,
    содержащий данную сущность и все связанные с ней узлы и ребра.
    """
    # Поиск узла по имени сущности
    entity_node = matcher.match("Entity").where(f"_.name = '{entity_name}'").first()

    if not entity_node:
        print(f"Сущность с именем {entity_name} не найдена.")
        return None

    # Извлечение ID сущности
    entity_id = entity_node.identity

    # Запрос для получения всех связанных узлов и рёбер
    result = graph_db.run("""
        MATCH path = (n)-[*0..1]-(:Entity {name: $entity_name})
        RETURN nodes(path) AS nodes, relationships(path) AS rels
    """, {"entity_name": entity_name})

    # Сбор данных для построения подграфа
    subgraph_nodes = {}
    subgraph_rels = {}

    for record in result:
        for node in record["nodes"]:
            subgraph_nodes[node.identity] = dict(node.items())

        for rel in record["rels"]:
            subgraph_rels[(rel.start_node.identity, rel.end_node.identity)] = dict(rel.items())

    # Построение подграфа
    from networkx import MultiDiGraph
    nx_graph = MultiDiGraph()

    for node_id, props in subgraph_nodes.items():
        nx_graph.add_node(node_id, **props)

    for (start, end), props in subgraph_rels.items():
        nx_graph.add_edge(start, end, **props)

    return nx_graph

def display_subgraph(subgraph):
    """
    Функция выводит информацию о вершинах и рёбрах подграфа.
    """
    if subgraph is None:
        print("Не удалось создать подграф.")
        return

    # Вывод информации о вершинах
    print("\nВершины:")
    for node in subgraph.nodes.data():
        print(f"{node[0]} ({node[1].get('name', '')})")
        print(f"\tТип: {node[1].get('type', '')}")
        print(f"\tОписание: {node[1].get('description', '')}\n")

    # Вывод информации о рёбрах
    print("\nРёбра:")
    for edge in subgraph.edges.data():
        start_node = subgraph.nodes[edge[0]]
        end_node = subgraph.nodes[edge[1]]
        print(f"{start_node.get('name', '')} → {end_node.get('name', '')}")
        print(f"\tТип: {edge[2].get('type', '')}")
        print(f"\tОписание: {edge[2].get('description', '')}\n")

# Пример использования функции
entity_name = "БАЛЛЫ"
subgraph = get_subgraph_by_entity_name(entity_name)
if subgraph is not None:
    display_subgraph(subgraph)
    # Отображаем подграф
    import matplotlib.pyplot as plt
    import networkx as nx
    pos = nx.spring_layout(subgraph)
    nx.draw_networkx(subgraph, pos=pos, with_labels=True)
    plt.show()
else:
    print("Не удалось создать подграф.")