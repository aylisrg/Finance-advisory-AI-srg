from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.portfolio import AssetType, Portfolio, PortfolioAsset
from src.models.transaction import Transaction, TransactionType
from src.services.financial_calculator import FinancialCalculator


class PortfolioService:
    """Service for managing user portfolios."""

    @staticmethod
    async def create_portfolio(
        db: AsyncSession, user_id: int, name: str, description: str | None = None
    ) -> Portfolio:
        portfolio = Portfolio(user_id=user_id, name=name, description=description)
        db.add(portfolio)
        await db.flush()
        await db.refresh(portfolio, ["assets"])
        return portfolio

    @staticmethod
    async def get_user_portfolios(db: AsyncSession, user_id: int) -> list[Portfolio]:
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.user_id == user_id)
            .options(selectinload(Portfolio.assets))
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_portfolio(db: AsyncSession, portfolio_id: int, user_id: int) -> Portfolio | None:
        result = await db.execute(
            select(Portfolio)
            .where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
            .options(selectinload(Portfolio.assets))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def add_asset(
        db: AsyncSession,
        portfolio_id: int,
        symbol: str,
        asset_type: AssetType,
        quantity: float,
        purchase_price: float,
        current_price: float | None = None,
    ) -> PortfolioAsset:
        asset = PortfolioAsset(
            portfolio_id=portfolio_id,
            symbol=symbol,
            asset_type=asset_type,
            quantity=quantity,
            purchase_price=purchase_price,
            current_price=current_price or purchase_price,
        )
        db.add(asset)
        await db.flush()
        await db.refresh(asset)
        return asset

    @staticmethod
    async def record_transaction(
        db: AsyncSession,
        user_id: int,
        portfolio_id: int | None,
        transaction_type: TransactionType,
        price: float,
        quantity: float | None = None,
        symbol: str | None = None,
    ) -> Transaction:
        total_amount = price * (quantity or 1)
        txn = Transaction(
            user_id=user_id,
            portfolio_id=portfolio_id,
            transaction_type=transaction_type,
            symbol=symbol,
            quantity=quantity,
            price=price,
            total_amount=total_amount,
        )
        db.add(txn)
        await db.flush()
        await db.refresh(txn)
        return txn

    @staticmethod
    def calculate_portfolio_summary(portfolio: Portfolio) -> dict:
        """Calculate portfolio summary metrics."""
        assets = portfolio.assets
        if not assets:
            return {
                "total_value": 0,
                "total_cost": 0,
                "total_gain_loss": 0,
                "total_return_pct": 0,
                "asset_count": 0,
            }

        total_value = sum(a.quantity * a.current_price for a in assets)
        total_cost = sum(a.quantity * a.purchase_price for a in assets)
        total_gain_loss = total_value - total_cost
        total_return_pct = FinancialCalculator.simple_return(total_cost, total_value)

        return {
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain_loss": round(total_gain_loss, 2),
            "total_return_pct": round(total_return_pct, 2),
            "asset_count": len(assets),
        }
