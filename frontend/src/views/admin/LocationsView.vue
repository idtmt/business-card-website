<script setup lang="ts">
import { onMounted, ref } from 'vue'

import LocationForm from '../../components/admin/LocationForm.vue'
import LocationCard from '../../components/admin/LocationCard.vue'
import ScheduleEditor from '../../components/admin/ScheduleEditor.vue'

import { useLocations } from '../../composables/useLocations'

import type {
  LocationCreate,
  LocationResponse,
} from '../../types/location'

import type {
  ScheduleCreate,
} from '../../types/schedule'


const {
  locations,
  schedules,
  loading,
  error,

  loadLocations,
  loadSchedules,

  addLocation,
  editLocation,
  removeLocation,

  addSchedule,
  editSchedule,
  removeSchedule,
} = useLocations()


const showForm = ref(false)
const editingLocation = ref<LocationResponse | null>(null)

const selectedLocation = ref<LocationResponse | null>(null)

const actionLoading = ref(false)


async function openCreateForm() {
  editingLocation.value = null
  showForm.value = true
}


function openEditForm(location: LocationResponse) {
  editingLocation.value = location
  showForm.value = true
}


function closeForm() {
  showForm.value = false
  editingLocation.value = null
}


async function handleLocationSubmit(
  data: LocationCreate,
) {
  actionLoading.value = true

  try {
    if (editingLocation.value) {
      await editLocation(
        editingLocation.value.id,
        data,
      )
    } else {
      await addLocation(data)
    }

    closeForm()
  } finally {
    actionLoading.value = false
  }
}


async function handleDelete(
  location: LocationResponse,
) {
  const confirmed = window.confirm(
    `Удалить локацию «${location.title}»?`,
  )

  if (!confirmed) {
    return
  }

  actionLoading.value = true

  try {
    await removeLocation(location.id)

    if (
      selectedLocation.value?.id === location.id
    ) {
      selectedLocation.value = null
    }
  } finally {
    actionLoading.value = false
  }
}


async function openSchedules(
  location: LocationResponse,
) {
  selectedLocation.value = location

  await loadSchedules(location.id)
}


function closeSchedules() {
  selectedLocation.value = null
}


async function handleScheduleSave(
  data: ScheduleCreate,
) {
  actionLoading.value = true

  try {
    const existingSchedule =
      schedules.value[data.location_id]?.find(
        (schedule) =>
          schedule.weekday === data.weekday,
      )

    if (existingSchedule) {
      await editSchedule(
        existingSchedule.id,
        data.location_id,
        {
          weekday: data.weekday,
          start_time: data.start_time,
          end_time: data.end_time,
          is_day_off: data.is_day_off,
        },
      )
    } else {
      await addSchedule(data)
    }
  } finally {
    actionLoading.value = false
  }
}


async function handleScheduleDelete(
  scheduleId: number,
) {
  if (!selectedLocation.value) {
    return
  }

  const confirmed = window.confirm(
    'Удалить это расписание?',
  )

  if (!confirmed) {
    return
  }

  actionLoading.value = true

  try {
    await removeSchedule(
      scheduleId,
      selectedLocation.value.id,
    )
  } finally {
    actionLoading.value = false
  }
}


onMounted(loadLocations)
</script>


<template>
  <div class="space-y-8">

    <!-- Page header -->
    <div
      class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <h1 class="text-2xl font-semibold tracking-tight text-gray-900">
          Локации
        </h1>

        <p class="mt-1 text-sm text-gray-500">
          Управление адресами и расписанием работы.
        </p>
      </div>


      <button
        v-if="!showForm"
        type="button"
        class="rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800"
        @click="openCreateForm"
      >
        Добавить локацию
      </button>
    </div>


    <!-- Error -->
    <div
      v-if="error"
      class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      {{ error }}
    </div>


    <!-- Form -->
    <LocationForm
      v-if="showForm"
      :location="editingLocation"
      :loading="actionLoading"
      @submit="handleLocationSubmit"
      @cancel="closeForm"
    />


    <!-- Loading -->
    <div
      v-if="loading"
      class="rounded-xl border border-gray-200 bg-white p-8 text-center text-sm text-gray-500"
    >
      Загрузка локаций...
    </div>


    <!-- Empty -->
    <div
      v-else-if="locations.length === 0 && !showForm"
      class="rounded-xl border border-dashed border-gray-300 bg-white p-12 text-center"
    >
      <h2 class="text-base font-medium text-gray-900">
        Локаций пока нет
      </h2>

      <p class="mt-1 text-sm text-gray-500">
        Добавьте первый адрес компании.
      </p>

      <button
        type="button"
        class="mt-5 rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800"
        @click="openCreateForm"
      >
        Добавить локацию
      </button>
    </div>


    <!-- Locations -->
    <div
      v-else
      class="grid gap-5 lg:grid-cols-2"
    >
      <LocationCard
        v-for="location in locations"
        :key="location.id"
        :location="location"
        @edit="openEditForm(location)"
        @delete="handleDelete(location)"
        @schedules="openSchedules(location)"
      />
    </div>


    <!-- Schedule -->
    <section
      v-if="selectedLocation"
      class="space-y-4"
    >
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-900">
            Расписание: {{ selectedLocation.title }}
          </h2>

          <p class="mt-1 text-sm text-gray-500">
            {{ selectedLocation.address }}
          </p>
        </div>

        <button
          type="button"
          class="rounded-lg px-3 py-2 text-sm text-gray-600 transition hover:bg-gray-100"
          @click="closeSchedules"
        >
          Закрыть
        </button>
      </div>


      <ScheduleEditor
        :location-id="selectedLocation.id"
        :schedules="schedules[selectedLocation.id] ?? []"
        :loading="actionLoading"
        @save="handleScheduleSave"
        @delete="handleScheduleDelete"
      />
    </section>

  </div>
</template>