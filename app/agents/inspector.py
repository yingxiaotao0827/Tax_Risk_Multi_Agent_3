from tax_risk_ai.app.data.schemas import Evidence, RiskFinding, RiskLevel
from tax_risk_ai.app.tools.metrics_tool import FinancialMetricsTool
from tax_risk_ai.app.tools.rule_retriever import TaxRuleRetriever
from tax_risk_ai.app.tools.sql_tool import ReadOnlySQLTool


class TaxInspectorAgent:
    """ReAct-style deterministic inspector with auditable tool calls."""

    def __init__(
        self,
        sql_tool: ReadOnlySQLTool,
        metrics_tool: FinancialMetricsTool,
        rule_retriever: TaxRuleRetriever,
        max_tool_calls: int,
    ):
        self.sql_tool = sql_tool
        self.metrics_tool = metrics_tool
        self.rule_retriever = rule_retriever
        self.max_tool_calls = max_tool_calls

    def diagnose(self, company_id: str, year: int) -> tuple[list[RiskFinding], list[Evidence], list[str]]:
        tool_calls = 0
        warnings: list[str] = []
        evidence_chain: list[Evidence] = []
        findings: list[RiskFinding] = []

        metrics = [
            self.metrics_tool.vat_burden_rate(company_id, year),
            self.metrics_tool.input_vat_growth(company_id, year),
            self.metrics_tool.revenue_invoice_gap(company_id, year),
        ]
        tool_calls += 3

        for metric in metrics:
            evidence_chain.append(
                Evidence(
                    source="financial_metrics",
                    title=metric.name,
                    detail=metric.detail,
                    value=metric.value,
                )
            )

        vat_burden, input_growth, invoice_gap = metrics

        if input_growth.value > 0.35 and vat_burden.value < 0.025:
            rules = self.rule_retriever.search("进项税额 异常 增值税 发票 抵扣")
            tool_calls += 1
            refs = [rule["source"] for rule in rules]
            findings.append(
                RiskFinding(
                    risk_code="VAT-INPUT-ABNORMAL",
                    title="进项税额异常增长且税负率偏低",
                    level=RiskLevel.high,
                    confidence=0.86,
                    reason="进项税额同比增长超过 35%，同时增值税税负率低于 2.5%，存在异常抵扣或采购发票真实性风险。",
                    evidences=evidence_chain[:2],
                    rule_refs=refs,
                    remediation="抽样核验大额进项发票、供应商工商状态、合同物流和付款流水，必要时转人工复核。",
                )
            )

        if abs(invoice_gap.value) > 0.08:
            rules = self.rule_retriever.search("收入 确认 销项发票 纳税申报 差异")
            tool_calls += 1
            refs = [rule["source"] for rule in rules]
            findings.append(
                RiskFinding(
                    risk_code="REV-INVOICE-GAP",
                    title="确认收入与销项发票金额背离",
                    level=RiskLevel.medium,
                    confidence=0.78,
                    reason="销项发票金额与营业收入差异超过 8%，可能存在收入确认跨期、未开票收入或发票开具不匹配。",
                    evidences=[evidence_chain[2]],
                    rule_refs=refs,
                    remediation="核对收入台账、销项发票、合同履约节点和纳税申报表，解释差异形成原因。",
                )
            )

        if tool_calls > self.max_tool_calls:
            warnings.append("工具调用超过预算，建议进入人工复核。")
        if not findings:
            findings.append(
                RiskFinding(
                    risk_code="NO-MAJOR-RISK",
                    title="未发现重大税务异常",
                    level=RiskLevel.low,
                    confidence=0.74,
                    reason="核心税负、进项增长和收入发票匹配指标未触发高风险阈值。",
                    evidences=evidence_chain,
                    rule_refs=[],
                    remediation="保持月度指标监控，持续完善发票和申报口径一致性校验。",
                )
            )
        return findings, evidence_chain, warnings

