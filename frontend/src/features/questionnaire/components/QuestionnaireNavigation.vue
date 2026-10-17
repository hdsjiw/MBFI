<script setup lang="ts">
defineProps<{
  isFirst: boolean
  isLast: boolean
  canContinue: boolean
}>()

defineEmits<{
  previous: []
  next: []
}>()
</script>

<template>
  <div class="questionnaire-navigation">
    <button class="secondary-button" type="button" :disabled="isFirst" @click="$emit('previous')">
      ← 이전
    </button>
    <button class="primary-button" type="button" :disabled="!canContinue" @click="$emit('next')">
      {{ isLast ? '결과 확인하기' : '다음' }} <span aria-hidden="true">→</span>
    </button>
  </div>
</template>
