import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminQuiz from '../views/AdminQuiz.vue'
import AdminSummary from '../views/AdminSummary.vue'
import UserDashboard from '../views/UserDashboard.vue'
import UserScores from '../views/UserScores.vue'
import UserSummary from '../views/UserSummary.vue'
import QuizTaking from '../views/QuizTaking.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard
    },
    {
      path: '/admin/quiz',
      name: 'admin-quiz',
      component: AdminQuiz
    },
    {
      path: '/admin/summary',
      name: 'admin-summary',
      component: AdminSummary
    },
    {
      path: '/user/dashboard',
      name: 'user-dashboard',
      component: UserDashboard
    },
    {
      path: '/user/scores',
      name: 'user-scores',
      component: UserScores
    },
    {
      path: '/user/summary',
      name: 'user-summary',
      component: UserSummary
    },
    {
      path: '/user/quiz/:quizId',
      name: 'quiz-taking',
      component: QuizTaking
    }
  ]
})

export default router
