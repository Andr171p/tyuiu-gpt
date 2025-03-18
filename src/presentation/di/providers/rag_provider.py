from dishka import Provider, provide, Scope

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever

from langchain.prompts import ChatPromptTemplate
from langchain.retrievers import EnsembleRetriever
from langchain_community.llms.yandex import YandexGPT
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.output_parsers.string import StrOutputParser

from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel, BaseLLM
from langchain_core.output_parsers import BaseTransformOutputParser
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever

from src.rag import RAG
from src.rag import BaseRAG
from src.config import settings
from src.misc.file_readers import read_txt


class RAGProvider(Provider):
    @provide(scope=Scope.APP)
    def get_embeddings(self) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=settings.embeddings.model_name,
            model_kwargs=settings.embeddings.model_kwargs,
            encode_kwargs=settings.embeddings.encode_kwargs
        )

    @provide(scope=Scope.APP)
    def get_elastic_client(self) -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elastic.host,
            basic_auth=(settings.elastic.user, settings.elastic.password)
        )

    @provide(scope=Scope.APP)
    def get_vector_store(self, embeddings: Embeddings) -> VectorStore:
        return ElasticsearchStore(
            es_url=settings.elastic.host,
            es_user=settings.elastic.user,
            es_password=settings.elastic.password,
            index_name="tyuiu_index",
            embedding=embeddings
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, vector_store: VectorStore) -> VectorStoreRetriever:
        return vector_store.as_retriever()

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elastic_client: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elastic_client,
            index_name="docs-tyuiu-index",
        )

    @provide(scope=Scope.APP)
    def get_retriever(
            self,
            vector_store_retriever: VectorStoreRetriever,
            bm25_retriever: ElasticSearchBM25Retriever
    ) -> BaseRetriever:
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[0.6, 0.4]
        )

    @provide(scope=Scope.APP)
    def get_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(read_txt(settings.prompts.rag_prompt))

    @provide(scope=Scope.APP)
    def get_model(self) -> BaseChatModel | BaseLLM:
        return YandexGPT(
            api_key=settings.yandexgpt.api_key,
            folder_id=settings.yandexgpt.folder_id
        )

    @provide(scope=Scope.APP)
    def get_parser(self) -> BaseTransformOutputParser:
        return StrOutputParser()

    @provide(scope=Scope.APP)
    def get_rag(
            self,
            retriever: BaseRetriever,
            prompt: ChatPromptTemplate,
            model: BaseChatModel | BaseLLM,
            parser: BaseTransformOutputParser
    ) -> BaseRAG:
        return RAG(
            retriever=retriever,
            prompt=prompt,
            model=model,
            parser=parser
        )
