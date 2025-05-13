from collections.abc import AsyncIterable

from dishka import Provider, provide, Scope, from_context, make_async_container

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from faststream.rabbit import RabbitBroker

from redis.asyncio import Redis as AsyncRedis

from elasticsearch import Elasticsearch
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.retrievers import ElasticSearchBM25Retriever

from langchain.retrievers import EnsembleRetriever
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever

from langgraph.checkpoint.base import BaseCheckpointSaver

from .infrastructure.llms.yandex_gpt import YandexGPTChatModel
from .infrastructure.checkpoint_savers.redis import AsyncRedisCheckpointSaver
from .infrastructure.database.session import create_session_maker
from .infrastructure.database.repository import SQLMessageRepository

from .interfaces import AIAgent, MessageRepository

from .ai_agent.agents import RAGAgent
from .ai_agent.nodes import RetrieverNode, GenerationNode

from .settings import Settings
from .constants import (
    VECTOR_STORE_INDEX,
    BM25_INDEX,
    SIMILARITY_WEIGHT,
    BM25_WEIGHT,
    YANDEX_GPT_PRO
)


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_rabbit_broker(self, config: Settings) -> RabbitBroker:
        return RabbitBroker(config.rabbit.rabbit_url)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Settings) -> async_sessionmaker[AsyncSession]:
        return create_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_message_repository(self, session: AsyncSession) -> MessageRepository:
        return SQLMessageRepository(session)

    @provide(scope=Scope.APP)
    def get_embeddings(self, config: Settings) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=config.embeddings.MODEL_NAME,
            model_kwargs=config.embeddings.MODEL_KWARGS,
            encode_kwargs=config.embeddings.ENCODE_KWARGS
        )

    @provide(scope=Scope.APP)
    def get_elasticsearch(self, config: Settings) -> Elasticsearch:
        return Elasticsearch(
            hosts=config.elasticsearch.elasticsearch_url,
            basic_auth=(config.elasticsearch.ELASTIC_USER, config.elasticsearch.ELASTIC_PASSWORD)
        )

    @provide(scope=Scope.APP)
    def get_redis(self, config: Settings) -> AsyncRedis:
        return AsyncRedis.from_url(config.redis.redis_url)

    @provide(scope=Scope.APP)
    def get_vector_store(self, config: Settings, embeddings: Embeddings) -> VectorStore:
        return ElasticsearchStore(
            es_url=config.elasticsearch.elasticsearch_ur,
            es_user=config.elasticsearch.ELASTIC_USER,
            es_password=config.elasticsearch.ELASTIC_PASSWORD,
            index_name=VECTOR_STORE_INDEX,
            embedding=embeddings
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, vector_store: VectorStore) -> VectorStoreRetriever:
        return vector_store.as_retriever()

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elasticsearch: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elasticsearch,
            index_name=BM25_INDEX,
        )

    @provide(scope=Scope.APP)
    def get_retriever(
            self,
            vector_store_retriever: VectorStoreRetriever,
            bm25_retriever: ElasticSearchBM25Retriever
    ) -> BaseRetriever:
        return EnsembleRetriever(
            retrievers=[vector_store_retriever, bm25_retriever],
            weights=[SIMILARITY_WEIGHT, BM25_WEIGHT]
        )

    @provide(scope=Scope.APP)
    def get_model(self, confi: Settings) -> BaseChatModel:
        return YandexGPTChatModel(
            api_key=confi.yandex_gpt.API_KEY,
            folder_id=confi.yandex_gpt.FOLDER_ID,
            model=YANDEX_GPT_PRO
        )

    @provide(scope=Scope.APP)
    def get_checkpoint_saver(self, redis: AsyncRedis) -> BaseCheckpointSaver:
        return AsyncRedisCheckpointSaver(redis)

    @provide(scope=Scope.APP)
    def get_retriever_node(self, retriever: BaseRetriever) -> RetrieverNode:
        return RetrieverNode(retriever)

    @provide(scope=Scope.APP)
    def get_generation_node(self, model: BaseChatModel) -> GenerationNode:
        return GenerationNode(model)

    @provide(scope=Scope.APP)
    def get_ai_agent(
            self,
            retriever: RetrieverNode,
            generation: GenerationNode,
            checkpoint_saver: BaseCheckpointSaver
    ) -> AIAgent:
        return RAGAgent(
            retriever=retriever,
            generation=generation,
            checkpoint_saver=checkpoint_saver
        )


settings = Settings()


container = make_async_container(AppProvider(), context={Settings: settings})
