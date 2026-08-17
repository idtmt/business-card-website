<script setup lang="ts">
import type { FaqResponse } from '../../types/faq'


defineProps<{
  faq: FaqResponse
}>()


defineEmits<{
  edit: []
  delete: []
}>()
</script>


<template>
  <div
    class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm"
  >
    <div class="flex items-start justify-between gap-6">

      <div class="min-w-0">
        <div class="flex items-center gap-3">
          <h3 class="text-sm font-semibold text-gray-900">
            {{ faq.question }}
          </h3>

          <span
            v-if="faq.is_hidden"
            class="shrink-0 rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-500"
          >
            Скрыт
          </span>
        </div>

        <p class="mt-2 whitespace-pre-line text-sm leading-6 text-gray-600">
          {{ faq.answer }}
        </p>

        <p class="mt-3 text-xs text-gray-400">
          Позиция: {{ faq.position }}
        </p>
      </div>


      <div class="flex shrink-0 items-center gap-2">
        <button
          type="button"
          class="rounded-lg border border-gray-200 px-3 py-2 text-sm font-medium text-gray-700 transition hover:border-gray-300 hover:bg-gray-50"
          @click="$emit('edit')"
        >
          Изменить
        </button>

        <button
          type="button"
          class="rounded-lg border border-red-100 px-3 py-2 text-sm font-medium text-red-600 transition hover:bg-red-50"
          @click="$emit('delete')"
        >
          Удалить
        </button>
      </div>

    </div>
  </div>
</template>