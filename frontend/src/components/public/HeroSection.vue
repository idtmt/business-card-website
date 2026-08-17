<script setup lang="ts">
import type { CompanyResponse } from '../../types/company'

defineProps<{
  company: CompanyResponse | null
  loading: boolean
}>()
</script>

<template>
  <section
    class="relative overflow-hidden bg-stone-950 text-white"
  >
    <div
      class="absolute inset-0 bg-[radial-gradient(circle_at_75%_20%,rgba(217,119,6,0.22),transparent_32%),radial-gradient(circle_at_20%_80%,rgba(255,255,255,0.06),transparent_28%)]"
    />

    <div
      class="absolute -right-40 top-20 h-96 w-96 rounded-full border border-white/5"
    />

    <div
      class="absolute -right-20 top-40 h-72 w-72 rounded-full border border-white/5"
    />

    <div
      class="relative mx-auto flex min-h-[720px] max-w-7xl items-end px-6 pb-24 pt-36 lg:px-8 lg:pb-28"
    >
      <div class="max-w-4xl">
        <div
          class="mb-7 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3.5 py-2 text-xs font-medium text-white/60 backdrop-blur"
        >
          <span class="h-1.5 w-1.5 rounded-full bg-amber-400" />
          Добро пожаловать
        </div>

        <template v-if="loading">
          <div class="h-16 w-80 animate-pulse rounded-2xl bg-white/10 sm:h-24 sm:w-[42rem]" />
          <div class="mt-7 h-16 max-w-2xl animate-pulse rounded-2xl bg-white/10" />
        </template>

        <template v-else-if="company">
          <h1
            class="max-w-4xl text-5xl font-semibold leading-[0.98] tracking-[-0.04em] sm:text-6xl lg:text-8xl"
          >
            {{ company.name }}
          </h1>

          <p
            v-if="company.description"
            class="mt-8 max-w-2xl text-base leading-7 text-white/55 sm:text-lg"
          >
            {{ company.description }}
          </p>

          <div class="mt-10 flex flex-wrap gap-3">
            <a
              href="#services"
              class="rounded-xl bg-amber-400 px-6 py-3.5 text-sm font-semibold text-stone-950 transition hover:bg-amber-300"
            >
              Наши услуги
            </a>

            <a
              href="#contacts"
              class="rounded-xl border border-white/15 bg-white/5 px-6 py-3.5 text-sm font-medium text-white transition hover:bg-white/10"
            >
              Связаться
            </a>
          </div>
        </template>

        <template v-else>
          <h1
            class="text-5xl font-semibold leading-[0.98] tracking-[-0.04em] sm:text-6xl lg:text-8xl"
          >
            Компания
          </h1>

          <p class="mt-8 max-w-2xl text-lg leading-7 text-white/50">
            Информация о компании пока не добавлена.
          </p>
        </template>
      </div>
    </div>

    <div class="absolute bottom-0 left-0 right-0">
      <div class="mx-auto max-w-7xl px-6 lg:px-8">
        <div class="border-t border-white/10" />
      </div>
    </div>
  </section>
</template>