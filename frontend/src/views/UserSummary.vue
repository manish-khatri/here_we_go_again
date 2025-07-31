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
      
      <!-- Loading state -->
      <div v-if="loading" class="loading">
        Loading summary data...
      </div>
      
      <!-- Error state -->
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <!-- Content -->
      <div v-else class="charts-container">
        <!-- Overall Statistics -->
        <div class="stats-overview">
          <div class="stat-card">
            <h3>Total Attempts</h3>
            <div class="stat-number">{{ summaryData.total_attempts || 0 }}</div>
          </div>
          <div class="stat-card">
            <h3>Average Score</h3>
            <div class="stat-number">{{ summaryData.average_score || 0 }}%</div>
          </div>
        </div>

        <!-- Subject wise no. of quizzes -->
        <div class="chart-card">
          <h3>Subject wise no. of quiz attempts</h3>
          <div class="chart-container">
            <div v-if="summaryData.subject_wise_quizzes && summaryData.subject_wise_quizzes.length > 0" class="bar-chart">
              <div v-for="subject in summaryData.subject_wise_quizzes" :key="subject.subject_name" class="bar-item">
                <div class="bar-label">{{ subject.subject_name }}</div>
                <div class="bar-wrapper">
                  <div class="bar" :style="{ width: getBarWidth(subject.attempt_count, maxSubjectAttempts) + '%' }">
                    {{ subject.attempt_count }}
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              No quiz attempts found
            </div>
          </div>
        </div>

        <!-- Month wise no. of quizzes attempted -->
        <div class="chart-card">
          <h3>Month wise no. of quizzes attempted</h3>
          <div class="chart-container">
            <div v-if="summaryData.month_wise_attempts && summaryData.month_wise_attempts.length > 0" class="month-chart">
              <div class="month-bars">
                <div v-for="month in summaryData.month_wise_attempts" :key="`${month.year}-${month.month}`" class="month-item">
                  <div class="month-bar-wrapper">
                    <div class="month-bar" :style="{ height: getBarHeight(month.attempt_count, maxMonthAttempts) + '%' }">
                      <span class="month-count">{{ month.attempt_count }}</span>
                    </div>
                  </div>
                  <div class="month-label">{{ month.month_name.substring(0, 3) }} {{ month.year }}</div>
                </div>
              </div>
            </div>
            <div v-else class="no-data">
              No monthly data available
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'UserSummary',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const summaryData = ref({})
    const loading = ref(false)
    const error = ref('')

    const maxSubjectAttempts = computed(() => {
      if (!summaryData.value.subject_wise_quizzes) return 1
      return Math.max(...summaryData.value.subject_wise_quizzes.map(s => s.attempt_count), 1)
    })

    const maxMonthAttempts = computed(() => {
      if (!summaryData.value.month_wise_attempts) return 1
      return Math.max(...summaryData.value.month_wise_attempts.map(m => m.attempt_count), 1)
    })

    const getBarWidth = (value, max) => {
      return Math.max((value / max) * 100, 5) // Minimum 5% width for visibility
    }

    const getBarHeight = (value, max) => {
      return Math.max((value / max) * 100, 10) // Minimum 10% height for visibility
    }

    const fetchSummaryData = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const response = await fetch('/api/user/summary')
        if (!response.ok) {
          throw new Error('Failed to fetch summary data')
        }
        
        const data = await response.json()
        summaryData.value = data
        console.log('Summary data loaded:', data)
      } catch (err) {
        console.error('Error fetching summary:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchSummaryData()
    })

    return {
      searchQuery,
      summaryData,
      loading,
      error,
      maxSubjectAttempts,
      maxMonthAttempts,
      getBarWidth,
      getBarHeight,
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

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #666;
}

.error {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 5px;
  margin-bottom: 2rem;
  text-align: center;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  font-weight: 500;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #667eea;
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

.no-data {
  text-align: center;
  color: #999;
  font-style: italic;
  padding: 2rem;
}

/* Bar Chart Styles */
.bar-chart {
  width: 100%;
  max-width: 500px;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.bar-label {
  width: 100px;
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.bar-wrapper {
  flex: 1;
  height: 35px;
  background-color: #f0f0f0;
  border-radius: 17px;
  overflow: hidden;
  margin-left: 1rem;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 17px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 0.875rem;
  transition: width 0.5s ease;
  min-width: 30px;
}

/* Month Chart Styles */
.month-chart {
  width: 100%;
  max-width: 600px;
}

.month-bars {
  display: flex;
  align-items: end;
  justify-content: center;
  gap: 1rem;
  height: 250px;
  padding: 1rem 0;
}

.month-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
}

.month-bar-wrapper {
  height: 200px;
  width: 40px;
  background-color: #f0f0f0;
  border-radius: 20px;
  display: flex;
  align-items: end;
  overflow: hidden;
}

.month-bar {
  width: 100%;
  background: linear-gradient(180deg, #667eea, #764ba2);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: height 0.5s ease;
  min-height: 20px;
  position: relative;
}

.month-count {
  color: white;
  font-weight: bold;
  font-size: 0.8rem;
  position: absolute;
  top: 5px;
}

.month-label {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #666;
  text-align: center;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    padding: 1rem;
  }
  
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .bar-label {
    width: 80px;
    font-size: 0.8rem;
  }
  
  .month-bars {
    gap: 0.5rem;
  }
  
  .month-item {
    min-width: 40px;
  }
  
  .month-bar-wrapper {
    width: 30px;
  }
}
</style> 