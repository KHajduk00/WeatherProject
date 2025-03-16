<template>
    <div class="weather-view">
      <h1>Weather Data</h1>
      
      <div class="controls">
        <input 
          v-model="cityFilter"
          placeholder="Filter by city"
          @input="loadWeatherData"
        />
      </div>
  
      <div class="weather-grid">
        <WeatherCard
          v-for="data in weatherData"
          :key="data.city"
          :city="data.city"
          :temperature="data.temperature"
          :feels-like="data.feels_like"
          :humidity="data.humidity"
          :wind-speed="data.wind_speed"
          :weather-description="data.weather_description"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import WeatherCard from '../components/WeatherCard.vue'
  import { weatherApi } from '../services/api'
  
  const weatherData = ref([])
  const cityFilter = ref('')
  
  async function loadWeatherData() {
    try {
      const params = {}
      if (cityFilter.value) {
        params.city = cityFilter.value
      }
      weatherData.value = await weatherApi.getWeatherData(params)
    } catch (error) {
      console.error('Error loading weather data:', error)
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
  
  .weather-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  </style>