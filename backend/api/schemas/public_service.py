from pydantic import BaseModel


class PublicPriceResponse(BaseModel):
    id: int
    title: str
    price: str
    position: int


class PublicServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    position: int
    prices: list[PublicPriceResponse]