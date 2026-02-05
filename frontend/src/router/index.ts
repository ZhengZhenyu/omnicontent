import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue'),
    },
    {
      path: '/contents',
      name: 'ContentList',
      component: () => import('../views/ContentList.vue'),
    },
    {
      path: '/contents/new',
      name: 'ContentNew',
      component: () => import('../views/ContentEdit.vue'),
    },
    {
      path: '/contents/:id/edit',
      name: 'ContentEdit',
      component: () => import('../views/ContentEdit.vue'),
    },
    {
      path: '/publish/:id?',
      name: 'PublishView',
      component: () => import('../views/PublishView.vue'),
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
    },
  ],
})

export default router
