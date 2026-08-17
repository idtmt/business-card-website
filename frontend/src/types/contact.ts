export interface ContactCreate {
  title: string
  value: string
  url?: string | null
  icon?: string | null
  position?: number
  is_hidden?: boolean
}

export interface ContactUpdate {
  title: string
  value: string
  url?: string | null
  icon?: string | null
  position?: number
  is_hidden?: boolean
}

export interface ContactResponse {
  id: number
  title: string
  value: string
  url: string | null
  icon: string | null
  position: number
  is_hidden: boolean
}