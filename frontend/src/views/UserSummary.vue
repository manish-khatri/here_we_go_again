<template>
  <div class="user-summary">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo">
            <i class="bi bi-mortarboard-fill"></i>
            <span>Quiz Master</span>
          </div>
        </div>
        
        <nav class="nav">
          <router-link to="/user/dashboard" class="nav-link">
            <i class="bi bi-house"></i>
            Dashboard
          </router-link>
          <router-link to="/user/scores" class="nav-link">
            <i class="bi bi-trophy"></i>
            My Scores
          </router-link>
          <router-link to="/user/summary" class="nav-link active">
            <i class="bi bi-bar-chart"></i>
            Summary
          </router-link>
        </nav>
        
        <div class="header-right">
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search..."
            />
          </div>
          
          <div class="user-menu">
            <button class="user-btn">
              <i class="bi bi-person-circle"></i>
              <span>User</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <div class="dropdown-menu">
              <button @click="logout" class="dropdown-item">
                <i class="bi bi-box-arrow-right"></i>
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main">
      <div class="container">
        <div class="page-header">
          <div class="page-title">
            <h1>Performance Summary</h1>
            <p>Analyze your quiz performance and track your progress</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading summary data...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ error }}</p>
          <button @click="fetchSummaryData" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Content -->
        <div v-else class="content">
          <!-- Stats Overview -->
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <i class="bi bi-play-circle"></i>
              </div>
              <div class="stat-info">
                <h3>Total Attempts</h3>
                <div class="stat-number">{{ summaryData.total_attempts || 0 }}</div>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon">
                <i class="bi bi-trophy"></i>
              </div>
              <div class="stat-info">
                <h3>Average Score</h3>
                <div class="stat-number">{{ summaryData.average_score || 0 }}%</div>
              </div>
            </div>
          </div>

          <!-- Charts Section -->
          <div class="charts-section">
            <!-- Subject wise attempts -->
            <div class="chart-card">
              <div class="card-header">
                <h3>
                  <i class="bi bi-book"></i>
                  Subject-wise Quiz Attempts
                </h3>
              </div>
              <div class="chart-container">
                <div v-if="summaryData.subject_wise_quizzes && summaryData.subject_wise_quizzes.length > 0" class="bar-chart">
                  <div v-for="subject in summaryData.subject_wise_quizzes" :key="subject.subject_name" class="bar-item">
                    <div class="bar-label">{{ subject.subject_name }}</div>
                    <div class="bar-wrapper">
                      <div class="bar" :style="{ width: getBarWidth(subject.attempt_count, maxSubjectAttempts) + '%' }">
                        <span class="bar-value">{{ subject.attempt_count }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-state">
                  <i class="bi bi-graph-up"></i>
                  <h4>No quiz attempts found</h4>
                  <p>Start taking quizzes to see your performance data</p>
                </div>
              </div>
            </div>

            <!-- Month wise attempts -->
            <div class="chart-card">
              <div class="card-header">
                <h3>
                  <i class="bi bi-calendar-month"></i>
                  Monthly Quiz Activity
                </h3>
              </div>
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
                <div v-else class="empty-state">
                  <i class="bi bi-calendar-x"></i>
                  <h4>No monthly data available</h4>
                  <p>Complete more quizzes to track your monthly progress</p>
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
/* User Summary - Modern Pastel Blue Design */
.user-summary {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 100%);
}

/* Header Styles */
.header {
  background: var(--white);
  border-bottom: 1px solid var(--gray-200);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.header-left .logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
}

.logo i {
  color: var(--primary);
  font-size: 2rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  text-decoration: none;
  color: var(--text-light);
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: var(--gray-100);
  color: var(--text);
}

.nav-link.active {
  background: var(--primary);
  color: var(--text);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box i {
  position: absolute;
  left: 1rem;
  color: var(--text-light);
}

.search-box input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid var(--gray-200);
  border-radius: 12px;
  font-size: 0.875rem;
  width: 250px;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.user-menu {
  position: relative;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--gray-100);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.user-btn:hover {
  background: var(--primary-light);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: var(--white);
  border-radius: 12px;
  box-shadow: var(--shadow-lg);
  min-width: 150px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
}

.user-menu:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: var(--gray-100);
}

/* Main Content */
.main {
  padding: 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.page-title h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.page-title p {
  color: var(--text-light);
  font-size: 1.1rem;
}

/* Loading and Error States */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--gray-200);
  border-left: 4px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.error-state i {
  font-size: 3rem;
  color: var(--error);
  margin-bottom: 1rem;
}

.error-state h3 {
  color: var(--text);
  margin-bottom: 0.5rem;
}

.error-state p {
  color: var(--text-light);
  margin-bottom: 2rem;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: var(--white);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: all 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.stat-icon {
  width: 60px;
  height: 60px;
  background: var(--primary-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--primary-dark);
}

.stat-info h3 {
  color: var(--text-light);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text);
}

/* Charts Section */
.charts-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.chart-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: all 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--gray-200);
}

.card-header h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text);
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.card-header i {
  color: var(--primary);
}

.chart-container {
  padding: 2rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.empty-state i {
  font-size: 3rem;
  color: var(--text-light);
  margin-bottom: 1rem;
}

.empty-state h4 {
  color: var(--text);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-light);
}

/* Bar Chart Styles */
.bar-chart {
  width: 100%;
  max-width: 600px;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.bar-label {
  width: 120px;
  font-weight: 600;
  color: var(--text);
  font-size: 0.875rem;
}

.bar-wrapper {
  flex: 1;
  height: 40px;
  background: var(--gray-100);
  border-radius: 20px;
  overflow: hidden;
  margin-left: 1rem;
  position: relative;
}

.bar {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: width 0.6s ease;
  min-width: 40px;
  position: relative;
}

.bar-value {
  color: var(--white);
  font-weight: 600;
  font-size: 0.875rem;
}

/* Month Chart Styles */
.month-chart {
  width: 100%;
  max-width: 800px;
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
  background: var(--gray-100);
  border-radius: 20px;
  display: flex;
  align-items: end;
  overflow: hidden;
  position: relative;
}

.month-bar {
  width: 100%;
  background: linear-gradient(180deg, var(--primary), var(--primary-dark));
  border-radius: 20px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  transition: height 0.6s ease;
  min-height: 20px;
  position: relative;
  padding-top: 0.5rem;
}

.month-count {
  color: var(--white);
  font-weight: 600;
  font-size: 0.75rem;
}

.month-label {
  margin-top: 0.75rem;
  font-size: 0.75rem;
  color: var(--text-light);
  text-align: center;
  font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .nav {
    order: 3;
    width: 100%;
    justify-content: center;
  }

  .search-box input {
    width: 200px;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 1.5rem;
  }

  .chart-container {
    padding: 1rem;
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

@media (max-width: 480px) {
  .header-content {
    padding: 0.75rem;
  }

  .nav {
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-link {
    justify-content: center;
    padding: 0.5rem;
  }

  .main {
    padding: 1rem;
  }

  .page-title h1 {
    font-size: 2rem;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .bar-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .bar-wrapper {
    margin-left: 0;
    width: 100%;
  }
}
</style> 