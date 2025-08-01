<template>
  <div class="quiz-result">
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
            Scores
          </router-link>
          <router-link to="/user/summary" class="nav-link">
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
              <span>{{ authStore.currentUser?.name || 'User' }}</span>
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
        <!-- Back Button -->
        <div class="back-section">
          <button @click="goBack" class="btn-back">
            <i class="bi bi-arrow-left"></i>
            Back to Scores
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading quiz result details...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ error }}</p>
          <button @click="goToScores" class="btn btn-primary">
            Back to Scores
          </button>
        </div>

        <!-- Quiz Result Content -->
        <div v-else-if="quizResult" class="result-content">
          <div class="page-header">
            <div class="page-title">
              <h1>Quiz Result Details</h1>
              <p>Review your performance and see how you did</p>
            </div>
          </div>

          <!-- Quiz Overview -->
          <div class="quiz-overview">
            <div class="overview-grid">
              <div class="overview-card">
                <div class="card-icon">
                  <i class="bi bi-file-text"></i>
                </div>
                <div class="card-content">
                  <h3>Quiz Name</h3>
                  <p>{{ quizResult.quiz_name || quizId }}</p>
                </div>
              </div>
              
              <div class="overview-card">
                <div class="card-icon">
                  <i class="bi bi-calendar"></i>
                </div>
                <div class="card-content">
                  <h3>Date Taken</h3>
                  <p>{{ formatDate(quizResult.time_stamp) }}</p>
                </div>
              </div>
              
              <div class="overview-card score-card">
                <div class="card-icon">
                  <i class="bi bi-star"></i>
                </div>
                <div class="card-content">
                  <h3>Total Score</h3>
                  <p class="score-value">{{ formatScore(quizResult.total_score) }}%</p>
                </div>
              </div>
              
              <div class="overview-card">
                <div class="card-icon">
                  <i class="bi bi-question-circle"></i>
                </div>
                <div class="card-content">
                  <h3>Questions</h3>
                  <p>{{ quizResult.correct_answers || 0 }} / {{ quizResult.total_questions || 0 }} correct</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="action-buttons">
            <button @click="retakeQuiz" class="btn btn-primary">
              <i class="bi bi-arrow-clockwise"></i>
              Retake Quiz
            </button>
            <button @click="goToScores" class="btn btn-secondary">
              <i class="bi bi-list-ul"></i>
              View All Scores
            </button>
          </div>
        </div>

        <!-- No result found -->
        <div v-else class="empty-state">
          <i class="bi bi-search"></i>
          <h3>Quiz Result Not Found</h3>
          <p>The quiz result you're looking for could not be found.</p>
          <button @click="goToScores" class="btn btn-primary">
            <i class="bi bi-arrow-left"></i>
            Back to Scores
          </button>
        </div>
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
/* Modern Quiz Result Design */
.quiz-result {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 100%);
}

/* Header */
.header {
  background: var(--white);
  box-shadow: var(--shadow);
  border-bottom: 1px solid var(--gray-200);
  padding: 0 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 0;
}

.header-left .logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
}

.header-left .logo i {
  margin-right: 0.75rem;
  font-size: 1.75rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text);
  text-decoration: none;
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  background: var(--primary-light);
  color: var(--primary-dark);
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
  font-size: 1rem;
}

.search-box input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  background: var(--white);
  font-size: 0.875rem;
  width: 250px;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(168, 213, 232, 0.1);
}

.user-menu {
  position: relative;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--text);
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-btn:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--white);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--gray-200);
  min-width: 150px;
  z-index: 100;
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
  border: none;
  background: none;
  color: var(--text);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: var(--gray-100);
  color: var(--error);
}

/* Main Content */
.main {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.container {
  width: 100%;
}

.back-section {
  margin-bottom: 2rem;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--text);
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-back:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-state .spinner {
  margin: 0 auto 1rem;
}

.loading-state p {
  color: var(--text-light);
  font-size: 1rem;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.error-state i {
  font-size: 3rem;
  color: var(--error);
  margin-bottom: 1rem;
}

.error-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.error-state p {
  color: var(--text-light);
  margin-bottom: 1.5rem;
}

/* Result Content */
.result-content {
  margin-top: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-title h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.page-title p {
  color: var(--text-light);
  font-size: 1rem;
}

/* Quiz Overview */
.quiz-overview {
  margin-bottom: 2rem;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.overview-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-100);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.overview-card.score-card {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: var(--white);
}

.overview-card.score-card .card-content h3,
.overview-card.score-card .card-content p {
  color: var(--white);
}

.card-icon {
  width: 50px;
  height: 50px;
  background: var(--primary-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-dark);
  font-size: 1.5rem;
  flex-shrink: 0;
}

.score-card .card-icon {
  background: rgba(255, 255, 255, 0.2);
  color: var(--white);
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-light);
  margin: 0 0 0.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-content p {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.score-value {
  font-size: 1.5rem !important;
  font-weight: 700 !important;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.action-buttons .btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
}

.empty-state i {
  font-size: 4rem;
  color: var(--text-light);
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-light);
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
  }
  
  .nav {
    margin-left: 0;
  }
  
  .header-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .search-box input {
    width: 200px;
  }
  
  .overview-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }
  
  .header {
    padding: 0 1rem;
  }
  
  .search-box input {
    width: 150px;
  }
  
  .overview-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 640px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .header-right {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box input {
    width: 100%;
  }
}
</style>
