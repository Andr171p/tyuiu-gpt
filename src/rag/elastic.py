from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.embeddings import HuggingFaceEmbeddings

from src.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name="ai-forever/sbert_large_nlu_ru",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': False},
)


elastic_client = Elasticsearch(
    hosts=settings.elastic.host,
    basic_auth=(settings.elastic.user, settings.elastic.password)
)

elastic_store = ElasticsearchStore(
    es_url=settings.elastic.host,
    index_name="nodes_embeddings",
    embedding=embeddings,
    es_user=settings.elastic.user,
    es_password=settings.elastic.password,
)

bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="nodes_documents"
)


docs = elastic_store.similarity_search("Какие льготы доступны участникам СВО")
print(docs)


docs = bm25_retriever.invoke("Какие льготы доступны участникам СВО")
print(docs)