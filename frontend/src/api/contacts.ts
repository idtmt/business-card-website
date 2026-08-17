import { apiRequest } from './client'
import type {
  ContactCreate,
  ContactUpdate,
  ContactResponse,
} from '../types/contact'

export function getPublicContacts(): Promise<ContactResponse[]> {
  return apiRequest<ContactResponse[]>('/contacts')
}

export function getPublicContact(
  contactId: number,
): Promise<ContactResponse> {
  return apiRequest<ContactResponse>(
    `/contacts/${contactId}`,
  )
}

export function getAdminContacts(
  isHidden?: boolean,
): Promise<ContactResponse[]> {
  const query = isHidden === undefined
    ? ''
    : `?is_hidden=${isHidden}`

  return apiRequest<ContactResponse[]>(
    `/admin/contacts${query}`,
  )
}

export function getAdminContact(
  contactId: number,
): Promise<ContactResponse> {
  return apiRequest<ContactResponse>(
    `/admin/contacts/${contactId}`,
  )
}

export function createContact(
  data: ContactCreate,
): Promise<number> {
  return apiRequest<number>('/admin/contacts', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateContact(
  contactId: number,
  data: ContactUpdate,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/contacts/${contactId}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )
}

export function deleteContact(
  contactId: number,
): Promise<{ message: string }> {
  return apiRequest<{ message: string }>(
    `/admin/contacts/${contactId}`,
    {
      method: 'DELETE',
    },
  )
}