import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import type { LoginRequest } from '../types/auth'

export function useAuth() {
  const router = useRouter()
  const authStore = useAuthStore()

  const loading = ref(false)
  const error = ref('')

  async function login(data: LoginRequest) {
    error.value = ''
    loading.value = true

    try {
      await authStore.login(data)

      await router.push({
        name: 'admin-dashboard',
      })
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось выполнить вход.'

      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    await authStore.logout()

    await router.push({
      name: 'login',
    })
  }

  return {
    loading,
    error,
    isAuthenticated: authStore.isAuthenticated,
    user: authStore.user,
    login,
    logout,
  }
}