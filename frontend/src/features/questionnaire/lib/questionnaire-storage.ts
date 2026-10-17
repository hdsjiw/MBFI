import type { QuestionnaireAnswers, QuestionnaireSubmission } from '../types/questionnaire'
import { isComplete, validateSubmission } from './questionnaire-validation'
import type { Question } from '../types/questionnaire'

const STORAGE_KEY = 'mbfi.questionnaire.progress'

export function loadAnswers(questions: Question[], version: string): QuestionnaireAnswers {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return {}
    const parsed: unknown = JSON.parse(raw)
    if (!validateSubmission(parsed, questions, version, true)) return {}
    return Object.fromEntries(parsed.answers.map((answer) => [answer.questionId, answer.optionId]))
  } catch {
    return {}
  }
}

export function saveAnswers(answers: QuestionnaireAnswers, questions: Question[], version: string) {
  const submission: QuestionnaireSubmission = {
    questionnaireVersion: version,
    answers: questions
      .filter((question) => answers[question.id])
      .map((question) => ({ questionId: question.id, optionId: answers[question.id] })),
  }
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify(submission))
}

export function clearAnswers() {
  sessionStorage.removeItem(STORAGE_KEY)
}

export function hasSavedProgress(questions: Question[], version: string) {
  const answers = loadAnswers(questions, version)
  return Object.keys(answers).length > 0 && !isComplete(answers, questions)
}
