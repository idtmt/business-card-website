<script setup lang="ts">
import { reactive, watch } from 'vue'

import type {
  ServiceCreate,
  ServiceUpdate,
} from '../../types/service'

const props = defineProps<{
  service?: ServiceUpdate | null
  loading?: boolean
}>()

const emit = defineEmits<{
  submit: [data: ServiceCreate | ServiceUpdate]
  cancel: []
}>()

const form = reactive<ServiceCreate>({
  name: '',
  description: '',
  position: 0,
  is_hidden: false,
})

watch(
  () => props.service,
  (service) => {
    form.name = service?.name ?? ''
    form.description = service?.description ?? ''
    form.position = service?.position ?? 0
    form.is_hidden = service?.is_hidden ?? false
  },
  { immediate: true },
)

function handleSubmit() {
  emit('submit', {
    name: form.name,
    description: form.description || null,
    position: form.position,
    is_hidden: form.is_hidden,
  })
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="handleSubmit">
    <div>
      <label
        for="service-name"
        class="block text-sm font-medium text-gray-700"
      >
        Название
      </label>

      <input
        id="service-name"
        v-model="form.name"
        type="text"
        required
        class="mt-1.5 block w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        placeholder="Например, Мужская стрижка"
      />
    </div>

    <div>
      <label
        for="service-description"
        class="block text-sm font-medium text-gray-700"
      >
        Описание
      </label>

      <textarea
        id="service-description"
        v-model="form.description"
        rows="4"
        class="mt-1.5 block w-full resize-none rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        placeholder="Описание услуги"
      />
    </div>

    <div>
      <label
        for="service-position"
        class="block text-sm font-medium text-gray-700"
      >
        Позиция
      </label>

      <input
        id="service-position"
        v-model.number="form.position"
        type="number"
        min="0"
        class="mt-1.5 block w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
      />
    </div>

    <label class="flex items-center gap-3">
      <input
        v-model="form.is_hidden"
        type="checkbox"
        class="h-4 w-4 rounded border-gray-300"
      />

      <span class="text-sm text-gray-700">
        Скрыть услугу
      </span>
    </label>

    <div class="flex justify-end gap-3 pt-2">
      <button
        type="button"
        class="rounded-lg border border-gray-300 px-4 py-2.5 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
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