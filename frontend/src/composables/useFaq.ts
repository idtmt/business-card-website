import { ref } from 'vue'

import {
  createFaq,
  deleteFaq,
  getAdminFaq,
  updateFaq,
} from '../api/faq'

import type {
  FaqCreate,
  FaqResponse,
  FaqUpdate,
} from '../types/faq'


export function useFaq() {
  const faq = ref<FaqResponse[]>([])

  const loading = ref(false)
  const saving = ref(false)
  const deleting = ref(false)

  const error = ref('')
  const success = ref('')


  async function load() {
    loading.value = true
    error.value = ''

    try {
      faq.value = await getAdminFaq()
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось загрузить FAQ.'
    } finally {
      loading.value = false
    }
  }


  async function save(
    data: FaqCreate | FaqUpdate,
    faqId?: number,
  ) {
    saving.value = true
    error.value = ''
    success.value = ''

    try {
      if (faqId !== undefined) {
        await updateFaq(faqId, data as FaqUpdate)

        const index = faq.value.findIndex(
          item => item.id === faqId,
        )

        if (index !== -1) {
          faq.value[index] = {
            ...faq.value[index],
            ...data,
          }
        }

        success.value = 'Вопрос обновлён.'
      } else {
        const id = await createFaq(data as FaqCreate)

        faq.value.push({
          id,
          question: data.question,
          answer: data.answer,
          position: data.position ?? 0,
          is_hidden: data.is_hidden ?? false,
        })

        faq.value.sort(
          (a, b) => a.position - b.position,
        )

        success.value = 'Вопрос создан.'
      }
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось сохранить вопрос.'

      throw err
    } finally {
      saving.value = false
    }
  }


  async function remove(faqId: number) {
    deleting.value = true
    error.value = ''
    success.value = ''

    try {
      await deleteFaq(faqId)

      faq.value = faq.value.filter(
        item => item.id !== faqId,
      )

      success.value = 'Вопрос удалён.'
    } catch (err) {
      error.value =
        err instanceof Error
          ? err.message
          : 'Не удалось удалить вопрос.'

      throw err
    } finally {
      deleting.value = false
    }
  }


  return {
    faq,
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