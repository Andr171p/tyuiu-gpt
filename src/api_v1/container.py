from langchain.embeddings import HuggingFaceEmbeddings
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat
from langchain_core.output_parsers.string import StrOutputParser

from src.rag.hybrid import HybridRAG
from src.rag.rag_utils import format_docs, load_txt
from src.chat_bot import ChatBot
from src.config import settings


class Container:
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embeddings.model_name,
        model_kwargs=settings.embeddings.model_kwargs,
        encode_kwargs=settings.embeddings.encode_kwargs
    )
    elastic_client = Elasticsearch(
        hosts=settings.elastic.host,
        basic_auth=(settings.elastic.user, settings.elastic.password),
    )
    vector_store = ElasticsearchStore(
        es_url=settings.elastic.host,
        es_user=settings.elastic.user,
        es_password=settings.elastic.password,
        index_name="tyuiu_index",
        embedding=embeddings
    )
    bm25_retriever = ElasticSearchBM25Retriever(
        client=elastic_client,
        index_name="docs-tyuiu-index",
    )
    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_store.as_retriever(), bm25_retriever],
        weights=[0.6, 0.4]
    )
    prompt = ChatPromptTemplate.from_template(
        template=load_txt(r"C:\Users\andre\IdeaProjects\TyuiuAIChatBotAPI\prompts\Сотрудник_приёмной_комиссии.txt")
    )
    model = GigaChat(
        credentials=settings.gigachat.api_key,
        scope=settings.gigachat.scope,
        model=settings.gigachat.model_name,
        verify_ssl_certs=False,
        profanity_check=False
    )
    parser = StrOutputParser()
    rag = HybridRAG(
        retriever=ensemble_retriever,
        format_docs_func=format_docs,
        prompt=prompt,
        model=model,
        parser=parser
    )
    chat_bot = ChatBot(rag)
