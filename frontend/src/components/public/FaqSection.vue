<script setup lang="ts">
import type { FaqResponse } from '../../types/faq'

defineProps<{
  faq: FaqResponse[]
  loading: boolean
  error: boolean
}>()
</script>

<template>
  <section
    id="faq"
    class="bg-white py-24 sm:py-28"
  >
    <div class="mx-auto max-w-4xl px-6 lg:px-8">
      <div class="text-center">
        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-amber-600">
          FAQ
        </p>

        <h2
          class="mt-3 text-3xl font-semibold tracking-[-0.03em] text-stone-950 sm:text-5xl"
        >
          Частые вопросы
        </h2>
      </div>

      <div
        v-if="loading"
        class="mt-12 space-y-2"
      >
        <div
          v-for="item in 4"
          :key="item"
          class="h-16 animate-pulse rounded-xl bg-stone-100"
        />
      </div>

      <div
        v-else-if="error"
        class="mt-12 rounded-2xl bg-red-50 p-6 text-sm text-red-700"
      >
        Не удалось загрузить часто задаваемые вопросы.
      </div>

      <div
        v-else-if="faq.length === 0"
        class="mt-12 text-center text-stone-400"
      >
        Частые вопросы пока не добавлены.
      </div>

      <div
        v-else
        class="mt-12 overflow-hidden rounded-2xl border border-stone-200"
      >
        <details
          v-for="(item, index) in faq"
          :key="item.id"
          class="group border-b border-stone-200 last:border-b-0"
        >
          <summary
            class="flex cursor-pointer list-none items-center justify-between gap-6 px-6 py-6 text-left font-medium text-stone-950 transition hover:bg-stone-50 sm:px-7"
          >
            <span>
              <span class="mr-4 text-xs font-medium text-stone-300">
                {{ String(index + 1).padStart(2, '0') }}
              </span>

              {{ item.question }}
            </span>

            <span
              class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-stone-100 text-lg font-normal text-stone-400 transition group-open:rotate-45"
            >
              +
            </span>
          </summary>

          <div class="px-6 pb-6 pl-16 text-sm leading-7 text-stone-500 sm:px-7 sm:pl-20">
            {{ item.answer }}
          </div>
        </details>
      </div>
    </div>
  </section>
</template>