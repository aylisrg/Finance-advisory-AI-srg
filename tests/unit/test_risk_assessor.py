from src.models.portfolio import AssetType
from src.services.risk_assessor import RiskAssessor


class TestRiskAssessor:
    def test_empty_portfolio(self):
        result = RiskAssessor.assess_portfolio([])
        assert result.score == 0
        assert result.level == "low"

    def test_conservative_portfolio(self):
        assets = [
            {"asset_type": AssetType.BOND, "market_value": 7000},
            {"asset_type": AssetType.CASH, "market_value": 3000},
        ]
        result = RiskAssessor.assess_portfolio(assets)
        assert result.score < 30
        assert result.level == "low"

    def test_aggressive_portfolio(self):
        assets = [
            {"asset_type": AssetType.CRYPTO, "market_value": 8000},
            {"asset_type": AssetType.STOCK, "market_value": 2000},
        ]
        result = RiskAssessor.assess_portfolio(assets)
        assert result.score > 60
        assert result.level == "high"

    def test_diversified_portfolio(self):
        assets = [
            {"asset_type": AssetType.STOCK, "market_value": 2000},
            {"asset_type": AssetType.BOND, "market_value": 2000},
            {"asset_type": AssetType.ETF, "market_value": 2000},
            {"asset_type": AssetType.CASH, "market_value": 2000},
            {"asset_type": AssetType.REAL_ESTATE, "market_value": 2000},
        ]
        result = RiskAssessor.assess_portfolio(assets)
        assert result.diversification_score > 50
        assert result.concentration_risk < 30

    def test_concentrated_portfolio(self):
        assets = [
            {"asset_type": AssetType.STOCK, "market_value": 9000},
            {"asset_type": AssetType.BOND, "market_value": 1000},
        ]
        result = RiskAssessor.assess_portfolio(assets)
        assert result.concentration_risk > 80

    def test_recommendations_for_no_bonds(self):
        assets = [
            {"asset_type": AssetType.STOCK, "market_value": 5000},
            {"asset_type": AssetType.CRYPTO, "market_value": 5000},
        ]
        result = RiskAssessor.assess_portfolio(assets)
        has_bond_recommendation = any("bonds" in r.lower() for r in result.recommendations)
        assert has_bond_recommendation

    def test_zero_value_portfolio(self):
        assets = [{"asset_type": AssetType.STOCK, "market_value": 0}]
        result = RiskAssessor.assess_portfolio(assets)
        assert result.score == 0
