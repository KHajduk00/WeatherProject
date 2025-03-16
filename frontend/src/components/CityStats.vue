<template>
    <div class="city-stats-card">
      <h3>{{ city }}</h3>
      <div class="stats-grid">
        <div class="stat">
          <span class="label">Average Temperature</span>
          <span class="value">{{ avgTemperature.toFixed(1) }}°C</span>
        </div>
        <div class="stat">
          <span class="label">Max Temperature</span>
          <span class="value">{{ maxTemperature.toFixed(1) }}°C</span>
        </div>
        <div class="stat">
          <span class="label">Min Temperature</span>
          <span class="value">{{ minTemperature.toFixed(1) }}°C</span>
        </div>
        <div class="stat">
          <span class="label">Average AQI</span>
          <span class="value">{{ avgAqi.toFixed(1) }}</span>
        </div>
      </div>
      <div class="measurements-count">
        Measurements: {{ measurementsCount }}
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    city: String,
    avgTemperature: Number,
    maxTemperature: Number,
    minTemperature: Number,
    avgAqi: Number,
    measurementsCount: Number
  })
  </script>
  
  <style scoped>
  .city-stats-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 15px 0;
  }
  
  .stat {
    display: flex;
    flex-direction: column;
  }
  
  .label {
    font-size: 0.9em;
    color: #666;
  }
  
  .value {
    font-size: 1.2em;
    font-weight: bold;
  }
  
  .measurements-count {
    font-size: 0.9em;
    color: #666;
    margin-top: 10px;
  }
  </style>