<template>
  <div class="quiz-taking">
    <!-- Header -->
    <header class="header">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="quiz-info">
              <h2 class="h4 mb-1">{{ quiz?.q_name || 'Quiz' }}</h2>
              <div class="quiz-meta d-flex gap-3">
                <span class="badge bg-primary-custom">
                  <i class="bi bi-question-circle me-1"></i>
                  Q{{ currentQuestionIndex + 1 }}/{{ questions.length }}
                </span>
                <span class="badge bg-warning text-dark">
                  <i class="bi bi-clock me-1"></i>
                  {{ formatTime(timeRemaining) }}
                </span>
              </div>
            </div>
          </div>
          <div class="col-md-4 text-end">
            <button @click="confirmExit" class="btn btn-outline-danger">
              <i class="bi bi-x-circle me-1"></i>
              Exit Quiz
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="container-fluid">
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary-custom" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="mt-3 text-muted">Loading quiz...</p>
        </div>
        
        <div v-else-if="error" class="alert alert-danger" role="alert">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          Error: {{ error }}
        </div>
        
        <div v-else-if="quiz && questions.length > 0" class="quiz-content">
          <div class="row">
            <div class="col-lg-8">
              <!-- Question Card -->
              <div class="card mb-4">
                <div class="card-header">
                  <h3 class="card-title mb-0">Question {{ currentQuestionIndex + 1 }}</h3>
                </div>
                <div class="card-body">
                  <div class="question-statement mb-4">
                    <p class="lead mb-0">{{ currentQuestion.statement }}</p>
                  </div>
                  
                  <!-- Options -->
                  <div class="options-section">
                    <h5 class="mb-3">Select your answer:</h5>
                    <div class="options">
                      <div 
                        v-for="(option, index) in currentQuestion.options" 
                        :key="index"
                        class="option-item mb-3"
                      >
                        <div class="form-check">
                          <input 
                            type="radio" 
                            :name="'question-' + currentQuestion.ques_id"
                            :value="(index + 1).toString()"
                            v-model="answers[currentQuestion.ques_id]"
                            class="form-check-input"
                            :id="'option-' + index"
                          />
                          <label class="form-check-label" :for="'option-' + index">
                            <strong>{{ index + 1 }})</strong> {{ option }}
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-lg-4">
              <!-- Navigation Card -->
              <div class="card">
                <div class="card-header">
                  <h5 class="card-title mb-0">Navigation</h5>
                </div>
                <div class="card-body">
                  <!-- Question Progress -->
                  <div class="mb-4">
                    <h6 class="mb-3">Question Progress</h6>
                    <div class="question-dots d-flex flex-wrap gap-1">
                      <button 
                        v-for="(question, index) in questions" 
                        :key="index"
                        :class="['btn btn-sm', { 
                          'btn-primary': index === currentQuestionIndex,
                          'btn-outline-success': answers[question.ques_id] && index !== currentQuestionIndex,
                          'btn-outline-secondary': !answers[question.ques_id] && index !== currentQuestionIndex
                        }]"
                        @click="goToQuestion(index)"
                      >
                        {{ index + 1 }}
                      </button>
                    </div>
                  </div>
                  
                  <!-- Navigation Buttons -->
                  <div class="d-grid gap-2">
                    <button 
                      @click="previousQuestion" 
                      :disabled="currentQuestionIndex === 0"
                      class="btn btn-outline-secondary"
                    >
                      <i class="bi bi-arrow-left me-1"></i>
                      Previous
                    </button>
                    
                    <button 
                      v-if="currentQuestionIndex < questions.length - 1"
                      @click="nextQuestion" 
                      class="btn btn-primary"
                    >
                      Save and Next
                      <i class="bi bi-arrow-right ms-1"></i>
                    </button>
                    
                    <button 
                      v-else
                      @click="submitQuiz" 
                      class="btn btn-success"
                    >
                      <i class="bi bi-check-circle me-1"></i>
                      Submit Quiz
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-5">
          <i class="bi bi-inbox display-6 text-muted"></i>
          <h4 class="mt-3 text-muted">No questions available</h4>
          <p class="text-muted">This quiz doesn't have any questions yet.</p>
          <button @click="$router.go(-1)" class="btn btn-secondary">
            <i class="bi bi-arrow-left me-1"></i>
            Go Back
          </button>
        </div>
      </div>
    </main>

    <!-- Exit Confirmation Modal -->
    <div v-if="showExitModal" class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Exit Quiz</h5>
            <button type="button" class="btn-close" @click="showExitModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to exit the quiz? Your progress will be lost.</p>
          </div>
          <div class="modal-footer">
            <button @click="showExitModal = false" class="btn btn-secondary">Cancel</button>
            <button @click="exitQuiz" class="btn btn-danger">Exit Quiz</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '../stores/quiz'

export default {
  name: 'QuizTaking',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const quizStore = useQuizStore()
    
    const quizId = route.params.quizId
    const quiz = ref(null)
    const questions = ref([])
    const currentQuestionIndex = ref(0)
    const answers = ref({})
    const loading = ref(true)
    const error = ref(null)
    const timeRemaining = ref(600) // 10 minutes in seconds
    const showExitModal = ref(false)
    const timer = ref(null)

    const currentQuestion = computed(() => {
      return questions.value[currentQuestionIndex.value] || {}
    })

    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const startTimer = () => {
      timer.value = setInterval(() => {
        if (timeRemaining.value > 0) {
          timeRemaining.value--
        } else {
          submitQuiz()
        }
      }, 1000)
    }

    const stopTimer = () => {
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
    }

    const loadQuiz = async () => {
      try {
        loading.value = true
        error.value = null
        
        const result = await quizStore.startQuiz(quizId)
        if (result.success) {
          quiz.value = result.quiz
          questions.value = result.quiz.questions || []
          startTimer()
        } else {
          error.value = result.error
        }
      } catch (err) {
        error.value = 'Failed to load quiz'
        console.error('Load quiz error:', err)
      } finally {
        loading.value = false
      }
    }

    const nextQuestion = () => {
      if (currentQuestionIndex.value < questions.value.length - 1) {
        currentQuestionIndex.value++
      }
    }

    const previousQuestion = () => {
      if (currentQuestionIndex.value > 0) {
        currentQuestionIndex.value--
      }
    }

    const goToQuestion = (index) => {
      if (index >= 0 && index < questions.value.length) {
        currentQuestionIndex.value = index
      }
    }

    const submitQuiz = async () => {
      if (confirm('Are you sure you want to submit the quiz?')) {
        try {
          const result = await quizStore.submitQuizScore(quizId, answers.value)
          if (result.success) {
            alert(`Quiz submitted! Your score: ${result.score.score}%`)
            router.push('/user/dashboard')
          } else {
            alert('Failed to submit quiz: ' + result.error)
          }
        } catch (err) {
          alert('Failed to submit quiz')
          console.error('Submit quiz error:', err)
        }
      }
    }

    const confirmExit = () => {
      showExitModal.value = true
    }

    const exitQuiz = () => {
      stopTimer()
      router.push('/user/dashboard')
    }

    onMounted(() => {
      loadQuiz()
    })

    onUnmounted(() => {
      stopTimer()
    })

    return {
      quiz,
      questions,
      currentQuestionIndex,
      currentQuestion,
      answers,
      loading,
      error,
      timeRemaining,
      showExitModal,
      formatTime,
      nextQuestion,
      previousQuestion,
      goToQuestion,
      submitQuiz,
      confirmExit,
      exitQuiz
    }
  }
}
</script>

<style scoped>
.quiz-taking {
  min-height: 100vh;
  background-color: var(--gray-100);
}

.header {
  background: var(--white);
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-bottom: 1px solid var(--gray-200);
}

.quiz-info h2 {
  margin: 0;
  color: var(--text-dark);
}

.quiz-meta {
  display: flex;
  gap: 2rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--text-light);
}

.question-counter {
  font-weight: 600;
}

.timer {
  font-weight: 600;
  color: var(--danger);
}

.exit-btn {
  background: var(--danger);
  color: var(--white);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.exit-btn:hover {
  background: #c82333;
}

.main-content {
  padding: 2rem 0;
}

.loading, .error, .no-questions {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.loading {
  color: var(--primary-blue);
}

.error {
  color: var(--danger);
}

.quiz-content {
  background: var(--white);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.question-section {
  margin-bottom: 2rem;
}

.question-section h3 {
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.question-statement {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text-dark);
  padding: 1rem;
  background: var(--lighter-blue);
  border-radius: 8px;
  border-left: 4px solid var(--primary-blue);
}

.options-section {
  margin-bottom: 2rem;
}

.options-section h4 {
  color: var(--text-dark);
  margin-bottom: 1rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 2px solid var(--gray-300);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option-item:hover {
  border-color: var(--primary-blue);
  background: var(--lighter-blue);
}

.option-radio {
  margin-right: 1rem;
  transform: scale(1.2);
}

.option-text {
  font-size: 1rem;
  color: var(--text-dark);
}

.navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid var(--gray-300);
}

.question-dots {
  display: flex;
  gap: 0.5rem;
}

.dot {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-300);
  color: var(--text-dark);
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.dot.active {
  background: var(--primary-blue);
  color: var(--white);
}

.dot.answered {
  background: var(--success);
  color: var(--white);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--primary-blue);
  color: var(--white);
}

.btn-secondary {
  background: var(--gray-300);
  color: var(--text-dark);
}

.btn-success {
  background: var(--success);
  color: var(--white);
}

.btn-danger {
  background: var(--danger);
  color: var(--white);
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: var(--white);
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-bottom: 1rem;
  color: var(--text-dark);
}

.modal-content p {
  margin-bottom: 1.5rem;
  color: var(--text-light);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .quiz-meta {
    justify-content: center;
  }
  
  .navigation {
    flex-direction: column;
    gap: 1rem;
  }
  
  .question-dots {
    order: -1;
  }
}
</style>