import { ref } from 'vue'

import {
  getAdminLocations,
  createLocation,
  updateLocation,
  deleteLocation,
} from '../api/locations'

import {
  getSchedulesByLocation,
  createSchedule,
  updateSchedule,
  deleteSchedule,
} from '../api/schedules'

import type {
  LocationCreate,
  LocationUpdate,
  LocationResponse,
} from '../types/location'

import type {
  ScheduleCreate,
  ScheduleUpdate,
  ScheduleResponse,
} from '../types/schedule'


export function useLocations() {
  const locations = ref<LocationResponse[]>([])
  const schedules = ref<Record<number, ScheduleResponse[]>>({})

  const loading = ref(false)
  const error = ref<string | null>(null)


  async function loadLocations() {
    loading.value = true
    error.value = null

    try {
      locations.value = await getAdminLocations()
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить локации.'
    } finally {
      loading.value = false
    }
  }


  async function loadSchedules(locationId: number) {
    try {
      schedules.value[locationId] =
        await getSchedulesByLocation(locationId)
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить расписание.'
    }
  }


  async function addLocation(data: LocationCreate) {
    await createLocation(data)
    await loadLocations()
  }


  async function editLocation(
    locationId: number,
    data: LocationUpdate,
  ) {
    await updateLocation(locationId, data)
    await loadLocations()
  }


  async function removeLocation(locationId: number) {
    await deleteLocation(locationId)

    delete schedules.value[locationId]

    await loadLocations()
  }


  async function addSchedule(data: ScheduleCreate) {
    await createSchedule(data)
    await loadSchedules(data.location_id)
  }


  async function editSchedule(
    scheduleId: number,
    locationId: number,
    data: ScheduleUpdate,
  ) {
    await updateSchedule(scheduleId, data)
    await loadSchedules(locationId)
  }


  async function removeSchedule(
    scheduleId: number,
    locationId: number,
  ) {
    await deleteSchedule(scheduleId)
    await loadSchedules(locationId)
  }


  return {
    locations,
    schedules,
    loading,
    error,

    loadLocations,
    loadSchedules,

    addLocation,
    editLocation,
    removeLocation,

    addSchedule,
    editSchedule,
    removeSchedule,
  }
}