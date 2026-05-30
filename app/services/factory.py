from tax_risk_ai.app.agents.inspector import TaxInspectorAgent
from tax_risk_ai.app.agents.orchestrator import DiagnosticOrchestrator
from tax_risk_ai.app.agents.supervisor import SupervisorAgent
from tax_risk_ai.app.core.config import Settings, get_settings
from tax_risk_ai.app.services.review_queue import HumanReviewQueue
from tax_risk_ai.app.tools.metrics_tool import FinancialMetricsTool
from tax_risk_ai.app.tools.rule_retriever import TaxRuleRetriever
from tax_risk_ai.app.tools.sql_tool import ReadOnlySQLTool


def build_orchestrator(settings: Settings | None = None) -> DiagnosticOrchestrator:
    settings = settings or get_settings()
    sql_tool = ReadOnlySQLTool(settings.sqlite_path)
    metrics_tool = FinancialMetricsTool(sql_tool)
    rule_retriever = TaxRuleRetriever(settings.data_dir / "rules")
    inspector = TaxInspectorAgent(sql_tool, metrics_tool, rule_retriever, settings.max_tool_calls)
    supervisor = SupervisorAgent(settings.min_supervisor_score)
    queue = HumanReviewQueue(settings.data_dir / "review_queue.json")
    return DiagnosticOrchestrator(inspector, supervisor, queue)

