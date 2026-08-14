from pydantic import BaseModel, Field


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class ServiceUpdate(BaseModel):
    name: str
    description: str | None = None
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    position: int
    is_hidden: bool