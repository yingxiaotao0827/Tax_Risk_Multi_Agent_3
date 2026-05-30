from pathlib import Path
from typing import Any

from langchain_core.documents import Document


class TaxRuleRetriever:
    name = "tax_rule_retriever"
    description = "检索税务法规库，返回与风险判断相关的政策依据。"

    def __init__(self, rules_dir: Path):
        self.rules_dir = rules_dir
        self._documents = self._load_documents()

    def _load_documents(self) -> list[Document]:
        docs: list[Document] = []
        for path in sorted(self.rules_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            docs.append(Document(page_content=text, metadata={"source": path.name}))
        return docs

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        tokens = set(query.lower().split())
        scored = []
        for doc in self._documents:
            content = doc.page_content.lower()
            score = sum(1 for token in tokens if token in content)
            if score or not tokens:
                scored.append((score, doc))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            {
                "source": doc.metadata["source"],
                "content": doc.page_content[:500],
                "score": score,
            }
            for score, doc in scored[:top_k]
        ]

