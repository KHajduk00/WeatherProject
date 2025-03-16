import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import WeatherView from '@/views/WeatherView.vue'
import AirQualityView from '@/views/AirQualityView.vue'
import StatsView from '@/views/StatsView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/weather',
    name: 'Weather',
    component: WeatherView
  },
  {
    path: '/air-quality',
    name: 'AirQuality',
    component: AirQualityView
  },
  {
    path: '/stats',
    name: 'Stats',
    component: StatsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router