<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="border-b border-slate-200 bg-white">
    <nav class="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
      <RouterLink to="/" class="text-xl font-bold text-slate-900">MBFI</RouterLink>
      <RouterLink to="/health" class="text-sm text-slate-500 hover:text-slate-900">서비스 상태</RouterLink>
    </nav>
  </header>
  <main><RouterView /></main>
</template>
