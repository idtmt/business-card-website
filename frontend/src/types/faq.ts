export interface FaqCreate {
  question: string
  answer: string
  position?: number
  is_hidden?: boolean
}

export interface FaqUpdate {
  question: string
  answer: string
  position?: number
  is_hidden?: boolean
}

export interface FaqResponse {
  id: number
  question: string
  answer: string
  position: number
  is_hidden: boolean
}