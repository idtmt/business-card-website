<script setup lang="ts">
import { reactive, watch } from 'vue'

import type {
  LocationCreate,
  LocationResponse,
} from '../../types/location'


const props = defineProps<{
  location?: LocationResponse | null
  loading?: boolean
}>()


const emit = defineEmits<{
  submit: [data: LocationCreate]
  cancel: []
}>()


const form = reactive<LocationCreate>({
  title: '',
  address: '',
  latitude: 0,
  longitude: 0,
  position: 0,
  is_hidden: false,
})


function resetForm() {
  form.title = props.location?.title ?? ''
  form.address = props.location?.address ?? ''
  form.latitude = props.location?.latitude ?? 0
  form.longitude = props.location?.longitude ?? 0
  form.position = props.location?.position ?? 0
  form.is_hidden = props.location?.is_hidden ?? false
}


watch(
  () => props.location,
  resetForm,
  { immediate: true },
)


function handleSubmit() {
  emit('submit', {
    title: form.title.trim(),
    address: form.address.trim(),
    latitude: Number(form.latitude),
    longitude: Number(form.longitude),
    position: Number(form.position),
    is_hidden: form.is_hidden,
  })
}
</script>


<template>
  <form
    class="space-y-5 rounded-xl border border-gray-200 bg-white p-6"
    @submit.prevent="handleSubmit"
  >
    <div>
      <h2 class="text-lg font-semibold text-gray-900">
        {{ location ? 'Редактирование локации' : 'Новая локация' }}
      </h2>

      <p class="mt-1 text-sm text-gray-500">
        Адрес и координаты будут отображаться на сайте.
      </p>
    </div>


    <div class="grid gap-5 md:grid-cols-2">

      <div class="md:col-span-2">
        <label
          for="location-title"
          class="mb-1.5 block text-sm font-medium text-gray-700"
        >
          Название
        </label>

        <input
          id="location-title"
          v-model="form.title"
          type="text"
          required
          placeholder="Основной филиал"
          class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        />
      </div>


      <div class="md:col-span-2">
        <label
          for="location-address"
          class="mb-1.5 block text-sm font-medium text-gray-700"
        >
          Адрес
        </label>

        <input
          id="location-address"
          v-model="form.address"
          type="text"
          required
          placeholder="ул. Примерная, 10"
          class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        />
      </div>


      <div>
        <label
          for="location-latitude"
          class="mb-1.5 block text-sm font-medium text-gray-700"
        >
          Широта
        </label>

        <input
          id="location-latitude"
          v-model.number="form.latitude"
          type="number"
          step="any"
          required
          class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        />
      </div>


      <div>
        <label
          for="location-longitude"
          class="mb-1.5 block text-sm font-medium text-gray-700"
        >
          Долгота
        </label>

        <input
          id="location-longitude"
          v-model.number="form.longitude"
          type="number"
          step="any"
          required
          class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        />
      </div>


      <div>
        <label
          for="location-position"
          class="mb-1.5 block text-sm font-medium text-gray-700"
        >
          Позиция
        </label>

        <input
          id="location-position"
          v-model.number="form.position"
          type="number"
          min="0"
          class="w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        />
      </div>


      <label class="flex items-center gap-3 self-end pb-2">
        <input
          v-model="form.is_hidden"
          type="checkbox"
          class="h-4 w-4 rounded border-gray-300"
        />

        <span class="text-sm text-gray-700">
          Скрыть локацию
        </span>
      </label>

    </div>


    <div class="flex justify-end gap-3 border-t border-gray-100 pt-5">
      <button
        type="button"
        class="rounded-lg px-4 py-2.5 text-sm font-medium text-gray-600 transition hover:bg-gray-100"
        @click="emit('cancel')"
      >
        Отмена
      </button>

      <button
        type="submit"
        :disabled="loading"
        class="rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {{ loading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </div>
  </form>
</template>