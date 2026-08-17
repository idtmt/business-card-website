<script setup lang="ts">
defineProps<{
  title: string
  value: number | string
  description: string
  loading?: boolean
}>()
</script>


<template>
  <div
    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
  >
    <p class="text-sm font-medium text-gray-500">
      {{ title }}
    </p>

    <div class="mt-3">
      <div
        v-if="loading"
        class="h-9 w-16 animate-pulse rounded bg-gray-100"
      />

      <p
        v-else
        class="text-3xl font-bold tracking-tight text-gray-900"
      >
        {{ value }}
      </p>
    </div>

    <p class="mt-2 text-sm text-gray-500">
      {{ description }}
    </p>
  </div>
</template>