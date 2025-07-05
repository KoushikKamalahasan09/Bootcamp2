<script setup>
import { ref, onMounted } from 'vue'

const token = localStorage.getItem('token')
const userId = localStorage.getItem('user_id')

const admin = ref({})
const editing = ref(false)
const updatedUsername = ref('')
const updatedEmail = ref('')
const message = ref('')

const fetchProfile = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    if (res.ok) {
      admin.value = data.user
      updatedUsername.value = data.user.username
      updatedEmail.value = data.user.email
    } else {
      message.value = data.msg || 'Failed to fetch profile.'
    }
  } catch (err) {
    message.value = 'Error fetching profile.'
  }
}

const updateProfile = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        username: updatedUsername.value,
        email: updatedEmail.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      admin.value = data.user
      message.value = 'Profile updated successfully!'
      editing.value = false
    } else {
      message.value = data.msg || 'Update failed.'
    }
  } catch (err) {
    message.value = 'Error updating profile.'
  }
}

onMounted(fetchProfile)
</script>

<template>
  <div class="max-w-lg mx-auto p-6 bg-white shadow-lg rounded-lg mt-10">
    <h1 class="text-2xl font-bold mb-4 text-center">Admin Profile</h1>

    <div v-if="message" class="text-center text-red-600 mb-4">{{ message }}</div>
    <router-link to="/admin/dashboard"
      class="text-blue-600 hover:underline mb-4 inline-block">Back to Dashboard</router-link>

    <div v-if="!editing">
      <p><strong>Username:</strong> {{ admin.username }}</p>
      <p><strong>Email:</strong> {{ admin.email }}</p>
      <button @click="editing = true"
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Update Profile
      </button>
    </div>

    <div v-else>
      <label class="block mt-3 font-semibold">Username:</label>
      <input v-model="updatedUsername" class="w-full px-3 py-1 border rounded" />

      <label class="block mt-3 font-semibold">Email:</label>
      <input v-model="updatedEmail" type="email" class="w-full px-3 py-1 border rounded" />

      <div class="flex gap-3 mt-4">
        <button @click="updateProfile"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Save</button>
        <button @click="editing = false"
          class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Cancel</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Container styles */
.max-w-lg {
  max-width: 600px;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.mt-10 {
  margin-top: 2.5rem;
}

.p-6 {
  padding: 1.5rem;
}

.bg-white {
  background-color: #fff;
}

.shadow-lg {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.rounded-lg {
  border-radius: 0.5rem;
}

/* Text styles */
.text-2xl {
  font-size: 1.5rem;
}

.font-bold {
  font-weight: 700;
}

.mb-4 {
  margin-bottom: 1rem;
}

.text-center {
  text-align: center;
}

.text-red-600 {
  color: #dc2626;
}

/* Label styles */
label {
  margin-bottom: 0.5rem;
  display: block;
}

/* Input styles */
input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

/* Button styles */
button {
  cursor: pointer;
  font-weight: 600;
}

.bg-blue-600 {
  background-color: #2563eb;
}

.bg-blue-700 {
  background-color: #1d4ed8;
}

.bg-green-600 {
  background-color: #16a34a;
}

.bg-green-700 {
  background-color: #15803d;
}

.bg-gray-500 {
  background-color: #6b7280;
}

.bg-gray-600 {
  background-color: #4b5563;
}

.text-white {
  color: #fff;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.mt-4 {
  margin-top: 1rem;
}

.mt-3 {
  margin-top: 0.75rem;
}

.w-full {
  width: 100%;
}

.flex {
  display: flex;
}

.gap-3 {
  gap: 0.75rem;
}

.rounded {
  border-radius: 4px;
}

.hover\:bg-blue-700:hover {
  background-color: #1d4ed8;
}

.hover\:bg-green-700:hover {
  background-color: #15803d;
}

.hover\:bg-gray-600:hover {
  background-color: #4b5563;
}
</style>
