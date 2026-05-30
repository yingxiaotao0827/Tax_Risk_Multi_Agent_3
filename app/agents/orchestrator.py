from uuid import uuid4

from tax_risk_ai.app.agents.inspector import TaxInspectorAgent
from tax_risk_ai.app.agents.supervisor import SupervisorAgent
from tax_risk_ai.app.data.schemas import DiagnosticReport, ReviewStatus
from tax_risk_ai.app.services.report import build_charts
from tax_risk_ai.app.services.review_queue import HumanReviewQueue


class DiagnosticOrchestrator:
    def __init__(
        self,
        inspector: TaxInspectorAgent,
        supervisor: SupervisorAgent,
        review_queue: HumanReviewQueue,
    ):
        self.inspector = inspector
        self.supervisor = supervisor
        self.review_queue = review_queue

    def run(self, company_id: str, year: int) -> DiagnosticReport:
        findings, evidence_chain, warnings = self.inspector.diagnose(company_id, year)
        supervisor = self.supervisor.review(findings, warnings)
        review_status = (
            ReviewStatus.pending_human if supervisor.required_human_review else ReviewStatus.passed
        )
        high_count = sum(1 for finding in findings if finding.level.value == "high")
        medium_count = sum(1 for finding in findings if finding.level.value == "medium")
        summary = f"本次诊断识别高风险 {high_count} 项、中风险 {medium_count} 项。"
        report = DiagnosticReport(
            report_id=f"TAX-{uuid4().hex[:10].upper()}",
            company_id=company_id,
            year=year,
            summary=summary,
            findings=findings,
            supervisor=supervisor,
            review_status=review_status,
            evidence_chain=evidence_chain,
            charts=build_charts(evidence_chain),
        )
        if review_status == ReviewStatus.pending_human:
            self.review_queue.enqueue(report)
        return report

