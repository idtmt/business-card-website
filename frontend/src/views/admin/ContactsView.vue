<script setup lang="ts">
import { onMounted, ref } from 'vue'

import ContactForm from '../../components/admin/ContactForm.vue'
import ContactItem from '../../components/admin/ContactItem.vue'
import AdminFormMessage from '../../components/admin/AdminFormMessage.vue'

import { useContacts } from '../../composables/useContacts'

import type {
  ContactCreate,
  ContactResponse,
  ContactUpdate,
} from '../../types/contact'


const {
  contacts,
  loading,
  saving,
  deleting,
  error,
  success,
  load,
  save,
  remove,
} = useContacts()


const editingContact = ref<ContactResponse | null>(null)
const showForm = ref(false)


function handleCreate() {
  editingContact.value = null
  error.value = ''
  success.value = ''
  showForm.value = true
}


function handleEdit(contact: ContactResponse) {
  editingContact.value = contact
  error.value = ''
  success.value = ''
  showForm.value = true
}


function handleCancel() {
  editingContact.value = null
  error.value = ''
  showForm.value = false
}


async function handleSubmit(
  data: ContactCreate | ContactUpdate,
) {
  try {
    await save(
      data,
      editingContact.value?.id,
    )

    editingContact.value = null
    showForm.value = false
  } catch {
    return
  }
}


async function handleDelete(contact: ContactResponse) {
  const confirmed = window.confirm(
    `Удалить контакт «${contact.title}»?`,
  )

  if (!confirmed) {
    return
  }

  try {
    await remove(contact.id)
  } catch {
    return
  }
}


onMounted(load)
</script>


<template>
  <section>

    <!-- Header -->
    <div class="flex items-start justify-between gap-6">
      <div>
        <p class="text-sm font-medium text-gray-500">
          Управление
        </p>

        <h1
          class="mt-1 text-3xl font-bold tracking-tight text-gray-900"
        >
          Контакты
        </h1>

        <p class="mt-2 text-sm text-gray-500">
          Управление контактной информацией компании.
        </p>
      </div>

      <button
        v-if="!showForm"
        type="button"
        class="shrink-0 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700"
        @click="handleCreate"
      >
        Добавить контакт
      </button>
    </div>


    <!-- Messages -->
    <div
      v-if="error"
      class="mt-6"
    >
      <AdminFormMessage
        type="error"
        :message="error"
      />
    </div>

    <div
      v-if="success"
      class="mt-6"
    >
      <AdminFormMessage
        type="success"
        :message="success"
      />
    </div>


    <!-- Form -->
    <div
      v-if="showForm"
      class="mt-8 max-w-3xl"
    >
      <div class="mb-4">
        <h2 class="text-lg font-semibold text-gray-900">
          {{ editingContact ? 'Редактирование контакта' : 'Новый контакт' }}
        </h2>

        <p class="mt-1 text-sm text-gray-500">
          {{
            editingContact
              ? 'Измените данные контакта.'
              : 'Добавьте новый способ связи с компанией.'
          }}
        </p>
      </div>

      <ContactForm
        :contact="editingContact"
        :loading="saving"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </div>


    <!-- Loading -->
    <div
      v-else-if="loading"
      class="mt-8 space-y-4"
    >
      <div
        v-for="index in 3"
        :key="index"
        class="animate-pulse rounded-xl border border-gray-200 bg-white p-5"
      >
        <div class="h-4 w-32 rounded bg-gray-100" />
        <div class="mt-3 h-4 w-56 rounded bg-gray-100" />
        <div class="mt-2 h-3 w-40 rounded bg-gray-100" />
      </div>
    </div>


    <!-- Empty -->
    <div
      v-else-if="contacts.length === 0"
      class="mt-8 rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center"
    >
      <h2 class="text-sm font-semibold text-gray-900">
        Контактов пока нет
      </h2>

      <p class="mt-1 text-sm text-gray-500">
        Добавьте первый контакт компании.
      </p>

      <button
        type="button"
        class="mt-5 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700"
        @click="handleCreate"
      >
        Добавить контакт
      </button>
    </div>


    <!-- List -->
    <div
      v-else
      class="mt-8 space-y-4"
    >
      <ContactItem
        v-for="contact in contacts"
        :key="contact.id"
        :contact="contact"
        :class="{ 'pointer-events-none opacity-60': deleting }"
        @edit="handleEdit(contact)"
        @delete="handleDelete(contact)"
      />
    </div>

  </section>
</template>