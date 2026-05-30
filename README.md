# 税务风险智能诊断分析系统

面向“大模型应用开发工程师”展示的生产级可运行样例。系统模拟税务专家“发现风险、补充证据、交叉验证、复核审查”的流程，基于企业财报、发票流向和税务法规库生成《企业税务健康体检报告》。

## 技术成熟度校验

项目周期设定为 `2025.04 - 2025.08` 是合理的：

- Qwen2.5-14B-Instruct 已于 2024-09 发布，2025 年上半年可通过 vLLM、Ollama 或 OpenAI-compatible 服务部署。
- LangChain v0.3 已于 2024-09 发布，2025.04 时 Agent、Tool Calling、Runnable、structured output 已足够成熟。
- Milvus 2.5 已于 2024-12 发布，2025.04 已有 2.5.x 稳定迭代，支持语义检索、元数据过滤和混合检索场景。

## 架构亮点

- 双 Agent 质量控制：`TaxInspectorAgent` 负责 ReAct 风险诊断，`SupervisorAgent` 负责口径、证据、法规引用和结论一致性审核。
- 异构工具箱：只读 SQL、财务指标计算、Milvus 法规检索、证据链构建。
- Human-in-the-Loop：数据缺失、逻辑冲突、工具预算超限、监督审核不通过时自动进入人工复核队列。
- 可追溯报告：每个风险结论包含证据、SQL/指标来源、法规引用、置信度和复核状态。

## 快速开始

```bash
conda env create -f environment.yml
conda activate tax-risk-ai

# 可选：启动 Milvus Standalone
docker compose up -d

# 初始化演示数据库
python scripts/init_demo_data.py

# 运行一次诊断
python scripts/run_diagnosis.py --company-id C001 --year 2024

# 启动 API
uvicorn tax_risk_ai.app.main:app --reload --port 8000
```

访问：

- `GET /health`
- `POST /diagnostics/run`
- `GET /reviews/pending`

## 模型配置

默认使用 mock LLM，方便无 GPU 环境演示。接入 Qwen2.5-14B-Instruct 时，推荐用 vLLM 暴露 OpenAI-compatible API：

```bash
export LLM_PROVIDER=openai_compatible
export LLM_BASE_URL=http://localhost:8001/v1
export LLM_API_KEY=local
export LLM_MODEL=Qwen2.5-14B-Instruct
```

## 项目结构

```text
tax_risk_ai/
  app/
    agents/          # 稽查主 Agent、监督 Agent、编排器
    api/             # FastAPI 路由
    core/            # 配置、日志、异常
    services/        # 诊断、报告、复核队列、法规索引
    tools/           # SQL、指标、法规检索工具
    data/            # 结构化 schema
  data/
    rules/           # 税务规则样例
    seed/            # 演示企业财税数据
  scripts/           # 初始化和运行脚本
  tests/             # 单元测试
```

