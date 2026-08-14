from fastapi import APIRouter, Depends, status

from backend.api.dependencies import get_schedule_service
from backend.api.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)
from backend.services.schedule_service import ScheduleService


router = APIRouter(
    prefix="/schedules",
    tags=["Admin — Schedules"],
)


@router.post(
    "",
    response_model=int,
    status_code=status.HTTP_201_CREATED,
)
async def create_schedule(
    data: ScheduleCreate,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    return await service.create(
        location_id=data.location_id,
        weekday=data.weekday,
        start_time=data.start_time,
        end_time=data.end_time,
        is_day_off=data.is_day_off,
    )


@router.get(
    "/location/{location_id}/weekday/{weekday}",
    response_model=ScheduleResponse,
)
async def get_schedule_by_location_and_weekday(
    location_id: int,
    weekday: int,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    return await service.get_by_location_and_weekday(
        location_id=location_id,
        weekday=weekday,
    )


@router.get(
    "/location/{location_id}",
    response_model=list[ScheduleResponse],
)
async def get_schedules_by_location(
    location_id: int,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    return await service.get_by_location(
        location_id,
    )


@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse,
)
async def get_schedule(
    schedule_id: int,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    return await service.get_by_id(
        schedule_id,
    )


@router.put(
    "/{schedule_id}",
)
async def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    await service.update(
        schedule_id=schedule_id,
        weekday=data.weekday,
        start_time=data.start_time,
        end_time=data.end_time,
        is_day_off=data.is_day_off,
    )

    return {
        "message": "Расписание обновлено.",
    }


@router.delete(
    "/{schedule_id}",
)
async def delete_schedule(
    schedule_id: int,
    service: ScheduleService = Depends(
        get_schedule_service,
    ),
):
    await service.delete(
        schedule_id,
    )

    return {
        "message": "Расписание удалено.",
    }