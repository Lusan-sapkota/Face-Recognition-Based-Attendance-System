import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import AdminView from '../views/AdminView.vue'
import ProfileView from '../views/ProfileView.vue'
import FAQView from '../views/FAQView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'user-login',
      component: LoginView,
      props: { userType: 'user' }
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: LoginView,
      props: { userType: 'admin' }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView,
      props: true,
    },
    {
      path: '/faq',
      name: 'faq',
      component: FAQView,
    },
  ],
})

// Navigation guard for authentication
router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !token) {
    // Redirect to appropriate login based on the route
    if (to.path.startsWith('/admin')) {
      return '/admin/login'
    }
    return '/login'
  }

  if (to.meta.requiresAdmin && userRole !== 'admin') {
    return '/dashboard'
  }
})

export default router
