import { computed, ref } from 'vue'
import { loadAnswers, saveAnswers } from '../lib/questionnaire-storage'
import type { Question, QuestionnaireAnswers } from '../types/questionnaire'

export function useQuestionnaire(questions: Question[], version: string) {
  const answers = ref<QuestionnaireAnswers>(loadAnswers(questions, version))
  const firstUnansweredIndex = questions.findIndex((question) => !answers.value[question.id])
  const currentIndex = ref(firstUnansweredIndex === -1 ? questions.length - 1 : firstUnansweredIndex)
  const completed = ref(false)
  const currentQuestion = computed(() => questions[currentIndex.value])
  const currentAnswer = computed(() => answers.value[currentQuestion.value.id])
  const answeredCount = computed(() => Object.keys(answers.value).length)
  const progress = computed(() => Math.round((answeredCount.value / questions.length) * 100))
  const isFirst = computed(() => currentIndex.value === 0)
  const isLast = computed(() => currentIndex.value === questions.length - 1)

  function selectAnswer(optionId: string) {
    answers.value = { ...answers.value, [currentQuestion.value.id]: optionId }
    saveAnswers(answers.value, questions, version)
  }

  function next() {
    if (!currentAnswer.value) return false
    if (isLast.value) {
      completed.value = answeredCount.value === questions.length
      return completed.value
    }
    currentIndex.value += 1
    return true
  }

  function previous() {
    if (!isFirst.value) currentIndex.value -= 1
  }

  function reset() {
    answers.value = {}
    currentIndex.value = 0
    completed.value = false
    saveAnswers(answers.value, questions, version)
  }

  return { currentIndex, currentQuestion, currentAnswer, answeredCount, progress, isFirst, isLast, completed, selectAnswer, next, previous, reset }
}
