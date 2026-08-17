<script setup lang="ts">
import { ref } from 'vue'

import type { LoginRequest } from '../../types/auth'

const props = defineProps<{
  loading?: boolean
  error?: string
}>()

const emit = defineEmits<{
  submit: [data: LoginRequest]
}>()

const username = ref('')
const password = ref('')

function handleSubmit() {
  if (!username.value || !password.value) {
    return
  }

  emit('submit', {
    username: username.value,
    password: password.value,
  })
}
</script>

<template>
  <form
    class="mt-8 space-y-5"
    @submit.prevent="handleSubmit"
  >
    <div>
      <label
        for="username"
        class="block text-sm font-medium text-gray-700"
      >
        Логин
      </label>

      <input
        id="username"
        v-model="username"
        type="text"
        autocomplete="username"
        placeholder="Введите логин"
        :disabled="props.loading"
        class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:bg-gray-50"
      />
    </div>

    <div>
      <label
        for="password"
        class="block text-sm font-medium text-gray-700"
      >
        Пароль
      </label>

      <input
        id="password"
        v-model="password"
        type="password"
        autocomplete="current-password"
        placeholder="Введите пароль"
        :disabled="props.loading"
        class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:bg-gray-50"
      />
    </div>

    <div
      v-if="props.error"
      class="rounded-lg border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      {{ props.error }}
    </div>

    <button
      type="submit"
      :disabled="props.loading || !username || !password"
      class="w-full rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {{ props.loading ? 'Вход...' : 'Войти' }}
    </button>
  </form>
</template>