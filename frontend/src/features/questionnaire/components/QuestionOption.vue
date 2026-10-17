<script setup lang="ts">
import type { QuestionOption } from '../types/questionnaire'

defineProps<{
  option: QuestionOption
  selected: boolean
}>()

defineEmits<{
  select: [optionId: string]
}>()
</script>

<template>
  <label class="question-option" :class="{ selected }">
    <input
      type="radio"
      :value="option.id"
      :checked="selected"
      :aria-label="option.label"
      @change="$emit('select', option.id)"
    />
    <span class="option-letter">{{ option.id.slice(-1) }}</span>
    <span class="option-label">{{ option.label }}</span>
    <span v-if="selected" class="option-check" aria-label="선택됨">✓</span>
  </label>
</template>
