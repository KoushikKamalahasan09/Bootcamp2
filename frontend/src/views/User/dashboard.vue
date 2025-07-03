<!-- src/views/admin/Dashboard.vue -->
<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <h1>🛠️ Dashboard</h1>

    <section>
      <p>Welcome, User! Use the links below to manage your account.</p>

      <ul>
        <li>
          👉 <RouterLink to="/profile">View Profile</RouterLink>
        </li>
        <!-- Add more links as needed -->
      </ul>
    </section>
  </main>
</template>
