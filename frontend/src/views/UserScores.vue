<template>
  <div class="user-scores">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/user/dashboard" class="nav-link">Home</router-link>
        <router-link to="/user/scores" class="nav-link active">Scores</router-link>
        <router-link to="/user/summary" class="nav-link">Summary</router-link>
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
      <div class="welcome">Welcome {{ authStore.currentUser?.name || 'User' }}</div>
    </header>

    <main class="main-content">
      <h1>Quiz Scores</h1>
      
      <div v-if="quizStore.loading" class="loading">
        Loading scores...
      </div>
      
      <div v-else-if="quizStore.error" class="error">
        Error: {{ quizStore.error }}
      </div>
      
      <div v-else class="scores-table-container">
        <table class="scores-table">
          <thead>
            <tr>
              <th>Quiz ID</th>
              <th>Date Taken</th>
              <th>Score</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="score in filteredScores" :key="score.score_id">
              <td>{{ score.q_id }}</td>
              <td>{{ formatDate(score.time_stamp) }}</td>
              <td class="score">{{ score.total_score }}%</td>
              <td>
                <button @click="viewScore(score)" class="btn-view">View Details</button>
              </td>
            </tr>
            <tr v-if="filteredScores.length === 0">
              <td colspan="4" class="no-data">No scores available</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="note">Searching subjects/quizzes by date/scores</p>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useQuizStore } from '../stores/quiz'

export default {
  name: 'UserScores',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const quizStore = useQuizStore()
    const searchQuery = ref('')

    const filteredScores = computed(() => {
      if (!searchQuery.value) return quizStore.userScores
      return quizStore.userScores.filter(score => 
        score.q_id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        formatDate(score.time_stamp).toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleDateString()
      } catch {
        return dateString
      }
    }

    const viewScore = (score) => {
      // Navigate to quiz details or show a modal with score details
      router.push(`/user/quiz/${score.q_id}/result`)
    }

    onMounted(async () => {
      // Load user scores data
      await quizStore.fetchUserScores()
    })

    return {
      searchQuery,
      filteredScores,
      quizStore,
      authStore,
      logout,
      formatDate,
      viewScore
    }
  }
}
</script>

<style scoped>
.user-scores {
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

.scores-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 1rem;
}

.scores-table {
  width: 100%;
  border-collapse: collapse;
}

.scores-table th,
.scores-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.scores-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.scores-table tr:hover {
  background-color: #f8f9fa;
}

.score {
  font-weight: bold;
  color: #28a745;
}

.scores-table tr:hover {
  background-color: #f8f9fa;
}

.btn-view {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s;
  background-color: #17a2b8;
  color: white;
}

.btn-view:hover {
  background-color: #138496;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.loading {
  color: #667eea;
}

.error {
  color: #dc3545;
}

.no-data {
  text-align: center;
  color: #666;
  font-style: italic;
}

.score {
  font-weight: bold;
  color: #28a745;
}

.note {
  color: #666;
  font-style: italic;
  margin: 1rem 0;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .scores-table {
    font-size: 0.875rem;
  }
  
  .scores-table th,
  .scores-table td {
    padding: 0.75rem 0.5rem;
  }
}
</style> 