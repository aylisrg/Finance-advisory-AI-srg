from unittest.mock import MagicMock

from src.services.portfolio_service import PortfolioService


class TestPortfolioSummary:
    def _make_asset(self, quantity, purchase_price, current_price):
        asset = MagicMock()
        asset.quantity = quantity
        asset.purchase_price = purchase_price
        asset.current_price = current_price
        return asset

    def test_empty_portfolio(self):
        portfolio = MagicMock()
        portfolio.assets = []
        summary = PortfolioService.calculate_portfolio_summary(portfolio)
        assert summary["total_value"] == 0
        assert summary["asset_count"] == 0

    def test_portfolio_with_assets(self):
        portfolio = MagicMock()
        portfolio.assets = [
            self._make_asset(10, 100, 150),
            self._make_asset(5, 200, 180),
        ]
        summary = PortfolioService.calculate_portfolio_summary(portfolio)
        assert summary["total_value"] == 10 * 150 + 5 * 180
        assert summary["total_cost"] == 10 * 100 + 5 * 200
        assert summary["total_gain_loss"] == summary["total_value"] - summary["total_cost"]
        assert summary["asset_count"] == 2

    def test_portfolio_with_loss(self):
        portfolio = MagicMock()
        portfolio.assets = [self._make_asset(10, 100, 50)]
        summary = PortfolioService.calculate_portfolio_summary(portfolio)
        assert summary["total_gain_loss"] < 0
        assert summary["total_return_pct"] < 0
