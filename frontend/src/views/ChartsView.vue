<template>
  <div class="charts-view">
    <h1>Weather Charts & Analytics</h1>
    
    <div class="chart-controls">
      <select v-model="selectedChart" class="chart-selector">
        <option value="temperature">Q1.Smart Alert Triggering</option>
        <option value="humidity">Q2.Weather-Pollution Link </option>
        <option value="wind">Q3.AQI Forecasting Model</option>
   
      </select>
    </div>

    <div class="charts-container">
      <!-- Question text that changes based on selection -->
      <div class="question-text">
        <h2>{{ getQuestionText() }}</h2>
      </div>
    
      <div v-if="!loading" class="chart-grid">
        <!-- Placeholder for your charts -->
        <div class="chart-placeholder">
          <h3>{{ getChartTitle() }}</h3>
          <p>Chart will be rendered here</p>
          <p>Selected: {{ selectedChart }} | Time Range: {{ timeRange }}</p>
        </div>
        
        <!-- You can add more chart containers here -->
        <div class="chart-placeholder">
          <h3>Weather Summary</h3>
          <p>Summary statistics chart</p>
        </div>
      </div>
      <LoadingSpinner v-else />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { weatherApi } from '../services/api'

const selectedChart = ref('temperature')
const timeRange = ref('24h')
const loading = ref(false)
const chartData = ref([])

function getChartTitle() {
  const titles = {
    temperature: 'Weather-Driven Alerts',
    humidity: 'Humidity Analysis',
    wind: 'Wind Speed Analysis',
    comparison: 'City Comparison'
  }
  return titles[selectedChart.value] || 'Chart'
}

function getQuestionText() {
  const questions = {
    temperature: 'How can real-time weather and air quality data from OpenWeather be used to trigger smart alerts or health advisories in cities experiencing high pollution under specific weather conditions?',
    humidity: 'What weather conditions (e.g., high humidity and low wind) are most associated with elevated PM2.5 or NO₂ levels, and how can this information support dynamic environmental regulations?',
    wind: 'Can patterns in weather and pollution data from OpenWeather be used to build a simple predictive model to forecast AQI levels 12–24 hours ahead?'
  }
  return questions[selectedChart.value] || 'Select a question'
}

async function loadChartData() {
  try {
    loading.value = true
    // You can modify this to load specific data for charts
    chartData.value = await weatherApi.getWeatherData()
  } catch (error) {
    console.error('Error loading chart data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadChartData()
})
</script>

<style scoped>
.charts-view {
  padding: 20px;
}

.chart-controls {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  flex-wrap: wrap;
}

.chart-selector,
.time-selector {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-size: 14px;
}

.charts-container {
  min-height: 400px;
}

.question-text {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: var(--card-background, #f8f9fa);
  border-radius: var(--border-radius, 8px);
  border: 2px solid var(--primary-color, #42b983);
}

.question-text h2 {
  margin: 0;
  color: var(--primary-color, #42b983);
  font-size: 24px;
  font-weight: 600;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 30px;
}

.chart-placeholder {
  background: var(--card-background, white);
  border-radius: var(--border-radius, 8px);
  padding: 30px;
  box-shadow: var(--shadow, 0 2px 8px rgba(0,0,0,0.1));
  text-align: center;
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border: 2px dashed #e0e0e0;
}

.chart-placeholder h3 {
  margin-bottom: 15px;
  color: var(--primary-color, #42b983);
}

.chart-placeholder p {
  color: #666;
  margin: 5px 0;
}
</style>