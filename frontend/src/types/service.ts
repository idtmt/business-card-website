import type { PublicPriceResponse } from './price'

export interface ServiceCreate {
  name: string
  description?: string | null
  position?: number
  is_hidden?: boolean
}

export interface ServiceUpdate {
  name: string
  description?: string | null
  position?: number
  is_hidden?: boolean
}

export interface ServiceResponse {
  id: number
  name: string
  description: string | null
  position: number
  is_hidden: boolean
}

export interface PublicServiceResponse {
  id: number
  name: string
  description: string | null
  position: number
  prices: PublicPriceResponse[]
}