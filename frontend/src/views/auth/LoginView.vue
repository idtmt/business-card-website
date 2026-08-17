<script setup lang="ts">
import LoginForm from '../../components/auth/LoginForm.vue'
import { useAuth } from '../../composables/useAuth'

const {
  loading,
  error,
  login,
} = useAuth()
</script>

<template>
  <main
    class="flex min-h-screen items-center justify-center bg-gray-50 px-6"
  >
    <div class="w-full max-w-md">
      <div
        class="rounded-2xl border border-gray-200 bg-white p-8 shadow-sm"
      >
        <div class="text-center">
          <p
            class="text-sm font-medium uppercase tracking-widest text-gray-500"
          >
            Администратор
          </p>

          <h1
            class="mt-3 text-3xl font-bold tracking-tight text-gray-900"
          >
            Вход
          </h1>

          <p class="mt-3 text-sm text-gray-500">
            Войдите для управления сайтом.
          </p>
        </div>

        <LoginForm
          :loading="loading"
          :error="error"
          @submit="login"
        />
      </div>
    </div>
  </main>
</template>