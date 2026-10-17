<script setup lang="ts">
import { computed, ref } from 'vue'

type Score = { label: string; value: number; tone: 'green' | 'yellow' }
type Allocation = { label: string; value: number; color: string }

const menuOpen = ref(false)
const selectedAnswer = ref(0)
const scores: Score[] = [
  { label: '안정성', value: 72, tone: 'green' }, { label: '성장성', value: 64, tone: 'green' },
  { label: '유동성', value: 81, tone: 'green' }, { label: '위험수용도', value: 55, tone: 'yellow' },
  { label: '소비성향', value: 43, tone: 'yellow' },
]
const allocations: Allocation[] = [
  { label: '현금성 자산', value: 20, color: '#15986f' }, { label: '예·적금', value: 30, color: '#c6d65d' },
  { label: 'ETF', value: 30, color: '#54c1bb' }, { label: '주식', value: 15, color: '#ffc642' }, { label: '기타', value: 5, color: '#ff9169' },
]
const answers = [
  { icon: '🐷', text: '일단 예금하고\n통장에 보관한다.' }, { icon: '📊', text: '일부는 저축하고\n일부는 투자한다.' },
  { icon: '🚀', text: '투자 기회를 찾아\n적극적으로 운용한다.' }, { icon: '🛍️', text: '평소 사고 싶었던 것에\n일부를 사용한다.' },
]
const selectedAnswerText = computed(() => answers[selectedAnswer.value]?.text.replace('\n', ' '))
const donutGradient = computed(() => {
  let start = 0
  const stops = allocations.map((item) => {
    const end = start + item.value
    const stop = `${item.color} ${start}% ${end}%`
    start = end
    return stop
  })
  return `conic-gradient(${stops.join(', ')})`
})
function closeMenu() { menuOpen.value = false }
function scrollTo(id: string) { closeMenu(); document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' }) }
</script>

<template>
  <div class="landing-page">
    <header class="site-header">
      <div class="container header-inner">
        <a class="brand" href="#top" aria-label="MBFI 홈으로 이동" @click="closeMenu"><span class="brand-mark" aria-hidden="true"><i></i><i></i></span><span>MBFI</span></a>
        <nav class="desktop-nav" aria-label="주요 메뉴"><button type="button" @click="scrollTo('about')">서비스 소개</button><button type="button" @click="scrollTo('question')">테스트 소개</button><button type="button" @click="scrollTo('guide')">이용안내</button></nav>
        <button class="menu-button" type="button" :aria-expanded="menuOpen" aria-controls="mobile-navigation" :aria-label="menuOpen ? '메뉴 닫기' : '메뉴 열기'" @click="menuOpen = !menuOpen"><span></span><span></span><span></span></button>
      </div>
      <nav v-if="menuOpen" id="mobile-navigation" class="mobile-nav" aria-label="모바일 메뉴"><button type="button" @click="scrollTo('about')">서비스 소개</button><button type="button" @click="scrollTo('question')">테스트 소개</button><button type="button" @click="scrollTo('guide')">이용안내</button></nav>
    </header>

    <main id="top">
      <section class="hero section-shell"><div class="hero-copy"><span class="eyebrow">My Best Financial Identity</span><h1>나는 어떤<br /><em>금융 유형</em>일까?</h1><p class="hero-description">몇 가지 질문으로 나의 금융 습관과 투자 성향을 알아보고<br class="desktop-only" /> 나에게 맞는 자산관리 방향을 확인해보세요.</p><RouterLink class="primary-button" to="/test">무료로 테스트 시작하기 <span aria-hidden="true">→</span></RouterLink><div class="meta-list" aria-label="테스트 정보"><span><b aria-hidden="true">◷</b> 약 3~5분</span><span><b aria-hidden="true">♙</b> 회원가입 없음</span></div></div><div class="hero-visual" aria-label="금융 성향 결과 미리보기 일러스트"><div class="leaf leaf-one" aria-hidden="true">◜</div><div class="leaf leaf-two" aria-hidden="true">◝</div><div class="speech-bubble">나의 금융<br />성향은?</div><div class="character character-woman" aria-hidden="true"><span>◡</span></div><div class="hero-result mini-card"><div class="result-icon">✦</div><div><small>당신의 MBFI는</small><strong>균형 성장형</strong></div><div class="mini-score"><span>안정성</span><b>72</b><span>성장성</span><b>64</b></div></div></div></section>

      <section id="about" class="section-shell feature-section"><div class="section-heading"><span class="section-number">01</span><h2>MBFI가 특별한 이유</h2><p>나를 알아가는 가장 쉬운 금융 습관</p></div><div class="feature-grid"><article class="feature-card"><div class="feature-icon">▤</div><span>01</span><h3>간단한 금융 성향 테스트</h3><p>일상 속 선택으로 알아보는<br />나의 금융 성향</p></article><article class="feature-card"><div class="feature-icon">▥</div><span>02</span><h3>내 금융 성향 분석</h3><p>재무 상태, 소비·저축, 투자 성향을<br />종합적으로 분석</p></article><article class="feature-card"><div class="feature-icon">◈</div><span>03</span><h3>나에게 맞는 자산관리 방향</h3><p>나의 유형에 맞는 자산배분 방향과<br />실천 가이드를 제시</p></article></div></section>

      <section id="question" class="section-shell question-section"><div class="section-heading"><span class="section-number">02</span><h2>어떤 질문이 나오나요?</h2><p>실제 테스트 화면을 미리 경험해보세요.</p></div><div class="question-card"><div class="question-title"><span>Q.</span><p>예상하지 못한 100만 원의 여유자금이 생겼습니다.<br />가장 먼저 하고 싶은 행동은 무엇인가요?</p></div><div class="answer-grid"><button v-for="(answer, index) in answers" :key="answer.text" type="button" class="answer-card" :class="{ selected: selectedAnswer === index }" @click="selectedAnswer = index"><span class="answer-icon" aria-hidden="true">{{ answer.icon }}</span><strong>{{ answer.text }}</strong><span v-if="selectedAnswer === index" class="check" aria-label="선택됨">✓</span></button></div><p class="selection-note" aria-live="polite">선택한 답변: {{ selectedAnswerText }}</p></div></section>

      <section id="guide" class="section-shell result-section"><div class="section-heading"><span class="section-number">03</span><h2>이런 결과를 얻을 수 있어요</h2><p>나의 금융 습관을 한눈에 확인해보세요.</p></div><div class="result-layout"><article class="profile-card"><div class="profile-art character character-man" aria-hidden="true"><span>◡</span></div><small>당신의 MBFI는</small><h3>균형 성장형<span>이에요</span></h3><p>안정성을 중요하게 생각하면서도<br />적절한 투자 기회에는 적극적인 유형이에요.</p><div class="tags"><span>#안정성과 성장의 균형</span><span>#장기적 관점</span><span>#계획적인 투자</span></div></article><article class="analysis-card"><h3>금융 성향 분석 <small>예시 데이터</small></h3><div class="score-list"><div v-for="score in scores" :key="score.label" class="score-row"><span>{{ score.label }}</span><i><b :class="score.tone" :style="{ width: `${score.value}%` }"></b></i><strong :class="score.tone">{{ score.value }}</strong></div></div><div class="allocation-divider"></div><h3>추천 자산 구성</h3><div class="allocation-area"><div class="donut" :style="{ background: `conic-gradient(${allocations.map((item, index) => `${item.color} ${allocations.slice(0, index).reduce((sum, previous) => sum + previous.value, 0)}% ${allocations.slice(0, index + 1).reduce((sum, previous) => sum + previous.value, 0)}%`).join(', ')})` }"><span>30%</span></div><ul><li v-for="item in allocations" :key="item.label"><i :style="{ background: item.color }"></i>{{ item.label }}<b>{{ item.value }}%</b></li></ul></div><p class="example-note">* 실제 분석 결과가 아닌 디자인 시연용 예시 데이터입니다.</p></article></div></section>

      <section class="section-shell audience-section"><div class="section-heading"><span class="section-number">04</span><h2>이런 분들께 추천해요</h2><p>나에게 맞는 금융 습관을 찾아보세요.</p></div><div class="audience-grid"><article><div class="avatar avatar-one">☺</div><div><h3>지금 나의 투자 성향이 궁금한 분</h3><p>막연한 불안을 알아가는 재미로</p></div></article><article><div class="avatar avatar-two">☺</div><div><h3>자산관리를 이제 시작하는 분</h3><p>나에게 맞는 방향이 필요해요</p></div></article><article><div class="avatar avatar-three">☺</div><div><h3>체계적으로 하고 싶은 분</h3><p>실천 가능한 가이드를 얻어요</p></div></article></div></section>
      <section class="section-shell testimonial-section"><div class="section-heading"><span class="section-number">05</span><h2>이런 경험을 할 수 있어요</h2><p>후기가 준비되면 실제 이용자 이야기로 업데이트됩니다.</p></div><div class="testimonial-card"><span class="quote-mark">“</span><blockquote>내 금융 습관을 돌아보고<br /><strong>나에게 맞는 방향을 찾는 시간</strong>이 되었어요.</blockquote><p class="testimonial-placeholder">예시 문구 · 실제 이용자 후기 아님</p></div></section>
      <section class="bottom-cta section-shell"><div class="cta-orb" aria-hidden="true">✦</div><h2>지금, 나의 금융 유형을<br />확인해보세요.</h2><p>작은 선택이 더 나은 자산관리의 시작이 될 수 있어요.</p><RouterLink class="primary-button" to="/test">무료로 테스트 시작하기 <span aria-hidden="true">→</span></RouterLink><div class="meta-list"><span>◷ 약 3~5분</span><span>♙ 회원가입 없음</span><span>▥ 무료</span></div></section>
    </main>

    <footer class="site-footer"><div class="footer-inner section-shell"><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true"><i></i><i></i></span><span>MBFI</span></a><p>더 나은 나의 금융 생활을 위한<br />작은 질문에서 시작합니다.</p><div class="footer-links"><button type="button" @click="scrollTo('about')">서비스 소개</button><button type="button" @click="scrollTo('question')">테스트 소개</button><button type="button" @click="scrollTo('guide')">이용안내</button><button type="button">개인정보처리방침</button><button type="button">문의하기</button></div><small>© 2026 MBFI. All rights reserved.</small></div></footer>
  </div>
</template>
