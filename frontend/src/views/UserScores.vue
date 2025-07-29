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
      <div class="welcome">Welcome User</div>
    </header>

    <main class="main-content">
      <h1>Quiz Scores</h1>
      
      <div class="scores-table-container">
        <table class="scores-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>No. of Questions</th>
              <th>Date</th>
              <th>Score</th>
            </tr>
          </thead>
                      <tbody>
              <tr v-for="score in userScores" :key="score.score_id">
                <td>{{ score.q_id }}</td>
                <td>{{ score.total_score }}</td>
                <td>{{ new Date(score.time_stamp).toLocaleDateString() }}</td>
                <td class="score">{{ score.total_score }}</td>
              </tr>
            </tbody>
        </table>
      </div>

      <p class="note">Searching subjects/quizzes by date/scores</p>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
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

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      // Load user scores data
      quizStore.fetchUserScores()
    })

    return {
      searchQuery,
      userScores: quizStore.userScores,
      logout
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