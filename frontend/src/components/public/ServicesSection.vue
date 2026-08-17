<script setup lang="ts">
import type { PublicServiceResponse } from '../../types/service'

defineProps<{
  services: PublicServiceResponse[]
  loading: boolean
  error: boolean
}>()
</script>

<template>
  <section
    id="services"
    class="bg-stone-50 py-24 sm:py-28"
  >
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div
        class="flex flex-col justify-between gap-8 border-b border-stone-200 pb-10 md:flex-row md:items-end"
      >
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.22em] text-amber-600">
            Услуги
          </p>

          <h2
            class="mt-3 text-3xl font-semibold tracking-[-0.03em] text-stone-950 sm:text-5xl"
          >
            Что мы предлагаем
          </h2>
        </div>

        <p class="max-w-sm text-sm leading-6 text-stone-500">
          Ознакомьтесь с нашими услугами и актуальными ценами.
        </p>
      </div>

      <div
        v-if="loading"
        class="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3"
      >
        <div
          v-for="item in 3"
          :key="item"
          class="h-72 animate-pulse rounded-2xl bg-stone-200"
        />
      </div>

      <div
        v-else-if="error"
        class="mt-10 rounded-2xl border border-red-100 bg-red-50 p-6 text-sm text-red-700"
      >
        Не удалось загрузить услуги.
      </div>

      <div
        v-else-if="services.length === 0"
        class="mt-10 rounded-2xl bg-white p-10 text-center text-stone-400"
      >
        Услуги пока не добавлены.
      </div>

      <div
        v-else
        class="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3"
      >
        <article
          v-for="(service, index) in services"
          :key="service.id"
          class="group flex min-h-72 flex-col rounded-2xl border border-stone-200 bg-white p-7 transition duration-300 hover:-translate-y-1 hover:border-stone-300 hover:shadow-xl hover:shadow-stone-900/5"
        >
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium tracking-wider text-stone-400">
              {{ String(index + 1).padStart(2, '0') }}
            </span>

            <span
              class="flex h-8 w-8 items-center justify-center rounded-full bg-stone-100 text-sm text-stone-400 transition group-hover:bg-amber-100 group-hover:text-amber-700"
            >
              ↗
            </span>
          </div>

          <div class="mt-auto pt-14">
            <h3 class="text-xl font-semibold tracking-tight text-stone-950">
              {{ service.name }}
            </h3>

            <p
              v-if="service.description"
              class="mt-3 text-sm leading-6 text-stone-500"
            >
              {{ service.description }}
            </p>

            <div
              v-if="service.prices.length"
              class="mt-7 space-y-3 border-t border-stone-100 pt-5"
            >
              <div
                v-for="price in service.prices"
                :key="price.id"
                class="flex items-center justify-between gap-4 text-sm"
              >
                <span class="text-stone-500">
                  {{ price.title }}
                </span>

                <span class="font-semibold text-stone-950">
                  {{ price.price }}
                </span>
              </div>
            </div>

            <p
              v-else
              class="mt-7 border-t border-stone-100 pt-5 text-sm text-stone-400"
            >
              Цена уточняется.
            </p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>