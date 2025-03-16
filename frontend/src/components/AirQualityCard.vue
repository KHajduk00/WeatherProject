<template>
    <div class="air-quality-card" :class="aqiClass">
      <h3>{{ city }}</h3>
      <div class="aqi-info">
        <div class="aqi-value">
          AQI: {{ aqi }}
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
  </script>
  
  <style scoped>
  .air-quality-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .aqi-value {
    font-size: 1.5em;
    font-weight: bold;
    margin: 10px 0;
  }
  
  .pollutants {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .pollutant {
    font-size: 0.9em;
  }
  
  .pollutant span {
    font-weight: bold;
  }
  
  .aqi-good { border-left: 4px solid #4caf50; }
  .aqi-moderate { border-left: 4px solid #ff9800; }
  .aqi-poor { border-left: 4px solid #f44336; }
  .aqi-very-poor { border-left: 4px solid #9c27b0; }
  </style>