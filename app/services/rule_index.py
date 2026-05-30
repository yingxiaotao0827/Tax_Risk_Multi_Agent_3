from pathlib import Path

from langchain_core.documents import Document


def load_rule_documents(rules_dir: Path) -> list[Document]:
    return [
        Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name})
        for path in sorted(rules_dir.glob("*.md"))
    ]


def build_milvus_index(settings) -> str:
    """Build a Milvus collection for tax rules.

    This is intentionally isolated because CI and interview laptops often do not have
    Milvus running. The runtime retriever falls back to local lexical search.
    """
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_milvus import Milvus

    docs = load_rule_documents(settings.data_dir / "rules")
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
    Milvus.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=settings.milvus_collection,
        connection_args={"uri": settings.milvus_uri},
        drop_old=True,
    )
    return settings.milvus_collection

