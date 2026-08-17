import { ref } from 'vue'

import {
  createCompany,
  getCompany,
  updateCompany,
} from '../api/company'

import type {
  CompanyCreate,
  CompanyResponse,
  CompanyUpdate,
} from '../types/company'


export function useCompany() {
  const company = ref<CompanyResponse | null>(null)

  const loading = ref(false)
  const saving = ref(false)

  const error = ref('')
  const success = ref('')


  async function load() {
    loading.value = true
    error.value = ''

    try {
      company.value = await getCompany()
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить информацию о компании.'
    } finally {
      loading.value = false
    }
  }


  async function save(
    data: CompanyCreate | CompanyUpdate,
  ) {
    saving.value = true
    error.value = ''
    success.value = ''

    try {
      if (company.value) {
        await updateCompany(data as CompanyUpdate)

        company.value = {
          ...company.value,
          ...data,
        }

        success.value = 'Информация о компании обновлена.'
      } else {
        await createCompany(data as CompanyCreate)

        company.value = {
          name: data.name,
          description: data.description ?? null,
        }

        success.value = 'Информация о компании создана.'
      }
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось сохранить информацию о компании.'

      throw err
    } finally {
      saving.value = false
    }
  }


  return {
    company,
    loading,
    saving,
    error,
    success,
    load,
    save,
  }
}