from langchain.embeddings import HuggingFaceEmbeddings
from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatYandexGPT
from langchain_core.output_parsers.string import StrOutputParser

from src.rag.naive import HybridRAG
from src.rag.rag_utils import format_docs, load_txt
from src.services.chat_bot_service import ChatBotService
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
        template=load_txt(settings.gigachat.prompt)
    )
    '''gigachat_model = GigaChat(
        credentials=settings.gigachat.api_key,
        scope=settings.gigachat.scope,
        model=settings.gigachat.model_name,
        verify_ssl_certs=False,
        profanity_check=False
    )'''
    yandex_gpt_model = ChatYandexGPT(
        folder_id=settings.yandexgpt.folder_id,
        api_key=settings.yandexgpt.api_key
    )
    str_output_parser = StrOutputParser()
    hybrid_rag = HybridRAG(
        retriever=ensemble_retriever,
        format_docs_func=format_docs,
        prompt=prompt,
        model=yandex_gpt_model,
        parser=str_output_parser
    )
    chat_bot = ChatBotService(hybrid_rag)
