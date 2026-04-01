from dataclasses import dataclass

from src.config.settings import get_settings


@dataclass
class AdvisoryResponse:
    advice: str
    confidence: float
    disclaimer: str = (
        "This is AI-generated financial guidance, not professional financial advice. "
        "Always consult a certified financial advisor before making investment decisions."
    )


class AIAdvisor:
    """AI-powered financial advisory service using Google Gemini."""

    SYSTEM_PROMPT = (
        "You are a knowledgeable financial advisor AI. Provide clear, actionable financial "
        "guidance based on the user's portfolio, risk tolerance, and financial goals. "
        "Always mention that your advice is for informational purposes only and recommend "
        "consulting a certified financial advisor for personalized advice."
    )

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.api_key_gemini
        self._client = None

    def _get_client(self):
        if not self.api_key:
            raise RuntimeError(
                "Gemini API key not configured. Set API_KEY_GEMINI environment variable."
            )
        if self._client is None:
            from google import genai

            self._client = genai.Client(api_key=self.api_key)
        return self._client

    async def get_advice(
        self,
        query: str,
        portfolio_summary: str | None = None,
        risk_tolerance: str = "moderate",
    ) -> AdvisoryResponse:
        """Get AI-powered financial advice."""
        user_message = self._build_user_message(query, portfolio_summary, risk_tolerance)

        try:
            client = self._get_client()
            response = await client.aio.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"{self.SYSTEM_PROMPT}\n\n{user_message}",
            )
            advice = response.text
            return AdvisoryResponse(advice=advice, confidence=0.85)
        except RuntimeError:
            raise
        except Exception as e:
            return AdvisoryResponse(
                advice=f"Unable to generate advice at this time: {e}",
                confidence=0.0,
            )

    @staticmethod
    def _build_user_message(
        query: str,
        portfolio_summary: str | None,
        risk_tolerance: str,
    ) -> str:
        parts = [f"Risk tolerance: {risk_tolerance}"]
        if portfolio_summary:
            parts.append(f"Portfolio summary:\n{portfolio_summary}")
        parts.append(f"Question: {query}")
        return "\n\n".join(parts)
