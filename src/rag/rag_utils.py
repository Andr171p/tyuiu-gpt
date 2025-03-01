from typing import List, Union

from pathlib import Path
import networkx as nx
from py2neo.cypher import Cursor

from langchain_core.documents import Document


def load_txt(file_path: Union[Path, str]) -> str:
    with open(
            file=file_path,
            mode="r",
            encoding="utf-8",
    ) as file:
        return file.read()


def extract_page_content(documents: List[Document]) -> List[str]:
    return [document.page_content for document in documents]


def format_docs(documents: List[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def select_top_k_documents(documents: List[Document], k: int = 5) -> List[Document]:
    return documents[:k]


def build_subgraph_from_cursor(cursor: Cursor) -> nx.MultiDiGraph:
    subgraph_nodes = {}
    subgraph_rels = {}
    for record in cursor:
        for node in record["nodes"]:
            subgraph_nodes[node.identity] = dict(node.items())
        for rel in record["rels"]:
            subgraph_rels[(rel.start_node.identity, rel.end_node.identity)] = dict(rel.items())
    graph = nx.MultiDiGraph()
    for node_id, props in subgraph_nodes.items():
        graph.add_node(node_id, **props)
    for (start, end), props in subgraph_rels.items():
        graph.add_edge(start, end, **props)
    return graph

