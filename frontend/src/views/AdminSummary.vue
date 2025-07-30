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

    const loadChartData = async () => {
      try {
        // Fetch admin dashboard data
        const response = await fetch('/api/admin/dashboard')
        const data = await response.json()
        
        if (response.ok) {
          createScoresChart(data.subjectScores || [])
          createAttemptsChart(data.subjectAttempts || [])
          createPerformanceChart(data.performanceData || [])
        }
      } catch (error) {
        console.error('Error loading chart data:', error)
      }
    }

    const createScoresChart = (subjectScores) => {
      if (!scoresChart.value) return
      
      const ctx = scoresChart.value.getContext('2d')
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: subjectScores.map(item => item.subject_name || 'Unknown'),
          datasets: [{
            label: 'Average Score',
            data: subjectScores.map(item => item.average_score || 0),
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
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
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      })
    }

    const createAttemptsChart = (subjectAttempts) => {
      if (!attemptsChart.value) return
      
      const ctx = attemptsChart.value.getContext('2d')
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: subjectAttempts.map(item => item.subject_name || 'Unknown'),
          datasets: [{
            data: subjectAttempts.map(item => item.attempt_count || 0),
            backgroundColor: [
              'rgba(255, 99, 132, 0.8)',
              'rgba(54, 162, 235, 0.8)',
              'rgba(255, 205, 86, 0.8)',
              'rgba(75, 192, 192, 0.8)',
              'rgba(153, 102, 255, 0.8)'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
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
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: performanceData.map(item => item.date || 'Unknown'),
          datasets: [{
            label: 'Average Performance',
            data: performanceData.map(item => item.average_score || 0),
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
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
      exportLoading,
      exportTaskId,
      exportMessage,
      exportMessageType,
      downloadUrl,
      logout,
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