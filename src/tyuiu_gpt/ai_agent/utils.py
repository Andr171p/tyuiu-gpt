from langchain_core.documents import Document


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])
