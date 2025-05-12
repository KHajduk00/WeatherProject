<template>
  <div class="stats-view">
    <h1>Weather Statistics</h1>
    
    <div class="controls">
      <input 
        v-model="cityFilter"
        placeholder="Filter by city"
        class="filter-input"
      />
      <select v-model="selectedDays" class="days-select">
        <option value="7">Last 7 days</option>
        <option value="14">Last 14 days</option>
        <option value="30">Last 30 days</option>
      </select>
      <button @click="loadStats" class="update-btn">Update</button>
    </div>

    <div v-if="!loading" class="stats-grid">
      <CityStats
        v-for="stat in filteredStatistics"
        :key="stat.city"
        v-bind="stat"
      />
    </div>
    <LoadingSpinner v-else />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import CityStats from '../components/CityStats.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { weatherApi } from '../services/api'

const loading = ref(true)
const statistics = ref([])
const cityFilter = ref('')
const selectedDays = ref('7')

// Filter cities that include the filter string (case insensitive)
const filteredStatistics = computed(() => {
  if (!cityFilter.value) return statistics.value
  
  const filter = cityFilter.value.toLowerCase()
  return statistics.value.filter(stat => 
    stat.city.toLowerCase().includes(filter)
  )
})

async function loadStats() {
  try {
    loading.value = true
    const params = {
      days: selectedDays.value
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

.filter-input, .days-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.update-btn {
  padding: 8px 16px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.update-btn:hover {
  background: #3aa876;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>