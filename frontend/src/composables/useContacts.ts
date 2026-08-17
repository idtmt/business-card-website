import { ref } from 'vue'

import {
  createContact,
  deleteContact,
  getAdminContacts,
  updateContact,
} from '../api/contacts'

import type {
  ContactCreate,
  ContactResponse,
  ContactUpdate,
} from '../types/contact'


export function useContacts() {
  const contacts = ref<ContactResponse[]>([])

  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)

  const error = ref('')
  const success = ref('')


  async function load() {
    loading.value = true
    error.value = ''

    try {
      contacts.value = await getAdminContacts()
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить контакты.'
    } finally {
      loading.value = false
    }
  }


  async function save(
    data: ContactCreate | ContactUpdate,
    contactId?: number,
  ) {
    saving.value = true
    error.value = ''
    success.value = ''

    try {
      if (contactId !== undefined) {
        await updateContact(contactId, data as ContactUpdate)

        const index = contacts.value.findIndex(
          contact => contact.id === contactId,
        )

        if (index !== -1) {
          contacts.value[index] = {
            ...contacts.value[index],
            ...data,
          }
        }

        success.value = 'Контакт обновлён.'
      } else {
        const id = await createContact(data as ContactCreate)

        contacts.value.push({
          id,
          title: data.title,
          value: data.value,
          url: data.url ?? null,
          icon: data.icon ?? null,
          position: data.position ?? 0,
          is_hidden: data.is_hidden ?? false,
        })

        contacts.value.sort(
          (a, b) => a.position - b.position,
        )

        success.value = 'Контакт создан.'
      }
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось сохранить контакт.'

      throw err
    } finally {
      saving.value = false
    }
  }


  async function remove(contactId: number) {
    deleting.value = true
    error.value = ''
    success.value = ''

    try {
      await deleteContact(contactId)

      contacts.value = contacts.value.filter(
        contact => contact.id !== contactId,
      )

      success.value = 'Контакт удалён.'
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось удалить контакт.'

      throw err
    } finally {
      deleting.value = false
    }
  }


  return {
    contacts,
    loading,
    saving,
    deleting,
    error,
    success,
    load,
    save,
    remove,
  }
}