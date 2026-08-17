export interface LocationCreate {
  title: string
  address: string
  latitude: number
  longitude: number
  position?: number
  is_hidden?: boolean
}

export interface LocationUpdate {
  title: string
  address: string
  latitude: number
  longitude: number
  position?: number
  is_hidden?: boolean
}

export interface LocationResponse {
  id: number
  title: string
  address: string
  latitude: number
  longitude: number
  position: number
  is_hidden: boolean
}

export interface PublicScheduleResponse {
  id: number
  weekday: number
  start_time: string | null
  end_time: string | null
  is_day_off: boolean
}

export interface PublicLocationResponse {
  id: number
  title: string
  address: string
  latitude: number
  longitude: number
  position: number
  schedules: PublicScheduleResponse[]
}