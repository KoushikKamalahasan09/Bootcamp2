<template>
  <div class="register-container">
    <h2>Create a New Account</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="name">Username</label>
        <input
          v-model="username"
          type="text"
          id="Username"
          name="Username"
          required
          placeholder="Your username"
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
      username: '',
      email: '',
      password: ''
    };
  },
  methods: {
    handleRegister() {
      // Replace with real registration logic
      console.log('Registering user:', this.username, this.email, this.password);
      
      const postData={"email": this.email,"username":this.username, "password": this.password};
      fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)   // Convert Javascript to JSON string
      })
      .then(response=> {
        if (!response.ok) {
          if (response.status === 409) {
            alert('Account already exists. Please login.');

          }
          if (response.status === 400) {
            alert('Please provide all required information.');
          }
          console.log(response.status);

        }
        alert('Registration successful! You can now login.');
        return response.json();

      })
      .then(data => {
        console.log(data);
        // Redirect to dashboard page or handle successful login
        
      })

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