import { ref } from 'vue'

import {
  getAdminServices,
  createService,
  updateService,
  deleteService,
} from '../api/services'

import {
  getPricesByService,
  createPrice,
  updatePrice,
  deletePrice,
} from '../api/prices'

import type {
  ServiceCreate,
  ServiceUpdate,
  ServiceResponse,
} from '../types/service'

import type {
  PriceCreate,
  PriceUpdate,
  PriceResponse,
} from '../types/price'

export function useServices() {
  const services = ref<ServiceResponse[]>([])
  const prices = ref<Record<number, PriceResponse[]>>({})

  const loading = ref(false)
  const actionLoading = ref(false)
  const error = ref<string | null>(null)

  async function loadServices() {
    loading.value = true
    error.value = null

    try {
      services.value = await getAdminServices()

      const result = await Promise.all(
        services.value.map(async (service) => ({
          serviceId: service.id,
          prices: await getPricesByService(service.id),
        })),
      )

      prices.value = Object.fromEntries(
        result.map((item) => [
          item.serviceId,
          item.prices,
        ]),
      )
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить услуги.'
    } finally {
      loading.value = false
    }
  }

  async function addService(data: ServiceCreate) {
    actionLoading.value = true

    try {
      await createService(data)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  async function editService(
    serviceId: number,
    data: ServiceUpdate,
  ) {
    actionLoading.value = true

    try {
      await updateService(serviceId, data)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  async function removeService(serviceId: number) {
    actionLoading.value = true

    try {
      await deleteService(serviceId)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  async function addPrice(data: PriceCreate) {
    actionLoading.value = true

    try {
      await createPrice(data)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  async function editPrice(
    priceId: number,
    data: PriceUpdate,
  ) {
    actionLoading.value = true

    try {
      await updatePrice(priceId, data)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  async function removePrice(priceId: number) {
    actionLoading.value = true

    try {
      await deletePrice(priceId)
      await loadServices()
    } finally {
      actionLoading.value = false
    }
  }

  function getPrices(serviceId: number) {
    return prices.value[serviceId] ?? []
  }

  return {
    services,
    prices,
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
  }
}