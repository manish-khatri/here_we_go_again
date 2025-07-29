<template>
  <div class="admin-quiz">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/admin/dashboard" class="nav-link">Home</router-link>
        <router-link to="/admin/quiz" class="nav-link active">Quiz</router-link>
        <router-link to="/admin/summary" class="nav-link">Summary</router-link>
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
      <div class="welcome">Welcome Admin</div>
    </header>

    <main class="main-content">
      <div class="quiz-header">
        <h1>Quiz Management</h1>
        <button @click="showNewQuizModal = true" class="btn-add-quiz">+ New Quiz</button>
      </div>
      
      <!-- Quiz Tables -->
      <div class="quizzes-container">
        <!-- Quiz 1 -->
        <div class="quiz-card">
          <h3>Quiz1 (CSS)</h3>
          <table class="quiz-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Q-Title</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>Classes</td>
                <td>
                  <button class="btn-edit">Edit</button>
                  <button class="btn-delete">Delete</button>
                </td>
              </tr>
              <tr>
                <td>2</td>
                <td>Internal styles</td>
                <td>
                  <button class="btn-edit">Edit</button>
                  <button class="btn-delete">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button @click="showNewQuestionModal = true" class="btn-add-question">+ Question</button>
        </div>

        <!-- Quiz 2 -->
        <div class="quiz-card">
          <h3>Quiz2 (HTML)</h3>
          <table class="quiz-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Q-Title</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>&lt;b&gt; element</td>
                <td>
                  <button class="btn-edit">Edit</button>
                  <button class="btn-delete">Delete</button>
                </td>
              </tr>
              <tr>
                <td>2</td>
                <td>&lt;h&gt; element</td>
                <td>
                  <button class="btn-edit">Edit</button>
                  <button class="btn-delete">Delete</button>
                </td>
              </tr>
              <tr>
                <td>3</td>
                <td>&lt;form&gt; element</td>
                <td>
                  <button class="btn-edit">Edit</button>
                  <button class="btn-delete">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
          <button @click="showNewQuestionModal = true" class="btn-add-question">+ Question</button>
        </div>
      </div>

      <p class="note">All quizzes here...</p>
    </main>

    <!-- New Quiz Modal -->
    <div v-if="showNewQuizModal" class="modal-overlay" @click="showNewQuizModal = false">
      <div class="modal-content" @click.stop>
        <h3>New Quiz</h3>
        <form @submit.prevent="addNewQuiz" class="modal-form">
          <div class="form-group">
            <label for="chapter-id">Chapter ID</label>
            <input type="text" id="chapter-id" v-model="newQuiz.chapterId" required />
          </div>
          <div class="form-group">
            <label for="quiz-date">Date</label>
            <input type="date" id="quiz-date" v-model="newQuiz.date" required />
          </div>
          <div class="form-group">
            <label for="quiz-duration">Duration</label>
            <input type="time" id="quiz-duration" v-model="newQuiz.duration" required />
          </div>
          <p class="note">Note: may include more input fields...</p>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="showNewQuizModal = false" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- New Question Modal -->
    <div v-if="showNewQuestionModal" class="modal-overlay" @click="showNewQuestionModal = false">
      <div class="modal-content large-modal" @click.stop>
        <h3>New Question</h3>
        <form @submit.prevent="addNewQuestion" class="modal-form">
          <div class="form-group">
            <label for="question-chapter-id">Chapter ID</label>
            <input type="text" id="question-chapter-id" v-model="newQuestion.chapterId" required />
          </div>
          <div class="form-group">
            <label for="question-title">Question Title</label>
            <input type="text" id="question-title" v-model="newQuestion.title" required />
          </div>
          <div class="form-group">
            <label for="question-statement">Question Statement</label>
            <textarea id="question-statement" v-model="newQuestion.statement" required></textarea>
          </div>
          
          <!-- Single Option Correct Section -->
          <div class="options-section">
            <h4>Single Option Correct</h4>
            <div class="options-grid">
              <div class="form-group">
                <label for="option-1">Option 1</label>
                <input type="text" id="option-1" v-model="newQuestion.options[0]" required />
              </div>
              <div class="form-group">
                <label for="option-2">Option 2</label>
                <input type="text" id="option-2" v-model="newQuestion.options[1]" required />
              </div>
              <div class="form-group">
                <label for="option-3">Option 3</label>
                <input type="text" id="option-3" v-model="newQuestion.options[2]" required />
              </div>
              <div class="form-group">
                <label for="option-4">Option 4</label>
                <input type="text" id="option-4" v-model="newQuestion.options[3]" required />
              </div>
            </div>
            <div class="form-group">
              <label for="correct-option">Correct option</label>
              <input 
                type="number" 
                id="correct-option" 
                v-model="newQuestion.correctOption" 
                min="1" 
                max="4" 
                required 
              />
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save and Next</button>
            <button type="button" @click="showNewQuestionModal = false" class="btn btn-secondary">Close</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'AdminQuiz',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const showNewQuizModal = ref(false)
    const showNewQuestionModal = ref(false)
    
    const newQuiz = ref({
      chapterId: '',
      date: '',
      duration: ''
    })
    
    const newQuestion = ref({
      chapterId: '',
      title: '',
      statement: '',
      options: ['', '', '', ''],
      correctOption: 2
    })

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const addNewQuiz = () => {
      // TODO: Implement add quiz logic
      console.log('Adding new quiz:', newQuiz.value)
      showNewQuizModal.value = false
      newQuiz.value = { chapterId: '', date: '', duration: '' }
    }

    const addNewQuestion = () => {
      // TODO: Implement add question logic
      console.log('Adding new question:', newQuestion.value)
      showNewQuestionModal.value = false
      newQuestion.value = {
        chapterId: '',
        title: '',
        statement: '',
        options: ['', '', '', ''],
        correctOption: 2
      }
    }

    return {
      searchQuery,
      showNewQuizModal,
      showNewQuestionModal,
      newQuiz,
      newQuestion,
      logout,
      addNewQuiz,
      addNewQuestion
    }
  }
}
</script>

<style scoped>
.admin-quiz {
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

.quiz-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.quiz-header h1 {
  color: #333;
  margin: 0;
}

.btn-add-quiz {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
}

.quizzes-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.quiz-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.quiz-card h3 {
  color: #333;
  margin-bottom: 1rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.quiz-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.quiz-table th,
.quiz-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.quiz-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.btn-edit,
.btn-delete {
  padding: 0.25rem 0.5rem;
  margin: 0 0.25rem;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-edit {
  background-color: #28a745;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.btn-add-question {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.875rem;
}

.note {
  color: #666;
  font-style: italic;
  margin: 1rem 0;
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.large-modal {
  max-width: 700px;
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #333;
}

.modal-form .form-group {
  margin-bottom: 1rem;
}

.modal-form label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.modal-form input,
.modal-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.modal-form textarea {
  resize: vertical;
  min-height: 100px;
}

.options-section {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.options-section h4 {
  color: #333;
  margin-bottom: 1rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}
</style> 