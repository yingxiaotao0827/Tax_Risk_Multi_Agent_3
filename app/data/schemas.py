from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ReviewStatus(str, Enum):
    passed = "passed"
    pending_human = "pending_human"
    rejected = "rejected"


class Evidence(BaseModel):
    source: str
    title: str
    detail: str
    value: float | str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class RiskFinding(BaseModel):
    risk_code: str
    title: str
    level: RiskLevel
    confidence: float
    reason: str
    evidences: list[Evidence] = Field(default_factory=list)
    rule_refs: list[str] = Field(default_factory=list)
    remediation: str


class SupervisorResult(BaseModel):
    score: float
    status: ReviewStatus
    issues: list[str] = Field(default_factory=list)
    required_human_review: bool = False


class DiagnosticRequest(BaseModel):
    company_id: str
    year: int


class DiagnosticReport(BaseModel):
    report_id: str
    company_id: str
    year: int
    summary: str
    findings: list[RiskFinding]
    supervisor: SupervisorResult
    review_status: ReviewStatus
    evidence_chain: list[Evidence]
    charts: list[dict[str, Any]] = Field(default_factory=list)

