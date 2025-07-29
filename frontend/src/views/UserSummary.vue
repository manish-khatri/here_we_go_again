<template>
  <div class="user-summary">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/user/dashboard" class="nav-link">Home</router-link>
        <router-link to="/user/scores" class="nav-link">Scores</router-link>
        <router-link to="/user/summary" class="nav-link active">Summary</router-link>
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
      <div class="welcome">Welcome User</div>
    </header>

    <main class="main-content">
      <h1>Summary Charts</h1>
      
      <div class="charts-container">
        <!-- Subject wise no. of quizzes -->
        <div class="chart-card">
          <h3>Subject wise no. of quizzes</h3>
          <div class="chart-container">
            <div class="bar-chart">
              <div class="bar-item">
                <div class="bar-label">Maths</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '60%' }">6</div>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Physics</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '80%' }">8</div>
                </div>
              </div>
              <div class="bar-item">
                <div class="bar-label">Chemistry</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: '40%' }">4</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Month wise no. of quizzes attempted -->
        <div class="chart-card">
          <h3>Month wise no. of quizzes attempted</h3>
          <div class="chart-container">
            <div class="pie-chart">
              <div class="pie">
                <div class="pie-segment segment-1" style="--percentage: 40%"></div>
                <div class="pie-segment segment-2" style="--percentage: 35%"></div>
                <div class="pie-segment segment-3" style="--percentage: 25%"></div>
              </div>
              <div class="pie-legend">
                <div class="legend-item">
                  <span class="legend-color segment-1"></span>
                  <span>01 - January</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color segment-2"></span>
                  <span>02 - February</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color segment-3"></span>
                  <span>03 - March</span>
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
  name: 'UserSummary',
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
.user-summary {
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

/* Pie Chart Styles */
.pie-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.pie {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(
    #667eea 0deg 144deg,
    #28a745 144deg 252deg,
    #ffc107 252deg 360deg
  );
}

.pie-legend {
  display: flex;
  flex-direction: column;
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

/* Responsive Design */
@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    padding: 1rem;
  }
  
  .pie {
    width: 150px;
    height: 150px;
  }
  
  .pie-legend {
    grid-template-columns: 1fr;
  }
}
</style> 