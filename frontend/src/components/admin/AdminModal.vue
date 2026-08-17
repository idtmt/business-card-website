<script setup lang="ts">
defineProps<{
  title: string
}>()

const emit = defineEmits<{
  close: []
}>()
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4"
    @click.self="emit('close')"
  >
    <div class="w-full max-w-lg rounded-xl bg-white shadow-xl">
      <div
        class="flex items-center justify-between border-b border-gray-200 px-6 py-4"
      >
        <h2 class="text-lg font-semibold text-gray-900">
          {{ title }}
        </h2>

        <button
          type="button"
          class="text-2xl leading-none text-gray-400 transition hover:text-gray-700"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <div class="p-6">
        <slot />
      </div>
    </div>
  </div>
</template>