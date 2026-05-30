import csv
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "tax_demo.db"


def load_csv(conn: sqlite3.Connection, table: str, path: Path) -> None:
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return
    columns = rows[0].keys()
    placeholders = ",".join(["?"] * len(columns))
    conn.executemany(
        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
        [tuple(row[col] for col in columns) for row in rows],
    )


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE monthly_tax (
              company_id TEXT,
              year INTEGER,
              month INTEGER,
              revenue REAL,
              output_vat REAL,
              input_vat REAL,
              cost REAL
            );
            CREATE TABLE invoices (
              company_id TEXT,
              year INTEGER,
              month INTEGER,
              direction TEXT,
              counterparty TEXT,
              amount REAL,
              tax_amount REAL
            );
            """
        )
        load_csv(conn, "monthly_tax", DATA_DIR / "seed" / "monthly_tax.csv")
        load_csv(conn, "invoices", DATA_DIR / "seed" / "invoices.csv")
    print(f"initialized {DB_PATH}")


if __name__ == "__main__":
    main()

