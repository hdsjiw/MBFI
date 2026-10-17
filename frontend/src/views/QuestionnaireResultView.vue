<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { questions, QUESTIONNAIRE_VERSION } from '../features/questionnaire/data/questions'
import { loadAnswers } from '../features/questionnaire/lib/questionnaire-storage'
import { isComplete } from '../features/questionnaire/lib/questionnaire-validation'

const answers = loadAnswers(questions, QUESTIONNAIRE_VERSION)
const complete = computed(() => isComplete(answers, questions))
</script>

<template>
  <div class="questionnaire-page result-placeholder-page">
    <header class="questionnaire-header">
      <div class="questionnaire-header-inner">
        <RouterLink class="brand" to="/" aria-label="MBFI 홈으로 이동">
          <span class="brand-mark" aria-hidden="true"><i></i><i></i></span>
          <span>MBFI</span>
        </RouterLink>
      </div>
    </header>
    <main class="questionnaire-main">
      <section class="completion-card" aria-labelledby="completion-title">
        <div class="completion-icon" aria-hidden="true">✓</div>
        <p class="question-category">TEST COMPLETE</p>
        <h1 id="completion-title">{{ complete ? '응답을 모두 완료했어요.' : '아직 테스트가 끝나지 않았어요.' }}</h1>
        <p v-if="complete">응답 데이터가 분석 엔진으로 전달될 수 있는 상태입니다. 결과 분석 API가 연결되면 이 화면에서 분석 결과를 보여드릴 예정입니다.</p>
        <p v-else>모든 문항에 답한 뒤 결과를 확인할 수 있습니다.</p>
        <div class="completion-actions">
          <RouterLink v-if="!complete" class="primary-button" to="/test">테스트 이어서 하기 <span aria-hidden="true">→</span></RouterLink>
          <RouterLink class="secondary-button" to="/">홈으로 돌아가기</RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>
