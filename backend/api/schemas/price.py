from pydantic import BaseModel, Field


class PriceCreate(BaseModel):
    service_id: int
    title: str
    price: str
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class PriceUpdate(BaseModel):
    title: str
    price: str
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class PriceResponse(BaseModel):
    id: int
    service_id: int
    title: str
    price: str
    position: int
    is_hidden: bool