import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Auth/login.vue' // Import the Login view
import Register from '../views/Auth/register.vue' // Import the Register view
import AdminDashboard from '../views/Admin/dashboard.vue'
import AdminProfile from '../views/Admin/profile.vue'
import UserDashboard from '../views/User/dashboard.vue'
import UserProfile from '../views/User/profile.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path:'/login',
      name: 'login',
      component: Login, 
    },
    {
      path : '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/admin/dashboard',
      name: 'admin_dashboard',
      component: AdminDashboard, // Admin Dashboard view
    },
    {
      path:'/admin/profile',
      name: 'admin_profile',
      component: AdminProfile, // Admin Profile view
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: UserDashboard, // Admin Dashboard view
    },
    {
      path:'/profile',
      name: 'profile',
      component: UserProfile, // Admin Profile view
    },

    /*{
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },*/
  ],
})

export default router
