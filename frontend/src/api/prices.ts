import { apiRequest } from './client'
import type {
  PriceCreate,
  PriceUpdate,
  PriceResponse,
} from '../types/price'

export function getAdminPrices(
  isHidden?: boolean,
): Promise<PriceResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<PriceResponse[]>(
    `/admin/prices${query}`,
  )
}

export function getAdminPrice(
  priceId: number,
): Promise<PriceResponse> {
  return apiRequest<PriceResponse>(
    `/admin/prices/${priceId}`,
  )
}

export function getPricesByService(
  serviceId: number,
  isHidden?: boolean,
): Promise<PriceResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<PriceResponse[]>(
    `/admin/prices/service/${serviceId}${query}`,
  )
}

export function createPrice(
  data: PriceCreate,
): Promise<number> {
  return apiRequest<number>('/admin/prices', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updatePrice(
  priceId: number,
  data: PriceUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/prices/${priceId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deletePrice(
  priceId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/prices/${priceId}`,
    {
      method: 'DELETE',
    },
  )
}