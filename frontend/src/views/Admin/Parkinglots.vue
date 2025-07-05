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
    const response = await fetch('http://localhost:5000/lots', {
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

// Delete parking lot
const deleteLot = async (lotId) => {
  const confirmDelete = confirm("Are you sure you want to delete this parking lot?")
  if (!confirmDelete) return

  try {
    const response = await fetch(`http://localhost:5000/lots/${lotId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const data = await response.json()

    if (response.ok) {
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

// State for editing
const showEditModal = ref(false)
const editLotData = ref({
  id: null,
  location_name: '',
  price_per_hour: '',
  address: '',
  pin_code: '',
  number_of_spots: ''
})

const openEditModal = (lot) => {
  editLotData.value = { ...lot }
  showEditModal.value = true
}

const submitEdit = async () => {
  try {
    const response = await fetch(`http://localhost:5000/lots/${editLotData.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        location_name: editLotData.value.location_name,
        price_per_hour: editLotData.value.price_per_hour,
        address: editLotData.value.address,
        pin_code: editLotData.value.pin_code,
        number_of_spots: editLotData.value.number_of_spots
      })
    })

    const data = await response.json()

    if (response.ok) {
      alert('Parking lot updated successfully!')
      showEditModal.value = false
      fetchLots()
    } else {
      alert(data.msg || 'Failed to update parking lot')
    }
  } catch (error) {
    console.error('Update error:', error)
    alert('An error occurred while updating.')
  }
}
</script>

<template>
  <div style="padding: 2rem; font-family: Arial, sans-serif;">
    <h1 style="margin-bottom: 1rem;">All Parking Lots</h1>

    <router-link
      to="/admin/dashboard"
      style="display: inline-block; margin-bottom: 1.5rem; color: #007bff; text-decoration: none;"
    >
      ← Back to Dashboard
    </router-link>

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

        <div style="margin-top: 1rem;">
          <router-link :to="`/admin/parkinglots/${lot.id}`">
            <button style="margin-right: 0.5rem;">Open Lot</button>
          </router-link>
          <button style="margin-right: 0.5rem;" @click="() => openEditModal(lot)">Update Lot</button>
          <button style="margin-right: 0.5rem;" @click="() => deleteLot(lot.id)">Delete Lot</button>
        </div>
      </div>
    </div>

    <div v-else>
      <p>No parking lots available.</p>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
         background: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 1000;">
      <div style="background: white; padding: 2rem; border-radius: 10px; width: 90%; max-width: 500px;">
        <h2>Edit Parking Lot</h2>
        <form @submit.prevent="submitEdit">
          <div style="margin-bottom: 1rem;">
            <label>Location Name:</label>
            <input v-model="editLotData.location_name" type="text" required />
          </div>
          <div style="margin-bottom: 1rem;">
            <label>Address:</label>
            <input v-model="editLotData.address" type="text" required />
          </div>
          <div style="margin-bottom: 1rem;">
            <label>Pin Code:</label>
            <input v-model="editLotData.pin_code" type="text" required />
          </div>
          <div style="margin-bottom: 1rem;">
            <label>Price Per Hour:</label>
            <input v-model.number="editLotData.price_per_hour" type="number" step="0.01" required />
          </div>
          <div style="margin-bottom: 1rem;">
            <label>Total Spots:</label>
            <input v-model.number="editLotData.number_of_spots" type="number" required />
          </div>
          <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
            <button type="button" @click="showEditModal = false">Cancel</button>
            <button type="submit">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

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

input {
  width: 100%;
  padding: 6px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 4px;
}
</style>
