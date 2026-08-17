<script setup lang="ts">
import { computed, reactive, watch } from 'vue'

import type {
  ScheduleCreate,
  ScheduleResponse,
} from '../../types/schedule'


const props = defineProps<{
  locationId: number
  schedules: ScheduleResponse[]
  loading?: boolean
}>()


const emit = defineEmits<{
  save: [data: ScheduleCreate]
  delete: [scheduleId: number]
}>()


const weekdays = [
  { value: 0, label: 'Понедельник' },
  { value: 1, label: 'Вторник' },
  { value: 2, label: 'Среда' },
  { value: 3, label: 'Четверг' },
  { value: 4, label: 'Пятница' },
  { value: 5, label: 'Суббота' },
  { value: 6, label: 'Воскресенье' },
]


interface DayForm {
  id?: number
  weekday: number
  start_time: string
  end_time: string
  is_day_off: boolean
}


const days = reactive<DayForm[]>(
  weekdays.map((day) => ({
    weekday: day.value,
    start_time: '09:00',
    end_time: '18:00',
    is_day_off: false,
  })),
)


function reset() {
  for (const day of days) {
    const schedule = props.schedules.find(
      (item) => item.weekday === day.weekday,
    )

    day.id = schedule?.id

    day.start_time = schedule?.start_time ?? '09:00'
    day.end_time = schedule?.end_time ?? '18:00'
    day.is_day_off = schedule?.is_day_off ?? false
  }
}


watch(
  () => props.schedules,
  reset,
  {
    immediate: true,
    deep: true,
  },
)


const hasSchedules = computed(() =>
  props.schedules.length > 0,
)


function saveDay(day: DayForm) {
  emit('save', {
    location_id: props.locationId,
    weekday: day.weekday,
    start_time: day.is_day_off
      ? null
      : day.start_time,
    end_time: day.is_day_off
      ? null
      : day.end_time,
    is_day_off: day.is_day_off,
  })
}
</script>


<template>
  <div class="rounded-xl border border-gray-200 bg-white p-6">

    <div class="mb-5">
      <h2 class="text-lg font-semibold text-gray-900">
        Расписание
      </h2>

      <p class="mt-1 text-sm text-gray-500">
        Рабочие часы для выбранной локации.
      </p>
    </div>


    <div class="space-y-3">

      <div
        v-for="day in days"
        :key="day.weekday"
        class="rounded-lg border border-gray-200 p-4"
      >
        <div
          class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"
        >

          <div class="w-32 shrink-0">
            <p class="text-sm font-medium text-gray-900">
              {{ weekdays[day.weekday].label }}
            </p>
          </div>


          <div class="flex flex-1 flex-wrap items-center gap-3">

            <label class="flex items-center gap-2">
              <input
                v-model="day.is_day_off"
                type="checkbox"
                class="h-4 w-4 rounded border-gray-300"
              />

              <span class="text-sm text-gray-600">
                Выходной
              </span>
            </label>


            <template v-if="!day.is_day_off">
              <input
                v-model="day.start_time"
                type="time"
                class="rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-gray-500"
              />

              <span class="text-sm text-gray-400">
                —
              </span>

              <input
                v-model="day.end_time"
                type="time"
                class="rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-gray-500"
              />
            </template>

          </div>


          <div class="flex gap-2">
            <button
              type="button"
              :disabled="loading"
              class="rounded-lg bg-gray-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-gray-800 disabled:opacity-50"
              @click="saveDay(day)"
            >
              Сохранить
            </button>

            <button
              v-if="day.id"
              type="button"
              class="rounded-lg px-3 py-2 text-sm text-red-600 transition hover:bg-red-50"
              @click="emit('delete', day.id)"
            >
              Удалить
            </button>
          </div>

        </div>
      </div>

    </div>


    <p
      v-if="!hasSchedules"
      class="mt-4 text-xs text-gray-400"
    >
      Для этой локации расписание ещё не создано.
    </p>

  </div>
</template>