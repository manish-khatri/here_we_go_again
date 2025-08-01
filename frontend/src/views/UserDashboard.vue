<template>
  <div class="dashboard">
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
          <router-link to="/user/dashboard" class="nav-link active">
            <i class="bi bi-house"></i>
            Dashboard
          </router-link>
          <router-link to="/user/scores" class="nav-link">
            <i class="bi bi-bar-chart"></i>
            Scores
          </router-link>
          <router-link to="/user/summary" class="nav-link">
            <i class="bi bi-file-text"></i>
            Summary
          </router-link>
        </nav>
        
        <div class="header-right">
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search quizzes..."
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
            <h1>Dashboard</h1>
            <p>Welcome back, {{ authStore.currentUser?.name || 'User' }}! Here are your upcoming quizzes.</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="quizStore.loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading your quizzes...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="quizStore.error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ quizStore.error }}</p>
          <button @click="refreshQuizzes" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Quiz List -->
        <div v-else class="quiz-section">
          <div class="section-header">
            <h2>Available Quizzes</h2>
            <span class="quiz-count">{{ filteredQuizzes.length }} quizzes</span>
          </div>

          <div v-if="filteredQuizzes.length === 0" class="empty-state">
            <i class="bi bi-inbox"></i>
            <h3>No quizzes available</h3>
            <p>Check back later for new quizzes or contact your administrator.</p>
          </div>

          <div v-else class="quiz-grid">
            <div 
              v-for="quiz in filteredQuizzes" 
              :key="quiz.q_id" 
              class="quiz-card"
            >
              <div class="quiz-header">
                <div class="quiz-id">#{{ quiz.q_id }}</div>
                <div class="quiz-status">Available</div>
              </div>
              
              <div class="quiz-content">
                <h3 class="quiz-title">{{ quiz.subject || 'General Quiz' }}</h3>
                <p class="quiz-subtitle">{{ quiz.chapter || 'Comprehensive Assessment' }}</p>
                
                <div class="quiz-details">
                  <div class="detail">
                    <i class="bi bi-question-circle"></i>
                    <span>{{ quiz.questionCount || 'N/A' }} questions</span>
                  </div>
                  <div class="detail">
                    <i class="bi bi-calendar"></i>
                    <span>{{ formatDate(quiz.date_of_quiz) }}</span>
                  </div>
                  <div class="detail">
                    <i class="bi bi-clock"></i>
                    <span>{{ quiz.time_dur || 'N/A' }}</span>
                  </div>
                </div>
              </div>
              
              <div class="quiz-actions">
                <button @click="viewQuiz(quiz)" class="btn btn-secondary">
                  <i class="bi bi-eye"></i>
                  View
                </button>
                <button @click="startQuiz(quiz.q_id)" class="btn btn-primary">
                  <i class="bi bi-play-fill"></i>
                  Start Quiz
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Quiz Details Modal -->
    <div v-if="showViewQuizModal" class="modal" @click="showViewQuizModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Quiz Details</h3>
          <button @click="showViewQuizModal = false" class="close-btn">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="detail-grid">
            <div class="detail-item">
              <label>Quiz ID</label>
              <span>{{ selectedQuiz.q_id }}</span>
            </div>
            <div class="detail-item">
              <label>Subject</label>
              <span>{{ selectedQuiz.subject || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <label>Chapter</label>
              <span>{{ selectedQuiz.chapter || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <label>Questions</label>
              <span>{{ selectedQuiz.questionCount || 'N/A' }}</span>
            </div>
            <div class="detail-item">
              <label>Date</label>
              <span>{{ formatDate(selectedQuiz.date_of_quiz) }}</span>
            </div>
            <div class="detail-item">
              <label>Duration</label>
              <span>{{ selectedQuiz.time_dur || 'N/A' }}</span>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showViewQuizModal = false" class="btn btn-secondary">
            Close
          </button>
          <button @click="startQuiz(selectedQuiz.q_id)" class="btn btn-primary">
            <i class="bi bi-play-fill"></i>
            Start Quiz
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useQuizStore } from '../stores/quiz'

export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const quizStore = useQuizStore()
    const searchQuery = ref('')
    const showViewQuizModal = ref(false)
    const selectedQuiz = ref({})

    const filteredQuizzes = computed(() => {
      if (!searchQuery.value) return quizStore.upcomingQuizzes
      return quizStore.upcomingQuizzes.filter(quiz => 
        quiz.q_id.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        (quiz.subject && quiz.subject.toLowerCase().includes(searchQuery.value.toLowerCase()))
      )
    })

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const viewQuiz = (quiz) => {
      selectedQuiz.value = quiz
      showViewQuizModal.value = true
    }

    const startQuiz = (quizId) => {
      router.push(`/user/quiz/${quizId}`)
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      try {
        return new Date(dateString).toLocaleDateString()
      } catch {
        return dateString
      }
    }

    onMounted(async () => {
      console.log('UserDashboard mounted, fetching quizzes...')
      try {
        const result = await quizStore.fetchUpcomingQuizzes()
        console.log('Fetch result:', result)
        console.log('Quizzes in store:', quizStore.upcomingQuizzes)
      } catch (error) {
        console.error('Error in onMounted:', error)
      }
    })

    return {
      searchQuery,
      showViewQuizModal,
      selectedQuiz,
      authStore,
      quizStore,
      filteredQuizzes,
      logout,
      viewQuiz,
      startQuiz,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Modern Dashboard Design */
.dashboard {
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

/* Quiz Section */
.quiz-section {
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

.quiz-count {
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
}

/* Quiz Grid */
.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.quiz-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-100);
  overflow: hidden;
  transition: all 0.2s ease;
}

.quiz-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: var(--primary-light);
  border-bottom: 1px solid var(--gray-200);
}

.quiz-id {
  font-weight: 600;
  color: var(--primary-dark);
  font-size: 1.125rem;
}

.quiz-status {
  background: var(--success);
  color: var(--white);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.quiz-content {
  padding: 1.5rem;
}

.quiz-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.quiz-subtitle {
  color: var(--text-light);
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

.quiz-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-light);
}

.detail i {
  color: var(--primary);
  font-size: 1rem;
}

.quiz-actions {
  display: flex;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid var(--gray-200);
}

.quiz-actions .btn {
  flex: 1;
  justify-content: center;
}

/* Modal Styles */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item label {
  font-weight: 600;
  color: var(--text);
  font-size: 0.875rem;
}

.detail-item span {
  color: var(--text-light);
  font-size: 1rem;
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
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }
  
  .quiz-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    padding: 0 1rem;
  }
  
  .search-box input {
    width: 150px;
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