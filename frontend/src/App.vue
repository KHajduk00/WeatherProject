<template>
  <div class="app">
    <nav class="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/weather">Weather</router-link> |
      <router-link to="/air-quality">Air Quality</router-link> |
      <router-link to="/stats">Statistics</router-link>
    </nav>
    
    <main class="main">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
.app {
  min-height: 100vh;
  padding: 20px;
}

.nav {
  padding: 20px;
  text-align: center;
}

.nav a {
  color: #2c3e50;
  text-decoration: none;
  margin: 0 10px;
}

.nav a.router-link-active {
  color: #42b983;
}

.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>