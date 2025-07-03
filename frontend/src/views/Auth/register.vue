<template>
  <div class="register-container">
    <h2>Create a New Account</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="name">Name</label>
        <input
          v-model="name"
          type="text"
          id="name"
          name="name"
          required
          placeholder="Your full name"
        />
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
          v-model="email"
          type="email"
          id="email"
          name="email"
          required
          placeholder="you@example.com"
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          v-model="password"
          type="password"
          id="password"
          name="password"
          required
          placeholder="Create a password"
        />
      </div>

      <button type="submit" class="btn">Register</button>
    </form>

    <p class="login-link">
      Already have an account?
      <router-link to="/login">Click here to login</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'RegisterPage',
  data() {
    return {
      name: '',
      email: '',
      password: ''
    };
  },
  methods: {
    handleRegister() {
      // Replace with real registration logic
      console.log('Registering user:', this.name, this.email, this.password);
      // Example: this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border-radius: 8px;
  background-color: #fdfdfd;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  width: 100%;
  padding: 0.7rem;
  background-color: #008cba;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #007bb5;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>