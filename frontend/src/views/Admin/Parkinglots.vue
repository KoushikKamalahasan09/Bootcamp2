<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const lots = ref([])
const router = useRouter()

// JWT token stored in localStorage
const token = localStorage.getItem('token')

// Fetch all parking lots
const fetchLots = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/lots', {
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
    lots.value = data.lots || []
  } catch (error) {
    console.error('Failed to fetch lots:', error)
  }
}

onMounted(() => {
  fetchLots()
})

const deleteLot = async (lotId) => {
  const confirmDelete = confirm("Are you sure you want to delete this parking lot?")
  if (!confirmDelete) return

  try {
    const response = await fetch(`http://127.0.0.1:5000/lots/${lotId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await response.json()

    if (response.ok) {
      // Remove the deleted lot from the list
      lots.value = lots.value.filter(lot => lot.id !== lotId)
      alert(data.msg)
    } else {
      alert(data.msg || "Failed to delete lot")
    }
  } catch (error) {
    console.error("Error deleting lot:", error)
    alert("An error occurred while deleting the parking lot.")
  }
}

</script>

<template>
  <div style="padding: 2rem; font-family: Arial, sans-serif;">
    <h1 style="margin-bottom: 1rem;">All Parking Lots</h1>

    <!-- Back to Dashboard Link -->
    <router-link
      to="/admin/dashboard"
      style="display: inline-block; margin-bottom: 1.5rem; color: #007bff; text-decoration: none;"
    >
      ← Back to Dashboard
    </router-link>

    <!-- Parking Lot Cards -->
     <!--Add update and add spot-->
    <div v-if="lots.length > 0">
      <div
        v-for="lot in lots"
        :key="lot.id"
        style="background-color: #f9f9f9; border: 1px solid #ddd; padding: 1rem 1.5rem; margin-bottom: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"
      >
        <h2 style="margin: 0 0 0.5rem;">{{ lot.location_name }}</h2>
        <p><strong>Address:</strong> {{ lot.address }}</p>
        <p><strong>Pin Code:</strong> {{ lot.pin_code }}</p>
        <p><strong>Price per Hour:</strong> ₹{{ lot.price_per_hour }}</p>
        <p><strong>Total Spots:</strong> {{ lot.number_of_spots }}</p>

        <!-- Buttons -->
        <div style="margin-top: 1rem;">
            <router-link :to="`/admin/parkinglots/${lot.id}`">
                <button style="margin-right: 0.5rem;">Open Lot</button>
            </router-link>
          <button style="margin-right: 0.5rem;" @click="() => {}">Update Lot</button>
          <button style="margin-right: 0.5rem;" @click="deleteLot(lot.id)">"Delete Lot</button>
        </div>
      </div>
    </div>

    <!-- No lots -->
    <div v-else>
      <p>No parking lots available.</p>
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
</style>
