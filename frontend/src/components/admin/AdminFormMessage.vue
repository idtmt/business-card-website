<script setup lang="ts">
defineProps<{
  type: 'error' | 'success'
  message: string
}>()
</script>

<template>
  <div
    v-if="message"
    class="rounded-lg border px-4 py-3 text-sm"
    :class="
      type === 'error'
        ? 'border-red-100 bg-red-50 text-red-700'
        : 'border-green-100 bg-green-50 text-green-700'
    "
  >
    {{ message }}
  </div>
</template>