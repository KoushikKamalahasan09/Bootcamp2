<template>
  <div class="home-container">
    <div class="hero">
      <h1>Welcome to ParkEasy</h1>
      <p class="tagline">Find, reserve, and manage your parking spots with ease.</p>

      <div class="auth-buttons">
        <router-link to="/login" class="btn login-btn">Login</router-link>
        <router-link to="/register" class="btn register-btn">Register</router-link>
      </div>
    </div>

    <div class="info-section">
      <h2>Why ParkEasy?</h2>
      <ul>
        <li>🅿️ Easily locate available parking spots near you.</li>
        <li>🕒 Reserve spots ahead of time and avoid the hassle.</li>
        <li>📱 Manage your bookings and view parking history.</li>
        <li>🔐 Secure and reliable service for your vehicle.</li>
      </ul>

      <p class="note">You need to <strong>log in or create an account</strong> to access all features like booking and tracking.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
};
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: auto;
  padding: 2rem;
  text-align: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.hero {
  background-color: #e6f7ff;
  padding: 2rem;
  border-radius: 10px;
}

.tagline {
  font-size: 1.2rem;
  margin-top: 1rem;
  color: #555;
}

.auth-buttons {
  margin-top: 2rem;
}

.btn {
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  margin: 0 1rem;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.3s;
}

.login-btn {
  background-color: #28a745;
  color: white;
}

.login-btn:hover {
  background-color: #218838;
}

.register-btn {
  background-color: #007bff;
  color: white;
}

.register-btn:hover {
  background-color: #0056b3;
}

.info-section {
  margin-top: 3rem;
  text-align: left;
}

.info-section h2 {
  margin-bottom: 1rem;
}

.info-section ul {
  list-style: none;
  padding-left: 0;
}

.info-section li {
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.note {
  margin-top: 1.5rem;
  font-style: italic;
  color: #888;
}
</style>
