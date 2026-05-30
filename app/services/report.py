from tax_risk_ai.app.data.schemas import DiagnosticReport, Evidence


def build_charts(evidence_chain: list[Evidence]) -> list[dict]:
    return [
        {
            "type": "bar",
            "title": "核心税务指标",
            "series": [
                {"name": item.title, "value": item.value}
                for item in evidence_chain
                if isinstance(item.value, float)
            ],
        }
    ]


def render_markdown(report: DiagnosticReport) -> str:
    lines = [
        f"# 企业税务健康体检报告",
        f"",
        f"- 报告编号：{report.report_id}",
        f"- 企业编号：{report.company_id}",
        f"- 年度：{report.year}",
        f"- 复核状态：{report.review_status.value}",
        f"- 监督评分：{report.supervisor.score}",
        f"",
        f"## 总结",
        report.summary,
        "",
        "## 风险发现",
    ]
    for finding in report.findings:
        lines.extend(
            [
                f"### {finding.title}",
                f"- 风险编码：{finding.risk_code}",
                f"- 风险等级：{finding.level.value}",
                f"- 置信度：{finding.confidence}",
                f"- 判断理由：{finding.reason}",
                f"- 法规引用：{', '.join(finding.rule_refs) if finding.rule_refs else '无'}",
                f"- 整改建议：{finding.remediation}",
                "",
            ]
        )
    return "\n".join(lines)

