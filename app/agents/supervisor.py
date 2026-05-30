from tax_risk_ai.app.data.schemas import ReviewStatus, RiskFinding, SupervisorResult


class SupervisorAgent:
    """Quality gate for evidence, policy references, confidence and consistency."""

    def __init__(self, min_score: float):
        self.min_score = min_score

    def review(self, findings: list[RiskFinding], warnings: list[str]) -> SupervisorResult:
        issues: list[str] = list(warnings)
        score = 1.0

        for finding in findings:
            if not finding.evidences:
                score -= 0.25
                issues.append(f"{finding.risk_code} 缺少证据链")
            if finding.risk_code != "NO-MAJOR-RISK" and not finding.rule_refs:
                score -= 0.18
                issues.append(f"{finding.risk_code} 缺少法规引用")
            if finding.confidence < 0.68:
                score -= 0.15
                issues.append(f"{finding.risk_code} 置信度低于出具阈值")
            if finding.level == "high" and finding.confidence < 0.8:
                score -= 0.12
                issues.append(f"{finding.risk_code} 高风险结论置信度不足")

        score = max(round(score, 2), 0.0)
        required_human_review = score < self.min_score or bool(warnings)
        return SupervisorResult(
            score=score,
            status=ReviewStatus.pending_human if required_human_review else ReviewStatus.passed,
            issues=issues,
            required_human_review=required_human_review,
        )

