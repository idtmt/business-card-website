<script setup lang="ts">
import { onMounted } from 'vue'

import DashboardQuickLink from '../../components/admin/DashboardQuickLink.vue'
import DashboardStatCard from '../../components/admin/DashboardStatCard.vue'

import { useDashboard } from '../../composables/useDashboard'


const {
  loading,
  error,
  companyCount,
  servicesCount,
  contactsCount,
  faqCount,
  locationsCount,
  load,
} = useDashboard()


onMounted(load)
</script>


<template>
  <section>

    <!-- Heading -->
    <div>
      <p class="text-sm font-medium text-gray-500">
        Обзор
      </p>

      <h1
        class="mt-1 text-3xl font-bold tracking-tight text-gray-900"
      >
        Панель управления
      </h1>

      <p class="mt-2 text-sm text-gray-500">
        Управляйте содержимым сайта из одного места.
      </p>
    </div>


    <!-- Error -->
    <div
      v-if="error"
      class="mt-6 rounded-lg border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      {{ error }}
    </div>


    <!-- Statistics -->
    <div
      class="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-5"
    >

      <DashboardStatCard
        title="Компания"
        :value="companyCount"
        description="Основная информация"
        :loading="loading"
      />

      <DashboardStatCard
        title="Услуги"
        :value="servicesCount"
        description="Всего услуг"
        :loading="loading"
      />

      <DashboardStatCard
        title="Контакты"
        :value="contactsCount"
        description="Всего контактов"
        :loading="loading"
      />

      <DashboardStatCard
        title="FAQ"
        :value="faqCount"
        description="Вопросы и ответы"
        :loading="loading"
      />

      <DashboardStatCard
        title="Локации"
        :value="locationsCount"
        description="Адреса компании"
        :loading="loading"
      />

    </div>


    <!-- Quick links -->
    <div class="mt-10">

      <div>
        <h2 class="text-lg font-semibold text-gray-900">
          Управление
        </h2>

        <p class="mt-1 text-sm text-gray-500">
          Быстрый переход к разделам сайта.
        </p>
      </div>


      <div
        class="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3"
      >

        <DashboardQuickLink
          title="Компания"
          description="Название и описание компании"
          to="/admin/company"
        />

        <DashboardQuickLink
          title="Услуги"
          description="Добавление и редактирование услуг"
          to="/admin/services"
        />

        <DashboardQuickLink
          title="Контакты"
          description="Телефон, Telegram и другие контакты"
          to="/admin/contacts"
        />

        <DashboardQuickLink
          title="FAQ"
          description="Управление частыми вопросами"
          to="/admin/faq"
        />

        <DashboardQuickLink
          title="Локации"
          description="Адреса и расписание работы"
          to="/admin/locations"
        />

      </div>

    </div>

  </section>
</template>