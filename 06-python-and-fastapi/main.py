from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Loan Intake — Validation Test", version="1.0")


# Version 2: checks TYPES only (is it text? is it a number?)
class ApplicationTypes(BaseModel):
    applicant_name: str
    monthly_income: int
    amount_requested: int
    purpose: str


# Version 3: checks TYPES + BUSINESS RULES
class ApplicationRules(BaseModel):
    applicant_name: str = Field(min_length=2, max_length=100)
    monthly_income: int = Field(gt=0, le=10_000_000)      # above 0, max ₹1 crore/month
    amount_requested: int = Field(gt=0, le=50_000_000)    # above 0, max ₹5 crore
    purpose: str = Field(min_length=3, max_length=200)


@app.get("/health")
def health():
    return {"status": "ok"}


# Version 1: NO checks at all, accepts anything
@app.post("/v1/no-checks")
def no_checks(application: dict):
    return {"accepted": True, "received": application}


@app.post("/v2/types-only")
def types_only(application: ApplicationTypes):
    return {"accepted": True, "received": application}


@app.post("/v3/types-and-rules")
def types_and_rules(application: ApplicationRules):
    return {"accepted": True, "received": application}