<template>
  <div class="login-container">
    <h2>Login to Your Account</h2>


    <form @submit.prevent="handleLogin">  <!--Prevents normal action of html form action-->
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
          placeholder="Enter your password"
        />
      </div>

      <button type="submit" class="btn">Login</button>
    </form>

    <p class="register-link">
      Don't have an account?
      <router-link to="/register">Click here to register</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    handleLogin() {

      console.log('Logging in with:', this.email, this.password);
      const postData={"email": this.email, "password": this.password};
      fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)   // Convert Javascript to JSON string
      })
      .then(response=> {
        if (!response.ok) {
          if (response.status === 404) {
            alert('Account does not exist. Please register first.');

          }
          console.log(response.status);

        }
        return response.json();
      })
      .then(data => {
        console.log('Login successful:', data);
        // Redirect to dashboard page or handle successful login
        localStorage.setItem('token', data.token); // Store JWT token
        localStorage.setItem('user_id', data.user_id); // Store user ID

        if (data.isadmin){
          this.$router.push('/admin/dashboard'); // Redirect to admin dashboard
        
        } else {
          this.$router.push('/dashboard'); // Redirect to user dashboard
        
    }})
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  border-radius: 8px;
  background-color: #f9f9f9;
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
  background-color: #4caf50;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #45a049;
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>