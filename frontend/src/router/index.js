import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    children: [
      {
        path: '',
        name: 'Welcome',
        component: () => import('../views/Welcome.vue')
      },
      {
        path: 'page1',
        name: 'Page1',
        component: () => import('../views/Page1.vue')
      },
      {
        path: 'page2',
        name: 'Page2',
        component: () => import('../views/Page2.vue')
      },
      {
        path: 'page3',
        name: 'Page3',
        component: () => import('../views/Page3.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user')
  
  if (to.name !== 'Login' && !isAuthenticated) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router