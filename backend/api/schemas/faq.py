from pydantic import BaseModel, Field


class FaqCreate(BaseModel):
    question: str
    answer: str
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class FaqUpdate(BaseModel):
    question: str
    answer: str
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class FaqResponse(BaseModel):
    id: int
    question: str
    answer: str
    position: int
    is_hidden: bool