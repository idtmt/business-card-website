import { apiRequest } from './client'
import type {
  LoginRequest,
  LoginResponse,
  UserResponse,
} from '../types/auth'


export function login(
  data: LoginRequest,
): Promise<LoginResponse> {
  return apiRequest<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}


export function logout(): Promise<{ message: string }> {
  return apiRequest<{ message: string }>('/auth/logout', {
    method: 'POST',
  })
}


export function getCurrentUser(): Promise<UserResponse> {
  return apiRequest<UserResponse>('/auth/me')
}