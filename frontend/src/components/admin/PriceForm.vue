<script setup lang="ts">
import { reactive, watch } from 'vue'

import type {
  PriceCreate,
  PriceUpdate,
} from '../../types/price'

const props = defineProps<{
  serviceId: number
  price?: PriceUpdate | null
  loading?: boolean
}>()

const emit = defineEmits<{
  submit: [data: PriceCreate | PriceUpdate]
  cancel: []
}>()

const form = reactive({
  title: '',
  price: '',
  position: 0,
  is_hidden: false,
})

watch(
  () => props.price,
  (price) => {
    form.title = price?.title ?? ''
    form.price = price?.price ?? ''
    form.position = price?.position ?? 0
    form.is_hidden = price?.is_hidden ?? false
  },
  { immediate: true },
)

function handleSubmit() {
  if (props.price) {
    emit('submit', {
      title: form.title,
      price: form.price,
      position: form.position,
      is_hidden: form.is_hidden,
    })

    return
  }

  emit('submit', {
    service_id: props.serviceId,
    title: form.title,
    price: form.price,
    position: form.position,
    is_hidden: form.is_hidden,
  })
}
</script>

<template>
  <form class="space-y-5" @submit.prevent="handleSubmit">
    <div>
      <label
        for="price-title"
        class="block text-sm font-medium text-gray-700"
      >
        Название
      </label>

      <input
        id="price-title"
        v-model="form.title"
        type="text"
        required
        class="mt-1.5 block w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        placeholder="Например, Классическая стрижка"
      />
    </div>

    <div>
      <label
        for="price-value"
        class="block text-sm font-medium text-gray-700"
      >
        Цена
      </label>

      <input
        id="price-value"
        v-model="form.price"
        type="text"
        required
        class="mt-1.5 block w-full rounded-lg border border-gray-300 px-3 py-2.5 text-sm outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500"
        placeholder="100 000 сум"
      />
    </div>

    <div>
      <label
        for="price-position"
        class="block text-sm font-medium text-gray-700"
      >
        Позиция
      </label>

      <input
        id="price-position"
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
        Скрыть цену
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