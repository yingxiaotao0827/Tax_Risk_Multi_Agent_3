# 技术可行性说明

## 时间窗口

项目周期：2025.04 - 2025.08。

该时间窗口内，所选技术已经具备工程落地条件：

- Qwen2.5 系列在 2024-09-19 发布，覆盖 0.5B、1.5B、3B、7B、14B、32B、72B 等尺寸。`Qwen2.5-14B-Instruct` 适合作为私有化部署的主模型，在成本、效果和推理资源之间比较平衡。
- LangChain v0.3 在 2024-09 发布，2025.04 时其 Python 生态已围绕 Pydantic 2、Runnable、Tool、Agent 编排形成稳定实践。
- Milvus 2.5 在 2024-12 发布，2025.04 时 2.5.x 已有多个补丁版本，适合用于法规库语义检索、关键词检索和元数据过滤。

## 面试表述建议

可以这样讲：

> 这个项目不是单纯把法规丢给大模型问答，而是把税务专家的诊断流程拆成了可审计的 Agent 工作流。主 Agent 负责提出风险假设并调用 SQL、指标和法规检索工具补证；监督 Agent 负责检查数据口径、证据完整性和结论一致性。只要出现数据缺失、规则冲突或置信度不足，就进入人工复核队列，避免大模型直接生成不可追责的结论。

## 参考来源

- Qwen 官方博客：`https://qwenlm.github.io/blog/qwen2.5/`
- LangChain v0.3 发布公告：`https://www.langchain.com/blog/announcing-langchain-v0-3`
- Milvus v2.5 release notes：`https://milvus.io/docs/v2.5.x/release_notes.md`

