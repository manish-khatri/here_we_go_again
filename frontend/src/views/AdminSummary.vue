<template>
  <div class="admin-summary">
    <!-- Header -->
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <div class="logo">
            <i class="bi bi-mortarboard-fill"></i>
            <span>Quiz Master Admin</span>
          </div>
        </div>
        
        <nav class="nav">
          <router-link to="/admin/dashboard" class="nav-link">
            <i class="bi bi-house"></i>
            Dashboard
          </router-link>
          <router-link to="/admin/quiz" class="nav-link">
            <i class="bi bi-collection"></i>
            Quiz Management
          </router-link>
          <router-link to="/admin/summary" class="nav-link active">
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
              <span>Admin</span>
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
            <h1>Analytics Dashboard</h1>
            <p>Monitor quiz performance and generate comprehensive reports</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="chartsLoading" class="loading-state">
          <div class="spinner"></div>
          <h4>Loading Dashboard Data</h4>
          <p>Please wait while we fetch your analytics...</p>
        </div>
        
        <!-- Error State -->
        <div v-else-if="chartsError" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ chartsError }}</p>
          <button @click="loadChartData" class="btn btn-primary">
            <i class="bi bi-arrow-clockwise"></i>
            Try Again
          </button>
        </div>
        
        <!-- Charts Container -->
        <div v-else class="charts-container">
          <!-- Subject wise top scores -->
          <div class="chart-card">
            <div class="card-header">
              <h3>
                <i class="bi bi-trophy"></i>
                Subject-wise Top Scores
              </h3>
            </div>
            <div class="chart-content">
              <canvas ref="scoresChart" width="400" height="200"></canvas>
            </div>
          </div>

          <!-- Subject wise user attempts -->
          <div class="chart-card">
            <div class="card-header">
              <h3>
                <i class="bi bi-graph-up"></i>
                Subject-wise User Attempts
              </h3>
            </div>
            <div class="chart-content">
              <canvas ref="attemptsChart" width="400" height="200"></canvas>
            </div>
          </div>

          <!-- User Performance Over Time -->
          <div class="chart-card">
            <div class="card-header">
              <h3>
                <i class="bi bi-clock-history"></i>
                User Performance Over Time
              </h3>
            </div>
            <div class="chart-content">
              <canvas ref="performanceChart" width="400" height="200"></canvas>
            </div>
          </div>

          <!-- Export Actions -->
          <div class="chart-card">
            <div class="card-header">
              <h3>
                <i class="bi bi-download"></i>
                Export Data
              </h3>
            </div>
            <div class="export-content">
              <div class="export-actions">
                <button @click="exportAllScores" class="btn btn-primary" :disabled="exportLoading">
                  <i class="bi bi-download"></i>
                  {{ exportLoading ? 'Exporting...' : 'Export All Scores' }}
                </button>
                <button @click="checkExportStatus" class="btn btn-secondary" v-if="exportTaskId">
                  <i class="bi bi-check-circle"></i>
                  Check Export Status
                </button>
              </div>
              <div v-if="exportMessage" class="export-message" :class="exportMessageType">
                <div class="message-content">
                  <i class="bi bi-info-circle"></i>
                  {{ exportMessage }}
                </div>
                <a v-if="downloadUrl" :href="downloadUrl" class="btn btn-success btn-sm">
                  <i class="bi bi-download"></i> Download
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'AdminSummary',
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const chartsLoading = ref(false)
    const chartsError = ref('')
    const exportLoading = ref(false)
    const exportTaskId = ref('')
    const exportMessage = ref('')
    const exportMessageType = ref('')
    const downloadUrl = ref('')

    const loadChartData = async () => {
      try {
        chartsLoading.value = true
        chartsError.value = ''
        
        // Simulate API call for charts data
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Initialize charts here
        console.log('Charts loaded successfully')
      } catch (err) {
        console.error('Error loading charts:', err)
        chartsError.value = err.message
      } finally {
        chartsLoading.value = false
      }
    }

    const exportAllScores = async () => {
      try {
        exportLoading.value = true
        exportMessage.value = ''
        
        const response = await fetch('/api/admin/export/scores', {
          method: 'POST'
        })
        
        if (!response.ok) {
          throw new Error('Failed to start export')
        }
        
        const data = await response.json()
        exportTaskId.value = data.task_id
        exportMessage.value = 'Export started successfully. Please check status.'
        exportMessageType.value = 'success'
      } catch (err) {
        console.error('Error exporting scores:', err)
        exportMessage.value = err.message
        exportMessageType.value = 'error'
      } finally {
        exportLoading.value = false
      }
    }

    const checkExportStatus = async () => {
      try {
        const response = await fetch(`/api/admin/export/status/${exportTaskId.value}`)
        if (!response.ok) {
          throw new Error('Failed to check export status')
        }
        
        const data = await response.json()
        if (data.status === 'completed' && data.download_url) {
          downloadUrl.value = data.download_url
          exportMessage.value = 'Export completed! Click download to get your file.'
          exportMessageType.value = 'success'
        } else if (data.status === 'failed') {
          exportMessage.value = 'Export failed. Please try again.'
          exportMessageType.value = 'error'
        } else {
          exportMessage.value = 'Export is still in progress...'
          exportMessageType.value = 'info'
        }
      } catch (err) {
        console.error('Error checking export status:', err)
        exportMessage.value = err.message
        exportMessageType.value = 'error'
      }
    }

    const logout = () => {
      router.push('/login')
    }

    onMounted(() => {
      loadChartData()
    })

    return {
      searchQuery,
      chartsLoading,
      chartsError,
      exportLoading,
      exportTaskId,
      exportMessage,
      exportMessageType,
      downloadUrl,
      loadChartData,
      exportAllScores,
      checkExportStatus,
      logout
    }
  }
}
</script>

<style scoped>
/* Admin Summary - Modern Pastel Blue Design */
.admin-summary {
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

.loading-state h4 {
  color: var(--text);
  margin-bottom: 0.5rem;
}

.loading-state p {
  color: var(--text-light);
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

/* Charts Container */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
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

.chart-content {
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

/* Export Card */
.export-content {
  padding: 2rem;
}

.export-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.export-message {
  background: var(--gray-50);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.export-message.success {
  background: #f0f9ff;
  border: 1px solid var(--success);
}

.export-message.error {
  background: #fef2f2;
  border: 1px solid var(--error);
}

.export-message.info {
  background: #f0f9ff;
  border: 1px solid var(--primary);
}

.message-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text);
}

.message-content i {
  color: var(--primary);
}

.btn-success {
  background: var(--success);
  color: var(--white);
}

.btn-success:hover {
  background: #059669;
}

.btn-secondary {
  background: var(--gray-100);
  color: var(--text);
  border: 2px solid var(--gray-200);
}

.btn-secondary:hover {
  background: var(--primary-light);
  border-color: var(--primary);
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
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

  .charts-container {
    grid-template-columns: 1fr;
  }

  .export-actions {
    flex-direction: column;
  }

  .export-message {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
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

  .card-header,
  .chart-content,
  .export-content {
    padding: 1rem;
  }
}
</style>
