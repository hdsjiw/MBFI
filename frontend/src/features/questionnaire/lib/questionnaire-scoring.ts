import type { Question, QuestionnaireAnswers, QuestionnaireScores } from '../types/questionnaire'

const axisQuestions = {
  risk: ['Q01', 'Q02', 'Q03'],
  accumulation: ['Q04', 'Q05', 'Q06'],
  planning: ['Q07', 'Q08', 'Q09'],
  investment: ['Q10', 'Q11', 'Q12'],
} as const

function calculateAxis(questionIds: readonly string[], answers: QuestionnaireAnswers, questions: Question[]) {
  const rawScore = questionIds.reduce((total, questionId) => {
    const question = questions.find((item) => item.id === questionId)
    const optionId = answers[questionId]
    const option = question?.options.find((item) => item.id === optionId)
    return total + (option?.score ?? 0)
  }, 0)

  return { rawScore, normalizedScore: ((rawScore - 3) / 9) * 100 }
}

export function calculateQuestionnaireScores(
  answers: QuestionnaireAnswers,
  questions: Question[],
): QuestionnaireScores {
  return {
    risk: calculateAxis(axisQuestions.risk, answers, questions),
    accumulation: calculateAxis(axisQuestions.accumulation, answers, questions),
    planning: calculateAxis(axisQuestions.planning, answers, questions),
    investment: calculateAxis(axisQuestions.investment, answers, questions),
  }
}
