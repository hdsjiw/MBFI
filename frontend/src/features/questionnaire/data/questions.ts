import type { Question } from '../types/questionnaire'

export const QUESTIONNAIRE_VERSION = '2026-01'

const options = (questionId: string, labels: string[], scores?: number[]) =>
  labels.map((label, index) => ({
    id: `${questionId}-${String.fromCharCode(65 + index)}`,
    label,
    ...(scores ? { score: scores[index] } : {}),
  }))

export const questions: Question[] = [
  { id: 'F01', category: 'FINANCIAL_STATUS', step: 1, title: '현재 연령대는?', options: options('F01', ['20대', '30대', '40대', '50대 이상']) },
  { id: 'F02', category: 'FINANCIAL_STATUS', step: 1, title: '현재 보유한 금융자산은 어느 정도인가요?', description: '현금, 예금, 적금, 주식, ETF 등 금융자산을 포함합니다.', options: options('F02', ['500만원 미만', '500만~2,000만원', '2,000만~5,000만원', '5,000만원 이상']) },
  { id: 'F03', category: 'FINANCIAL_STATUS', step: 1, title: '한 달 평균 들어오는 소득은?', description: '소득이 없는 경우 첫 번째 항목을 선택하세요.', options: options('F03', ['100만원 미만', '100만~200만원', '200만~350만원', '350만원 이상']) },
  { id: 'F04', category: 'FINANCIAL_STATUS', step: 1, title: '한 달 평균 생활비와 소비는?', options: options('F04', ['100만원 미만', '100만~200만원', '200만~300만원', '300만원 이상']) },
  { id: 'F05', category: 'FINANCIAL_STATUS', step: 1, title: '소득이 들어오면 보통 어느 정도를 남길 수 있나요?', options: options('F05', ['거의 남기기 어렵다', '10% 정도', '10~30% 정도', '30% 이상']) },
  { id: 'F06', category: 'FINANCIAL_STATUS', step: 1, title: '현재 갚아야 하는 부채 부담은 어느 정도인가요?', options: options('F06', ['상환 부담이 매우 크다', '다소 부담된다', '있지만 부담은 크지 않다', '없거나 거의 없다']) },
  { id: 'F07', category: 'FINANCIAL_STATUS', step: 1, title: '현재 가장 중요한 재무 목표는 어느 정도인가요?', options: options('F07', ['1,000만원 미만', '1,000만~3,000만원', '3,000만~1억원', '1억원 이상']) },
  { id: 'F08', category: 'FINANCIAL_STATUS', step: 1, title: '이 돈이 필요한 시점은 언제인가요?', options: options('F08', ['1년 이내', '1~3년', '3~7년', '7년 이후']) },
  { id: 'Q01', category: 'RISK', step: 2, title: '투자한 1,000만원이 한 달 뒤 850만원이 됐습니다. 가장 가까운 행동은?', options: options('Q01', ['더 떨어질까 걱정돼 대부분 정리한다', '일부 줄이고 상황을 지켜본다', '일단 그대로 유지한다', '장기 계획이 변하지 않았다면 그대로 유지한다'], [1, 2, 3, 4]) },
  { id: 'Q02', category: 'RISK', step: 2, title: '여유자금 500만원을 3년간 사용하지 않아도 된다면?', options: options('Q02', ['원금 변동이 거의 없는 곳에 둔다', '대부분 안전하게 두고 일부만 투자한다', '안전자산과 투자자산을 비슷하게 나눈다', '가격 변동을 감수하고 대부분 투자한다'], [1, 2, 3, 4]) },
  { id: 'Q03', category: 'RISK', step: 2, title: '투자한 돈의 가격이 매일 크게 움직인다면 나는?', options: options('Q03', ['별로 신경 쓰이지 않는다', '조금 신경 쓰이지만 유지할 수 있다', '계속 확인하게 될 것 같다', '손실이 없어도 불안해서 정리하고 싶다'], [4, 3, 2, 1]) },
  { id: 'Q04', category: 'ACCUMULATION', step: 3, title: '예상하지 못한 보너스 100만원이 생겼다면?', options: options('Q04', ['대부분 갖고 싶었던 것에 쓴다', '절반 이상 쓰고 나머지를 남긴다', '일부만 쓰고 대부분 남긴다', '거의 전부 저축하거나 투자한다'], [1, 2, 3, 4]) },
  { id: 'Q05', category: 'ACCUMULATION', step: 3, title: '월급날 직후 가장 가까운 모습은?', options: options('Q05', ['필요한 소비부터 하고 남으면 저축한다', '대략 쓸 돈과 남길 돈을 생각한다', '먼저 일정 금액을 떼어놓고 소비한다', '저축·투자 금액을 먼저 자동으로 분리한다'], [1, 2, 3, 4]) },
  { id: 'Q06', category: 'ACCUMULATION', step: 3, title: '계획하지 않은 20만원 상당의 구매욕구가 생겼을 때 가장 가까운 행동은?', options: options('Q06', ['바로 구매한다', '가격만 확인한다', '필요성과 예산을 확인한다', '일정 기간 두고 재검토한다'], [1, 2, 3, 4]) },
  { id: 'Q07', category: 'PLANNING', step: 4, title: '다음 달 큰 지출이 예정되어 있다면?', options: options('Q07', ['일단 그때 가서 방법을 생각한다', '가까워지면 지출을 조금 줄인다', '이번 달부터 일부 돈을 따로 둔다', '필요한 금액을 나눠 미리 준비한다'], [1, 2, 3, 4]) },
  { id: 'Q08', category: 'PLANNING', step: 4, title: '내 계좌에 지금 얼마가 있는지 묻는다면?', options: options('Q08', ['거의 모른다', '대략적인 금액만 안다', '주요 계좌 정도는 알고 있다', '자산과 지출 규모를 꽤 정확히 알고 있다'], [1, 2, 3, 4]) },
  { id: 'Q09', category: 'PLANNING', step: 4, title: '최근 예상보다 많이 지출한 달에 가장 가까운 행동은?', options: options('Q09', ['별도 대응을 하지 않는다', '이후 소비를 조금 줄인다', '지출 항목을 확인한다', '원인을 확인하고 다음 달 예산도 조정한다'], [1, 2, 3, 4]) },
  { id: 'Q10', category: 'INVESTMENT', step: 5, title: '5년 이상 쓰지 않을 여유자금이 있다면 가장 끌리는 방법은?', options: options('Q10', ['예금·적금 중심으로 모은다', '예적금을 중심으로 일부 투자한다', '예적금과 ETF·주식 등을 함께 활용한다', 'ETF·주식 등 투자자산을 중심으로 운용한다'], [1, 2, 3, 4]) },
  { id: 'Q11', category: 'INVESTMENT', step: 5, title: '장기적인 자산형성에서 시장투자에 대한 생각은?', options: options('Q11', ['가능하면 이용하지 않고 싶다', '필요하면 일부 활용할 수 있다', '장기 자산형성 수단 중 하나라고 생각한다', '적극적으로 활용하고 싶다'], [1, 2, 3, 4]) },
  { id: 'Q12', category: 'INVESTMENT', step: 5, title: '예적금만으로 목표 금액을 만들기 어렵다는 걸 알게 됐다면?', options: options('Q12', ['목표 금액이나 기간을 조정한다', '저축액을 늘리는 방법부터 찾는다', '일부 자금을 장기 투자하는 방법도 검토한다', '장기 투자 비중을 적극적으로 늘리는 방법을 검토한다'], [1, 2, 3, 4]) },
]
