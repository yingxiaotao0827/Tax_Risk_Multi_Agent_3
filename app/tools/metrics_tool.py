from dataclasses import dataclass
from tax_risk_ai.app.tools.sql_tool import ReadOnlySQLTool


@dataclass
class MetricResult:
    name: str
    value: float
    detail: str


class FinancialMetricsTool:
    name = "financial_metrics"
    description = "计算税务风险相关财务指标，如税负率、进项增长率、收入发票差异率。"

    def __init__(self, sql_tool: ReadOnlySQLTool):
        self.sql_tool = sql_tool

    def vat_burden_rate(self, company_id: str, year: int) -> MetricResult:
        row = self.sql_tool.run(
            """
            SELECT SUM(output_vat) AS output_vat, SUM(input_vat) AS input_vat, SUM(revenue) AS revenue
            FROM monthly_tax
            WHERE company_id = ? AND year = ?
            """,
            (company_id, year),
        )[0]
        revenue = row["revenue"] or 1
        value = (row["output_vat"] - row["input_vat"]) / revenue
        return MetricResult("vat_burden_rate", round(value, 4), "应纳增值税额 / 营业收入")

    def input_vat_growth(self, company_id: str, year: int) -> MetricResult:
        rows = self.sql_tool.run(
            """
            SELECT year, SUM(input_vat) AS input_vat
            FROM monthly_tax
            WHERE company_id = ? AND year IN (?, ?)
            GROUP BY year
            ORDER BY year
            """,
            (company_id, year - 1, year),
        )
        values = {row["year"]: row["input_vat"] for row in rows}
        previous = values.get(year - 1) or 1
        current = values.get(year) or 0
        value = (current - previous) / previous
        return MetricResult("input_vat_growth", round(value, 4), "本年进项税额较上年增长率")

    def revenue_invoice_gap(self, company_id: str, year: int) -> MetricResult:
        row = self.sql_tool.run(
            """
            SELECT
              (SELECT SUM(revenue) FROM monthly_tax WHERE company_id = ? AND year = ?) AS revenue,
              (SELECT SUM(amount) FROM invoices WHERE company_id = ? AND year = ? AND direction = 'out') AS invoice_amount
            """,
            (company_id, year, company_id, year),
        )[0]
        revenue = row["revenue"] or 1
        invoice_amount = row["invoice_amount"] or 0
        value = (invoice_amount - revenue) / revenue
        return MetricResult("revenue_invoice_gap", round(value, 4), "销项发票金额与确认收入差异率")

