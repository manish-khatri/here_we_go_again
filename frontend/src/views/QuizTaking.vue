<template>
  <div class="quiz-taking">
    <!-- Header -->
    <header class="header">
      <div class="quiz-info">
        <h2>{{ quiz?.q_name || 'Quiz' }}</h2>
        <div class="quiz-meta">
          <span class="question-counter">QNo. {{ currentQuestionIndex + 1 }}/{{ questions.length }}</span>
          <span class="timer">{{ formatTime(timeRemaining) }}</span>
        </div>
      </div>
      <button @click="confirmExit" class="exit-btn">Exit Quiz</button>
    </header>

    <main class="main-content">
      <div v-if="loading" class="loading">
        Loading quiz...
      </div>
      
      <div v-else-if="error" class="error">
        Error: {{ error }}
      </div>
      
      <div v-else-if="quiz && questions.length > 0" class="quiz-content">
        <!-- Question -->
        <div class="question-section">
          <h3>Question {{ currentQuestionIndex + 1 }}</h3>
          <div class="question-statement">
            {{ currentQuestion.statement }}
          </div>
        </div>

        <!-- Options -->
        <div class="options-section">
          <h4>Select your answer:</h4>
          <div class="options">
            <label 
              v-for="(option, index) in currentQuestion.options" 
              :key="index"
              class="option-item"
            >
              <input 
                type="radio" 
                :name="'question-' + currentQuestion.ques_id"
                :value="(index + 1).toString()"
                v-model="answers[currentQuestion.ques_id]"
                class="option-radio"
              />
              <span class="option-text">{{ index + 1 }}) {{ option }}</span>
            </label>
          </div>
        </div>

        <!-- Navigation -->
        <div class="navigation">
          <button 
            @click="previousQuestion" 
            :disabled="currentQuestionIndex === 0"
            class="btn btn-secondary"
          >
            Previous
          </button>
          
          <div class="question-dots">
            <span 
              v-for="(question, index) in questions" 
              :key="index"
              :class="['dot', { 
                'active': index === currentQuestionIndex,
                'answered': answers[question.ques_id]
              }]"
              @click="goToQuestion(index)"
            >
              {{ index + 1 }}
            </span>
          </div>
          
          <button 
            v-if="currentQuestionIndex < questions.length - 1"
            @click="nextQuestion" 
            class="btn btn-primary"
          >
            Save and Next
          </button>
          
          <button 
            v-else
            @click="submitQuiz" 
            class="btn btn-success"
          >
            Submit Quiz
          </button>
        </div>
      </div>
      
      <div v-else class="no-questions">
        <p>No questions available for this quiz.</p>
        <button @click="$router.go(-1)" class="btn btn-secondary">Go Back</button>
      </div>
    </main>

    <!-- Exit Confirmation Modal -->
    <div v-if="showExitModal" class="modal-overlay" @click="showExitModal = false">
      <div class="modal-content" @click.stop>
        <h3>Exit Quiz?</h3>
        <p>Are you sure you want to exit? Your progress will be lost.</p>
        <div class="modal-actions">
          <button @click="exitQuiz" class="btn btn-danger">Exit</button>
          <button @click="showExitModal = false" class="btn btn-secondary">Cancel</button>
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

.quiz-info h2 {
  margin: 0;
  color: #333;
}

.quiz-meta {
  display: flex;
  gap: 2rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #666;
}

.question-counter {
  font-weight: 600;
}

.timer {
  font-weight: 600;
  color: #dc3545;
}

.exit-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
}

.main-content {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.loading, .error, .no-questions {
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

.quiz-content {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.question-section {
  margin-bottom: 2rem;
}

.question-section h3 {
  color: #333;
  margin-bottom: 1rem;
}

.question-statement {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.options-section {
  margin-bottom: 2rem;
}

.options-section h4 {
  color: #333;
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
  border: 2px solid #e9ecef;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-item:hover {
  border-color: #667eea;
  background: #f8f9fa;
}

.option-radio {
  margin-right: 1rem;
  transform: scale(1.2);
}

.option-text {
  font-size: 1rem;
  color: #333;
}

.navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
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
  background: #e9ecef;
  color: #666;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.3s;
}

.dot.active {
  background: #667eea;
  color: white;
}

.dot.answered {
  background: #28a745;
  color: white;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
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
  background: white;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.modal-content h3 {
  margin-bottom: 1rem;
  color: #333;
}

.modal-content p {
  margin-bottom: 1.5rem;
  color: #666;
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