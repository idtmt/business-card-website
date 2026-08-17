import { ref } from 'vue'

import { getCompany } from '../api/company'
import { getAdminServices } from '../api/services'
import { getAdminContacts } from '../api/contacts'
import { getAdminFaq } from '../api/faq'
import { getAdminLocations } from '../api/locations'


export function useDashboard() {
  const loading = ref(false)
  const error = ref('')

  const companyCount = ref(0)
  const servicesCount = ref(0)
  const contactsCount = ref(0)
  const faqCount = ref(0)
  const locationsCount = ref(0)


  async function load() {
    loading.value = true
    error.value = ''

    try {
      const [
        company,
        services,
        contacts,
        faq,
        locations,
      ] = await Promise.all([
        getCompany(),
        getAdminServices(),
        getAdminContacts(),
        getAdminFaq(),
        getAdminLocations(),
      ])

      companyCount.value = company ? 1 : 0
      servicesCount.value = services.length
      contactsCount.value = contacts.length
      faqCount.value = faq.length
      locationsCount.value = locations.length

    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить данные.'

    } finally {
      loading.value = false
    }
  }


  return {
    loading,
    error,
    companyCount,
    servicesCount,
    contactsCount,
    faqCount,
    locationsCount,
    load,
  }
}