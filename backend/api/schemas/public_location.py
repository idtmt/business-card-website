from pydantic import BaseModel


class PublicScheduleResponse(BaseModel):
    id: int
    weekday: int
    start_time: str | None
    end_time: str | None
    is_day_off: bool


class PublicLocationResponse(BaseModel):
    id: int
    title: str
    address: str
    latitude: float
    longitude: float
    position: int
    schedules: list[PublicScheduleResponse]