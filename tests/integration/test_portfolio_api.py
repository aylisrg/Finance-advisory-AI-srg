import pytest
from httpx import AsyncClient


class TestPortfolioAPI:
    @pytest.mark.asyncio
    async def test_create_portfolio(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "My Portfolio", "description": "Test portfolio"},
        )
        assert response.status_code == 201
        assert response.json()["name"] == "My Portfolio"

    @pytest.mark.asyncio
    async def test_list_portfolios(self, authenticated_client: AsyncClient):
        await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "Portfolio 1"},
        )
        await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "Portfolio 2"},
        )
        response = await authenticated_client.get("/api/v1/portfolios/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    @pytest.mark.asyncio
    async def test_get_portfolio_with_summary(self, authenticated_client: AsyncClient):
        create_resp = await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "Detailed Portfolio"},
        )
        portfolio_id = create_resp.json()["id"]

        response = await authenticated_client.get(f"/api/v1/portfolios/{portfolio_id}")
        assert response.status_code == 200
        assert "summary" in response.json()
        assert response.json()["summary"]["total_value"] == 0

    @pytest.mark.asyncio
    async def test_add_asset(self, authenticated_client: AsyncClient):
        create_resp = await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "Asset Portfolio"},
        )
        portfolio_id = create_resp.json()["id"]

        response = await authenticated_client.post(
            f"/api/v1/portfolios/{portfolio_id}/assets",
            json={
                "symbol": "AAPL",
                "asset_type": "stock",
                "quantity": 10,
                "purchase_price": 150.0,
                "current_price": 175.0,
            },
        )
        assert response.status_code == 201
        assert response.json()["symbol"] == "AAPL"

    @pytest.mark.asyncio
    async def test_portfolio_risk_assessment(self, authenticated_client: AsyncClient):
        create_resp = await authenticated_client.post(
            "/api/v1/portfolios/",
            json={"name": "Risk Portfolio"},
        )
        portfolio_id = create_resp.json()["id"]

        await authenticated_client.post(
            f"/api/v1/portfolios/{portfolio_id}/assets",
            json={
                "symbol": "AAPL",
                "asset_type": "stock",
                "quantity": 10,
                "purchase_price": 150.0,
                "current_price": 175.0,
            },
        )

        response = await authenticated_client.get(
            f"/api/v1/portfolios/{portfolio_id}/risk"
        )
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "level" in data
        assert "recommendations" in data

    @pytest.mark.asyncio
    async def test_portfolio_not_found(self, authenticated_client: AsyncClient):
        response = await authenticated_client.get("/api/v1/portfolios/999")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_unauthorized_access(self, client: AsyncClient):
        response = await client.get("/api/v1/portfolios/")
        assert response.status_code == 403
