const API_BASE_URL = 'http://localhost:8000/api/v1'

export const weatherApi = {
  async getWeatherData(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_BASE_URL}/weather?${queryString}`)
    return response.json()
  },

  async getAirPollutionData(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_BASE_URL}/air-pollution?${queryString}`)
    return response.json()
  },

  async getStatistics(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`${API_BASE_URL}/statistics?${queryString}`)
    return response.json()
  },

  async startCollector() {
    const response = await fetch(`${API_BASE_URL}/collector/start`, {
      method: 'POST'
    })
    return response.json()
  },

  async stopCollector() {
    const response = await fetch(`${API_BASE_URL}/collector/stop`, {
      method: 'POST'
    })
    return response.json()
  },

  async getCollectorStatus() {
    const response = await fetch(`${API_BASE_URL}/collector/status`)
    return response.json()
  }
}