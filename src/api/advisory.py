from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import AdvisoryRequest, AdvisoryResponseSchema
from src.config.database import get_db
from src.models.user import User
from src.services.ai_advisor import AIAdvisor
from src.services.portfolio_service import PortfolioService
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/advisory", tags=["AI Advisory"])


@router.post("/ask", response_model=AdvisoryResponseSchema)
async def ask_advisor(
    request: AdvisoryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    portfolio_summary = None
    if request.portfolio_id:
        portfolio = await PortfolioService.get_portfolio(db, request.portfolio_id, current_user.id)
        if portfolio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found"
            )
        summary = PortfolioService.calculate_portfolio_summary(portfolio)
        portfolio_summary = (
            f"Portfolio '{portfolio.name}': "
            f"Total value: ${summary['total_value']:,.2f}, "
            f"Return: {summary['total_return_pct']:.2f}%, "
            f"Assets: {summary['asset_count']}"
        )

    advisor = AIAdvisor()
    try:
        result = await advisor.get_advice(
            query=request.query,
            portfolio_summary=portfolio_summary,
            risk_tolerance=current_user.risk_tolerance.value,
        )
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))

    return AdvisoryResponseSchema(
        advice=result.advice,
        confidence=result.confidence,
        disclaimer=result.disclaimer,
    )
