<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const lotId = route.params.lot_id
const spots = ref([])
const token = localStorage.getItem('token')

// Modal state
const showEditModal = ref(false)

// Edit form
const editSpotData = ref({
  id: null,
  spot_number: ''
})

// Fetch spots for a specific lot
const fetchSpots = async () => {
  try {
    const res = await fetch(`http://localhost:5000/spots?lot_id=${lotId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    spots.value = data.spots || []
  } catch (err) {
    console.error("Failed to fetch spots:", err)
  }
}

onMounted(fetchSpots)

// Open Edit modal
const openEditModal = (spot) => {
  editSpotData.value = { ...spot }
  showEditModal.value = true
}

// Submit spot update
const submitEdit = async () => {
  try {
    const res = await fetch(`http://localhost:5000/spots/${editSpotData.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        spot_number: editSpotData.value.spot_number
      })
    })

    const data = await res.json()
    if (res.ok) {
      alert("Spot updated successfully")
      showEditModal.value = false
      fetchSpots()
    } else {
      alert(data.msg || "Update failed")
    }
  } catch (err) {
    console.error(err)
    alert("Error updating spot")
  }
}

// Delete spot
const deleteSpot = async (spotId) => {
  if (!confirm("Are you sure you want to delete this spot?")) return

  try {
    const res = await fetch(`http://localhost:5000/spots/${spotId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      spots.value = spots.value.filter(s => s.id !== spotId)
    } else {
      alert(data.msg || "Failed to delete")
    }
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div class="container">
    <router-link to="/admin/parkinglots" class="back-link">← Back to Parking Lots</router-link>

    <h1>Parking Spots for Lot {{ lotId }}</h1>

    <div class="grid">
      <div v-for="spot in spots" :key="spot.id" class="card">
        <p><strong>Spot Number:</strong> {{ spot.spot_number }}</p>
        <div class="btn-group">
          <button class="edit" @click="() => openEditModal(spot)">Update</button>
          <button class="delete" @click="() => deleteSpot(spot.id)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-card">
        <h2>Update Spot</h2>
        <label>Spot Number:</label>
        <input v-model="editSpotData.spot_number" type="text" />
        <div class="btn-group right">
          <button @click="showEditModal = false" class="cancel">Cancel</button>
          <button @click="submitEdit" class="save">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Same styles as before — just removed .add-btn and modal-card for Add */
.container {
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f8f9fa;
  min-height: 100vh;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #343a40;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.card {
  background-color: white;
  padding: 1.2rem;
  border-radius: 10px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
  flex: 0 0 300px;
}

.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

.btn-group.right {
  justify-content: flex-end;
}

button.edit {
  background-color: #007bff;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button.edit:hover {
  background-color: #0069d9;
}

button.delete {
  background-color: #dc3545;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button.delete:hover {
  background-color: #c82333;
}

button.cancel {
  background-color: #6c757d;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button.save {
  background-color: #28a745;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button.save:hover {
  background-color: #218838;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-card {
  background-color: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

.modal-card h2 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.modal-card input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #0056b3;
  text-decoration: underline;
}
</style>
