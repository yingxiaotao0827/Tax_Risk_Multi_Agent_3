from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

from tax_risk_ai.app.core.config import Settings


class MockTaxChatModel(BaseChatModel):
    """Deterministic fallback for demos and CI without GPU access."""

    model_name: str = Field(default="mock-qwen2.5-14b")

    @property
    def _llm_type(self) -> str:
        return "mock-tax-chat"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        content = (
            "已完成税务风险诊断。重点关注进项税额异常增长、收入与销项发票背离、"
            "成本费用率异常波动，并要求保留 SQL、指标和法规证据链。"
        )
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])


def build_chat_model(settings: Settings) -> BaseChatModel:
    if settings.llm_provider == "openai_compatible":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            temperature=0.1,
        )
    return MockTaxChatModel()

