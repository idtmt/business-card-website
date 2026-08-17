import { apiRequest } from './client'
import type {
  CompanyCreate,
  CompanyUpdate,
  CompanyResponse,
} from '../types/company'

export function getCompany(): Promise<CompanyResponse | null> {
  return apiRequest<CompanyResponse | null>('/company')
}

export function createCompany(
  data: CompanyCreate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/admin/company', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateCompany(
  data: CompanyUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/admin/company', {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}