<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const lotId = route.params.lot_id
const token = localStorage.getItem('token')

const spots = ref([])
const showModal = ref(false)
const selectedSpot = ref(null)

const reservationData = ref({
  parking_timestamp: '',
  leaving_timestamp: ''
})

// Fetch spots
const fetchSpots = async () => {
  try {
    const res = await fetch(`http://localhost:5000/spots?lot_id=${lotId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    spots.value = data.spots || []
  } catch (err) {
    console.error("Error fetching spots:", err)
  }
}

// Open modal
const openModal = (spot) => {
  selectedSpot.value = spot
  reservationData.value = {
    parking_timestamp: '',
    leaving_timestamp: ''
  }
  showModal.value = true
}

const isSpotAvailable = async () => {
  try {
    const { parking_timestamp, leaving_timestamp } = reservationData.value

    const res = await fetch(`http://localhost:5000/spots?lot_id=${lotId}&start=${parking_timestamp}&end=${leaving_timestamp}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    const data = await res.json()
    const availableIds = data.spots?.map(s => s.id) || []
    return availableIds.includes(selectedSpot.value.id)
  } catch (err) {
    console.error("Availability check failed:", err)
    return false
  }
}


// Submit reservation
const submitReservation = async () => {
  const available = await isSpotAvailable()
  if (!available) {
    alert("This spot is no longer available in the selected time range.")
    return
  }

  try {
    const res = await fetch('http://localhost:5000/reservations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        spot_id: selectedSpot.value.id,
        parking_timestamp: reservationData.value.parking_timestamp,
        leaving_timestamp: reservationData.value.leaving_timestamp
      })
    })

    const data = await res.json()
    if (res.ok) {
      alert('Reservation created successfully!')
      showModal.value = false
    } else {
      alert(data.msg || 'Reservation failed')
    }
  } catch (err) {
    console.error('Reservation error:', err)
    alert('Server error')
  }
}

onMounted(fetchSpots)
</script>

<template>
  <div class="container">
    <router-link to="/dashboard" class="back-link">← Back to Dashboard</router-link>
    <h1>Reserve a Spot (Lot {{ lotId }})</h1>

    <div class="grid">
      <div v-for="spot in spots" :key="spot.id" class="card">
        <p><strong>Spot Number:</strong> {{ spot.spot_number }}</p>
        <button @click="() => openModal(spot)" class="reserve-btn">Reserve</button>
      </div>
    </div>

    <!-- Reservation Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-card">
        <h2>Reserve Spot {{ selectedSpot?.spot_number }}</h2>
        <label>Start Time:</label>
        <input type="datetime-local" v-model="reservationData.parking_timestamp" />
        <label>End Time:</label>
        <input type="datetime-local" v-model="reservationData.leaving_timestamp" />

        <div class="btn-group right">
          <button class="cancel" @click="showModal = false">Cancel</button>
          <button class="save" @click="submitReservation">Reserve</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
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

.reserve-btn {
  background-color: #28a745;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.reserve-btn:hover {
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

.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

.btn-group.right {
  justify-content: flex-end;
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
  background-color: #007bff;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #007bff;
  font-weight: bold;
  text-decoration: none;
}

.back-link:hover {
  color: #0056b3;
  text-decoration: underline;
}
</style>
