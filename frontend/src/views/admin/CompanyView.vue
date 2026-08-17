<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'

import AdminFormActions from '../../components/admin/AdminFormActions.vue'
import AdminFormMessage from '../../components/admin/AdminFormMessage.vue'

import { useCompany } from '../../composables/useCompany'


const {
  company,
  loading,
  saving,
  error,
  success,
  load,
  save,
} = useCompany()


const form = reactive({
  name: '',
  description: '',
})


const initialized = ref(false)


function fillForm() {
  if (!company.value) {
    form.name = ''
    form.description = ''
    return
  }

  form.name = company.value.name
  form.description = company.value.description ?? ''
}


async function handleSubmit() {
  if (!form.name.trim()) {
    error.value = 'Введите название компании.'
    success.value = ''
    return
  }

  try {
    await save({
      name: form.name.trim(),
      description: form.description.trim() || null,
    })
  } catch {
    return
  }
}


function handleCancel() {
  fillForm()
  error.value = ''
  success.value = ''
}


onMounted(async () => {
  await load()

  fillForm()
  initialized.value = true
})
</script>


<template>
  <section>
    <!-- Header -->
    <div>
      <p class="text-sm font-medium text-gray-500">
        Управление
      </p>

      <h1
        class="mt-1 text-3xl font-bold tracking-tight text-gray-900"
      >
        Компания
      </h1>

      <p class="mt-2 text-sm text-gray-500">
        Управление основной информацией о компании.
      </p>
    </div>


    <!-- Loading -->
    <div
      v-if="loading"
      class="mt-8 rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    >
      <div class="animate-pulse space-y-6">
        <div class="space-y-2">
          <div class="h-4 w-24 rounded bg-gray-100" />
          <div class="h-11 w-full rounded-lg bg-gray-100" />
        </div>

        <div class="space-y-2">
          <div class="h-4 w-32 rounded bg-gray-100" />
          <div class="h-32 w-full rounded-lg bg-gray-100" />
        </div>
      </div>
    </div>


    <!-- Error while loading -->
    <div
      v-else-if="error && !initialized"
      class="mt-8"
    >
      <AdminFormMessage
        type="error"
        :message="error"
      />
    </div>


    <!-- Form -->
    <form
      v-else
      class="mt-8 max-w-3xl rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
      @submit.prevent="handleSubmit"
    >
      <div class="space-y-6">

        <!-- Name -->
        <div>
          <label
            for="company-name"
            class="block text-sm font-medium text-gray-700"
          >
            Название компании
          </label>

          <input
            id="company-name"
            v-model="form.name"
            type="text"
            autocomplete="organization"
            placeholder="Введите название компании"
            :disabled="saving"
            class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
          />
        </div>


        <!-- Description -->
        <div>
          <label
            for="company-description"
            class="block text-sm font-medium text-gray-700"
          >
            Описание
          </label>

          <textarea
            id="company-description"
            v-model="form.description"
            rows="6"
            placeholder="Введите описание компании"
            :disabled="saving"
            class="mt-2 w-full resize-y rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
          />
        </div>


        <!-- Messages -->
        <AdminFormMessage
          v-if="error"
          type="error"
          :message="error"
        />

        <AdminFormMessage
          v-if="success"
          type="success"
          :message="success"
        />


        <!-- Actions -->
        <AdminFormActions
          :loading="saving"
          submit-text="Сохранить"
          loading-text="Сохранение..."
          @cancel="handleCancel"
        />
      </div>
    </form>
  </section>
</template>