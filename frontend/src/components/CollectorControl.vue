<template>
    <div class="collector-control">
      <div class="status-info">
        <div class="status" :class="{ 'active': isRunning }">
          Status: {{ isRunning ? 'Running' : 'Stopped' }}
        </div>
        <div class="last-collection" v-if="lastCollection">
          Last Collection: {{ formatDate(lastCollection) }}
        </div>
      </div>
      
      <div class="controls">
        <button 
          @click="startCollector" 
          :disabled="isRunning"
          class="start-btn"
        >
          Start Collector
        </button>
        <button 
          @click="stopCollector" 
          :disabled="!isRunning"
          class="stop-btn"
        >
          Stop Collector
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { weatherApi } from '../services/api'
  
  const isRunning = ref(false)
  const lastCollection = ref(null)
  
  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString()
  }
  
  async function updateStatus() {
    try {
      const status = await weatherApi.getCollectorStatus()
      isRunning.value = status.running
      lastCollection.value = status.last_collection
    } catch (error) {
      console.error('Error fetching collector status:', error)
    }
  }
  
  async function startCollector() {
    try {
      await weatherApi.startCollector()
      await updateStatus()
    } catch (error) {
      console.error('Error starting collector:', error)
    }
  }
  
  async function stopCollector() {
    try {
      await weatherApi.stopCollector()
      await updateStatus()
    } catch (error) {
      console.error('Error stopping collector:', error)
    }
  }
  
  onMounted(() => {
    updateStatus()
    // Update status every 30 seconds
    setInterval(updateStatus, 30000)
  })
  </script>
  
  <style scoped>
  .collector-control {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .status-info {
    margin-bottom: 20px;
  }
  
  .status {
    font-size: 1.2em;
    font-weight: bold;
    color: #f44336;
  }
  
  .status.active {
    color: #4caf50;
  }
  
  .last-collection {
    font-size: 0.9em;
    color: #666;
    margin-top: 5px;
  }
  
  .controls {
    display: flex;
    gap: 10px;
  }
  
  button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
  }
  
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .start-btn {
    background: #4caf50;
    color: white;
  }
  
  .stop-btn {
    background: #f44336;
    color: white;
  }
  </style>