import { apiRequest } from './client'
import type {
  LocationCreate,
  LocationUpdate,
  LocationResponse,
  PublicLocationResponse,
} from '../types/location'

export function getPublicLocations(): Promise<PublicLocationResponse[]> {
  return apiRequest<PublicLocationResponse[]>('/locations')
}

export function getPublicLocation(
  locationId: number,
): Promise<PublicLocationResponse> {
  return apiRequest<PublicLocationResponse>(
    `/locations/${locationId}`,
  )
}

export function getAdminLocations(
  isHidden?: boolean,
): Promise<LocationResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<LocationResponse[]>(
    `/admin/locations${query}`,
  )
}

export function getAdminLocation(
  locationId: number,
): Promise<LocationResponse> {
  return apiRequest<LocationResponse>(
    `/admin/locations/${locationId}`,
  )
}

export function createLocation(
  data: LocationCreate,
): Promise<number> {
  return apiRequest<number>('/admin/locations', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateLocation(
  locationId: number,
  data: LocationUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/locations/${locationId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deleteLocation(
  locationId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/locations/${locationId}`,
    {
      method: 'DELETE',
    },
  )
}