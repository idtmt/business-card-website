<script setup lang="ts">
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'


const router = useRouter()
const authStore = useAuthStore()


const navigation = [
  {
    name: 'Обзор',
    route: { name: 'admin-dashboard' },
  },
  {
    name: 'Компания',
    route: { name: 'admin-company' },
  },
  {
    name: 'Услуги',
    route: { name: 'admin-services' },
  },
  {
    name: 'Контакты',
    route: { name: 'admin-contacts' },
  },
  {
    name: 'FAQ',
    route: { name: 'admin-faq' },
  },
  {
    name: 'Локации',
    route: { name: 'admin-locations' },
  },
]


async function handleLogout() {
  await authStore.logout()

  await router.push({
    name: 'login',
  })
}
</script>


<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-20 flex w-64 flex-col border-r border-gray-200 bg-white"
    >
      <!-- Logo -->
      <div class="border-b border-gray-200 px-6 py-5">
        <RouterLink
          :to="{ name: 'admin-dashboard' }"
          class="text-lg font-semibold tracking-tight text-gray-900"
        >
          Business Card
        </RouterLink>

        <p class="mt-1 text-xs text-gray-500">
          Панель администратора
        </p>
      </div>


      <!-- Navigation -->
      <nav class="flex-1 px-3 py-5">

        <p
          class="px-3 pb-2 text-xs font-medium uppercase tracking-wider text-gray-400"
        >
          Управление
        </p>

        <RouterLink
          v-for="item in navigation"
          :key="item.name"
          :to="item.route"
          class="mt-1 flex items-center rounded-lg px-3 py-2.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100 hover:text-gray-900"
          active-class="bg-gray-100 text-gray-900"
        >
          {{ item.name }}
        </RouterLink>

      </nav>


      <!-- User -->
      <div class="border-t border-gray-200 p-4">

        <div class="mb-3 px-3">
          <p class="text-xs text-gray-500">
            Вы вошли как
          </p>

          <p class="mt-1 truncate text-sm font-medium text-gray-900">
            {{ authStore.user?.username }}
          </p>
        </div>

        <button
          type="button"
          class="w-full rounded-lg px-3 py-2.5 text-left text-sm font-medium text-gray-600 transition hover:bg-gray-100 hover:text-gray-900"
          @click="handleLogout"
        >
          Выйти
        </button>

      </div>
    </aside>


    <!-- Main -->
    <div class="pl-64">

      <!-- Header -->
      <header
        class="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-gray-200 bg-white px-8"
      >
        <div>
          <p class="text-sm font-medium text-gray-900">
            Панель администратора
          </p>

          <p class="mt-0.5 text-xs text-gray-500">
            Управление содержимым сайта
          </p>
        </div>

        <RouterLink
          :to="{ name: 'home' }"
          class="text-sm text-gray-500 transition hover:text-gray-900"
        >
          Открыть сайт
        </RouterLink>
      </header>


      <!-- Page -->
      <main class="p-8">
        <div class="mx-auto max-w-7xl">
          <RouterView />
        </div>
      </main>

    </div>

  </div>
</template>