<template>
  <div class="user-scores">
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
          <router-link to="/user/scores" class="nav-link active">
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
              placeholder="Search scores..."
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
        <div class="page-header">
          <div class="page-title">
            <h1>Quiz Scores</h1>
            <p>Track your performance across all quizzes</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="quizStore.loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading scores...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="quizStore.error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ quizStore.error }}</p>
          <button @click="refreshScores" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Scores Content -->
        <div v-else class="scores-content">
          <div class="section-header">
            <h2>Your Quiz Results</h2>
            <span class="score-count">{{ filteredScores.length }} scores</span>
          </div>

          <div v-if="filteredScores.length === 0" class="empty-state">
            <i class="bi bi-trophy"></i>
            <h3>No scores available</h3>
            <p>Take your first quiz to see your scores here.</p>
            <router-link to="/user/dashboard" class="btn btn-primary">
              <i class="bi bi-play-circle"></i>
              Take a Quiz
            </router-link>
          </div>

          <div v-else class="scores-grid">
            <div 
              v-for="score in filteredScores" 
              :key="score.score_id" 
              class="score-card"
            >
              <div class="score-header">
                <div class="score-info">
                  <div class="score-icon">
                    <i class="bi bi-file-text"></i>
                  </div>
                  <div>
                    <h3 class="quiz-id">{{ score.q_id }}</h3>
                    <p class="score-date">{{ formatDate(score.time_stamp) }}</p>
                  </div>
                </div>
                <div class="score-value">
                  <span class="percentage">{{ score.total_score }}%</span>
                </div>
              </div>
              
              <div class="score-actions">
                <button @click="viewScore(score)" class="btn btn-primary btn-sm">
                  <i class="bi bi-eye"></i>
                  View Details
                </button>
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
/* Modern User Scores Design */
.user-scores {
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

/* Scores Content */
.scores-content {
  margin-top: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
}

.score-count {
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
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

/* Scores Grid */
.scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.score-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-100);
  overflow: hidden;
  transition: all 0.2s ease;
}

.score-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: var(--primary-light);
  border-bottom: 1px solid var(--gray-200);
}

.score-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.score-icon {
  width: 50px;
  height: 50px;
  background: var(--primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-size: 1.5rem;
}

.quiz-id {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.score-date {
  color: var(--text-light);
  font-size: 0.875rem;
  margin: 0;
}

.score-value {
  text-align: right;
}

.percentage {
  background: var(--primary);
  color: var(--white);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
}

.score-actions {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
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
  
  .scores-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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
  
  .scores-grid {
    grid-template-columns: 1fr;
  }
  
  .score-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .score-value {
    text-align: left;
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