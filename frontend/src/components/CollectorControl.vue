<template>
  <div class="collector-control card">
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
        class="control-btn start-btn"
      >
        Start Collector
      </button>
      <button 
        @click="stopCollector" 
        :disabled="!isRunning"
        class="control-btn stop-btn"
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
  background: var(--card-background);
  border-radius: var(--border-radius);
  padding: 20px;
  box-shadow: var(--shadow);
}

.status-info {
  margin-bottom: 20px;
}

.status {
  font-size: 1.2em;
  font-weight: bold;
  color: #f44336;
  display: flex;
  align-items: center;
}

.status::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  background-color: #f44336;
  border-radius: 50%;
  margin-right: 8px;
}

.status.active {
  color: var(--primary-color);
}

.status.active::before {
  background-color: var(--primary-color);
}

.last-collection {
  font-size: 0.9em;
  color: #666;
  margin-top: 8px;
}

.controls {
  display: flex;
  gap: 10px;
}

.control-btn {
  padding: 10px 20px;
  border: none;
  border-radius: var(--border-radius);
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.3s, background-color 0.3s;
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.start-btn {
  background: var(--primary-color);
  color: white;
}

.start-btn:hover:not(:disabled) {
  background: var(--primary-hover);
}

.stop-btn {
  background: #f44336;
  color: white;
}

.stop-btn:hover:not(:disabled) {
  background: #d32f2f;
}
</style>