<template>
  <div class="air-quality-card card" :class="aqiClass">
    <h3>{{ city }}</h3>
    <div class="aqi-info">
      <div class="aqi-value">
        <span class="aqi-label">AQI:</span> {{ aqi }}
        <span class="aqi-rating">{{ aqiRating }}</span>
      </div>
      <div class="pollutants">
        <div class="pollutant">
          <span>PM2.5:</span> {{ pm2_5 }} µg/m³
        </div>
        <div class="pollutant">
          <span>PM10:</span> {{ pm10 }} µg/m³
        </div>
        <div class="pollutant">
          <span>NO2:</span> {{ no2 }} µg/m³
        </div>
        <div class="pollutant">
          <span>O3:</span> {{ o3 }} µg/m³
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  city: String,
  aqi: Number,
  pm2_5: Number,
  pm10: Number,
  no2: Number,
  o3: Number
})

const aqiClass = computed(() => {
  const aqi = props.aqi
  if (aqi <= 2) return 'aqi-good'
  if (aqi <= 3) return 'aqi-moderate'
  if (aqi <= 4) return 'aqi-poor'
  return 'aqi-very-poor'
})

const aqiRating = computed(() => {
  const aqi = props.aqi
  if (aqi <= 2) return 'Good'
  if (aqi <= 3) return 'Moderate'
  if (aqi <= 4) return 'Poor'
  return 'Very Poor'
})
</script>

<style scoped>
.air-quality-card {
  position: relative;
  background: var(--card-background);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow);
  transition: transform 0.2s;
}

.air-quality-card:hover {
  transform: translateY(-3px);
}

.aqi-info {
  margin-top: 10px;
}

.aqi-value {
  display: flex;
  align-items: center;
  font-size: 1.3em;
  font-weight: bold;
  margin: 10px 0 15px;
}

.aqi-label {
  margin-right: 5px;
}

.aqi-rating {
  margin-left: auto;
  font-size: 0.75em;
  padding: 4px 8px;
  border-radius: 12px;
  color: white;
}

.aqi-good .aqi-rating {
  background-color: #4caf50;
}

.aqi-moderate .aqi-rating {
  background-color: #ff9800;
}

.aqi-poor .aqi-rating {
  background-color: #f44336;
}

.aqi-very-poor .aqi-rating {
  background-color: #9c27b0;
}

.pollutants {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.pollutant {
  font-size: 0.9em;
  padding: 5px 0;
  border-bottom: 1px solid var(--border-color);
}

.pollutant span {
  font-weight: bold;
  color: var(--secondary-color);
}

.aqi-good { border-left: 4px solid #4caf50; }
.aqi-moderate { border-left: 4px solid #ff9800; }
.aqi-poor { border-left: 4px solid #f44336; }
.aqi-very-poor { border-left: 4px solid #9c27b0; }
</style>