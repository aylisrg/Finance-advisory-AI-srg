from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas import (
    AddAssetRequest,
    PortfolioResponse,
    PortfolioSummaryResponse,
    CreatePortfolioRequest,
    RiskAssessmentResponse,
)
from src.config.database import get_db
from src.models.portfolio import AssetType
from src.models.user import User
from src.services.portfolio_service import PortfolioService
from src.services.risk_assessor import RiskAssessor
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/portfolios", tags=["Portfolios"])


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    request: CreatePortfolioRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    portfolio = await PortfolioService.create_portfolio(
        db, current_user.id, request.name, request.description
    )
    return portfolio


@router.get("/", response_model=list[PortfolioResponse])
async def list_portfolios(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await PortfolioService.get_user_portfolios(db, current_user.id)


@router.get("/{portfolio_id}", response_model=PortfolioSummaryResponse)
async def get_portfolio(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    portfolio = await PortfolioService.get_portfolio(db, portfolio_id, current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    summary = PortfolioService.calculate_portfolio_summary(portfolio)
    return PortfolioSummaryResponse(portfolio=portfolio, summary=summary)


@router.post("/{portfolio_id}/assets", status_code=status.HTTP_201_CREATED)
async def add_asset(
    portfolio_id: int,
    request: AddAssetRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    portfolio = await PortfolioService.get_portfolio(db, portfolio_id, current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    try:
        asset_type = AssetType(request.asset_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid asset type. Must be one of: {[t.value for t in AssetType]}",
        )

    asset = await PortfolioService.add_asset(
        db,
        portfolio_id,
        request.symbol,
        asset_type,
        request.quantity,
        request.purchase_price,
        request.current_price,
    )
    return {"id": asset.id, "symbol": asset.symbol, "asset_type": asset.asset_type.value}


@router.get("/{portfolio_id}/risk", response_model=RiskAssessmentResponse)
async def assess_risk(
    portfolio_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    portfolio = await PortfolioService.get_portfolio(db, portfolio_id, current_user.id)
    if portfolio is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    assets_data = [
        {"asset_type": a.asset_type, "market_value": a.quantity * a.current_price}
        for a in portfolio.assets
    ]
    risk_profile = RiskAssessor.assess_portfolio(assets_data)
    return RiskAssessmentResponse(
        score=risk_profile.score,
        level=risk_profile.level,
        diversification_score=risk_profile.diversification_score,
        concentration_risk=risk_profile.concentration_risk,
        recommendations=risk_profile.recommendations,
    )
