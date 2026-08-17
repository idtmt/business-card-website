<script setup lang="ts">
import type { LocationResponse } from '../../types/location'


defineProps<{
  location: LocationResponse
}>()


const emit = defineEmits<{
  edit: []
  delete: []
  schedules: []
}>()
</script>


<template>
  <article
    class="rounded-xl border border-gray-200 bg-white p-6"
  >
    <div class="flex items-start justify-between gap-4">

      <div class="min-w-0">
        <div class="flex items-center gap-2">
          <h3 class="text-base font-semibold text-gray-900">
            {{ location.title }}
          </h3>

          <span
            v-if="location.is_hidden"
            class="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500"
          >
            Скрыта
          </span>
        </div>

        <p class="mt-2 text-sm text-gray-600">
          {{ location.address }}
        </p>
      </div>

      <span class="shrink-0 text-xs text-gray-400">
        #{{ location.position }}
      </span>

    </div>


    <div class="mt-5 grid gap-3 rounded-lg bg-gray-50 p-4 text-sm">
      <div>
        <span class="text-gray-500">
          Широта:
        </span>

        <span class="ml-2 font-medium text-gray-900">
          {{ location.latitude }}
        </span>
      </div>

      <div>
        <span class="text-gray-500">
          Долгота:
        </span>

        <span class="ml-2 font-medium text-gray-900">
          {{ location.longitude }}
        </span>
      </div>
    </div>


    <div class="mt-5 flex flex-wrap gap-2">
      <button
        type="button"
        class="rounded-lg border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
        @click="emit('schedules')"
      >
        Расписание
      </button>

      <button
        type="button"
        class="rounded-lg border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
        @click="emit('edit')"
      >
        Изменить
      </button>

      <button
        type="button"
        class="rounded-lg px-3 py-2 text-sm font-medium text-red-600 transition hover:bg-red-50"
        @click="emit('delete')"
      >
        Удалить
      </button>
    </div>
  </article>
</template>