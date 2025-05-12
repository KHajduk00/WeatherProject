<template>
  <div class="home">
    <h1>Weather Data Collection System</h1>
    
    <div class="collector-section">
      <h2>Data Collector Status</h2>
      <CollectorControl />
    </div>
    
    <div class="summary-section">
      <h2>Latest Measurements</h2>
      <div class="summary-grid" v-if="!loading">
        <WeatherCard
          v-for="data in uniqueLatestWeather"
          :key="data.city"
          :city="data.city"
          :temperature="data.temperature"
          :feels-like="data.feels_like"
          :humidity="data.humidity"
          :wind-speed="data.wind_speed"
          :weather-description="data.weather_description"
        />
      </div>
      <LoadingSpinner v-else />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import CollectorControl from '@/components/CollectorControl.vue'
import WeatherCard from '@/components/WeatherCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { weatherApi } from '@/services/api'

const loading = ref(true)
const latestWeather = ref([])

// Get unique cities, keeping only the most recent data
const uniqueLatestWeather = computed(() => {
  const cityMap = new Map()
  
  // Group by city and keep most recent entry
  latestWeather.value.forEach(data => {
    cityMap.set(data.city, data)
  })
  
  return Array.from(cityMap.values())
})

async function loadLatestData() {
  try {
    loading.value = true
    latestWeather.value = await weatherApi.getWeatherData()
  } catch (error) {
    console.error('Error loading weather data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLatestData()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.collector-section {
  margin-bottom: 40px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

h1, h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}
</style>