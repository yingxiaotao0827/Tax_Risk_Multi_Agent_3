import argparse
import sys
from pathlib import Path

from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parents[2]))

from tax_risk_ai.app.services.factory import build_orchestrator
from tax_risk_ai.app.services.report import render_markdown


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--company-id", required=True)
    parser.add_argument("--year", required=True, type=int)
    args = parser.parse_args()

    report = build_orchestrator().run(args.company_id, args.year)
    markdown = render_markdown(report)
    out = Path("tax_risk_ai/data") / f"{report.report_id}.md"
    out.write_text(markdown, encoding="utf-8")
    Console().print(markdown)
    Console().print(f"\n报告已生成: {out}")


if __name__ == "__main__":
    main()
