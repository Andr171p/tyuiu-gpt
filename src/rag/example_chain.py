from langchain.embeddings import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from src.rag.graph.neo4j_retriever import Neo4jRetriever
from src.utils.files import load_txt
from src.rag.rag_helpers import extract_page_content, format_docs, select_top_k_documents
from src.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs
)


elastic_client = Elasticsearch(
    hosts=settings.elastic.host,
    basic_auth=(settings.elastic.user, settings.elastic.password)
)


vector_store = ElasticsearchStore(
    es_url=settings.elastic.host,
    index_name="nodes_embeddings",
    embedding=embeddings,
    es_user=settings.elastic.user,
    es_password=settings.elastic.password
)


nodes_vector_store_retriever = vector_store.as_retriever()


nodes_bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="nodes_documents",
)


nodes_retriever = EnsembleRetriever(
    retrievers=[nodes_vector_store_retriever, nodes_bm25_retriever],
    weights=[0.7, 0.3]
)


vector_store = ElasticsearchStore(
    es_url=settings.elastic.host,
    index_name="tyuiu_index",
    embedding=embeddings,
    es_user=settings.elastic.user,
    es_password=settings.elastic.password
)


vector_store_retriever = vector_store.as_retriever(search_kwargs={"k": 2})


bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="docs-tyuiu-index",
    search_kwargs={"k": 2}
)


neo4j_retriever = Neo4jRetriever(uri=settings.neo4j.uri)


ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)


model = GigaChat(
    credentials=settings.gigachat.api_key,
    scope=settings.gigachat.scope,
    model=settings.gigachat.model_name,
    verify_ssl_certs=False,
    profanity_check=False
)


file_path = r"C:\Users\andre\IdeaProjects\TyuiuAIChatBotAPI\prompts\Сотрудник_приёмной_комиссии.txt"


prompt = ChatPromptTemplate.from_template(load_txt(file_path))


parser = StrOutputParser()


graph_rag_chain = (
    {
        "context": nodes_retriever | extract_page_content | neo4j_retriever | format_docs,
        "question": RunnablePassthrough()
    } |
    prompt |
    model |
    parser
)


hybrid_rag_chain = (
    {
        "context": ensemble_retriever | format_docs,
        "question": RunnablePassthrough()
    } |
    prompt |
    model |
    parser
)


results = hybrid_rag_chain.invoke("Как работает система приоритетов")
print(results)
