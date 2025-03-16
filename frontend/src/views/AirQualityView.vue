<template>
    <div class="air-quality-view">
      <h1>Air Quality Data</h1>
      
      <div class="controls">
        <input 
          v-model="cityFilter"
          placeholder="Filter by city"
          @input="loadAirQualityData"
        />
      </div>
  
      <div v-if="!loading" class="air-quality-grid">
        <AirQualityCard
          v-for="data in airQualityData"
          :key="data.city"
          v-bind="data"
        />
      </div>
      <LoadingSpinner v-else />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import AirQualityCard from '../components/AirQualityCard.vue'
  import LoadingSpinner from '../components/LoadingSpinner.vue'
  import { weatherApi } from '../services/api'
  
  const loading = ref(true)
  const airQualityData = ref([])
  const cityFilter = ref('')
  
  async function loadAirQualityData() {
    try {
      loading.value = true
      const params = cityFilter.value ? { city: cityFilter.value } : {}
      airQualityData.value = await weatherApi.getAirPollutionData(params)
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
  
  .air-quality-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  input {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 200px;
  }
  </style>