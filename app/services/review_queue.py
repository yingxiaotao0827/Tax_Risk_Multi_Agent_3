import json
from pathlib import Path
from tax_risk_ai.app.data.schemas import DiagnosticReport


class HumanReviewQueue:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def enqueue(self, report: DiagnosticReport) -> None:
        rows = self.pending()
        rows.append(report.model_dump(mode="json"))
        self.path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def pending(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

