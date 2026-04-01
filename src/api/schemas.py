from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# --- Auth ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    risk_tolerance: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Portfolio ---
class CreatePortfolioRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class AddAssetRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    asset_type: str
    quantity: float = Field(gt=0)
    purchase_price: float = Field(gt=0)
    current_price: float | None = Field(default=None, gt=0)


class AssetResponse(BaseModel):
    id: int
    symbol: str
    asset_type: str
    quantity: float
    purchase_price: float
    current_price: float

    model_config = {"from_attributes": True}


class PortfolioResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    assets: list[AssetResponse] = []

    model_config = {"from_attributes": True}


class PortfolioSummaryResponse(BaseModel):
    portfolio: PortfolioResponse
    summary: dict


# --- Risk ---
class RiskAssessmentResponse(BaseModel):
    score: float
    level: str
    diversification_score: float
    concentration_risk: float
    recommendations: list[str]


# --- AI Advisory ---
class AdvisoryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    portfolio_id: int | None = None


class AdvisoryResponseSchema(BaseModel):
    advice: str
    confidence: float
    disclaimer: str


# --- Financial Calculator ---
class CompoundInterestRequest(BaseModel):
    principal: float = Field(gt=0)
    annual_rate: float = Field(ge=0, le=1)
    years: float = Field(gt=0)
    compounds_per_year: int = Field(default=12, gt=0)


class CompoundInterestResponse(BaseModel):
    principal: float
    final_amount: float
    total_interest: float
    annual_rate: float
    years: float
