<template>
  <div class="weather-view">
    <h1>Weather Data</h1>
    
    <div class="controls">
      <input 
        v-model="cityFilter"
        placeholder="Filter by city"
        @input="loadWeatherData"
        class="filter-input"
      />
    </div>

    <div v-if="!loading" class="weather-grid">
      <WeatherCard
        v-for="data in filteredWeatherData"
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
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import WeatherCard from '../components/WeatherCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { weatherApi } from '../services/api'

const weatherData = ref([])
const cityFilter = ref('')
const loading = ref(true)

// This will group by city and only keep the most recent entry
const uniqueWeatherData = computed(() => {
  const cityMap = new Map()
  
  // Group by city and keep most recent entry (assuming data is sorted)
  weatherData.value.forEach(data => {
    cityMap.set(data.city, data)
  })
  
  return Array.from(cityMap.values())
})

// Filter cities that include the filter string (case insensitive)
const filteredWeatherData = computed(() => {
  if (!cityFilter.value) return uniqueWeatherData.value
  
  const filter = cityFilter.value.toLowerCase()
  return uniqueWeatherData.value.filter(data => 
    data.city.toLowerCase().includes(filter)
  )
})

async function loadWeatherData() {
  try {
    loading.value = true
    weatherData.value = await weatherApi.getWeatherData()
  } catch (error) {
    console.error('Error loading weather data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadWeatherData()
})
</script>

<style scoped>
.weather-view {
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

.weather-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>