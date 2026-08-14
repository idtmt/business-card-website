from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    title: str
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class LocationUpdate(BaseModel):
    title: str
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    position: int = Field(default=0, ge=0)
    is_hidden: bool = False


class LocationResponse(BaseModel):
    id: int
    title: str
    address: str
    latitude: float
    longitude: float
    position: int
    is_hidden: bool