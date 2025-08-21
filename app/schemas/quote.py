from typing import Optional, Literal, List
from pydantic import BaseModel, Field, validator


Usage = Literal["particular", "comercial"]


class QuoteState(BaseModel):
    vehicle_year: Optional[int] = Field(None, ge=1980, le=2035)
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_value_usd: Optional[float] = Field(None, gt=0)
    usage: Optional[Usage] = None
    city: Optional[str] = None
    driver_age: Optional[int] = Field(None, ge=16, le=90)
    claims_last3y: Optional[int] = Field(None, ge=0, le=10)

    anti_theft: Optional[bool] = None
    garage_overnight: Optional[bool] = None
    deductible_pct: Optional[int] = None  # 5/10/15/20
    addons: Optional[List[Literal["asistencia_vial", "auto_reemplazo", "cobertura_lunas"]]] = None

    @validator("deductible_pct")
    def check_deductible(cls, v):
        if v is None:
            return v
        if v not in (5, 10, 15, 20):
            raise ValueError("deductible_pct debe ser 5, 10, 15 o 20")
        return v

    def missing_fields(self) -> List[str]:
        required = [
            "vehicle_year","vehicle_make","vehicle_model",
            "vehicle_value_usd","usage","city","driver_age","claims_last3y"
        ]
        return [f for f in required if getattr(self, f) in (None, "", [])]


class StartResponse(BaseModel):
    session_id: str
    message: str


class ReplyRequest(BaseModel):
    session_id: str
    user_text: str


class Offer(BaseModel):
    carrier: str
    plan: Literal["Básica","Media","Full"]
    annual_premium_usd: float
    deductible_pct: int
    addons: List[str]
    coverage_notes: str


class QuoteResult(BaseModel):
    offers: List[Offer]
    recommendation: str
    disclaimer: str


class ReplyResponse(BaseModel):
    session_id: str
    message: str
    state: QuoteState
    quote: Optional[QuoteResult] = None
