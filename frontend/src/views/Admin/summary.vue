<script setup>
import { onMounted, ref } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const token = localStorage.getItem('token')
const reservations = ref([])
const totalRevenue = ref(0)
const totalReservations = ref(0)
const totalUsers = ref(0)
const chartInstance = ref(null)

const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    reservations.value = data.reservations || []

    calculateSummary()
    renderChart()
  } catch (err) {
    console.error("Failed to fetch reservations:", err)
  }
}

const fetchUserCount = async () => {
  try {
    const res = await fetch('http://localhost:5000/users/count', {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await res.json()
    totalUsers.value = data.total_users || 0
  } catch (err) {
    console.error("Failed to fetch user count:", err)
  }
}

const calculateSummary = () => {
  let revenue = 0
  reservations.value.forEach(r => {
    revenue += r.parking_cost || 0
  })

  totalReservations.value = reservations.value.length
  totalRevenue.value = revenue.toFixed(2)
}

const renderChart = () => {
  const ctx = document.getElementById('globalChart')
  if (chartInstance.value) chartInstance.value.destroy()

  const counts = {}

  reservations.value.forEach(r => {
    const date = new Date(r.parking_timestamp)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    counts[key] = (counts[key] || 0) + 1
  })

  const labels = Object.keys(counts).sort()
  const values = labels.map(l => counts[l])

  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Monthly Reservations',
        data: values,
        borderColor: '#007bff',
        backgroundColor: 'rgba(0,123,255,0.1)',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true },
        title: { display: true, text: 'Monthly Reservation Activity' }
      }
    }
  })
}

onMounted(() => {
  fetchReservations()
  fetchUserCount()
})
</script>

<template>
  <div class="summary-container">
    <h1>Admin Summary Dashboard</h1>

    <div class="summary-boxes">
      <div class="summary-box">
        <h3>Total Reservations</h3>
        <p>{{ totalReservations }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Users</h3>
        <p>{{ totalUsers }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Revenue</h3>
        <p>₹ {{ totalRevenue }}</p>
      </div>
    </div>

    <canvas id="globalChart"></canvas>
  </div>
</template>

<style scoped>
.summary-container {
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
  background-color: #f4f7fa;
  min-height: 100vh;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
}

.summary-boxes {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-box {
  flex: 1;
  min-width: 200px;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: center;
}

canvas {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
</style>
