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
      
      <!-- Loading State -->
      <div v-if="chartsLoading" class="loading-state">
        <div class="loading-content">
          <div class="loading-spinner">
            <div class="spinner"></div>
          </div>
          <h4 class="loading-text">Loading Dashboard Data</h4>
          <p class="loading-subtitle">Please wait while we fetch your analytics...</p>
        </div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="chartsError" class="error-state">
        <div class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill me-3"></i>
          {{ chartsError }}
          <button @click="loadChartData" class="btn btn-sm btn-outline-danger ms-3">
            <i class="bi bi-arrow-clockwise"></i> Retry
          </button>
        </div>
      </div>
      
      <!-- Charts Container -->
      <div v-else class="charts-container">
        <!-- Subject wise top scores -->
        <div class="chart-card">
          <h3>Subject wise top scores</h3>
          <div class="chart-container">
            <canvas ref="scoresChart" width="400" height="200"></canvas>
          </div>
        </div>

        <!-- Subject wise user attempts -->
        <div class="chart-card">
          <h3>Subject wise user attempts</h3>
          <div class="chart-container">
            <canvas ref="attemptsChart" width="400" height="200"></canvas>
          </div>
        </div>

        <!-- User Performance Over Time -->
        <div class="chart-card">
          <h3>User Performance Over Time</h3>
          <div class="chart-container">
            <canvas ref="performanceChart" width="400" height="200"></canvas>
          </div>
        </div>

        <!-- Export Actions -->
        <div class="chart-card">
          <h3>Export Data</h3>
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
            {{ exportMessage }}
            <a v-if="downloadUrl" :href="downloadUrl" class="btn btn-sm btn-success ms-2">
              <i class="bi bi-download"></i> Download
            </a>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import {
  Chart,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement
} from 'chart.js'

// Register Chart.js components
Chart.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement
)

export default {
  name: 'AdminSummary',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')
    
    // Chart refs
    const scoresChart = ref(null)
    const attemptsChart = ref(null)
    const performanceChart = ref(null)
    
    // Export functionality
    const exportLoading = ref(false)
    const exportTaskId = ref(null)
    const exportMessage = ref('')
    const exportMessageType = ref('')
    const downloadUrl = ref('')

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    // Loading and error states for charts
    const chartsLoading = ref(true)
    const chartsError = ref('')

    const loadChartData = async () => {
      try {
        chartsLoading.value = true
        chartsError.value = ''
        
        // Fetch admin dashboard data
        const response = await fetch('/api/admin/dashboard')
        
        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`)
        }
        
        const data = await response.json()
        
        console.log('Dashboard data:', data) // For debugging
        
        createScoresChart(data.subjectScores || [])
        createAttemptsChart(data.subjectAttempts || [])
        createPerformanceChart(data.performanceData || [])
        
      } catch (error) {
        console.error('Error loading chart data:', error)
        chartsError.value = 'Failed to load dashboard data. Please try again.'
      } finally {
        chartsLoading.value = false
      }
    }

    const createScoresChart = (subjectScores) => {
      if (!scoresChart.value) return
      
      const ctx = scoresChart.value.getContext('2d')
      
      // Clear any existing chart
      if (scoresChart.value.chart) {
        scoresChart.value.chart.destroy()
      }
      
      const labels = subjectScores.length > 0 ? subjectScores.map(item => item.subject_name || 'Unknown') : ['No Data']
      const data = subjectScores.length > 0 ? subjectScores.map(item => item.average_score || 0) : [0]
      
      scoresChart.value.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Average Score (%)',
            data: data,
            backgroundColor: [
              'rgba(102, 126, 234, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)'
            ],
            borderColor: [
              'rgba(102, 126, 234, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 205, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Subject-wise Average Scores'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Score (%)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Subjects'
              }
            }
          }
        }
      })
    }

    const createAttemptsChart = (subjectAttempts) => {
      if (!attemptsChart.value) return
      
      const ctx = attemptsChart.value.getContext('2d')
      
      // Clear any existing chart
      if (attemptsChart.value.chart) {
        attemptsChart.value.chart.destroy()
      }
      
      const labels = subjectAttempts.length > 0 ? subjectAttempts.map(item => item.subject_name || 'Unknown') : ['No Data']
      const data = subjectAttempts.length > 0 ? subjectAttempts.map(item => item.attempt_count || 0) : [0]
      
      attemptsChart.value.chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: [
              'rgba(102, 126, 234, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)',
              'rgba(255, 99, 132, 0.8)'
            ],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Subject-wise Quiz Attempts'
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      })
    }

    const createPerformanceChart = (performanceData) => {
      if (!performanceChart.value) return
      
      const ctx = performanceChart.value.getContext('2d')
      
      // Clear any existing chart
      if (performanceChart.value.chart) {
        performanceChart.value.chart.destroy()
      }
      
      const labels = performanceData.length > 0 ? performanceData.map(item => {
        const date = new Date(item.date || Date.now())
        return date.toLocaleDateString()
      }) : ['No Data']
      const data = performanceData.length > 0 ? performanceData.map(item => item.average_score || 0) : [0]
      
      performanceChart.value.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Average Performance (%)',
            data: data,
            borderColor: 'rgba(102, 126, 234, 1)',
            backgroundColor: 'rgba(102, 126, 234, 0.2)',
            fill: true,
            tension: 0.4,
            pointBackgroundColor: 'rgba(102, 126, 234, 1)',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: 'Performance Trend (Last 30 Days)'
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Average Score (%)'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
      })
    }

    const exportAllScores = async () => {
      try {
        exportLoading.value = true
        exportMessage.value = ''
        
        const response = await fetch('/api/export/all-scores', {
          method: 'POST'
        })
        
        const data = await response.json()
        
        if (response.ok) {
          exportTaskId.value = data.task_id
          exportMessage.value = data.message
          exportMessageType.value = 'alert-info'
          
          // Start checking status
          setTimeout(checkExportStatus, 2000)
        } else {
          exportMessage.value = 'Failed to start export'
          exportMessageType.value = 'alert-danger'
        }
      } catch (error) {
        console.error('Export error:', error)
        exportMessage.value = 'Export failed'
        exportMessageType.value = 'alert-danger'
      } finally {
        exportLoading.value = false
      }
    }

    const checkExportStatus = async () => {
      if (!exportTaskId.value) return
      
      try {
        const response = await fetch(`/api/export/status/${exportTaskId.value}`)
        const data = await response.json()
        
        if (data.state === 'SUCCESS') {
          exportMessage.value = data.message
          exportMessageType.value = 'alert-success'
          downloadUrl.value = data.download_url
        } else if (data.state === 'FAILURE') {
          exportMessage.value = data.message
          exportMessageType.value = 'alert-danger'
        } else {
          exportMessage.value = data.message
          exportMessageType.value = 'alert-info'
          // Continue checking
          setTimeout(checkExportStatus, 3000)
        }
      } catch (error) {
        console.error('Status check error:', error)
      }
    }

    onMounted(() => {
      loadChartData()
    })

    return {
      searchQuery,
      scoresChart,
      attemptsChart,
      performanceChart,
      chartsLoading,
      chartsError,
      exportLoading,
      exportTaskId,
      exportMessage,
      exportMessageType,
      downloadUrl,
      logout,
      loadChartData,
      exportAllScores,
      checkExportStatus
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

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
}

.loading-content {
  text-align: center;
  max-width: 300px;
}

.loading-spinner {
  margin-bottom: 2rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #374151;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.loading-subtitle {
  color: #6b7280;
  margin-bottom: 0;
}

/* Error State */
.error-state {
  margin-bottom: 2rem;
}

.alert {
  padding: 1rem 1.5rem;
  border-radius: 10px;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
}

.alert-danger {
  background-color: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

/* Export Actions */
.export-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.export-message {
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.export-message.alert-info {
  background-color: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.export-message.alert-success {
  background-color: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.export-message.alert-danger {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
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
  min-height: 400px;
  height: 400px;
  position: relative;
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

/* Button Styles */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-size: 0.95rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f8f9fa;
  color: #495057;
  border: 1px solid #dee2e6;
}

.btn-secondary:hover:not(:disabled) {
  background: #e9ecef;
  border-color: #adb5bd;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #218838;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.btn-outline-danger {
  background: transparent;
  color: #dc3545;
  border: 1px solid #dc3545;
}

.btn-outline-danger:hover:not(:disabled) {
  background: #dc3545;
  color: white;
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