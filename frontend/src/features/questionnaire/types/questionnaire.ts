export type QuestionCategory =
  | 'FINANCIAL_STATUS'
  | 'RISK'
  | 'ACCUMULATION'
  | 'PLANNING'
  | 'INVESTMENT'

export type QuestionOption = {
  id: string
  label: string
  score?: number
}

export type Question = {
  id: string
  category: QuestionCategory
  step: number
  title: string
  description?: string
  options: QuestionOption[]
}

export type QuestionnaireAnswer = {
  questionId: string
  optionId: string
}

export type QuestionnaireSubmission = {
  questionnaireVersion: string
  answers: QuestionnaireAnswer[]
}

export type QuestionnaireAnswers = Record<string, string>

export type AxisScore = {
  rawScore: number
  normalizedScore: number
}

export type QuestionnaireScores = {
  risk: AxisScore
  accumulation: AxisScore
  planning: AxisScore
  investment: AxisScore
}
