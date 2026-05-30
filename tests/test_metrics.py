from pathlib import Path

from tax_risk_ai.app.tools.metrics_tool import FinancialMetricsTool
from tax_risk_ai.app.tools.sql_tool import ReadOnlySQLTool


def test_metrics_after_demo_init():
    db = Path("tax_risk_ai/data/tax_demo.db")
    if not db.exists():
        import subprocess

        subprocess.run(["python", "tax_risk_ai/scripts/init_demo_data.py"], check=True)
    metrics = FinancialMetricsTool(ReadOnlySQLTool(db))
    assert metrics.input_vat_growth("C001", 2024).value > 0.35
    assert metrics.vat_burden_rate("C001", 2024).value < 0.025

