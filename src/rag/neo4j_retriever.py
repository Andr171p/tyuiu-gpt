from typing import Any, List, Optional

import networkx as nx
from py2neo import Graph, NodeMatcher

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.utils.graph import build_subgraph_from_cursor


class Neo4jRetriever(BaseRetriever):
    def __init__(
            self,
            uri: str,
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._graph = Graph(uri)
        self._node_matcher = NodeMatcher(self._graph)

    def get_subgraph_by_entity_name(
            self,
            entity_name: str
    ) -> nx.MultiDiGraph | None:
        cursor = self._graph.run(
            cypher="""
            MATCH path = (n)-[*0..1]-(:Entity {name: $entity_name})
            RETURN nodes(path) AS nodes, relationships(path) AS rels
            """,
            parameters={"entity_name": entity_name}
        )
        subgraph = build_subgraph_from_cursor(cursor)
        return subgraph

    def _get_relevant_documents(
            self,
            query: str,
            *,
            run_manager: CallbackManagerForRetrieverRun
    ) -> List[Optional[Document]]:
        subgraph = self.get_subgraph_by_entity_name(query)
        if subgraph is None:
            return []
        documents = []
        for node in subgraph.nodes.data():
            node_id = node[0]
            node_props = node[1]
            node_name = node_props.get('name', '')

            connections = []
            for edge in subgraph.edges.data():
                start_node = subgraph.nodes[edge[0]]
                end_node = subgraph.nodes[edge[1]]
                if start_node.get('name', '') == node_name or end_node.get('name', '') == node_name:
                    connection_info = f"{start_node.get('name', '')} → {end_node.get('name', '')} (Тип: {edge[2].get('type', '')}, Описание: {edge[2].get('description', '')})"
                    connections.append(connection_info)

            page_content = f"Сущность: {node_name}\nТип: {node_props.get('type', '')}\nОписание: {node_props.get('description', '')}\n"
            if connections:
                page_content += "Связи:\n" + "\n".join(connections)

            document = Document(
                page_content=page_content,
                metadata={"node_id": node_id, **node_props}
            )
            documents.append(document)

        return documents


'''from src.config import settings
graph = Graph(settings.neo4j.uri)
node_matcher = NodeMatcher(graph)
retriever = Neo4jRetriever(graph, node_matcher)
docs = retriever.invoke("ДОПОЛНИТЕЛЬНЫЕ_БАЛЛЫ")
for doc in docs:
    print(doc.page_content)'''
