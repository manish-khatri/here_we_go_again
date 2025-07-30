<template>
  <div class="admin-dashboard">
    <!-- Header Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <div class="navbar-nav me-auto">
          <router-link to="/admin/dashboard" class="nav-link">
            <i class="bi bi-house me-2"></i>Home
          </router-link>
          <router-link to="/admin/quiz" class="nav-link active">
            <i class="bi bi-puzzle me-2"></i>Quiz
          </router-link>
          <router-link to="/admin/summary" class="nav-link">
            <i class="bi bi-graph-up me-2"></i>Summary
          </router-link>
        </div>
        <div class="d-flex align-items-center">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search..." 
            class="form-control search-input me-3"
          />
          <span class="navbar-text me-3">Welcome Admin</span>
          <button @click="logout" class="btn btn-outline-light">
            <i class="bi bi-box-arrow-right me-2"></i>Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container-fluid mt-4">
      <!-- Page Header -->
      <div class="page-header mb-4">
        <div class="header-content">
          <div class="header-text">
            <h1 class="page-title">
              <i class="bi bi-puzzle-fill"></i>Quiz Management
            </h1>
            <p class="page-description">Create and manage quizzes for all subjects</p>
          </div>
          <button @click="openNewQuizModal" class="btn btn-create">
            <i class="bi bi-plus-lg"></i>Add Quiz
          </button>
        </div>
      </div>

      <!-- Loading State with Skeleton -->
      <div v-if="loading" class="skeleton-loader">
        <div class="skeleton-card" v-for="n in 4" :key="n">
          <div class="skeleton-header">
            <div class="skeleton-title"></div>
            <div class="skeleton-actions"></div>
          </div>
          <div class="skeleton-content">
            <div class="skeleton-text" v-for="i in 3" :key="i"></div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        {{ error }}
      </div>
      
      <!-- Quiz Cards -->
      <div v-else class="subjects-grid">
        <div v-if="filteredQuizzes.length > 0" class="row g-4">
          <div class="col-lg-6" v-for="quiz in filteredQuizzes" :key="quiz.q_id">
            <div class="subject-card">
              <div class="card-header">
                <div class="subject-info">
                  <div class="subject-icon">
                    <i class="bi bi-puzzle-fill"></i>
                  </div>
                  <div>
                    <h4 class="subject-name">{{ quiz.q_name }}</h4>
                    <p class="subject-meta">
                      <span class="badge bg-primary me-2">{{ quiz.sub_id || 'No Subject' }}</span>
                      {{ quiz.questions?.length || 0 }} questions
                    </p>
                  </div>
                </div>
                <div class="subject-actions">
                  <button @click="editQuiz(quiz)" class="btn btn-edit" title="Edit Quiz">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button @click="deleteQuiz(quiz.q_id)" class="btn btn-delete" title="Delete Quiz">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </div>
              
              <div class="quiz-details">
                <div class="detail-item">
                  <i class="bi bi-calendar3"></i>
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
                <h6 class="questions-title">Questions ({{ quiz.questions.length }})</h6>
                <div class="questions-preview">
                  <div class="question-preview" v-for="(question, index) in quiz.questions.slice(0, 3)" :key="question.qsn_id">
                    <span class="question-number">{{ index + 1 }}</span>
                    <span class="question-text">{{ (question.qsn_desc || question.question_text || '').substring(0, 50) }}...</span>
                    <div class="question-actions">
                      <button @click="editQuestion(question)" class="btn-edit-question" title="Edit Question">
                        <i class="bi bi-pencil"></i>
                      </button>
                      <button @click="deleteQuestion(question.qsn_id)" class="btn-delete-question" title="Delete Question">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <div v-if="quiz.questions.length > 3" class="more-questions">
                    +{{ quiz.questions.length - 3 }} more questions
                  </div>
                </div>
              </div>

              <div class="card-footer">
                <button @click="openNewQuestionModal(quiz.q_id)" class="btn btn-add-question">
                  <i class="bi bi-plus-circle me-2"></i>Add Question
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-puzzle"></i>
          </div>
          <h3>No Quizzes Found</h3>
          <p>Create your first quiz to get started with question management.</p>
          <button @click="openNewQuizModal" class="btn btn-create">
            <i class="bi bi-plus-circle me-2"></i>Create Your First Quiz
          </button>
        </div>
      </div>
    </div>

    <!-- Quiz Modal -->
    <div v-if="showNewQuizModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-puzzle-fill me-2"></i>
              {{ selectedQuizId ? 'Edit Quiz' : 'Create New Quiz' }}
            </h5>
            <button type="button" class="btn-close" @click="closeQuizModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuiz" id="quizForm">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="quiz-name" class="form-label">Quiz Name</label>
                    <input type="text" 
                           id="quiz-name" 
                           class="form-control" 
                           v-model="newQuiz.name" 
                           placeholder="Enter quiz name"
                           required />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="chapter-select" class="form-label">Chapter</label>
                    <select id="chapter-select" class="form-select" v-model="newQuiz.chapterId" required>
                      <option value="">Select Chapter</option>
                      <option v-for="chapter in availableChapters" 
                              :key="chapter.chp_id" 
                              :value="chapter.chp_id">
                        {{ chapter.chp_name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="quiz-date" class="form-label">Quiz Date</label>
                    <input type="date" 
                           id="quiz-date" 
                           class="form-control" 
                           v-model="newQuiz.date" 
                           required />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="quiz-duration" class="form-label">Duration (minutes)</label>
                    <input type="number" 
                           id="quiz-duration" 
                           class="form-control" 
                           v-model="newQuiz.duration" 
                           min="1" 
                           placeholder="60"
                           required />
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label for="quiz-remarks" class="form-label">Remarks (Optional)</label>
                <textarea id="quiz-remarks" 
                          class="form-control" 
                          v-model="newQuiz.remarks" 
                          rows="3" 
                          placeholder="Additional notes about this quiz..."></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeQuizModal">Cancel</button>
            <button type="submit" form="quizForm" class="btn btn-primary">
              <i class="bi bi-check-circle me-2"></i>
              {{ selectedQuizId ? 'Update Quiz' : 'Create Quiz' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Modal -->
    <div v-if="showNewQuestionModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-question-circle-fill me-2"></i>
              {{ selectedQuestionId ? 'Edit Question' : 'Add New Question' }}
            </h5>
            <button type="button" class="btn-close" @click="closeQuestionModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuestion" id="questionForm">
              <div class="mb-3" v-if="!selectedQuestionId">
                <label for="question-quiz" class="form-label">Quiz</label>
                <select id="question-quiz" class="form-select" v-model="newQuestion.quizId" required>
                  <option value="">Select Quiz</option>
                  <option v-for="quiz in quizzes" 
                          :key="quiz.q_id" 
                          :value="quiz.q_id">
                    {{ quiz.q_name }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="question-statement" class="form-label">Question Statement</label>
                <textarea id="question-statement" 
                          class="form-control" 
                          v-model="newQuestion.statement" 
                          rows="3" 
                          placeholder="Enter the question statement here..."
                          required></textarea>
              </div>
              
              <!-- Answer Options -->
              <div class="mb-4">
                <label class="form-label">Answer Options</label>
                <div class="row">
                  <div class="col-md-6 mb-3" v-for="(option, index) in newQuestion.options" :key="index">
                    <div class="input-group">
                      <span class="input-group-text">{{ String.fromCharCode(65 + index) }}</span>
                      <input type="text" 
                             class="form-control" 
                             v-model="newQuestion.options[index]" 
                             :placeholder="'Option ' + String.fromCharCode(65 + index)"
                             required />
                    </div>
                  </div>
                </div>
                
                <div class="mt-3">
                  <label class="form-label">Correct Answer</label>
                  <div class="btn-group w-100" role="group">
                    <input type="radio" class="btn-check" :id="'option-' + (index + 1)" 
                           :value="index + 1" v-model="newQuestion.correctOption"
                           v-for="(option, index) in newQuestion.options" :key="'radio-' + index">
                    <label class="btn btn-outline-primary" :for="'option-' + (index + 1)"
                           v-for="(option, index) in newQuestion.options" :key="'label-' + index">
                      {{ String.fromCharCode(65 + index) }}
                    </label>
                  </div>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="question-explanation" class="form-label">Explanation (Optional)</label>
                <textarea id="question-explanation" 
                          class="form-control" 
                          v-model="newQuestion.explanation" 
                          rows="2" 
                          placeholder="Provide an explanation for the correct answer..."></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeQuestionModal">Cancel</button>
            <button type="button" 
                    @click="saveAndAddAnother" 
                    v-if="!selectedQuestionId"
                    class="btn btn-success">
              <i class="bi bi-plus-circle me-2"></i>Save & Add Another
            </button>
            <button type="submit" form="questionForm" class="btn btn-primary">
              <i class="bi bi-check-circle me-2"></i>
              {{ selectedQuestionId ? 'Update Question' : 'Save Question' }}
            </button>
          </div>
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
    const error = ref('')
    const quizzes = ref([])
    const availableChapters = ref([])
    
    // Modal states
    const showNewQuizModal = ref(false)
    const showNewQuestionModal = ref(false)
    const selectedQuizId = ref(null)
    const selectedQuestionId = ref(null)
    
    // Form data
    const newQuiz = ref({
      name: '',
      chapterId: '',
      date: '',
      duration: 60,
      remarks: ''
    })
    
    const newQuestion = ref({
      quizId: '',
      statement: '',
      options: ['', '', '', ''],
      correctOption: 1,
      explanation: ''
    })

    // Computed
    const filteredQuizzes = computed(() => {
      if (!searchQuery.value) return quizzes.value
      return quizzes.value.filter(quiz => 
        quiz.q_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        quiz.sub_id?.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
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
        
        const response = await fetch('/api/quizzes')
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

    const fetchChapters = async () => {
      try {
        const response = await fetch('/api/chapters')
        if (response.ok) {
          availableChapters.value = await response.json()
        }
      } catch (err) {
        console.error('Error fetching chapters:', err)
      }
    }

    const openNewQuizModal = () => {
      newQuiz.value = {
        name: '',
        chapterId: '',
        date: '',
        duration: 60,
        remarks: ''
      }
      selectedQuizId.value = null
      showNewQuizModal.value = true
    }

    const closeQuizModal = () => {
      showNewQuizModal.value = false
      newQuiz.value = {
        name: '',
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
        correctOption: 1,
        explanation: ''
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
        correctOption: 1,
        explanation: ''
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
      newQuiz.value = {
        name: quiz.q_name,
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
        correct_option: newQuestion.value.correctOption,
        explanation: newQuestion.value.explanation
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
        correct_option: newQuestion.value.correctOption,
        explanation: newQuestion.value.explanation
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
        correctOption: question.correct_option || 1,
        explanation: question.explanation || ''
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
        correctOption: 1,
        explanation: ''
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Not set'
      return new Date(dateString).toLocaleDateString()
    }

    // Lifecycle
    onMounted(async () => {
      await Promise.all([fetchQuizzes(), fetchChapters()])
    })

    return {
      // State
      searchQuery,
      loading,
      error,
      quizzes,
      availableChapters,
      
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

/* Navigation */
.navbar {
  background: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.navbar-nav .nav-link {
  color: #2d3748 !important;
  font-weight: 600;
  padding: 0.75rem 1.5rem !important;
  border-radius: 12px;
  transition: all 0.3s ease;
  margin: 0 0.25rem;
}

.navbar-nav .nav-link:hover,
.navbar-nav .nav-link.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.search-input {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid rgba(102, 126, 234, 0.2);
  border-radius: 25px;
  padding: 0.5rem 1rem;
  width: 250px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
}

.navbar-text {
  color: #2d3748 !important;
  font-weight: 600;
}

.btn-outline-light {
  border-color: rgba(102, 126, 234, 0.3);
  color: #667eea;
  font-weight: 600;
}

.btn-outline-light:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  color: white;
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

/* Responsive Design */
@media (max-width: 768px) {
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
