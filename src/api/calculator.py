from fastapi import APIRouter

from src.api.schemas import CompoundInterestRequest, CompoundInterestResponse
from src.services.financial_calculator import FinancialCalculator

router = APIRouter(prefix="/calculator", tags=["Financial Calculator"])


@router.post("/compound-interest", response_model=CompoundInterestResponse)
async def compound_interest(request: CompoundInterestRequest):
    final_amount = FinancialCalculator.compound_interest(
        principal=request.principal,
        annual_rate=request.annual_rate,
        years=request.years,
        compounds_per_year=request.compounds_per_year,
    )
    return CompoundInterestResponse(
        principal=request.principal,
        final_amount=round(final_amount, 2),
        total_interest=round(final_amount - request.principal, 2),
        annual_rate=request.annual_rate,
        years=request.years,
    )
