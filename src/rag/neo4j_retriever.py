from typing import Any, List, Optional

import networkx as nx
from py2neo import Graph, NodeMatcher

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from src.utils.graph import build_subgraph_from_cursor
from src.config import settings


class Neo4jRetriever(BaseRetriever):
    def __init__(
            self,
            graph: Graph,
            node_matcher: NodeMatcher,
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self._graph = graph
        self._node_matcher = node_matcher

    def get_subgraph_by_entity_name(self, entity_name: str) -> nx.MultiDiGraph | None:
        entity_node = (
            self._node_matcher
            .match("Entity")
            .where(f"_.name = '{entity_name}'")
            .first()
        )
        if not entity_node:
            return
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
            document = Document(
                page_content=f"Сущность: {node_props.get('name', '')}\nТип: {node_props.get('type', '')}\nОписание: {node_props.get('description', '')}",
                metadata={"node_id": node_id, **node_props}
            )
            documents.append(document)

        for edge in subgraph.edges.data():
            start_node = subgraph.nodes[edge[0]]
            end_node = subgraph.nodes[edge[1]]
            document = Document(
                page_content=f"Связь: {start_node.get('name', '')} → {end_node.get('name', '')}\nТип: {edge[2].get('type', '')}\nОписание: {edge[2].get('description', '')}",
                metadata={"start_node_id": edge[0], "end_node_id": edge[1], **edge[2]}
            )
            documents.append(document)

        return documents


graph_db = Graph(settings.neo4j.uri)
matcher = NodeMatcher(graph_db)

retriever = Neo4jRetriever(graph_db, matcher)
entity_name = "ПРИКЛАДНОЕ_ПРОГРАММИРОВАНИЕ_И_КОМПЬЮТЕРНЫЕ_ТЕХНОЛОГИИ"
res = retriever.invoke(entity_name)
print(type(res))
print(res)
