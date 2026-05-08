import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import DSMDesktop from '../layouts/DSMDesktop.vue'

const routes = [
  { path: '/', component: DSMDesktop, children: [
      { path: '', redirect: '/files' },
      { path: 'files', component: () => import('../components/apps/FileManager.vue') },
      { path: 'storage', component: () => import('../components/apps/StorageManager.vue') },
      { path: 'users', component: () => import('../components/apps/UserManager.vue') },
      { path: 'shares', component: () => import('../components/apps/ShareManager.vue') },
      { path: 'network', component: () => import('../components/apps/NetworkManager.vue') },
      { path: 'tasks', component: () => import('../components/apps/TaskScheduler.vue') },
      { path: 'apps', component: () => import('../components/apps/AppCenter.vue') },
      { path: 'snapshots', component: () => import('../components/apps/SnapshotManager.vue') },
      { path: 'san', component: () => import('../components/apps/SanManager.vue') },
      { path: 'settings', component: () => import('../components/apps/Settings.vue') },
    ]
  },
  { path: '/login', component: Login }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
