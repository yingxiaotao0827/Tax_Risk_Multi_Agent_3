from fastapi import APIRouter

from tax_risk_ai.app.core.config import get_settings
from tax_risk_ai.app.data.schemas import DiagnosticRequest, DiagnosticReport
from tax_risk_ai.app.services.factory import build_orchestrator
from tax_risk_ai.app.services.review_queue import HumanReviewQueue

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {"status": "ok", "model": settings.llm_model, "environment": settings.environment}


@router.post("/diagnostics/run", response_model=DiagnosticReport)
def run_diagnostic(request: DiagnosticRequest) -> DiagnosticReport:
    return build_orchestrator().run(request.company_id, request.year)


@router.get("/reviews/pending")
def pending_reviews() -> list[dict]:
    settings = get_settings()
    return HumanReviewQueue(settings.data_dir / "review_queue.json").pending()

