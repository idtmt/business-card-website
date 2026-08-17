export interface PriceCreate {
  service_id: number
  title: string
  price: string
  position?: number
  is_hidden?: boolean
}

export interface PriceUpdate {
  title: string
  price: string
  position?: number
  is_hidden?: boolean
}

export interface PriceResponse {
  id: number
  service_id: number
  title: string
  price: string
  position: number
  is_hidden: boolean
}

export interface PublicPriceResponse {
  id: number
  title: string
  price: string
  position: number
}