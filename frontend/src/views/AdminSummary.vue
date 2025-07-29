<template>
  <div class="admin-summary">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/admin/dashboard" class="nav-link">Home</router-link>
        <router-link to="/admin/quiz" class="nav-link">Quiz</router-link>
        <router-link to="/admin/summary" class="nav-link active">Summary</router-link>
        <button @click="logout" class="nav-link logout-btn">Logout</button>
      </nav>
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search..." 
          class="search-input"
        />
      </div>
      <div class="welcome">Welcome Admin</div>
    </header>

    <main class="main-content">
      <h1>Summary Charts</h1>
      
      <div class="charts-container">
        <!-- Subject wise top scores -->
        <div class="chart-card">
          <h3>Subject wise top scores</h3>
          <div class="chart-container">
            <div class="bar-chart">
              <div class="bar-item">
                <div class="bar-label">Maths</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '70%' }">70</div>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Physics</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '90%' }">90</div>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Chemistry</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '80%' }">80</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Subject wise user attempts -->
        <div class="chart-card">
          <h3>Subject wise user attempts</h3>
          <div class="chart-container">
            <div class="donut-chart">
              <div class="donut">
                <div class="donut-segment segment-1" style="--percentage: 25%"></div>
                <div class="donut-segment segment-2" style="--percentage: 25%"></div>
                <div class="donut-segment segment-3" style="--percentage: 25%"></div>
                <div class="donut-segment segment-4" style="--percentage: 25%"></div>
                <div class="donut-center">
                  <span>Total</span>
                </div>
              </div>
              <div class="donut-legend">
                <div class="legend-item">
                  <span class="legend-color segment-1"></span>
                  <span>01 - Maths</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color segment-2"></span>
                  <span>02 - Physics</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color segment-3"></span>
                  <span>03 - Chemistry</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color segment-4"></span>
                  <span>04 - Biology</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'AdminSummary',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    return {
      searchQuery,
      logout
    }
  }
}
</script>

<style scoped>
.admin-summary {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #666;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.active {
  background-color: #667eea;
  color: white;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.search-container {
  flex: 1;
  max-width: 300px;
  margin: 0 2rem;
}

.search-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.welcome {
  font-weight: bold;
  color: #333;
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.main-content h1 {
  color: #333;
  margin-bottom: 2rem;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.chart-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

/* Bar Chart Styles */
.bar-chart {
  width: 100%;
  max-width: 400px;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.bar-label {
  width: 80px;
  font-weight: 600;
  color: #333;
}

.bar-wrapper {
  flex: 1;
  height: 30px;
  background-color: #f0f0f0;
  border-radius: 15px;
  overflow: hidden;
  margin-left: 1rem;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
  transition: width 0.5s ease;
}

/* Donut Chart Styles */
.donut-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.donut {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    #667eea 0deg 90deg,
    #28a745 90deg 180deg,
    #ffc107 180deg 270deg,
    #dc3545 270deg 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut-center {
  width: 120px;
  height: 120px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #333;
}

.donut-legend {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
}

.legend-color.segment-1 {
  background-color: #667eea;
}

.legend-color.segment-2 {
  background-color: #28a745;
}

.legend-color.segment-3 {
  background-color: #ffc107;
}

.legend-color.segment-4 {
  background-color: #dc3545;
}

/* Responsive Design */
@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    padding: 1rem;
  }
  
  .donut {
    width: 150px;
    height: 150px;
  }
  
  .donut-center {
    width: 90px;
    height: 90px;
  }
  
  .donut-legend {
    grid-template-columns: 1fr;
  }
}
</style> 