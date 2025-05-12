<template>
  <div class="air-quality-view">
    <h1>Air Quality Data</h1>
    
    <div class="controls">
      <input 
        v-model="cityFilter"
        placeholder="Filter by city"
        class="filter-input"
      />
    </div>

    <div v-if="!loading" class="air-quality-grid">
      <AirQualityCard
        v-for="data in filteredAirQualityData"
        :key="data.city"
        v-bind="data"
      />
    </div>
    <LoadingSpinner v-else />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import AirQualityCard from '../components/AirQualityCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { weatherApi } from '../services/api'

const loading = ref(true)
const airQualityData = ref([])
const cityFilter = ref('')

// Get unique cities, keeping only the most recent data
const uniqueAirQualityData = computed(() => {
  const cityMap = new Map()
  
  // Group by city and keep most recent entry
  airQualityData.value.forEach(data => {
    cityMap.set(data.city, data)
  })
  
  return Array.from(cityMap.values())
})

// Filter cities that include the filter string (case insensitive)
const filteredAirQualityData = computed(() => {
  if (!cityFilter.value) return uniqueAirQualityData.value
  
  const filter = cityFilter.value.toLowerCase()
  return uniqueAirQualityData.value.filter(data => 
    data.city.toLowerCase().includes(filter)
  )
})

async function loadAirQualityData() {
  try {
    loading.value = true
    airQualityData.value = await weatherApi.getAirPollutionData()
  } catch (error) {
    console.error('Error loading air quality data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadAirQualityData()
})
</script>

<style scoped>
.air-quality-view {
  padding: 20px;
}

.controls {
  margin-bottom: 20px;
}

.filter-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.air-quality-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>