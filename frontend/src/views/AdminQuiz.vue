<template>
  <div class="admin-quiz">
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
          <router-link to="/admin/quiz" class="nav-link active">
            <i class="bi bi-collection"></i>
            Quiz Management
          </router-link>
          <router-link to="/admin/summary" class="nav-link">
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
              placeholder="Search quizzes..."
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
            <h1>Quiz Management</h1>
            <p>Create and manage quizzes for all subjects</p>
          </div>
          <button @click="openNewQuizModal" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i>
            Add Quiz
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading quizzes...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ error }}</p>
          <button @click="refreshQuizzes" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Quiz Content -->
        <div v-else class="quiz-content">
          <div class="section-header">
            <h2>Quizzes</h2>
            <span class="quiz-count">{{ filteredQuizzes.length }} quizzes</span>
          </div>

          <div v-if="filteredQuizzes.length === 0" class="empty-state">
            <i class="bi bi-puzzle"></i>
            <h3>No quizzes available</h3>
            <p>Create your first quiz to get started.</p>
            <button @click="openNewQuizModal" class="btn btn-primary">
              <i class="bi bi-plus-circle"></i>
              Add First Quiz
            </button>
          </div>

          <div v-else class="quizzes-grid">
            <div 
              v-for="quiz in filteredQuizzes" 
              :key="quiz.q_id" 
              class="quiz-card"
            >
              <div class="quiz-header">
                <div class="quiz-info">
                  <div class="quiz-icon">
                    <i class="bi bi-puzzle"></i>
                  </div>
                  <div>
                    <h3 class="quiz-name">{{ quiz.q_name }}</h3>
                    <p class="quiz-meta">
                      <span class="subject-badge">{{ quiz.sub_id || 'No Subject' }}</span>
                      {{ quiz.questions?.length || 0 }} questions
                    </p>
                  </div>
                </div>
                <div class="quiz-actions">
                  <button @click="editQuiz(quiz)" class="btn btn-secondary btn-sm">
                    <i class="bi bi-pencil"></i>
                    Edit
                  </button>
                  <button @click="deleteQuiz(quiz.q_id)" class="btn btn-danger btn-sm">
                    <i class="bi bi-trash"></i>
                    Delete
                  </button>
                </div>
              </div>
              
              <div class="quiz-details">
                <div class="detail-item">
                  <i class="bi bi-calendar"></i>
                  <span>Date: {{ formatDate(quiz.date_of_quiz) }}</span>
                </div>
                <div class="detail-item">
                  <i class="bi bi-clock"></i>
                  <span>Duration: {{ quiz.time_dur }} minutes</span>
                </div>
                <div class="detail-item" v-if="quiz.remarks">
                  <i class="bi bi-journal-text"></i>
                  <span>{{ quiz.remarks }}</span>
                </div>
              </div>

              <div class="questions-section" v-if="quiz.questions?.length > 0">
                <h4>Questions</h4>
                <div class="questions-list">
                  <div 
                    v-for="question in quiz.questions.slice(0, 3)" 
                    :key="question.q_id" 
                    class="question-item"
                  >
                    <span class="question-text">{{ question.q_text }}</span>
                    <span class="question-type">{{ question.q_type }}</span>
                  </div>
                  <div v-if="quiz.questions.length > 3" class="more-questions">
                    +{{ quiz.questions.length - 3 }} more questions
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modals would go here -->
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'AdminQuiz',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const quizzes = ref([])
    const loading = ref(false)
    const error = ref('')

    const filteredQuizzes = computed(() => {
      if (!searchQuery.value) return quizzes.value
      return quizzes.value.filter(quiz =>
        quiz.q_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        quiz.sub_id?.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const fetchQuizzes = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const response = await fetch('/api/admin/quizzes')
        if (!response.ok) {
          throw new Error('Failed to fetch quizzes')
        }
        
        const data = await response.json()
        quizzes.value = data
      } catch (err) {
        console.error('Error fetching quizzes:', err)
        error.value = err.message
      } finally {
        loading.value = false
      }
    }

    const refreshQuizzes = () => {
      fetchQuizzes()
    }

    const openNewQuizModal = () => {
      // Implementation for opening new quiz modal
      console.log('Opening new quiz modal')
    }

    const editQuiz = (quiz) => {
      // Implementation for editing quiz
      console.log('Editing quiz:', quiz)
    }

    const deleteQuiz = async (quizId) => {
      if (!confirm('Are you sure you want to delete this quiz?')) return
      
      try {
        const response = await fetch(`/api/admin/quizzes/${quizId}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) {
          throw new Error('Failed to delete quiz')
        }
        
        await fetchQuizzes()
      } catch (err) {
        console.error('Error deleting quiz:', err)
        error.value = err.message
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'No date'
      return new Date(dateString).toLocaleDateString()
    }

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    onMounted(() => {
      fetchQuizzes()
    })

    return {
      searchQuery,
      quizzes,
      filteredQuizzes,
      loading,
      error,
      refreshQuizzes,
      openNewQuizModal,
      editQuiz,
      deleteQuiz,
      formatDate,
      logout
    }
  }
}
</script>

<style scoped>
/* Admin Quiz Management - Modern Pastel Blue Design */
.admin-quiz {
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

/* Quiz Content */
.quiz-content {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--gray-200);
}

.section-header h2 {
  color: var(--text);
  font-size: 1.5rem;
  font-weight: 600;
}

.quiz-count {
  color: var(--text-light);
  font-size: 0.875rem;
  font-weight: 500;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-state i {
  font-size: 4rem;
  color: var(--text-light);
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: var(--text);
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.empty-state p {
  color: var(--text-light);
  margin-bottom: 2rem;
}

/* Quiz Grid */
.quizzes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
}

.quiz-card {
  background: var(--white);
  border: 2px solid var(--gray-200);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.quiz-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.quiz-info {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  flex: 1;
}

.quiz-icon {
  width: 48px;
  height: 48px;
  background: var(--primary-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-dark);
  font-size: 1.25rem;
}

.quiz-name {
  color: var(--text);
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.quiz-meta {
  color: var(--text-light);
  font-size: 0.875rem;
  margin: 0;
}

.subject-badge {
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-right: 0.5rem;
}

.quiz-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
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

.btn-danger {
  background: var(--error);
  color: var(--white);
}

.btn-danger:hover {
  background: #dc2626;
}

.quiz-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-light);
  font-size: 0.875rem;
}

.detail-item i {
  color: var(--primary);
  width: 16px;
}

.questions-section h4 {
  color: var(--text);
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--gray-200);
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 0.75rem;
  background: var(--gray-50);
  border-radius: 8px;
  gap: 1rem;
}

.question-text {
  flex: 1;
  color: var(--text);
  font-size: 0.875rem;
  line-height: 1.4;
}

.question-type {
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.more-questions {
  text-align: center;
  color: var(--text-light);
  font-size: 0.875rem;
  font-style: italic;
  padding: 0.75rem;
  background: var(--gray-50);
  border-radius: 8px;
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

  .quizzes-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .quiz-header {
    flex-direction: column;
    gap: 1rem;
  }

  .quiz-actions {
    width: 100%;
    justify-content: flex-end;
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

  .quiz-card {
    padding: 1rem;
  }

  .quiz-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn-sm {
    width: 100%;
    justify-content: center;
  }
}
</style>
