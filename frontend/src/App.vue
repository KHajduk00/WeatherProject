<template>
  <div class="app">
    <nav class="nav">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/weather" class="nav-link">Weather</router-link>
      <router-link to="/air-quality" class="nav-link">Air Quality</router-link>
      <router-link to="/stats" class="nav-link">Statistics</router-link>
    </nav>
    
    <main class="main">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
.app {
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
}

.nav {
  background-color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.nav-link {
  color: var(--secondary-color);
  text-decoration: none;
  margin: 0 15px;
  padding: 5px 10px;
  font-weight: bold;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: var(--primary-color);
}

.router-link-active {
  color: var(--primary-color);
  background-color: rgba(66, 185, 131, 0.1);
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 40px;
}
</style>