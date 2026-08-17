<script setup lang="ts">
import { reactive, watch } from 'vue'

import type {
  FaqCreate,
  FaqResponse,
  FaqUpdate,
} from '../../types/faq'


const props = defineProps<{
  faq?: FaqResponse | null
  loading?: boolean
}>()

const emit = defineEmits<{
  submit: [data: FaqCreate | FaqUpdate]
  cancel: []
}>()


const form = reactive({
  question: '',
  answer: '',
  position: 0,
  is_hidden: false,
})


function fillForm() {
  form.question = props.faq?.question ?? ''
  form.answer = props.faq?.answer ?? ''
  form.position = props.faq?.position ?? 0
  form.is_hidden = props.faq?.is_hidden ?? false
}


watch(
  () => props.faq,
  fillForm,
  { immediate: true },
)


function handleSubmit() {
  if (!form.question.trim() || !form.answer.trim()) {
    return
  }

  emit('submit', {
    question: form.question.trim(),
    answer: form.answer.trim(),
    position: form.position,
    is_hidden: form.is_hidden,
  })
}
</script>


<template>
  <form
    class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
    @submit.prevent="handleSubmit"
  >
    <div class="space-y-6">

      <!-- Question -->
      <div>
        <label
          for="faq-question"
          class="block text-sm font-medium text-gray-700"
        >
          Вопрос
        </label>

        <input
          id="faq-question"
          v-model="form.question"
          type="text"
          placeholder="Например, Как записаться?"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />
      </div>


      <!-- Answer -->
      <div>
        <label
          for="faq-answer"
          class="block text-sm font-medium text-gray-700"
        >
          Ответ
        </label>

        <textarea
          id="faq-answer"
          v-model="form.answer"
          rows="6"
          placeholder="Введите ответ на вопрос"
          :disabled="loading"
          class="mt-2 w-full resize-y rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />
      </div>


      <!-- Position -->
      <div>
        <label
          for="faq-position"
          class="block text-sm font-medium text-gray-700"
        >
          Позиция
        </label>

        <input
          id="faq-position"
          v-model.number="form.position"
          type="number"
          min="0"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />

        <p class="mt-2 text-xs text-gray-500">
          Определяет порядок отображения вопросов.
        </p>
      </div>


      <!-- Hidden -->
      <label class="flex items-center gap-3">
        <input
          v-model="form.is_hidden"
          type="checkbox"
          :disabled="loading"
          class="h-4 w-4 rounded border-gray-300"
        />

        <span class="text-sm text-gray-700">
          Скрыть вопрос на сайте
        </span>
      </label>


      <!-- Actions -->
      <div
        class="flex items-center justify-end gap-3 border-t border-gray-200 pt-6"
      >
        <button
          type="button"
          :disabled="loading"
          class="rounded-lg border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-700 transition hover:border-gray-300 hover:bg-gray-50 hover:text-gray-900 disabled:cursor-not-allowed disabled:opacity-50"
          @click="emit('cancel')"
        >
          Отмена
        </button>

        <button
          type="submit"
          :disabled="
            loading ||
            !form.question.trim() ||
            !form.answer.trim()
          "
          class="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </div>

    </div>
  </form>
</template>