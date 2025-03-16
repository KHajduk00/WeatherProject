<template>
    <div class="weather-card">
      <h3>{{ city }}</h3>
      <div class="weather-info">
        <div class="temperature">
          {{ temperature }}°C
        </div>
        <div class="details">
          <p>Feels like: {{ feelsLike }}°C</p>
          <p>Humidity: {{ humidity }}%</p>
          <p>Wind: {{ windSpeed }} m/s</p>
        </div>
        <div class="description">
          {{ weatherDescription }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    city: String,
    temperature: Number,
    feelsLike: Number,
    humidity: Number,
    windSpeed: Number,
    weatherDescription: String
  })
  </script>
  
  <style scoped>
  .weather-card {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .temperature {
    font-size: 2em;
    font-weight: bold;
  }
  
  .details {
    margin: 10px 0;
  }
  
  .description {
    text-transform: capitalize;
  }
  </style>