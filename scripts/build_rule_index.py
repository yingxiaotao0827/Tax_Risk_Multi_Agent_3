import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from tax_risk_ai.app.core.config import get_settings
from tax_risk_ai.app.services.rule_index import build_milvus_index


if __name__ == "__main__":
    collection = build_milvus_index(get_settings())
    print(f"Milvus collection ready: {collection}")
