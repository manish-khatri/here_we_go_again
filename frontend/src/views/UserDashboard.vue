<template>
  <div class="user-dashboard">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/user/dashboard" class="nav-link active">Home</router-link>
        <router-link to="/user/scores" class="nav-link">Scores</router-link>
        <router-link to="/user/summary" class="nav-link">Summary</router-link>
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
      <div class="welcome">Welcome User</div>
    </header>

    <main class="main-content">
      <h1>Upcoming Quizzes</h1>
      
      <div class="quizzes-table-container">
        <table class="quizzes-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>No. of Questions</th>
              <th>Date</th>
              <th>Duration (hh:mm)</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>05</td>
              <td>xx/xx/yyyy</td>
              <td>00:10</td>
              <td>
                <button @click="viewQuiz(1)" class="btn-view">View</button>
                <button @click="startQuiz(1)" class="btn-start">Start</button>
              </td>
            </tr>
            <tr>
              <td>2</td>
              <td>10</td>
              <td>xx/xx/yyyy</td>
              <td>00:10</td>
              <td>
                <button @click="viewQuiz(2)" class="btn-view">View</button>
                <button @click="startQuiz(2)" class="btn-start">Start</button>
              </td>
            </tr>
            <tr>
              <td>3</td>
              <td>15</td>
              <td>xx/xx/yyyy</td>
              <td>00:30</td>
              <td>
                <button @click="viewQuiz(3)" class="btn-view">View</button>
                <button @click="startQuiz(3)" class="btn-start">Start</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- View Quiz Modal -->
    <div v-if="showViewQuizModal" class="modal-overlay" @click="showViewQuizModal = false">
      <div class="modal-content" @click.stop>
        <h3>Quiz Details</h3>
        <div class="quiz-details">
          <div class="detail-item">
            <span class="detail-label">ID:</span>
            <span class="detail-value">{{ selectedQuiz.id }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Subject:</span>
            <span class="detail-value">{{ selectedQuiz.subject }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Chapter:</span>
            <span class="detail-value">{{ selectedQuiz.chapter }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Number of Questions:</span>
            <span class="detail-value">{{ selectedQuiz.questions }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Scheduled Date:</span>
            <span class="detail-value">{{ selectedQuiz.date }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Duration (hh:mm):</span>
            <span class="detail-value">{{ selectedQuiz.duration }}</span>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="showViewQuizModal = false" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const searchQuery = ref('')
    const showViewQuizModal = ref(false)
    const selectedQuiz = ref({})

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const viewQuiz = (quizId) => {
      // TODO: Fetch quiz details from API
      selectedQuiz.value = {
        id: quizId,
        subject: 'Mathematics',
        chapter: 'Random Variables',
        questions: '05',
        date: 'dd/mm/yyyy',
        duration: '00:10'
      }
      showViewQuizModal.value = true
    }

    const startQuiz = (quizId) => {
      // TODO: Navigate to quiz taking interface
      router.push(`/user/quiz/${quizId}`)
    }

    return {
      searchQuery,
      showViewQuizModal,
      selectedQuiz,
      logout,
      viewQuiz,
      startQuiz
    }
  }
}
</script>

<style scoped>
.user-dashboard {
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

.main-content h1 {
  color: #333;
  margin-bottom: 2rem;
}

.quizzes-table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.quizzes-table {
  width: 100%;
  border-collapse: collapse;
}

.quizzes-table th,
.quizzes-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.quizzes-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #333;
}

.quizzes-table tr:hover {
  background-color: #f8f9fa;
}

.btn-view,
.btn-start {
  padding: 0.5rem 1rem;
  margin: 0 0.25rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.3s;
}

.btn-view {
  background-color: #17a2b8;
  color: white;
}

.btn-view:hover {
  background-color: #138496;
}

.btn-start {
  background-color: #28a745;
  color: white;
}

.btn-start:hover {
  background-color: #218838;
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
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #333;
  text-align: center;
}

.quiz-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 600;
  color: #555;
}

.detail-value {
  color: #333;
}

.modal-actions {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

/* Responsive Design */
@media (max-width: 768px) {
  .quizzes-table {
    font-size: 0.875rem;
  }
  
  .quizzes-table th,
  .quizzes-table td {
    padding: 0.75rem 0.5rem;
  }
  
  .btn-view,
  .btn-start {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
  }
  
  .detail-item {
    flex-direction: column;
    gap: 0.25rem;
  }
}
</style> 