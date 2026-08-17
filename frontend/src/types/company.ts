export interface CompanyCreate {
  name: string
  description?: string | null
}

export interface CompanyUpdate {
  name: string
  description?: string | null
}

export interface CompanyResponse {
  name: string
  description: string | null
}