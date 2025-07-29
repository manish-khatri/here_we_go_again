<template>
  <div class="quiz-taking">
    <div class="quiz-header">
      <div class="question-info">
        <span class="question-number">QNo. {{ currentQuestion }}/{{ totalQuestions }}</span>
      </div>
      <div class="timer">
        <span class="timer-text">{{ formatTime(timeRemaining) }}</span>
      </div>
    </div>

    <div class="quiz-content">
      <div class="question-container">
        <div class="question-statement">
          <p>{{ currentQuestionData.statement }}</p>
        </div>

        <div class="options-container">
          <div 
            v-for="(option, index) in currentQuestionData.options" 
            :key="index"
            class="option-item"
            :class="{ selected: selectedOption === index + 1 }"
            @click="selectOption(index + 1)"
          >
            <input 
              type="radio" 
              :id="`option-${index + 1}`" 
              :name="`question-${currentQuestion}`" 
              :value="index + 1"
              :checked="selectedOption === index + 1"
              @change="selectOption(index + 1)"
            />
            <label :for="`option-${index + 1}`">
              {{ index + 1 }}) {{ option }}
            </label>
          </div>
        </div>
      </div>

      <div class="quiz-actions">
        <button @click="saveAndNext" class="btn btn-primary">Save and Next</button>
        <button @click="submitQuiz" class="btn btn-secondary">Submit</button>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showSubmitModal" class="modal-overlay" @click="showSubmitModal = false">
      <div class="modal-content" @click.stop>
        <h3>Submit Quiz</h3>
        <p>Are you sure you want to submit the quiz? This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="confirmSubmit" class="btn btn-primary">Yes, Submit</button>
          <button @click="showSubmitModal = false" class="btn btn-secondary">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'QuizTaking',
  setup() {
    const router = useRouter()
    const route = useRoute()
    
    const currentQuestion = ref(1)
    const totalQuestions = ref(15)
    const timeRemaining = ref(13 * 60 + 52) // 13 minutes 52 seconds in seconds
    const selectedOption = ref(null)
    const showSubmitModal = ref(false)
    
    // Mock question data - replace with API call
    const currentQuestionData = ref({
      statement: "What is the primary purpose of CSS classes in web development?",
      options: [
        "To create animations and transitions",
        "To style and format HTML elements",
        "To handle user interactions",
        "To store data in the browser"
      ]
    })

    let timerInterval = null

    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }

    const selectOption = (optionNumber) => {
      selectedOption.value = optionNumber
    }

    const saveAndNext = () => {
      // TODO: Save current answer
      console.log('Saving answer:', selectedOption.value)
      
      if (currentQuestion.value < totalQuestions.value) {
        currentQuestion.value++
        selectedOption.value = null
        // TODO: Load next question from API
      } else {
        // Last question, show submit option
        showSubmitModal.value = true
      }
    }

    const submitQuiz = () => {
      showSubmitModal.value = true
    }

    const confirmSubmit = () => {
      // TODO: Submit quiz to backend
      console.log('Submitting quiz...')
      showSubmitModal.value = false
      router.push('/user/scores')
    }

    const startTimer = () => {
      timerInterval = setInterval(() => {
        if (timeRemaining.value > 0) {
          timeRemaining.value--
        } else {
          // Time's up, auto-submit
          clearInterval(timerInterval)
          confirmSubmit()
        }
      }, 1000)
    }

    onMounted(() => {
      startTimer()
      // TODO: Load quiz data from API using route.params.quizId
    })

    onUnmounted(() => {
      if (timerInterval) {
        clearInterval(timerInterval)
      }
    })

    return {
      currentQuestion,
      totalQuestions,
      timeRemaining,
      selectedOption,
      currentQuestionData,
      showSubmitModal,
      formatTime,
      selectOption,
      saveAndNext,
      submitQuiz,
      confirmSubmit
    }
  }
}
</script>

<style scoped>
.quiz-taking {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 2rem;
}

.quiz-header {
  background: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.question-info {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.timer {
  background: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  font-weight: bold;
  font-size: 1.1rem;
}

.quiz-content {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.question-container {
  margin-bottom: 2rem;
}

.question-statement {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  border-left: 4px solid #667eea;
}

.question-statement p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
  margin: 0;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-item:hover {
  border-color: #667eea;
  background-color: #f8f9fa;
}

.option-item.selected {
  border-color: #667eea;
  background-color: #e3f2fd;
}

.option-item input[type="radio"] {
  margin-right: 1rem;
  transform: scale(1.2);
}

.option-item label {
  flex: 1;
  cursor: pointer;
  font-size: 1rem;
  color: #333;
  margin: 0;
}

.quiz-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  min-width: 150px;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover {
  background-color: #5a6fd8;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
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
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.modal-actions .btn {
  min-width: 120px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .quiz-taking {
    padding: 1rem;
  }
  
  .quiz-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .quiz-content {
    padding: 1rem;
  }
  
  .question-statement {
    padding: 1rem;
  }
  
  .option-item {
    padding: 0.75rem;
  }
  
  .quiz-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style> 