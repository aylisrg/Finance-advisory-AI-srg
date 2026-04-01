import pytest

from src.services.ai_advisor import AIAdvisor


class TestAIAdvisor:
    def test_build_user_message_with_all_params(self):
        msg = AIAdvisor._build_user_message(
            query="Should I invest in stocks?",
            portfolio_summary="Total: $10,000",
            risk_tolerance="moderate",
        )
        assert "moderate" in msg
        assert "Total: $10,000" in msg
        assert "Should I invest in stocks?" in msg

    def test_build_user_message_without_portfolio(self):
        msg = AIAdvisor._build_user_message(
            query="What is a bond?",
            portfolio_summary=None,
            risk_tolerance="conservative",
        )
        assert "conservative" in msg
        assert "What is a bond?" in msg
        assert "Portfolio" not in msg

    def test_get_client_without_api_key(self):
        advisor = AIAdvisor()
        advisor.api_key = ""
        with pytest.raises(RuntimeError, match="OpenAI API key not configured"):
            advisor._get_client()

    @pytest.mark.asyncio
    async def test_get_advice_without_api_key(self):
        advisor = AIAdvisor()
        advisor.api_key = ""
        with pytest.raises(RuntimeError, match="OpenAI API key not configured"):
            await advisor.get_advice("test query")
