<template>
  <div class="weather-card card">
    <h3>{{ city }}</h3>
    <div class="weather-info">
      <div class="temperature">
        {{ convertedTemperature }}°C
      </div>
      <div class="description">
        {{ weatherDescription }}
      </div>
      <div class="details">
        <div class="detail-item">
          <span class="detail-label">Feels like:</span>
          <span class="detail-value">{{ convertedFeelsLike }}°C</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Humidity:</span>
          <span class="detail-value">{{ humidity }}%</span>
        </div>
        <div class="detail-item">
          <span class="detail-label">Wind:</span>
          <span class="detail-value">{{ windSpeed }} m/s</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  city: String,
  temperature: Number,
  feelsLike: Number,
  humidity: Number,
  windSpeed: Number,
  weatherDescription: String
})

// Convert Kelvin to Celsius if temperature is in Kelvin
const convertedTemperature = computed(() => {
  if (!props.temperature) return 'N/A'
  // If temperature is higher than 100, assume it's in Kelvin and convert
  return props.temperature > 100 
    ? (props.temperature - 273.15).toFixed(1) 
    : props.temperature.toFixed(1)
})

const convertedFeelsLike = computed(() => {
  if (!props.feelsLike) return 'N/A'
  // If feels_like is higher than 100, assume it's in Kelvin and convert
  return props.feelsLike > 100
    ? (props.feelsLike - 273.15).toFixed(1)
    : props.feelsLike.toFixed(1)
})
</script>

<style scoped>
.weather-card {
  background: var(--card-background);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow);
  transition: transform 0.2s;
}

.weather-card:hover {
  transform: translateY(-3px);
}

.temperature {
  font-size: 2.2em;
  font-weight: bold;
  margin: 15px 0 5px;
  color: var(--secondary-color);
}

.description {
  text-transform: capitalize;
  font-size: 1.1em;
  margin-bottom: 15px;
  font-weight: 500;
  color: var(--primary-color);
}

.details {
  background-color: rgba(66, 185, 131, 0.05);
  border-radius: var(--border-radius);
  padding: 12px;
  margin-top: 10px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-label {
  color: #666;
}

.detail-value {
  font-weight: 600;
}
</style>