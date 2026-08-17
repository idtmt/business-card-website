<script setup lang="ts">
import { reactive, watch } from 'vue'

import type {
  ContactCreate,
  ContactResponse,
  ContactUpdate,
} from '../../types/contact'


const props = defineProps<{
  contact?: ContactResponse | null
  loading?: boolean
}>()

const emit = defineEmits<{
  submit: [data: ContactCreate | ContactUpdate]
  cancel: []
}>()


const form = reactive({
  title: '',
  value: '',
  url: '',
  icon: '',
  position: 0,
  is_hidden: false,
})


function fillForm() {
  form.title = props.contact?.title ?? ''
  form.value = props.contact?.value ?? ''
  form.url = props.contact?.url ?? ''
  form.icon = props.contact?.icon ?? ''
  form.position = props.contact?.position ?? 0
  form.is_hidden = props.contact?.is_hidden ?? false
}


watch(
  () => props.contact,
  fillForm,
  { immediate: true },
)


function handleSubmit() {
  if (!form.title.trim() || !form.value.trim()) {
    return
  }

  emit('submit', {
    title: form.title.trim(),
    value: form.value.trim(),
    url: form.url.trim() || null,
    icon: form.icon.trim() || null,
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

      <!-- Title -->
      <div>
        <label
          for="contact-title"
          class="block text-sm font-medium text-gray-700"
        >
          Название
        </label>

        <input
          id="contact-title"
          v-model="form.title"
          type="text"
          placeholder="Например, Telegram"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />
      </div>


      <!-- Value -->
      <div>
        <label
          for="contact-value"
          class="block text-sm font-medium text-gray-700"
        >
          Значение
        </label>

        <input
          id="contact-value"
          v-model="form.value"
          type="text"
          placeholder="@username или +998 90 123 45 67"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />
      </div>


      <!-- URL -->
      <div>
        <label
          for="contact-url"
          class="block text-sm font-medium text-gray-700"
        >
          Ссылка
        </label>

        <input
          id="contact-url"
          v-model="form.url"
          type="url"
          placeholder="https://t.me/username"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />

        <p class="mt-2 text-xs text-gray-500">
          Необязательно. Используется для перехода по контакту.
        </p>
      </div>


      <!-- Icon -->
      <div>
        <label
          for="contact-icon"
          class="block text-sm font-medium text-gray-700"
        >
          Иконка
        </label>

        <input
          id="contact-icon"
          v-model="form.icon"
          type="text"
          placeholder="telegram"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />

        <p class="mt-2 text-xs text-gray-500">
          Название иконки, если используется в интерфейсе сайта.
        </p>
      </div>


      <!-- Position -->
      <div>
        <label
          for="contact-position"
          class="block text-sm font-medium text-gray-700"
        >
          Позиция
        </label>

        <input
          id="contact-position"
          v-model.number="form.position"
          type="number"
          min="0"
          :disabled="loading"
          class="mt-2 w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none transition focus:border-gray-500 focus:ring-1 focus:ring-gray-500 disabled:cursor-not-allowed disabled:bg-gray-50"
        />
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
          Скрыть контакт на сайте
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
            !form.title.trim() ||
            !form.value.trim()
          "
          class="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ loading ? 'Сохранение...' : 'Сохранить' }}
        </button>
      </div>

    </div>
  </form>
</template>