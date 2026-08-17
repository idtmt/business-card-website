<script setup lang="ts">
import AppHeader from '../../components/common/AppHeader.vue'
import AppFooter from '../../components/common/AppFooter.vue'

import HeroSection from '../../components/public/HeroSection.vue'
import ServicesSection from '../../components/public/ServicesSection.vue'
import ContactsSection from '../../components/public/ContactsSection.vue'
import FaqSection from '../../components/public/FaqSection.vue'
import LocationsSection from '../../components/public/LocationsSection.vue'

import { useHomePage } from '../../composables/useHomePage'

const {
  company,
  services,
  contacts,
  faq,
  locations,
  loading,
  error,
} = useHomePage()
</script>

<template>
  <div class="min-h-screen bg-white text-gray-900">
    <AppHeader />

    <main>
      <HeroSection
        :company="company"
        :loading="loading"
      />

      <ServicesSection
        :services="services"
        :loading="loading"
        :error="error"
      />

      <ContactsSection
        :contacts="contacts"
        :loading="loading"
        :error="error"
      />

      <FaqSection
        :faq="faq"
        :loading="loading"
        :error="error"
      />

      <LocationsSection
        :locations="locations"
        :loading="loading"
        :error="error"
      />
    </main>

    <AppFooter />
  </div>
</template>