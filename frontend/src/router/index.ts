import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Health from '../views/Health.vue'

export default createRouter({ history: createWebHistory(), routes: [
  { path: '/', name: 'home', component: Home },
  { path: '/health', name: 'health', component: Health },
] })
