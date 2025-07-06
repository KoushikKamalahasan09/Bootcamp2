<script setup>
import { ref, onMounted } from 'vue'

const token = localStorage.getItem('token')
const userId = localStorage.getItem('user_id')

const reservations = ref([])
const sortedAsc = ref(true)
const selectedReservation = ref(null)
const showEditModal = ref(false)

const editData = ref({
  parking_timestamp: '',
  leaving_timestamp: ''
})

// Fetch all user reservations
const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      reservations.value = data.reservations.sort((a, b) =>
        new Date(a.parking_timestamp) - new Date(b.parking_timestamp)
      )
    } else {
      alert(data.msg || 'Failed to fetch reservations')
    }
  } catch (err) {
    console.error('Error fetching reservations:', err)
  }
}

// Toggle sorting
const toggleSort = () => {
  sortedAsc.value = !sortedAsc.value
  reservations.value.reverse()
}

// Open modal to edit
const openEditModal = (r) => {
  selectedReservation.value = r
  editData.value.parking_timestamp = r.parking_timestamp.slice(0, 16)
  editData.value.leaving_timestamp = r.leaving_timestamp.slice(0, 16)
  showEditModal.value = true
}

// Check availability
const isAvailable = async (spot_id, start, end) => {
  const res = await fetch(`http://localhost:5000/spots?lot_id=${selectedReservation.value.spot_id}&start=${start}&end=${end}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  const data = await res.json()
  return data.spots?.some(s => s.id === spot_id)
}

// Submit time update
const submitEdit = async () => {
  const { parking_timestamp, leaving_timestamp } = editData.value
  if (new Date(parking_timestamp) >= new Date(leaving_timestamp)) {
    alert("Start must be before end")
    return
  }

  const available = await isAvailable(selectedReservation.value.spot_id, parking_timestamp, leaving_timestamp)
  if (!available) {
    alert("This spot is already reserved during that time.")
    return
  }

  try {
    const res = await fetch(`http://localhost:5000/reservations/${selectedReservation.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        parking_timestamp,
        leaving_timestamp
      })
    })
    const data = await res.json()
    if (res.ok) {
      alert('Updated successfully')
      showEditModal.value = false
      fetchReservations()
    } else {
      alert(data.msg || "Update failed")
    }
  } catch (err) {
    console.error(err)
    alert("Server error")
  }
}

const formatDateTime = (isoString) => {
  const date = new Date(isoString)
  const dd = String(date.getDate()).padStart(2, '0')
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const yyyy = date.getFullYear()
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  return `${dd}/${mm}/${yyyy} ${hh}:${min}`
}


// Cancel logic
const cancelReservation = async (r) => {
  const now = new Date()
  const start = new Date(r.parking_timestamp)

  if (start > now) {
    // Delete
    const res = await fetch(`http://localhost:5000/reservations/${r.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok) {
      alert("Reservation deleted")
      fetchReservations()
    } else {
      alert(data.msg || "Delete failed")
    }
  } else {
    // Soft cancel
    const nowISO = new Date().toISOString()
    const res = await fetch(`http://localhost:5000/reservations/${r.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ leaving_timestamp: nowISO })
    })
    const data = await res.json()
    if (res.ok) {
      alert("Reservation ended early")
      fetchReservations()
    } else {
      alert(data.msg || "Update failed")
    }
  }
}

onMounted(fetchReservations)
</script>

<template>
  <div class="container">
    <h1>My Reservations</h1>
    <button class="sort-btn" @click="toggleSort">
      Sort by Start Time {{ sortedAsc ? '↑' : '↓' }}
    </button>

    <div class="grid">
      <div v-for="r in reservations" :key="r.id" class="card">
        <p><strong>Spot:</strong> {{ r.spot_number || r.spot_id }}</p>
        <p><strong>From:</strong> {{ formatDateTime(r.parking_timestamp) }}</p>
        <p><strong>To:</strong> {{ formatDateTime(r.leaving_timestamp) }}</p>
        <p><strong>Cost:</strong> ₹{{ r.parking_cost }}</p>
        <div class="btn-group">
          <button class="edit" @click="openEditModal(r)">Update</button>
          <button class="cancel" @click="cancelReservation(r)">Cancel</button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-card">
        <h2>Update Reservation</h2>
        <label>Start Time:</label>
        <input type="datetime-local" v-model="editData.parking_timestamp" />
        <label>End Time:</label>
        <input type="datetime-local" v-model="editData.leaving_timestamp" />
        <div class="btn-group right">
          <button class="cancel" @click="showEditModal = false">Cancel</button>
          <button class="save" @click="submitEdit">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 2rem;
  background-color: #f8f9fa;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.sort-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  cursor: pointer;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  background-color: white;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  flex: 0 0 300px;
}

.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 0.5rem;
}

button.edit {
  background-color: #ffc107;
  color: black;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

button.cancel {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

button.save {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 400px;
}

.modal-card input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
}
</style>
