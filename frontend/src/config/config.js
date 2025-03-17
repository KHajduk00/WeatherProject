const config = {
    development: {
      API_BASE_URL: 'http://localhost:8000/api/v1'
    },
    production: {
      API_BASE_URL: 'http://192.168.0.104:8000/api/v1'
    }
  }
  
  const environment = import.meta.env.MODE || 'development'
  export const currentConfig = config[environment]