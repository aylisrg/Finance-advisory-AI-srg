import pytest
from httpx import AsyncClient


class TestCalculatorAPI:
    @pytest.mark.asyncio
    async def test_compound_interest(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/calculator/compound-interest",
            json={
                "principal": 10000,
                "annual_rate": 0.05,
                "years": 10,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["principal"] == 10000
        assert data["final_amount"] > 10000
        assert data["total_interest"] > 0

    @pytest.mark.asyncio
    async def test_compound_interest_invalid_principal(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/calculator/compound-interest",
            json={
                "principal": -1000,
                "annual_rate": 0.05,
                "years": 10,
            },
        )
        assert response.status_code == 422
