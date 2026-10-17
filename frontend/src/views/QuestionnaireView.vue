<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import QuestionnaireNavigation from '../features/questionnaire/components/QuestionnaireNavigation.vue'
import QuestionnaireProgress from '../features/questionnaire/components/QuestionnaireProgress.vue'
import QuestionOption from '../features/questionnaire/components/QuestionOption.vue'
import { questions, QUESTIONNAIRE_VERSION } from '../features/questionnaire/data/questions'
import { useQuestionnaire } from '../features/questionnaire/composables/useQuestionnaire'

const router = useRouter()
const questionHeading = ref<HTMLElement | null>(null)
const categoryLabels: Record<string, string> = {
  FINANCIAL_STATUS: '재무 상태',
  RISK: '위험 감수 성향',
  ACCUMULATION: '소비·축적 성향',
  PLANNING: '금융관리 성향',
  INVESTMENT: '시장투자 선호',
}
const questionnaire = useQuestionnaire(questions, QUESTIONNAIRE_VERSION)
const categoryLabel = computed(() => categoryLabels[questionnaire.currentQuestion.value.category])
const { currentIndex, currentQuestion, currentAnswer, answeredCount, isFirst, isLast } = questionnaire

function goNext() {
  const wasLast = questionnaire.isLast.value
  if (questionnaire.next() && wasLast) {
    router.push('/test/result')
  }
}

function resetQuestionnaire() {
  questionnaire.reset()
  nextTick(() => questionHeading.value?.focus())
}

watch(questionnaire.currentIndex, () => {
  nextTick(() => questionHeading.value?.focus())
})
</script>

<template>
  <div class="questionnaire-page">
    <header class="questionnaire-header">
      <div class="questionnaire-header-inner">
        <RouterLink class="brand" to="/" aria-label="MBFI 홈으로 이동">
          <span class="brand-mark" aria-hidden="true"><i></i><i></i></span>
          <span>MBFI</span>
        </RouterLink>
        <RouterLink class="exit-link" to="/">테스트 나가기</RouterLink>
      </div>
    </header>

    <main class="questionnaire-main">
      <section class="questionnaire-panel" aria-labelledby="question-title">
        <QuestionnaireProgress
          :current="currentIndex + 1"
          :total="questions.length"
          :answered="answeredCount"
          :category-label="categoryLabel"
        />

        <div class="question-content">
          <p class="question-category">{{ categoryLabel }}</p>
          <h1 id="question-title" ref="questionHeading" tabindex="-1">
            {{ currentQuestion.title }}
          </h1>
          <p v-if="currentQuestion.description" class="question-description">
            {{ currentQuestion.description }}
          </p>

          <fieldset class="question-options">
            <legend class="sr-only">답변 선택</legend>
            <QuestionOption
              v-for="option in currentQuestion.options"
              :key="option.id"
              :option="option"
              :selected="currentAnswer === option.id"
              @select="questionnaire.selectAnswer"
            />
          </fieldset>
        </div>

        <QuestionnaireNavigation
          :is-first="isFirst"
          :is-last="isLast"
          :can-continue="Boolean(currentAnswer)"
          @previous="questionnaire.previous"
          @next="goNext"
        />

        <div class="questionnaire-actions">
          <button class="reset-link" type="button" @click="resetQuestionnaire">처음부터 다시 시작</button>
          <p>응답은 이 브라우저의 현재 탭에만 임시 저장됩니다.</p>
        </div>
      </section>
    </main>
  </div>
</template>
