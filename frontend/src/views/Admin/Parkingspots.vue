<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const lotId = route.params.lot_id
const spots = ref([])
const token = localStorage.getItem('token')

// Fetch spots for a given lot_id
const fetchSpots = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/spots?lot_id=${lotId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    spots.value = data.spots || []
  } catch (err) {
    console.error("Failed to fetch spots:", err)
  }
}

// Delete a spot
const deleteSpot = async (spotId) => {
  if (!confirm("Are you sure you want to delete this spot?")) return

  try {
    const res = await fetch(`http://127.0.0.1:5000/spots/${spotId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
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

onMounted(fetchSpots)
</script>
<!--Add update and add spot-->
<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Parking Spots for Lot {{ lotId }}</h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div v-for="spot in spots" :key="spot.id" class="border rounded-lg p-4 shadow bg-white dark:bg-gray-800">
        <p><strong>ID:</strong> {{ spot.id }}</p>
        <p><strong>Spot Number:</strong> {{ spot.spot_number }}</p>
        <p><strong>Available:</strong> {{ spot.is_avail ? 'Yes' : 'No' }}</p>
        <div class="mt-2 flex gap-2">
          <button class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">Update</button>
          <button @click="deleteSpot(spot.id)" class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>
