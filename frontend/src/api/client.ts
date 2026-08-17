const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

interface RequestOptions extends RequestInit {
  body?: BodyInit | null
}

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    let message = 'Произошла ошибка.'

    try {
      const data = await response.json()

      if (typeof data.detail === 'string') {
        message = data.detail
      }
    } catch {
      // Ответ не содержит JSON
    }

    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}