import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCommunityStore } from '../stores/community'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/initial-setup',
      name: 'InitialSetup',
      component: () => import('../views/InitialSetup.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/forgot-password',
      name: 'ForgotPassword',
      component: () => import('../views/ForgotPassword.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/reset-password',
      name: 'ResetPassword',
      component: () => import('../views/ResetPassword.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/contents',
      name: 'ContentList',
      component: () => import('../views/ContentList.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/contents/new',
      name: 'ContentNew',
      component: () => import('../views/ContentEdit.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/contents/:id/edit',
      name: 'ContentEdit',
      component: () => import('../views/ContentEdit.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/publish/:id?',
      name: 'PublishView',
      component: () => import('../views/PublishView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const communityStore = useCommunityStore()
  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login if not authenticated
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    // Redirect to dashboard if already logged in
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
