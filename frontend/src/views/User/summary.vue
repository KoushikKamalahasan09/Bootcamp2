<script setup>
import { onMounted, ref } from 'vue'
import { Chart, registerables } from 'chart.js'

// Register Chart.js components
Chart.register(...registerables)

const token = localStorage.getItem('token')
const reservations = ref([])
const totalHours = ref(0)
const totalAmount = ref(0)
const chartInstance = ref(null)

const fetchReservations = async () => {
  try {
    const res = await fetch('http://localhost:5000/reservations', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    reservations.value = data.reservations || []

    calculateStats()
    renderChart()
  } catch (err) {
    console.error("Failed to fetch reservations:", err)
  }
}

const calculateStats = () => {
  let hours = 0
  let amount = 0

  reservations.value.forEach(r => {
    const start = new Date(r.parking_timestamp)
    const end = new Date(r.leaving_timestamp)
    const diff = (end - start) / (1000 * 60 * 60)
    hours += diff
    amount += r.parking_cost || 0
  })

  totalHours.value = hours.toFixed(2)
  totalAmount.value = amount.toFixed(2)
}

const renderChart = () => {
  const ctx = document.getElementById('reservationChart')
  if (chartInstance.value) chartInstance.value.destroy()

  const counts = {} // key: "YYYY-MM", value: count

  reservations.value.forEach(r => {
    const date = new Date(r.parking_timestamp)
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
    counts[key] = (counts[key] || 0) + 1
  })

  const labels = Object.keys(counts).sort()
  const values = labels.map(label => counts[label])

  chartInstance.value = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Reservations per Month',
        data: values,
        backgroundColor: '#007bff'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Monthly Reservation Activity'
        }
      }
    }
  })
}

onMounted(fetchReservations)
</script>

<template>
  <div class="summary-container">
    <h1>User Summary</h1>

    <div class="summary-boxes">
      <div class="summary-box">
        <h3>Total Reservations</h3>
        <p>{{ reservations.length }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Hours Parked</h3>
        <p>{{ totalHours }}</p>
      </div>
      <div class="summary-box">
        <h3>Total Amount Spent</h3>
        <p>₹ {{ totalAmount }}</p>
      </div>
    </div>

    <canvas id="reservationChart"></canvas>
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
  font-size: 2rem;
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
