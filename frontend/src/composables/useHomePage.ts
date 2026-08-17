import { onMounted, ref } from 'vue'

import { getCompany } from '../api/company'
import { getPublicServices } from '../api/services'
import { getPublicContacts } from '../api/contacts'
import { getPublicFaq } from '../api/faq'
import { getPublicLocations } from '../api/locations'

import type { CompanyResponse } from '../types/company'
import type { PublicServiceResponse } from '../types/service'
import type { ContactResponse } from '../types/contact'
import type { FaqResponse } from '../types/faq'
import type { PublicLocationResponse } from '../types/location'

export function useHomePage() {
  const company = ref<CompanyResponse | null>(null)
  const services = ref<PublicServiceResponse[]>([])
  const contacts = ref<ContactResponse[]>([])
  const faq = ref<FaqResponse[]>([])
  const locations = ref<PublicLocationResponse[]>([])

  const loading = ref(true)
  const error = ref(false)

  async function load() {
    loading.value = true
    error.value = false

    try {
      const [
        companyData,
        servicesData,
        contactsData,
        faqData,
        locationsData,
      ] = await Promise.all([
        getCompany(),
        getPublicServices(),
        getPublicContacts(),
        getPublicFaq(),
        getPublicLocations(),
      ])

      company.value = companyData
      services.value = servicesData
      contacts.value = contactsData
      faq.value = faqData
      locations.value = locationsData
    } catch {
      error.value = true
    } finally {
      loading.value = false
    }
  }

  onMounted(load)

  return {
    company,
    services,
    contacts,
    faq,
    locations,
    loading,
    error,
    reload: load,
  }
}