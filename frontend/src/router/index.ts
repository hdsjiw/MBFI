import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Health from '../views/Health.vue'
import QuestionnaireResultView from '../views/QuestionnaireResultView.vue'
import QuestionnaireView from '../views/QuestionnaireView.vue'

export default createRouter({ history: createWebHistory(), routes: [
  { path: '/', name: 'home', component: Home },
  { path: '/health', name: 'health', component: Health },
  { path: '/test', name: 'questionnaire', component: QuestionnaireView },
  { path: '/test/result', name: 'questionnaire-result', component: QuestionnaireResultView },
] })
