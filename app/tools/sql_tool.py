import re
import sqlite3
from pathlib import Path
from typing import Any


class ReadOnlySQLTool:
    name = "readonly_tax_sql"
    description = "执行只读 SQL，用于查询企业财报、发票流向和税务申报数据。"

    def __init__(self, db_path: Path):
        self.db_path = db_path

    def run(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
        normalized = sql.strip().lower()
        if not normalized.startswith("select"):
            raise ValueError("只允许执行 SELECT 查询")
        if re.search(r"\b(insert|update|delete|drop|alter|attach|pragma|vacuum)\b", normalized):
            raise ValueError("SQL 包含非只读关键字")
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(sql, params).fetchall()
        return [dict(row) for row in rows]

