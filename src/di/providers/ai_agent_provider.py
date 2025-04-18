from dishka import Provider, provide, Scope

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

from src.infrastructure.llms.yandex_gpt import YandexGPTChatModel
from src.infrastructure.checkpoint_savers.redis import AsyncRedisCheckpointSaver

from src.ai_agent import BaseAgent, ReACTAgent
from src.ai_agent.tools import RetrievalTool

from src.misc.files import read_txt
from src.settings import Settings


class AIAgentProvider(Provider):
    @provide(scope=Scope.APP)
    def get_embeddings(self, settings: Settings) -> Embeddings:
        return HuggingFaceEmbeddings(
            model_name=settings.embeddings.model_name,
            model_kwargs=settings.embeddings.model_kwargs,
            encode_kwargs=settings.embeddings.encode_kwargs
        )

    @provide(scope=Scope.APP)
    def get_elasticsearch(self, settings: Settings) -> Elasticsearch:
        return Elasticsearch(
            hosts=settings.elasticsearch.host,
            basic_auth=(settings.elasticsearch.user, settings.elasticsearch.password)
        )

    @provide(scope=Scope.APP)
    def get_redis(self, settings: Settings) -> AsyncRedis:
        return AsyncRedis(
            host=settings.redis.host,
            port=settings.redis.port,
            username=settings.redis.user,
            password=settings.redis.password
        )

    @provide(scope=Scope.APP)
    def get_vector_store(self, settings: Settings, embeddings: Embeddings) -> VectorStore:
        return ElasticsearchStore(
            es_url=settings.elasticsearch.host,
            es_user=settings.elasticsearch.user,
            es_password=settings.elasticsearch.password,
            index_name="tyuiu_index",
            embedding=embeddings
        )

    @provide(scope=Scope.APP)
    def get_vector_store_retriever(self, vector_store: VectorStore) -> VectorStoreRetriever:
        return vector_store.as_retriever()

    @provide(scope=Scope.APP)
    def get_bm25_retriever(self, elasticsearch: Elasticsearch) -> ElasticSearchBM25Retriever:
        return ElasticSearchBM25Retriever(
            client=elasticsearch,
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
    def get_model(self, settings: Settings) -> BaseChatModel:
        return YandexGPTChatModel(
            api_key=settings.yandex_gpt.api_key,
            folder_id=settings.yandex_gpt.folder_id,
            model="yandexgpt"
        )

    @provide(scope=Scope.APP)
    def get_checkpoint_saver(self, redis: AsyncRedis) -> BaseCheckpointSaver:
        return AsyncRedisCheckpointSaver(redis)

    @provide(scope=Scope.APP)
    def get_retrieval_tool(self, retriever: BaseRetriever) -> RetrievalTool:
        return RetrievalTool(retriever)

    @provide(scope=Scope.APP)
    def get_react_agent(
            self,
            settings: Settings,
            checkpoint_saver: BaseCheckpointSaver,
            retrieval_tool: RetrievalTool,
            model: BaseChatModel
    ) -> BaseAgent:
        return ReACTAgent(
            checkpoint_saver=checkpoint_saver,
            tools=[retrieval_tool],
            prompt_template=read_txt(settings.prompts.agent_prompt),
            model=model
        )
