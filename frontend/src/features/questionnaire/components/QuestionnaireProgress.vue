<script setup lang="ts">
defineProps<{
  current: number
  total: number
  answered: number
  categoryLabel: string
}>()
</script>

<template>
  <div class="questionnaire-progress">
    <div class="progress-topline">
      <span>STEP {{ categoryLabel }}</span>
      <strong>{{ current }} / {{ total }}</strong>
    </div>
    <div
      class="progress-track"
      role="progressbar"
      aria-label="설문 진행률"
      :aria-valuenow="current"
      :aria-valuemin="1"
      :aria-valuemax="total"
    >
      <span :style="{ width: ((current / total) * 100) + '%' }"></span>
    </div>
    <p>{{ answered }}개 응답 완료</p>
  </div>
</template>
