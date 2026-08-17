<script setup lang="ts">
defineProps<{
  loading?: boolean
  submitText?: string
  loadingText?: string
}>()

defineEmits<{
  cancel: []
}>()
</script>

<template>
  <div
    class="flex items-center justify-end gap-3 border-t border-gray-200 pt-6"
  >
    <button
      type="button"
      class="rounded-lg border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-700 transition hover:border-gray-300 hover:bg-gray-50 hover:text-gray-900"
      :disabled="loading"
      @click="$emit('cancel')"
    >
      Отмена
    </button>

    <button
      type="submit"
      class="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="loading"
    >
      {{ loading ? loadingText ?? 'Сохранение...' : submitText ?? 'Сохранить' }}
    </button>
  </div>
</template>