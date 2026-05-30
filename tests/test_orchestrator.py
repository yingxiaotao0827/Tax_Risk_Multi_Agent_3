from pathlib import Path

from tax_risk_ai.app.services.factory import build_orchestrator


def test_orchestrator_generates_risk_report():
    db = Path("tax_risk_ai/data/tax_demo.db")
    if not db.exists():
        import subprocess

        subprocess.run(["python", "tax_risk_ai/scripts/init_demo_data.py"], check=True)
    report = build_orchestrator().run("C001", 2024)
    codes = {finding.risk_code for finding in report.findings}
    assert "VAT-INPUT-ABNORMAL" in codes
    assert report.supervisor.score >= 0.72

