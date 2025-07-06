<script setup>
import { useRoute, useRouter } from 'vue-router'
import { ref, watchEffect } from 'vue'

const router = useRouter()
const route = useRoute()

const isAdmin = ref(false)
const showNavbar = ref(false)
const hasToken = ref(false)

watchEffect(() => {
  const currentRoute = route.name
  const token = localStorage.getItem('token')
  hasToken.value = !!token

  // Show/hide navbar based on route
  if (currentRoute === 'Login' || currentRoute === 'Register' || currentRoute === null) {
    showNavbar.value = false
  } else {
    showNavbar.value = true
  }

  // Update admin status
  const storedAdmin = localStorage.getItem('isadmin')
  isAdmin.value = storedAdmin === 'true'
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user_id')
  localStorage.removeItem('isadmin')
  router.push('/login')
}
</script>

<template>
  <nav v-if="showNavbar" class="navbar">
    <ul class="navbar-list">
      <template v-if="hasToken">
        <template v-if="isAdmin">
          <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
          <li><router-link to="/admin/profile">Profile</router-link></li>
          <li><router-link to="/admin/parkinglots">Parking Lots</router-link></li>
          <li><router-link to="/admin/user_list">Users</router-link></li>
          <li><router-link to="/admin/summary">Summary</router-link></li>
        </template>
        <template v-else>
          <li><router-link to="/dashboard">Dashboard</router-link></li>
          <li><router-link to="/profile">Profile</router-link></li>
          <li><router-link to="/reservations">Current Reservations</router-link></li>
          <li><router-link to="/summary">Summary</router-link></li>
        </template>
        <li>
          <button @click="logout" class="logout-btn">Logout</button>
        </li>
      </template>

      <template v-else>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/login">Login</router-link></li>
        <li><router-link to="/register">Register</router-link></li>
      </template>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  background-color: #f5f5f5;
  padding: 0.75rem 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  font-family: Arial, sans-serif;
  margin-bottom: 1rem;
}

.navbar-list {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  align-items: center;
  margin: 0;
  padding: 0;
}

.navbar-list li {
  margin: 0;
}

.navbar-list a {
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

.navbar-list a:hover {
  color: #007bff;
}

.logout-btn {
  background-color: #e53935;
  color: white;
  border: none;
  padding: 6px 12px;
  font-weight: bold;
  border-radius: 6px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #c62828;
}
</style>
