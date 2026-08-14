from pydantic import BaseModel


class CompanyCreate(BaseModel):
    name: str
    description: str | None = None


class CompanyUpdate(BaseModel):
    name: str
    description: str | None = None


class CompanyResponse(BaseModel):
    name: str
    description: str | None = None