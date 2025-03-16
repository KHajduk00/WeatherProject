<template>
    <div class="stats-view">
      <h1>Weather Statistics</h1>
      
      <div class="controls">
        <input 
          v-model="cityFilter"
          placeholder="Filter by city"
        />
        <select v-model="selectedDays">
          <option value="7">Last 7 days</option>
          <option value="14">Last 14 days</option>
          <option value="30">Last 30 days</option>
        </select>
        <button @click="loadStats">Update</button>
      </div>
  
      <div v-if="!loading" class="stats-grid">
        <CityStats
          v-for="stat in statistics"
          :key="stat.city"
          v-bind="stat"
        />
      </div>
      <LoadingSpinner v-else />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import CityStats from '../components/CityStats.vue'
  import LoadingSpinner from '../components/LoadingSpinner.vue'
  import { weatherApi } from '../services/api'
  
  const loading = ref(true)
  const statistics = ref([])
  const cityFilter = ref('')
  const selectedDays = ref('7')
  
  async function loadStats() {
    try {
      loading.value = true
      const params = {
        days: selectedDays.value
      }
      if (cityFilter.value) {
        params.city = cityFilter.value
      }
      statistics.value = await weatherApi.getStatistics(params)
    } catch (error) {
      console.error('Error loading statistics:', error)
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    loadStats()
  })
  </script>
  
  <style scoped>
  .stats-view {
    padding: 20px;
  }
  
  .controls {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
  
  input, select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    padding: 8px 16px;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background: #3aa876;
  }
  </style>