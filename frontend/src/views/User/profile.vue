<!-- src/views/admin/Profile.vue -->
<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <h1>👤 Profile</h1>

    <section>
        <div>
      <p>This is your profile page. Here you can view and edit your admin details.</p>

      <p>
        🔙 <RouterLink to="/dashboard">Return to Dashboard</RouterLink>
      </p>
      </div>
    </section>
  </main>
</template>
