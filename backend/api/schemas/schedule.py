from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    location_id: int
    weekday: int = Field(ge=0, le=6)
    start_time: str | None = None
    end_time: str | None = None
    is_day_off: bool = False


class ScheduleUpdate(BaseModel):
    weekday: int = Field(ge=0, le=6)
    start_time: str | None = None
    end_time: str | None = None
    is_day_off: bool = False


class ScheduleResponse(BaseModel):
    id: int
    location_id: int
    weekday: int
    start_time: str | None
    end_time: str | None
    is_day_off: bool