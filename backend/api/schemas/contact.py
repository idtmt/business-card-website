from pydantic import BaseModel, Field


class ContactCreate(BaseModel):
    title: str
    value: str
    url: str | None = None
    icon: str | None = None
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class ContactUpdate(BaseModel):
    title: str
    value: str
    url: str | None = None
    icon: str | None = None
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class ContactResponse(BaseModel):
    id: int
    title: str
    value: str
    url: str | None
    icon: str | None
    position: int
    is_hidden: bool