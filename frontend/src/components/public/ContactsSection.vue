<script setup lang="ts">
import type { ContactResponse } from '../../types/contact'

defineProps<{
  contacts: ContactResponse[]
  loading: boolean
  error: boolean
}>()
</script>

<template>
  <section
    id="contacts"
    class="bg-stone-950 py-24 text-white sm:py-28"
  >
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div
        class="flex flex-col justify-between gap-8 md:flex-row md:items-end"
      >
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.22em] text-amber-400">
            Информация
          </p>

          <h2
            class="mt-3 text-3xl font-semibold tracking-[-0.03em] sm:text-5xl"
          >
            Контакты и ссылки
          </h2>
        </div>

        <p class="max-w-sm text-sm leading-6 text-white/40">
          Актуальная информация и полезные ссылки.
        </p>
      </div>

      <div
        v-if="loading"
        class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
      >
        <div
          v-for="item in 3"
          :key="item"
          class="h-32 animate-pulse rounded-2xl bg-white/5"
        />
      </div>

      <div
        v-else-if="error"
        class="mt-12 rounded-2xl border border-red-400/10 bg-red-400/10 p-6 text-sm text-red-300"
      >
        Не удалось загрузить контакты.
      </div>

      <div
        v-else-if="contacts.length === 0"
        class="mt-12 rounded-2xl border border-white/10 bg-white/5 p-8 text-white/40"
      >
        Контакты пока не добавлены.
      </div>

      <div
        v-else
        class="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
      >
        <component
          :is="contact.url ? 'a' : 'div'"
          v-for="contact in contacts"
          :key="contact.id"
          :href="contact.url || undefined"
          :target="contact.url ? '_blank' : undefined"
          :rel="contact.url ? 'noopener noreferrer' : undefined"
          class="group rounded-2xl border border-white/10 bg-white/[0.03] p-7 transition duration-300"
          :class="
            contact.url
              ? 'hover:-translate-y-1 hover:border-white/20 hover:bg-white/[0.06]'
              : ''
          "
        >
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium uppercase tracking-wider text-white/35">
              {{ contact.title }}
            </p>

            <span
              v-if="contact.url"
              class="text-white/20 transition group-hover:text-amber-400"
            >
              ↗
            </span>
          </div>

          <p class="mt-5 text-lg font-medium text-white">
            {{ contact.value }}
          </p>
        </component>
      </div>
    </div>
  </section>
</template>