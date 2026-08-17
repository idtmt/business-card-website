<script setup lang="ts">
import { onMounted, ref } from 'vue'

import FaqForm from '../../components/admin/FaqForm.vue'
import FaqItem from '../../components/admin/FaqItem.vue'
import AdminFormMessage from '../../components/admin/AdminFormMessage.vue'

import { useFaq } from '../../composables/useFaq'

import type {
  FaqCreate,
  FaqResponse,
  FaqUpdate,
} from '../../types/faq'


const {
  faq,
  loading,
  saving,
  deleting,
  error,
  success,
  load,
  save,
  remove,
} = useFaq()


const editingFaq = ref<FaqResponse | null>(null)
const showForm = ref(false)


function handleCreate() {
  editingFaq.value = null
  error.value = ''
  success.value = ''
  showForm.value = true
}


function handleEdit(item: FaqResponse) {
  editingFaq.value = item
  error.value = ''
  success.value = ''
  showForm.value = true
}


function handleCancel() {
  editingFaq.value = null
  error.value = ''
  showForm.value = false
}


async function handleSubmit(
  data: FaqCreate | FaqUpdate,
) {
  try {
    await save(
      data,
      editingFaq.value?.id,
    )

    editingFaq.value = null
    showForm.value = false
  } catch {
    return
  }
}


async function handleDelete(item: FaqResponse) {
  const confirmed = window.confirm(
    `Удалить вопрос «${item.question}»?`,
  )

  if (!confirmed) {
    return
  }

  try {
    await remove(item.id)
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
          FAQ
        </h1>

        <p class="mt-2 text-sm text-gray-500">
          Управление часто задаваемыми вопросами.
        </p>
      </div>

      <button
        v-if="!showForm"
        type="button"
        class="shrink-0 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700"
        @click="handleCreate"
      >
        Добавить вопрос
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
          {{ editingFaq ? 'Редактирование вопроса' : 'Новый вопрос' }}
        </h2>

        <p class="mt-1 text-sm text-gray-500">
          {{
            editingFaq
              ? 'Измените вопрос и ответ.'
              : 'Добавьте новый вопрос в раздел FAQ.'
          }}
        </p>
      </div>

      <FaqForm
        :faq="editingFaq"
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
        <div class="h-4 w-64 rounded bg-gray-100" />
        <div class="mt-3 h-4 w-full rounded bg-gray-100" />
        <div class="mt-2 h-4 w-3/4 rounded bg-gray-100" />
      </div>
    </div>


    <!-- Empty -->
    <div
      v-else-if="faq.length === 0"
      class="mt-8 rounded-xl border border-dashed border-gray-300 bg-white p-10 text-center"
    >
      <h2 class="text-sm font-semibold text-gray-900">
        Вопросов пока нет
      </h2>

      <p class="mt-1 text-sm text-gray-500">
        Добавьте первый вопрос в FAQ.
      </p>

      <button
        type="button"
        class="mt-5 rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-700"
        @click="handleCreate"
      >
        Добавить вопрос
      </button>
    </div>


    <!-- List -->
    <div
      v-else
      class="mt-8 space-y-4"
    >
      <FaqItem
        v-for="item in faq"
        :key="item.id"
        :faq="item"
        :class="{ 'pointer-events-none opacity-60': deleting }"
        @edit="handleEdit(item)"
        @delete="handleDelete(item)"
      />
    </div>

  </section>
</template>