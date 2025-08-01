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

    <!-- New Quiz Modal -->
    <div v-if="showNewQuizModal" class="modal" @click="showNewQuizModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Add New Quiz</h3>
          <button @click="showNewQuizModal = false" class="close-btn">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="addQuiz" class="quiz-form">
            <div class="form-group">
              <label class="form-label">Quiz Name</label>
              <input 
                type="text" 
                class="form-control"
                v-model="newQuiz.name" 
                placeholder="Enter quiz name"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Subject ID</label>
              <input 
                type="text" 
                class="form-control"
                v-model="newQuiz.subjectId" 
                placeholder="Enter subject ID"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Duration (minutes)</label>
              <input 
                type="number" 
                class="form-control"
                v-model="newQuiz.duration" 
                placeholder="Enter duration"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Date</label>
              <input 
                type="date" 
                class="form-control"
                v-model="newQuiz.date" 
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Remarks</label>
              <textarea 
                class="form-control"
                v-model="newQuiz.remarks" 
                placeholder="Enter remarks (optional)"
                rows="3"
              ></textarea>
            </div>
            
            <div class="modal-footer">
              <button type="button" @click="showNewQuizModal = false" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="addingQuiz">
                <div v-if="addingQuiz" class="spinner"></div>
                <span v-else>Add Quiz</span>
              </button>
            </div>
          </form>
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
  name: 'AdminQuiz',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const quizStore = useQuizStore()
    
    // State
    const searchQuery = ref('')
    const loading = ref(false)
    const subjectsLoading = ref(false)
    const chaptersLoading = ref(false)
    const error = ref('')
    const subjectsError = ref('')
    const chaptersError = ref('')
    const quizzes = ref([])
    const availableChapters = ref([])
    const availableSubjects = ref([])
    
    // Modal states
    const showNewQuizModal = ref(false)
    const showNewQuestionModal = ref(false)
    const selectedQuizId = ref(null)
    const selectedQuestionId = ref(null)
    
    // Form data
    const newQuiz = ref({
      name: '',
      subjectId: '',
      chapterId: '',
      date: '',
      duration: 60,
      remarks: ''
    })
    
    const newQuestion = ref({
      quizId: '',
      statement: '',
      options: ['', '', '', ''],
      correctOption: 1
    })

    // Computed
    const filteredQuizzes = computed(() => {
      if (!searchQuery.value) return quizzes.value
      return quizzes.value.filter(quiz => 
        quiz.q_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        quiz.sub_id?.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const chaptersForSelectedSubject = computed(() => {
      if (!newQuiz.value.subjectId) return []
      return availableChapters.value.filter(c => c.sub_id === newQuiz.value.subjectId)
    })

    // Methods
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const fetchQuizzes = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const response = await fetch('/api/admin/quizzes')
        if (response.ok) {
          const data = await response.json()
          quizzes.value = data
          
          // Fetch questions for each quiz
          for (const quiz of quizzes.value) {
            try {
              const questionsResponse = await fetch(`/api/quizzes/${quiz.q_id}/questions`)
              if (questionsResponse.ok) {
                quiz.questions = await questionsResponse.json()
              }
            } catch (err) {
              console.warn(`Failed to fetch questions for quiz ${quiz.q_id}:`, err)
              quiz.questions = []
            }
          }
        } else {
          error.value = 'Failed to fetch quizzes'
        }
      } catch (err) {
        console.error('Error fetching quizzes:', err)
        error.value = 'Failed to load quiz data'
      } finally {
        loading.value = false
      }
    }

    const fetchSubjects = async () => {
      try {
        subjectsLoading.value = true
        subjectsError.value = ''
        const response = await fetch('/api/admin/subjects') // Updated endpoint
        if (!response.ok) {
          throw new Error('Failed to fetch subjects')
        }
        const data = await response.json()
        availableSubjects.value = data
        console.log('Subjects loaded:', data) // Debug log
      } catch (err) {
        console.error('Error fetching subjects:', err)
        subjectsError.value = 'Failed to load subjects. Please try again.'
      } finally {
        subjectsLoading.value = false
      }
    }

    const fetchChapters = async () => {
      try {
        chaptersLoading.value = true
        chaptersError.value = ''
        const response = await fetch('/api/admin/chapters') // Updated endpoint
        if (!response.ok) {
          throw new Error('Failed to fetch chapters')
        }
        const data = await response.json()
        availableChapters.value = data
        console.log('Chapters loaded:', data) // Debug log
      } catch (err) {
        console.error('Error fetching chapters:', err)
        chaptersError.value = 'Failed to load chapters. Please try again.'
      } finally {
        chaptersLoading.value = false
      }
    }

    const openNewQuizModal = async () => {
      // Show modal first to avoid delay
      showNewQuizModal.value = true
      
      try {
        // Fetch data if not already loaded
        if (availableSubjects.value.length === 0) {
          await fetchSubjects()
        }
        if (availableChapters.value.length === 0) {
          await fetchChapters()
        }
      } catch (err) {
        console.error('Error initializing modal:', err)
      }

      // Reset form
      newQuiz.value = {
        name: '',
        subjectId: '',
        chapterId: '',
        date: '',
        duration: 60,
        remarks: ''
      }
      selectedQuizId.value = null
    }

    const closeQuizModal = () => {
      showNewQuizModal.value = false
      newQuiz.value = {
        name: '',
        subjectId: '',
        chapterId: '',
        date: '',
        duration: 60,
        remarks: ''
      }
      selectedQuizId.value = null
    }

    const openNewQuestionModal = (quizId = null) => {
      newQuestion.value = {
        quizId: quizId || '',
        statement: '',
        options: ['', '', '', ''],
        correctOption: 1
      }
      selectedQuestionId.value = null
      showNewQuestionModal.value = true
    }

    const closeQuestionModal = () => {
      showNewQuestionModal.value = false
      newQuestion.value = {
        quizId: '',
        statement: '',
        options: ['', '', '', ''],
        correctOption: 1
      }
      selectedQuestionId.value = null
    }

    const saveQuiz = async () => {
      try {
        if (selectedQuizId.value) {
          await updateQuiz()
        } else {
          await createQuiz()
        }
      } catch (err) {
        console.error('Error saving quiz:', err)
        alert('Failed to save quiz. Please try again.')
      }
    }

    const createQuiz = async () => {
      const quizData = {
        q_id: `QUIZ_${Date.now()}`,
        q_name: newQuiz.value.name,
        chp_id: newQuiz.value.chapterId,
        date_of_quiz: newQuiz.value.date,
        time_dur: newQuiz.value.duration,
        remarks: newQuiz.value.remarks
      }

      const response = await fetch('/api/quizzes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(quizData)
      })

      if (response.ok) {
        alert('Quiz created successfully!')
        closeQuizModal()
        await fetchQuizzes()
      } else {
        const error = await response.json()
        alert(`Failed to create quiz: ${error.error}`)
      }
    }

    const updateQuiz = async () => {
      const quizData = {
        q_name: newQuiz.value.name,
        date_of_quiz: newQuiz.value.date,
        time_dur: newQuiz.value.duration,
        remarks: newQuiz.value.remarks
      }

      const response = await fetch(`/api/quizzes/${selectedQuizId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(quizData)
      })

      if (response.ok) {
        alert('Quiz updated successfully!')
        closeQuizModal()
        await fetchQuizzes()
      } else {
        const error = await response.json()
        alert(`Failed to update quiz: ${error.error}`)
      }
    }

    const editQuiz = (quiz) => {
      const chapter = availableChapters.value.find(c => c.chp_id === quiz.chp_id);
      
      newQuiz.value = {
        name: quiz.q_name,
        subjectId: chapter ? chapter.sub_id : '',
        chapterId: quiz.chp_id,
        date: quiz.date_of_quiz,
        duration: quiz.time_dur,
        remarks: quiz.remarks || ''
      }
      selectedQuizId.value = quiz.q_id
      showNewQuizModal.value = true
    }

    const deleteQuiz = async (quizId) => {
      if (!confirm('Are you sure you want to delete this quiz? This will also delete all associated questions.')) {
        return
      }

      try {
        const response = await fetch(`/api/quizzes/${quizId}`, {
          method: 'DELETE'
        })

        if (response.ok) {
          alert('Quiz deleted successfully!')
          await fetchQuizzes()
        } else {
          const error = await response.json()
          alert(`Failed to delete quiz: ${error.error}`)
        }
      } catch (err) {
        console.error('Error deleting quiz:', err)
        alert('Failed to delete quiz. Please try again.')
      }
    }

    const saveQuestion = async () => {
      try {
        if (selectedQuestionId.value) {
          await updateQuestion()
        } else {
          await createQuestion()
        }
      } catch (err) {
        console.error('Error saving question:', err)
        alert('Failed to save question. Please try again.')
      }
    }

    const createQuestion = async () => {
      const questionData = {
        qsn_id: `QSN_${Date.now()}`,
        qsn_desc: newQuestion.value.statement,
        option_1: newQuestion.value.options[0],
        option_2: newQuestion.value.options[1],
        option_3: newQuestion.value.options[2],
        option_4: newQuestion.value.options[3],
        correct_option: newQuestion.value.correctOption
      }

      const response = await fetch(`/api/quizzes/${newQuestion.value.quizId}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(questionData)
      })

      if (response.ok) {
        alert('Question added successfully!')
        closeQuestionModal()
        await fetchQuizzes()
      } else {
        const error = await response.json()
        alert(`Failed to add question: ${error.error}`)
      }
    }

    const updateQuestion = async () => {
      const questionData = {
        qsn_desc: newQuestion.value.statement,
        option_1: newQuestion.value.options[0],
        option_2: newQuestion.value.options[1],
        option_3: newQuestion.value.options[2],
        option_4: newQuestion.value.options[3],
        correct_option: newQuestion.value.correctOption
      }

      const response = await fetch(`/api/questions/${selectedQuestionId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(questionData)
      })

      if (response.ok) {
        alert('Question updated successfully!')
        closeQuestionModal()
        await fetchQuizzes()
      } else {
        const error = await response.json()
        alert(`Failed to update question: ${error.error}`)
      }
    }

    const editQuestion = (question) => {
      newQuestion.value = {
        quizId: question.q_id,
        statement: question.qsn_desc || question.question_text,
        options: [
          question.option_1 || '',
          question.option_2 || '',
          question.option_3 || '',
          question.option_4 || ''
        ],
        correctOption: question.correct_option || 1
      }
      selectedQuestionId.value = question.qsn_id
      showNewQuestionModal.value = true
    }

    const deleteQuestion = async (questionId) => {
      if (!confirm('Are you sure you want to delete this question?')) {
        return
      }

      try {
        const response = await fetch(`/api/questions/${questionId}`, {
          method: 'DELETE'
        })

        if (response.ok) {
          alert('Question deleted successfully!')
          await fetchQuizzes()
        } else {
          const error = await response.json()
          alert(`Failed to delete question: ${error.error}`)
        }
      } catch (err) {
        console.error('Error deleting question:', err)
        alert('Failed to delete question. Please try again.')
      }
    }

    const saveAndAddAnother = async () => {
      await createQuestion()
      // Reset form but keep quiz ID
      const quizId = newQuestion.value.quizId
      newQuestion.value = {
        quizId: quizId,
        statement: '',
        options: ['', '', '', ''],
        correctOption: 1
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Not set'
      return new Date(dateString).toLocaleDateString()
    }

    // Lifecycle
    onMounted(async () => {
      try {
        await Promise.all([
          fetchQuizzes(),
          fetchSubjects(),
          fetchChapters()
        ])
      } catch (err) {
        console.error('Error during initial data load:', err)
      }
    })

    return {
      // State
      searchQuery,
      loading,
      subjectsLoading,
      chaptersLoading,
      error,
      subjectsError,
      chaptersError,
      quizzes,
      availableChapters,
      availableSubjects,
      
      // Modal states
      showNewQuizModal,
      showNewQuestionModal,
      selectedQuizId,
      selectedQuestionId,
      
      // Form data
      newQuiz,
      newQuestion,
      
      // Computed
      filteredQuizzes,
      chaptersForSelectedSubject,
      
      // Methods
      logout,
      openNewQuizModal,
      closeQuizModal,
      openNewQuestionModal,
      closeQuestionModal,
      saveQuiz,
      editQuiz,
      deleteQuiz,
      saveQuestion,
      editQuestion,
      deleteQuestion,
      saveAndAddAnother,
      formatDate
    }
  }
}
</script>

<style scoped>
/* Match AdminDashboard.vue styling exactly */
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 2rem;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.search-container {
  max-width: 300px;
  margin: 0 2rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  background: white;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3);
}

.welcome {
  font-weight: 600;
  color: white;
  font-size: 1.1rem;
}

/* Main Content */
.main-content {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.page-description {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0.5rem 0 0 0;
}

.btn-create {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
}

.btn-create:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

/* Loading Skeleton */
.skeleton-loader {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
}

.skeleton-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.skeleton-title {
  height: 24px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  border-radius: 12px;
  width: 60%;
  animation: shimmer 1.5s infinite;
}

.skeleton-actions {
  height: 36px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  border-radius: 18px;
  width: 80px;
  animation: shimmer 1.5s infinite;
}

.skeleton-content .skeleton-text {
  height: 16px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  border-radius: 8px;
  margin-bottom: 0.75rem;
  animation: shimmer 1.5s infinite;
}

.skeleton-content .skeleton-text:nth-child(1) { width: 100%; }
.skeleton-content .skeleton-text:nth-child(2) { width: 80%; }
.skeleton-content .skeleton-text:nth-child(3) { width: 60%; }

@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

/* Subject Cards Grid */
.subjects-grid {
  display: grid;
  gap: 2rem;
}

.subject-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.subject-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.subject-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.subject-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.subject-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.subject-name {
  color: #2d3748;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.subject-meta {
  color: #6c757d;
  font-size: 0.95rem;
  margin: 0.25rem 0 0 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.subject-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit, .btn-delete {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-size: 0.9rem;
}

.btn-edit {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.btn-delete {
  background: linear-gradient(135deg, #dc3545, #c82333);
}

.btn-edit:hover, .btn-delete:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

/* Quiz Details */
.quiz-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  color: #2d3748;
  font-weight: 500;
}

.detail-item i {
  color: #667eea;
  font-size: 1.1rem;
}

/* Questions Section */
.questions-section {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 1.5rem;
}

.questions-title {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.question-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 12px;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
}

.question-preview:hover {
  background: rgba(102, 126, 234, 0.1);
}

.question-number {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.question-text {
  flex: 1;
  color: #2d3748;
  font-weight: 500;
}

.question-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit-question, .btn-delete-question {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-size: 0.8rem;
}

.btn-edit-question {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.btn-delete-question {
  background: linear-gradient(135deg, #dc3545, #c82333);
}

.btn-edit-question:hover, .btn-delete-question:hover {
  transform: scale(1.1);
}

.more-questions {
  color: #6c757d;
  font-style: italic;
  text-align: center;
  padding: 0.75rem;
  background: rgba(108, 117, 125, 0.1);
  border-radius: 12px;
  margin-top: 0.75rem;
}

/* Card Footer */
.card-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding-top: 1.5rem;
  margin-top: 1.5rem;
}

.btn-add-question {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  justify-content: center;
  font-size: 0.95rem;
}

.btn-add-question:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: white;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  opacity: 0.7;
}

.empty-state h3 {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.empty-state p {
  font-size: 1.1rem;
  opacity: 0.8;
  margin-bottom: 2rem;
}

/* Error Alert */
.alert-danger {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
  color: #dc3545;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

/* Modal Container */
.modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1050; /* Ensure it's above other content */
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .search-container {
    margin: 0;
    max-width: 100%;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .subjects-grid .row {
    margin: 0;
  }
  
  .subjects-grid .col-lg-6 {
    padding: 0 0 1rem 0;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>
