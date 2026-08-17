<script setup lang="ts">
defineProps<{
  title: string
  description: string
  to: string
}>()
</script>


<template>
  <RouterLink
    :to="to"
    class="group rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-gray-300 hover:shadow"
  >
    <div class="flex items-center justify-between">

      <div>
        <h3 class="text-sm font-semibold text-gray-900">
          {{ title }}
        </h3>

        <p class="mt-1 text-sm text-gray-500">
          {{ description }}
        </p>
      </div>

      <span
        class="text-gray-400 transition group-hover:translate-x-1 group-hover:text-gray-700"
      >
        →
      </span>

    </div>
  </RouterLink>
</template>