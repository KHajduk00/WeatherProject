<template>
  <div class="city-stats-card card">
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
  background: var(--card-background);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow);
  transition: transform 0.2s;
}

.city-stats-card:hover {
  transform: translateY(-3px);
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
  padding: 10px;
  background-color: rgba(66, 185, 131, 0.05);
  border-radius: var(--border-radius);
}

.label {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.value {
  font-size: 1.2em;
  font-weight: bold;
  color: var(--secondary-color);
}

.measurements-count {
  display: inline-block;
  font-size: 0.9em;
  color: #666;
  margin-top: 10px;
  background-color: #f0f0f0;
  padding: 4px 8px;
  border-radius: 12px;
}
</style>