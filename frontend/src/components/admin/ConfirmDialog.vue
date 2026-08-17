<script setup lang="ts">
defineProps<{
  title: string
  message: string
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4"
    @click.self="emit('cancel')"
  >
    <div class="w-full max-w-md rounded-xl bg-white shadow-xl">
      <div class="p-6">
        <h2 class="text-lg font-semibold text-gray-900">
          {{ title }}
        </h2>

        <p class="mt-2 text-sm leading-6 text-gray-500">
          {{ message }}
        </p>

        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
            @click="emit('cancel')"
          >
            Отмена
          </button>

          <button
            type="button"
            class="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
            @click="emit('confirm')"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>