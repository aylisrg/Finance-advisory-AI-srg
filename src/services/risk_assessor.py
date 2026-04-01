from dataclasses import dataclass

from src.models.portfolio import AssetType


@dataclass
class RiskProfile:
    score: float  # 0-100
    level: str  # low, medium, high
    diversification_score: float  # 0-100
    concentration_risk: float  # 0-100
    recommendations: list[str]


class RiskAssessor:
    """Assess portfolio risk based on asset allocation and diversification."""

    ASSET_RISK_WEIGHTS: dict[str, float] = {
        AssetType.CASH: 0.05,
        AssetType.BOND: 0.2,
        AssetType.REAL_ESTATE: 0.4,
        AssetType.ETF: 0.5,
        AssetType.STOCK: 0.7,
        AssetType.COMMODITY: 0.75,
        AssetType.CRYPTO: 0.95,
    }

    @staticmethod
    def assess_portfolio(
        assets: list[dict],
    ) -> RiskProfile:
        """Assess risk for a list of portfolio assets.

        Each asset dict should have: asset_type, market_value
        """
        if not assets:
            return RiskProfile(
                score=0,
                level="low",
                diversification_score=0,
                concentration_risk=0,
                recommendations=["Add assets to your portfolio to begin assessment."],
            )

        total_value = sum(a["market_value"] for a in assets)
        if total_value == 0:
            return RiskProfile(
                score=0,
                level="low",
                diversification_score=0,
                concentration_risk=0,
                recommendations=["Portfolio has no market value."],
            )

        # Weighted risk score
        risk_score = 0.0
        for asset in assets:
            weight = asset["market_value"] / total_value
            asset_risk = RiskAssessor.ASSET_RISK_WEIGHTS.get(asset["asset_type"], 0.5)
            risk_score += weight * asset_risk
        risk_score *= 100

        # Diversification: based on number of distinct asset types
        unique_types = len({a["asset_type"] for a in assets})
        total_types = len(AssetType)
        diversification_score = min((unique_types / total_types) * 100, 100)

        # Concentration risk: largest single position
        max_position = max(a["market_value"] for a in assets)
        concentration_risk = (max_position / total_value) * 100

        # Risk level
        if risk_score < 30:
            level = "low"
        elif risk_score < 60:
            level = "medium"
        else:
            level = "high"

        recommendations = RiskAssessor._generate_recommendations(
            risk_score, diversification_score, concentration_risk, assets
        )

        return RiskProfile(
            score=round(risk_score, 2),
            level=level,
            diversification_score=round(diversification_score, 2),
            concentration_risk=round(concentration_risk, 2),
            recommendations=recommendations,
        )

    @staticmethod
    def _generate_recommendations(
        risk_score: float,
        diversification_score: float,
        concentration_risk: float,
        assets: list[dict],
    ) -> list[str]:
        recommendations = []

        if diversification_score < 40:
            recommendations.append(
                "Consider diversifying across more asset classes to reduce risk."
            )

        if concentration_risk > 50:
            recommendations.append(
                "High concentration risk: consider spreading investments more evenly."
            )

        if risk_score > 70:
            recommendations.append(
                "Portfolio risk is high. Consider adding bonds or cash positions."
            )

        has_bonds = any(a["asset_type"] == AssetType.BOND for a in assets)
        if not has_bonds and risk_score > 40:
            recommendations.append("Adding bonds could help balance your portfolio risk.")

        if not recommendations:
            recommendations.append("Portfolio risk profile looks well-balanced.")

        return recommendations
