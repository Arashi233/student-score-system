import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import StudentDashboard from '../views/StudentDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 1 }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 2 }
  },
  {
    path: '/super-admin/dashboard',
    name: 'SuperAdminDashboard',
    component: () => import('../views/SuperAdminDashboard.vue'),
    meta: { requiresAuth: true, role: 3 }
  }
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth) {
    if (!token || !user) {
      next({ path: '/', replace: true })
      return
    }

    if (to.meta.role && to.meta.role !== user.type) {
      next({ path: '/', replace: true })
      return
    }
  }

  if (to.path === '/' && token) {
    if (user?.type === 1) next({ path: '/student/dashboard', replace: true })
    else if (user?.type === 2) next({ path: '/admin/dashboard', replace: true })
    else if (user?.type === 3) next({ path: '/super-admin/dashboard', replace: true })
    else next()
    return
  }

  next()
})

export default router
