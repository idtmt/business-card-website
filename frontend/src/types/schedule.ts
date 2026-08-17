export interface ScheduleCreate {
  location_id: number
  weekday: number
  start_time?: string | null
  end_time?: string | null
  is_day_off?: boolean
}

export interface ScheduleUpdate {
  weekday: number
  start_time?: string | null
  end_time?: string | null
  is_day_off?: boolean
}

export interface ScheduleResponse {
  id: number
  location_id: number
  weekday: number
  start_time: string | null
  end_time: string | null
  is_day_off: boolean
}