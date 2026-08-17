<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import AdminModal from '../../components/admin/AdminModal.vue'
import ConfirmDialog from '../../components/admin/ConfirmDialog.vue'
import ServiceForm from '../../components/admin/ServiceForm.vue'
import PriceForm from '../../components/admin/PriceForm.vue'

import { useServices } from '../../composables/useServices'

import type {
  ServiceCreate,
  ServiceUpdate,
  ServiceResponse,
} from '../../types/service'

import type {
  PriceCreate,
  PriceUpdate,
  PriceResponse,
} from '../../types/price'

const {
  services,
  loading,
  actionLoading,
  error,
  loadServices,
  addService,
  editService,
  removeService,
  addPrice,
  editPrice,
  removePrice,
  getPrices,
} = useServices()

const showServiceModal = ref(false)
const editingService = ref<ServiceResponse | null>(null)

const showPriceModal = ref(false)
const editingPrice = ref<PriceResponse | null>(null)
const selectedServiceId = ref<number | null>(null)

const confirmType = ref<'service' | 'price' | null>(null)
const confirmId = ref<number | null>(null)

const expandedServices = ref<Set<number>>(new Set())

const isEditingService = computed(
  () => editingService.value !== null,
)

const isEditingPrice = computed(
  () => editingPrice.value !== null,
)

onMounted(loadServices)

function toggleService(serviceId: number) {
  const next = new Set(expandedServices.value)

  if (next.has(serviceId)) {
    next.delete(serviceId)
  } else {
    next.add(serviceId)
  }

  expandedServices.value = next
}

function openCreateService() {
  editingService.value = null
  showServiceModal.value = true
}

function openEditService(service: ServiceResponse) {
  editingService.value = service
  showServiceModal.value = true
}

function closeServiceModal() {
  showServiceModal.value = false
  editingService.value = null
}

async function handleServiceSubmit(
  data: ServiceCreate | ServiceUpdate,
) {
  if (editingService.value) {
    await editService(
      editingService.value.id,
      data as ServiceUpdate,
    )
  } else {
    await addService(data as ServiceCreate)
  }

  closeServiceModal()
}

function openCreatePrice(serviceId: number) {
  selectedServiceId.value = serviceId
  editingPrice.value = null
  showPriceModal.value = true
}

function openEditPrice(
  serviceId: number,
  price: PriceResponse,
) {
  selectedServiceId.value = serviceId
  editingPrice.value = price
  showPriceModal.value = true
}

function closePriceModal() {
  showPriceModal.value = false
  editingPrice.value = null
  selectedServiceId.value = null
}

async function handlePriceSubmit(
  data: PriceCreate | PriceUpdate,
) {
  if (editingPrice.value) {
    await editPrice(
      editingPrice.value.id,
      data as PriceUpdate,
    )
  } else {
    await addPrice(data as PriceCreate)
  }

  closePriceModal()
}

function askDeleteService(serviceId: number) {
  confirmType.value = 'service'
  confirmId.value = serviceId
}

function askDeletePrice(priceId: number) {
  confirmType.value = 'price'
  confirmId.value = priceId
}

function closeConfirm() {
  confirmType.value = null
  confirmId.value = null
}

async function confirmDelete() {
  if (confirmId.value === null) {
    return
  }

  if (confirmType.value === 'service') {
    await removeService(confirmId.value)
  }

  if (confirmType.value === 'price') {
    await removePrice(confirmId.value)
  }

  closeConfirm()
}
</script>

<template>
  <section>
    <!-- Header -->
    <div
      class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <h1 class="text-2xl font-semibold tracking-tight text-gray-900">
          Услуги
        </h1>

        <p class="mt-1 text-sm text-gray-500">
          Управление услугами и их ценами
        </p>
      </div>

      <button
        type="button"
        class="rounded-lg bg-gray-900 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800"
        @click="openCreateService"
      >
        Добавить услугу
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      {{ error }}
    </div>

    <!-- Loading -->
    <div
      v-if="loading"
      class="mt-8 rounded-xl border border-gray-200 bg-white px-6 py-12 text-center text-sm text-gray-500"
    >
      Загрузка...
    </div>

    <!-- Empty -->
    <div
      v-else-if="services.length === 0"
      class="mt-8 rounded-xl border border-dashed border-gray-300 bg-white px-6 py-12 text-center"
    >
      <p class="text-sm text-gray-500">
        Услуг пока нет.
      </p>

      <button
        type="button"
        class="mt-4 text-sm font-medium text-gray-900 underline underline-offset-4"
        @click="openCreateService"
      >
        Добавить первую услугу
      </button>
    </div>

    <!-- Services -->
    <div
      v-else
      class="mt-8 space-y-4"
    >
      <article
        v-for="service in services"
        :key="service.id"
        class="overflow-hidden rounded-xl border border-gray-200 bg-white"
      >
        <!-- Service -->
        <div class="p-5">
          <div class="flex items-start justify-between gap-4">
            <button
              type="button"
              class="flex min-w-0 flex-1 items-start gap-3 text-left"
              @click="toggleService(service.id)"
            >
              <span
                class="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border border-gray-300 text-xs text-gray-500"
              >
                {{ expandedServices.has(service.id) ? '−' : '+' }}
              </span>

              <span class="min-w-0">
                <span
                  class="flex flex-wrap items-center gap-2"
                >
                  <span class="font-medium text-gray-900">
                    {{ service.name }}
                  </span>

                  <span
                    v-if="service.is_hidden"
                    class="rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500"
                  >
                    Скрыта
                  </span>
                </span>

                <span
                  v-if="service.description"
                  class="mt-1 block text-sm text-gray-500"
                >
                  {{ service.description }}
                </span>
              </span>
            </button>

            <div class="flex shrink-0 items-center gap-2">
              <button
                type="button"
                class="rounded-lg px-3 py-2 text-sm text-gray-600 transition hover:bg-gray-100 hover:text-gray-900"
                @click="openEditService(service)"
              >
                Изменить
              </button>

              <button
                type="button"
                class="rounded-lg px-3 py-2 text-sm text-red-600 transition hover:bg-red-50"
                @click="askDeleteService(service.id)"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>

        <!-- Prices -->
        <div
          v-if="expandedServices.has(service.id)"
          class="border-t border-gray-200 bg-gray-50"
        >
          <div class="flex items-center justify-between px-5 py-4">
            <div>
              <h2 class="text-sm font-medium text-gray-900">
                Цены
              </h2>

              <p class="mt-0.5 text-xs text-gray-500">
                {{ getPrices(service.id).length }} позиций
              </p>
            </div>

            <button
              type="button"
              class="rounded-lg bg-white px-3 py-2 text-sm font-medium text-gray-700 shadow-sm ring-1 ring-gray-200 transition hover:bg-gray-50"
              @click="openCreatePrice(service.id)"
            >
              Добавить цену
            </button>
          </div>

          <div
            v-if="getPrices(service.id).length === 0"
            class="border-t border-gray-200 px-5 py-6 text-center text-sm text-gray-500"
          >
            Для этой услуги цены ещё не добавлены.
          </div>

          <div
            v-else
            class="divide-y divide-gray-200 border-t border-gray-200"
          >
            <div
              v-for="price in getPrices(service.id)"
              :key="price.id"
              class="flex items-center justify-between gap-4 px-5 py-4"
            >
              <div class="min-w-0">
                <div class="flex flex-wrap items-center gap-2">
                  <p class="text-sm font-medium text-gray-900">
                    {{ price.title }}
                  </p>

                  <span
                    v-if="price.is_hidden"
                    class="rounded-full bg-gray-200 px-2 py-0.5 text-xs text-gray-500"
                  >
                    Скрыта
                  </span>
                </div>

                <p class="mt-1 text-sm text-gray-500">
                  {{ price.price }}
                </p>
              </div>

              <div class="flex shrink-0 items-center gap-2">
                <button
                  type="button"
                  class="rounded-lg px-3 py-2 text-sm text-gray-600 transition hover:bg-white hover:text-gray-900"
                  @click="openEditPrice(service.id, price)"
                >
                  Изменить
                </button>

                <button
                  type="button"
                  class="rounded-lg px-3 py-2 text-sm text-red-600 transition hover:bg-red-50"
                  @click="askDeletePrice(price.id)"
                >
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- Service modal -->
    <AdminModal
      v-if="showServiceModal"
      :title="
        isEditingService
          ? 'Редактировать услугу'
          : 'Новая услуга'
      "
      @close="closeServiceModal"
    >
      <ServiceForm
        :service="editingService"
        :loading="actionLoading"
        @submit="handleServiceSubmit"
        @cancel="closeServiceModal"
      />
    </AdminModal>

    <!-- Price modal -->
    <AdminModal
      v-if="showPriceModal && selectedServiceId !== null"
      :title="
        isEditingPrice
          ? 'Редактировать цену'
          : 'Новая цена'
      "
      @close="closePriceModal"
    >
      <PriceForm
        :service-id="selectedServiceId"
        :price="editingPrice"
        :loading="actionLoading"
        @submit="handlePriceSubmit"
        @cancel="closePriceModal"
      />
    </AdminModal>

    <!-- Confirm -->
    <ConfirmDialog
      v-if="confirmType === 'service'"
      title="Удалить услугу?"
      message="Услуга будет удалена. Убедитесь, что связанные цены также обрабатываются на стороне backend."
      @confirm="confirmDelete"
      @cancel="closeConfirm"
    />

    <ConfirmDialog
      v-if="confirmType === 'price'"
      title="Удалить цену?"
      message="Эта цена будет удалена без возможности восстановления."
      @confirm="confirmDelete"
      @cancel="closeConfirm"
    />
  </section>
</template>