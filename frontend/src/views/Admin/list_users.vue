<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const users = ref([])
const router = useRouter()

// JWT token stored in localStorage
const token = localStorage.getItem('token')

// Fetch all parking user
const fetchUsers = async () => {
  try {
    const response = await fetch('http://localhost:5000/users', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.status === 401) {
      // Unauthorized - redirect to login
      router.push('/login')
      return
    }

    const data = await response.json()
    users.value = data.users || []
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

onMounted(() => {
  fetchUsers()
})

const deleteUser = async (userId) => {
  const confirmDelete = confirm("Are you sure you want to delete this user?")
  if (!confirmDelete) return

  try {
    const response = await fetch(`http://localhost:5000/users/${userId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await response.json()

    if (response.ok) {
      // Remove the deleted user from the list
      users.value = users.value.filter(user => user.id !== userId)
      alert(data.msg)
    } else {
      alert(data.msg || "Failed to delete user")
    }
  } catch (error) {
    console.error("Error deleting user:", error)
    alert("An error occurred while deleting the parking user.")
  }
}

</script>

<template>
  <div style="padding: 2rem; font-family: Arial, sans-serif;">
    <h1 style="margin-bottom: 1rem;">All Users</h1>    

    <!-- Parking User Cards -->
    <div v-if="users.length > 0">
      <div
        v-for="user in users"
        :key="user.id"
        style="background-color: #f9f9f9; border: 1px solid #ddd; padding: 1rem 1.5rem; margin-bottom: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"
      >
        <h2 style="margin: 0 0 0.5rem;">{{ user.username }}</h2>
        <p><strong>Email:</strong> {{ user.email }}</p>

        <!-- Buttons -->
        <div style="margin-top: 1rem;">
            <button @click="deleteUser(user.id)">Delete User</button>
            <router-link
              :to="{ name: 'admin_user_summary', params: { user_id: user.id } }"
              class="button-link"
            >
              View Summary
            </router-link>
          </div>
      </div>
    </div>

    <!-- No users -->
    <div v-else>
      <p>No users available.</p>
    </div>
  </div>
</template>


<!-- Replace inline button styles with this -->
<style scoped>
button {
  background-color: #ffffff;
  border: 1px solid #bbb;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #f0f0f0;
}

button,
.button-link {
  background-color: #ffffff;
  border: 1px solid #bbb;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  text-decoration: none;
  color: #333;
  margin-left: 0.5rem;
}

button:hover,
.button-link:hover {
  background-color: #f0f0f0;
}

</style>
