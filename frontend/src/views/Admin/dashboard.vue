<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const location_name = ref('')
const price_per_hour = ref('')
const address = ref('')
const pincode = ref('')
const number_of_spots = ref('')

const handleSubmit = () => {
  const lotData = {
    location_name: location_name.value,
    price_per_hour: price_per_hour.value,
    address: address.value,
    pincode: pincode.value,
    number_of_spots: number_of_spots.value
  }

  console.log('Submitting lot data:', lotData)

  fetch('http://localhost:5000/lots', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    body: JSON.stringify(lotData)
  })
    .then(response => {
      if (!response.ok) {
        if (response.status === 403) {
          alert('You are not authorized to perform this action. Please log in as an admin.');
        } else if (response.status === 400) {
          alert('Please provide all required information!');
        } else {
          alert(`Error: ${response.status}`);
        }
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Lot registered successfully:', data);
      alert('Parking lot registered successfully!');
      // Reset form
      location_name.value = ''
      price_per_hour.value = ''
      address.value = ''
      pincode.value = ''
      number_of_spots.value = ''
    })
    .catch(error => {
      console.error('Error registering lot:', error);
    });
}
</script>

<template>
  <main class="admin-dashboard">
    <h1>🛠️ Admin Dashboard</h1>



    <section class="form-section">
      <h2>🚗 Register a Parking Lot</h2>

      <form @submit.prevent="handleSubmit" class="lot-form">
        <label>
          Location Name
          <input v-model="location_name" required type="text" placeholder="e.g. Sector 17" />
        </label>

        <label>
          Price Per Hour (₹)
          <input v-model="price_per_hour" required type="number" min="0" step="0.01" />
        </label>

        <label>
          Address
          <input v-model="address" required type="text" placeholder="Full address" />
        </label>

        <label>
          Pincode
          <input
            v-model="pincode"
            required
            type="text"
            inputmode="numeric"
            pattern="[0-9]{6}"
            placeholder="6-digit pincode"
          />
        </label>

        <label>
          Number of Spots
          <input v-model="number_of_spots" required type="number" min="1" />
        </label>

        <button type="submit">Register Lot</button>
      </form>
    </section>
  </main>
</template>

<style scoped>
.admin-dashboard {
  max-width: 700px;
  margin: auto;
  padding: 2rem;
  font-family: sans-serif;
}

.links ul {
  list-style: none;
  padding: 0;
}

.links li {
  margin-bottom: 0.5rem;
}

.form-section {
  margin-top: 2rem;
  background-color: #f4f4f4;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.lot-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

label {
  display: flex;
  flex-direction: column;
  font-weight: 500;
}

input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.7rem;
  background-color: #2c7be5;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #2566c0;
}
</style>
