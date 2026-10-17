<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getBackendHealth } from '../lib/api'
const status = ref('확인 중...')
onMounted(async () => {
  try {
    const health = await getBackendHealth()
    status.value = `${health.service}: ${health.status}`
  } catch {
    status.value = 'Backend에 연결할 수 없습니다.'
  }
})
</script>
<template><section class="mx-auto max-w-5xl px-6 py-20"><h1 class="text-3xl font-bold text-slate-900">서비스 상태</h1><p class="mt-4 text-slate-600">{{ status }}</p></section></template>
