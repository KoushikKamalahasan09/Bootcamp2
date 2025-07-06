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
    {
      path:'/admin/parkinglots',
      name: 'admin_parkinglots',
      component: () => import('../views/Admin/Parkinglots.vue'), // Lazy-loaded Admin Parking Lots
    },
    {
      path:'/admin/parkinglots/:lot_id',
      name: 'admin_parkingspots',
      component: () => import('../views/Admin/Parkingspots.vue'), // Lazy-loaded Admin Parking Spots
    },
    {
      path:'/admin/user_list',
      name: 'admin_user_list',
      component: () => import('../views/Admin/list_users.vue'), // Lazy-loaded Admin User List
    },
    {
      path:'/parkinglots/:lot_id',
      name: 'user_parking_lot',
      component: () => import('../views/User/lot_details.vue'), // Lazy-loaded User Parking Lot
    },
    {
      path:'/reservations',
      name: 'user_reservations',
      component: () => import('../views/User/reservations.vue'), // Lazy-loaded User Reservations
    },
    {
      path:'/summary',
      name: 'user_summary',
      component: () => import('../views/User/summary.vue'), // Lazy-loaded User Summary
    },
    {
      path:'/admin/summary',
      name: 'admin_summary',
      component: () => import('../views/Admin/summary.vue'), // Lazy-loaded Admin Summary
    },
    {
      path:'/admin/user/:user_id/summary',
      name: 'admin_user_summary',
      component: () => import('../views/Admin/user_summary.vue'), // Lazy-loaded Admin User Summary
    }

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
