import { defineStore } from 'pinia'

import {
  getCurrentUser,
  login,
  logout,
} from '../api/auth'

import type {
  LoginRequest,
  UserResponse,
} from '../types/auth'


export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as UserResponse | null,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
  },

  actions: {
    async initialize() {
      if (this.initialized) {
        return
      }

      try {
        this.user = await getCurrentUser()
      } catch {
        this.user = null
      } finally {
        this.initialized = true
      }
    },

    async login(data: LoginRequest) {
      await login(data)
      this.user = await getCurrentUser()
    },

    async logout() {
      try {
        await logout()
      } finally {
        this.user = null
      }
    },
  },
})