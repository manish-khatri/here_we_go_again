<template>
  <div class="quiz-result">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/user/dashboard" class="nav-link">Home</router-link>
        <router-link to="/user/scores" class="nav-link">Scores</router-link>
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
      <!-- Back Button -->
      <div class="back-button-container">
        <button @click="goBack" class="btn-back">
          ← Back to Scores
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        Loading quiz result details...
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <!-- Quiz Result Content -->
      <div v-else-if="quizResult" class="result-content">
        <!-- Quiz Overview -->
        <div class="quiz-overview">
          <h1>Quiz Result Details</h1>
          <div class="overview-cards">
            <div class="overview-card">
              <h3>Quiz Name</h3>
              <p>{{ quizResult.quiz_name || quizId }}</p>
            </div>
            <div class="overview-card">
              <h3>Date Taken</h3>
              <p>{{ formatDate(quizResult.time_stamp) }}</p>
            </div>
            <div class="overview-card">
              <h3>Total Score</h3>
              <p class="score-value">{{ formatScore(quizResult.total_score) }}%</p>
            </div>
            <div class="overview-card">
              <h3>Questions</h3>
              <p>{{ quizResult.correct_answers || 0 }} / {{ quizResult.total_questions || 0 }} correct</p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button @click="retakeQuiz" class="btn-retake">Retake Quiz</button>
          <button @click="goToScores" class="btn-scores">View All Scores</button>
        </div>
      </div>

      <!-- No result found -->
      <div v-else class="no-result">
        <h1>Quiz Result Not Found</h1>
        <p>The quiz result you're looking for could not be found.</p>
        <button @click="goToScores" class="btn-scores">Back to Scores</button>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'QuizResult',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    
    const searchQuery = ref('')
    const quizResult = ref(null)
    const questionDetails = ref([])
    const loading = ref(false)
    const error = ref('')
    const quizId = ref('')

    const fetchQuizResult = async () => {
      try {
        loading.value = true
        error.value = ''
        quizId.value = route.params.quizId

        // Fetch the specific quiz result
        const response = await fetch(`/api/scores/${quizId.value}`)
        if (!response.ok) {
          throw new Error('Failed to fetch quiz result')
        }
        
        const data = await response.json()
        quizResult.value = data

        // Try to fetch detailed question results if available
        try {
          const detailResponse = await fetch(`/api/scores/${quizId.value}/details`)
          if (detailResponse.ok) {
            const detailData = await detailResponse.json()
            questionDetails.value = detailData.questions || []
          }
        } catch (detailError) {
          console.log('Detailed question data not available:', detailError)
          // This is optional, so we don't show an error
        }

      } catch (err) {
        console.error('Error fetching quiz result:', err)
        error.value = err.message || 'Failed to load quiz result'
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch {
        return dateString
      }
    }

    const formatScore = (score) => {
      if (typeof score !== 'number') return '0.00'
      return score.toFixed(2)
    }

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const goBack = () => {
      router.go(-1)
    }

    const goToScores = () => {
      router.push('/user/scores')
    }

    const retakeQuiz = () => {
      router.push(`/user/quiz/${quizId.value}`)
    }

    onMounted(() => {
      fetchQuizResult()
    })

    return {
      searchQuery,
      quizResult,
      questionDetails,
      loading,
      error,
      quizId,
      authStore,
      formatDate,
      formatScore,
      logout,
      goBack,
      goToScores,
      retakeQuiz
    }
  }
}
</script>

<style scoped>
.quiz-result {
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

.back-button-container {
  margin-bottom: 2rem;
}

.btn-back {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-back:hover {
  background-color: #5a6268;
}

.loading, .error {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
}

.loading {
  color: #667eea;
}

.error {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 5px;
}

.result-content h1 {
  color: #333;
  margin-bottom: 2rem;
  text-align: center;
}

.quiz-overview {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.overview-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.overview-card h3 {
  margin: 0 0 1rem 0;
  color: #666;
  font-size: 0.9rem;
  font-weight: 500;
}

.overview-card p {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.score-value {
  color: #28a745 !important;
  font-size: 1.8rem !important;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-retake, .btn-scores {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
}

.btn-retake {
  background-color: #667eea;
  color: white;
}

.btn-retake:hover {
  background-color: #5a67d8;
}

.btn-scores {
  background-color: #6c757d;
  color: white;
}

.btn-scores:hover {
  background-color: #5a6268;
}

.no-result {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.no-result h1 {
  color: #333;
  margin-bottom: 1rem;
}

.no-result p {
  color: #666;
  margin-bottom: 2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn-retake, .btn-scores {
    width: 100%;
    max-width: 200px;
  }
}
</style>
