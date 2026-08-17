import { apiRequest } from './client'
import type {
  FaqCreate,
  FaqUpdate,
  FaqResponse,
} from '../types/faq'

export function getPublicFaq(): Promise<FaqResponse[]> {
  return apiRequest<FaqResponse[]>('/faq')
}

export function getPublicFaqItem(
  faqId: number,
): Promise<FaqResponse> {
  return apiRequest<FaqResponse>(
    `/faq/${faqId}`,
  )
}

export function getAdminFaq(
  isHidden?: boolean,
): Promise<FaqResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<FaqResponse[]>(
    `/admin/faq${query}`,
  )
}

export function getAdminFaqItem(
  faqId: number,
): Promise<FaqResponse> {
  return apiRequest<FaqResponse>(
    `/admin/faq/${faqId}`,
  )
}

export function createFaq(
  data: FaqCreate,
): Promise<number> {
  return apiRequest<number>('/admin/faq', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateFaq(
  faqId: number,
  data: FaqUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/faq/${faqId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deleteFaq(
  faqId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/faq/${faqId}`,
    {
      method: 'DELETE',
    },
  )
}