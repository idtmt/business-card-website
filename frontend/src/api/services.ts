import { apiRequest } from './client'
import type {
  ServiceCreate,
  ServiceUpdate,
  ServiceResponse,
  PublicServiceResponse,
} from '../types/service'

export function getPublicServices(): Promise<PublicServiceResponse[]> {
  return apiRequest<PublicServiceResponse[]>('/services')
}

export function getPublicService(
  serviceId: number,
): Promise<PublicServiceResponse> {
  return apiRequest<PublicServiceResponse>(
    `/services/${serviceId}`,
  )
}

export function getAdminServices(
  isHidden?: boolean,
): Promise<ServiceResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<ServiceResponse[]>(
    `/admin/services${query}`,
  )
}

export function getAdminService(
  serviceId: number,
): Promise<ServiceResponse> {
  return apiRequest<ServiceResponse>(
    `/admin/services/${serviceId}`,
  )
}

export function createService(
  data: ServiceCreate,
): Promise<number> {
  return apiRequest<number>('/admin/services', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateService(
  serviceId: number,
  data: ServiceUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/services/${serviceId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deleteService(
  serviceId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/services/${serviceId}`,
    {
      method: 'DELETE',
    },
  )
}