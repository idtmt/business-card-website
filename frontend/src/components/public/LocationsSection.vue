<script setup lang="ts">
import type {
  PublicLocationResponse,
  PublicScheduleResponse,
} from '../../types/location'

defineProps<{
  locations: PublicLocationResponse[]
  loading: boolean
  error: boolean
}>()

const weekdays = [
  'Понедельник',
  'Вторник',
  'Среда',
  'Четверг',
  'Пятница',
  'Суббота',
  'Воскресенье',
]

function formatSchedule(
  schedule: PublicScheduleResponse,
): string {
  if (schedule.is_day_off) {
    return 'Выходной'
  }

  if (!schedule.start_time || !schedule.end_time) {
    return 'Уточняется'
  }

  return `${schedule.start_time} — ${schedule.end_time}`
}

function getMapUrl(
  latitude: number,
  longitude: number,
): string {
  return `https://yandex.uz/maps/?ll=${longitude}%2C${latitude}&z=17&pt=${longitude},${latitude}`
}
</script>

<template>
  <section
    id="locations"
    class="bg-stone-100 py-24 sm:py-28"
  >
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div class="max-w-2xl">
        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-amber-600">
          Адрес
        </p>

        <h2
          class="mt-3 text-3xl font-semibold tracking-[-0.03em] text-stone-950 sm:text-5xl"
        >
          Где нас найти
        </h2>

        <p class="mt-5 text-stone-500">
          Наши адреса и график работы.
        </p>
      </div>

      <div
        v-if="loading"
        class="mt-12 grid gap-5 lg:grid-cols-2"
      >
        <div
          v-for="item in 2"
          :key="item"
          class="h-96 animate-pulse rounded-2xl bg-white"
        />
      </div>

      <div
        v-else-if="error"
        class="mt-12 rounded-2xl bg-white p-6 text-sm text-red-700"
      >
        Не удалось загрузить адреса.
      </div>

      <div
        v-else-if="locations.length === 0"
        class="mt-12 rounded-2xl bg-white p-10 text-center text-stone-400"
      >
        Адреса пока не добавлены.
      </div>

      <div
        v-else
        class="mt-12 grid gap-5 lg:grid-cols-2"
      >
        <article
          v-for="location in locations"
          :key="location.id"
          class="rounded-2xl border border-stone-200 bg-white p-7 shadow-sm"
        >
          <div class="flex items-start justify-between gap-6">
            <div>
              <div class="mb-3 flex items-center gap-2">
                <span class="h-2 w-2 rounded-full bg-amber-500" />

                <span class="text-xs font-medium uppercase tracking-wider text-stone-400">
                  Локация
                </span>
              </div>

              <h3 class="text-xl font-semibold tracking-tight text-stone-950">
                {{ location.title }}
              </h3>

              <p class="mt-2 text-sm leading-6 text-stone-500">
                {{ location.address }}
              </p>
            </div>

            <span class="text-2xl text-stone-200">
              ↗
            </span>
          </div>

          <div
            v-if="location.schedules.length"
            class="mt-8 border-t border-stone-100 pt-6"
          >
            <p class="mb-4 text-xs font-semibold uppercase tracking-wider text-stone-400">
              График работы
            </p>

            <div class="space-y-3">
              <div
                v-for="schedule in location.schedules"
                :key="schedule.id"
                class="flex items-center justify-between gap-4 text-sm"
              >
                <span class="text-stone-500">
                  {{ weekdays[schedule.weekday] ?? 'День' }}
                </span>

                <span
                  :class="
                    schedule.is_day_off
                      ? 'text-stone-400'
                      : 'font-medium text-stone-900'
                  "
                >
                  {{ formatSchedule(schedule) }}
                </span>
              </div>
            </div>
          </div>

          <a
            :href="
              getMapUrl(
                location.latitude,
                location.longitude,
              )
            "
            target="_blank"
            rel="noopener noreferrer"
            class="mt-8 inline-flex items-center gap-2 rounded-xl bg-stone-950 px-5 py-3 text-sm font-medium text-white transition hover:bg-stone-800"
          >
            Открыть на карте
            <span>↗</span>
          </a>
        </article>
      </div>
    </div>
  </section>
</template>