import type { Question, QuestionnaireAnswers, QuestionnaireSubmission } from '../types/questionnaire'

export function isComplete(answers: QuestionnaireAnswers, questions: Question[]) {
  return questions.every((question) => Boolean(answers[question.id]))
}

export function validateSubmission(
  submission: unknown,
  questions: Question[],
  version: string,
  allowPartial = false,
): submission is QuestionnaireSubmission {
  if (!submission || typeof submission !== 'object') return false
  const value = submission as Partial<QuestionnaireSubmission>
  if (value.questionnaireVersion !== version || !Array.isArray(value.answers)) return false
  if (allowPartial ? value.answers.length > questions.length : value.answers.length !== questions.length) return false

  const questionIds = new Set(questions.map((question) => question.id))
  const answerIds = new Set<string>()
  return value.answers.every((answer) => {
    if (!answer || !questionIds.has(answer.questionId) || answerIds.has(answer.questionId)) return false
    const question = questions.find((item) => item.id === answer.questionId)
    const isValidOption = question?.options.some((option) => option.id === answer.optionId) ?? false
    if (isValidOption) answerIds.add(answer.questionId)
    return isValidOption
  })
}
