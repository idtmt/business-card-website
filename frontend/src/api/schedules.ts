import { apiRequest } from './client'
import type {
  ScheduleCreate,
  ScheduleUpdate,
  ScheduleResponse,
} from '../types/schedule'

export function getSchedule(
  scheduleId: number,
): Promise<ScheduleResponse> {
  return apiRequest<ScheduleResponse>(
    `/admin/schedules/${scheduleId}`,
  )
}

export function getSchedulesByLocation(
  locationId: number,
): Promise<ScheduleResponse[]> {
  return apiRequest<ScheduleResponse[]>(
    `/admin/schedules/location/${locationId}`,
  )
}

export function getScheduleByLocationAndWeekday(
  locationId: number,
  weekday: number,
): Promise<ScheduleResponse> {
  return apiRequest<ScheduleResponse>(
    `/admin/schedules/location/${locationId}/weekday/${weekday}`,
  )
}

export function createSchedule(
  data: ScheduleCreate,
): Promise<number> {
  return apiRequest<number>('/admin/schedules', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateSchedule(
  scheduleId: number,
  data: ScheduleUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/schedules/${scheduleId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deleteSchedule(
  scheduleId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/schedules/${scheduleId}`,
    {
      method: 'DELETE',
    },
  )
}