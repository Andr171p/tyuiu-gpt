from uuid import uuid4
from pathlib import Path
from elasticsearch import Elasticsearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_elasticsearch import ElasticsearchStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import ElasticSearchBM25Retriever


BASE_DIR = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIR / "documents" / "texts" / "ТИУ_Описание_направлений_подготовки.txt"


with open(
        file=FILE_PATH,
        mode="r",
        encoding="utf-8"
) as file:
    text = file.read()

print(f"Длина текста: {len(text)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len,
)

chunks = text_splitter.create_documents([text])

N = 5

print(f"Всего чанков: {len(chunks)}")
print(f"Первые {N} чанков:")
# chunks[:N]

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-large",
    model_kwargs={"device": "cpu"},
    encode_kwargs={'normalize_embeddings': False},
)


elastic_client = Elasticsearch(
    hosts="https://elasticsearch-pv2s-production.up.railway.app/",
    basic_auth=("elastic", "2qq0lvgc89lwh6z5jp2q9280dcneaf95")
)
'''indices = elastic_client.cat.indices(h='index').split()

for index in indices:
    print(f"Удаляю индекс: {index}")
    elastic_client.indices.delete(index=index, ignore=[400, 404])

print("Все индексы удалены.")'''

elastic_store = ElasticsearchStore(
    es_url="https://elasticsearch-pv2s-production.up.railway.app/",
    index_name="tyuiu_index",
    embedding=embeddings,
    es_user="elastic",
    es_password="2qq0lvgc89lwh6z5jp2q9280dcneaf95",
)

elastic_store.add_documents(documents=chunks)
print("Документы добавлены в векторное  хранилище.")

bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name="docs-tyuiu-index",
)

bm25_retriever.add_texts([document.page_content for document in chunks])
print("Документы добавлены в индекс BM25.")