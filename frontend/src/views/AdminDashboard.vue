<template>
  <div class="admin-dashboard">
    <!-- Navigation Header -->
    <header class="header">
      <nav class="nav">
        <router-link to="/admin/dashboard" class="nav-link active">Home</router-link>
        <router-link to="/admin/quiz" class="nav-link">Quiz</router-link>
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
      <h1>Subject Management</h1>
      
      <div v-if="quizStore.loading" class="loading">
        Loading subjects...
      </div>
      
      <div v-else-if="quizStore.error" class="error">
        Error: {{ quizStore.error }}
      </div>
      
      <div v-else class="subjects-container">
        <div v-for="subject in filteredSubjects" :key="subject.sub_id" class="subject-card">
          <h3>{{ subject.sub_name }}</h3>
          <table class="subject-table">
            <thead>
              <tr>
                <th>Chapter</th>
                <th>No. of Questions</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="chapter in subject.chapters" :key="chapter.chp_id">
                <td>{{ chapter.chp_name }}</td>
                <td>{{ chapter.questionCount || 0 }}</td>
                <td>
                  <button @click="editChapter(chapter)" class="btn-edit">Edit</button>
                  <button @click="deleteChapter(chapter.chp_id)" class="btn-delete">Delete</button>
                </td>
              </tr>
              <tr v-if="subject.chapters.length === 0">
                <td colspan="3" class="no-data">No chapters available</td>
              </tr>
            </tbody>
          </table>
          <button @click="showNewChapterModal = true; selectedSubjectId = subject.sub_id" class="btn-add-chapter">+ Chapter</button>
        </div>
        
        <div v-if="filteredSubjects.length === 0" class="no-subjects">
          <p>No subjects available. Create your first subject!</p>
        </div>
      </div>

      <p class="note">All subjects here...</p>

      <!-- Add New Subject Button -->
      <button @click="showNewSubjectModal = true" class="btn-add-subject">+ New Subject</button>
    </main>

    <!-- New Subject Modal -->
    <div v-if="showNewSubjectModal" class="modal-overlay" @click="showNewSubjectModal = false">
      <div class="modal-content" @click.stop>
        <h3>New Subject</h3>
        <form @submit.prevent="addNewSubject" class="modal-form">
          <div class="form-group">
            <label for="subject-id">Subject ID</label>
            <input type="text" id="subject-id" v-model="newSubject.sub_id" required />
          </div>
          <div class="form-group">
            <label for="subject-name">Name</label>
            <input type="text" id="subject-name" v-model="newSubject.name" required />
          </div>
          <div class="form-group">
            <label for="subject-description">Description</label>
            <textarea id="subject-description" v-model="newSubject.description" required></textarea>
          </div>
          <p class="note">Notes may include more input Fields...</p>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="showNewSubjectModal = false" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- New Chapter Modal -->
    <div v-if="showNewChapterModal" class="modal-overlay" @click="showNewChapterModal = false">
      <div class="modal-content" @click.stop>
        <h3>New Chapter</h3>
        <form @submit.prevent="addNewChapter" class="modal-form">
          <div class="form-group">
            <label for="chapter-id">Chapter ID</label>
            <input type="text" id="chapter-id" v-model="newChapter.chp_id" required />
          </div>
          <div class="form-group">
            <label for="chapter-name">Name</label>
            <input type="text" id="chapter-name" v-model="newChapter.name" required />
          </div>
          <div class="form-group">
            <label for="chapter-description">Description</label>
            <textarea id="chapter-description" v-model="newChapter.description" required></textarea>
          </div>
          <p class="note">Note: may include more input fields...</p>
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <button type="button" @click="showNewChapterModal = false" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
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
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const quizStore = useQuizStore()
    const searchQuery = ref('')
    const showNewSubjectModal = ref(false)
    const showNewChapterModal = ref(false)
    const selectedSubjectId = ref(null)
    
    const newSubject = ref({
      sub_id: '',
      name: '',
      description: ''
    })
    
    const newChapter = ref({
      chp_id: '',
      name: '',
      description: ''
    })

    const filteredSubjects = computed(() => {
      if (!searchQuery.value) return quizStore.subjects
      return quizStore.subjects.filter(subject => 
        subject.sub_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        subject.sub_id.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const addNewSubject = async () => {
      const result = await quizStore.addSubject(newSubject.value)
      if (result.success) {
        showNewSubjectModal.value = false
        newSubject.value = { sub_id: '', name: '', description: '' }
      } else {
        alert('Failed to add subject: ' + result.error)
      }
    }

    const addNewChapter = async () => {
      if (!selectedSubjectId.value) {
        alert('No subject selected')
        return
      }
      
      const result = await quizStore.addChapter(selectedSubjectId.value, newChapter.value)
      if (result.success) {
        showNewChapterModal.value = false
        newChapter.value = { chp_id: '', name: '', description: '' }
        selectedSubjectId.value = null
      } else {
        alert('Failed to add chapter: ' + result.error)
      }
    }

    const editChapter = (chapter) => {
      // TODO: Implement edit chapter functionality
      console.log('Edit chapter:', chapter)
    }

    const deleteChapter = async (chapterId) => {
      if (confirm('Are you sure you want to delete this chapter?')) {
        // TODO: Implement delete chapter functionality
        console.log('Delete chapter:', chapterId)
      }
    }

    onMounted(async () => {
      await quizStore.fetchSubjects()
    })

    return {
      searchQuery,
      showNewSubjectModal,
      showNewChapterModal,
      selectedSubjectId,
      newSubject,
      newChapter,
      authStore,
      quizStore,
      filteredSubjects,
      logout,
      addNewSubject,
      addNewChapter,
      editChapter,
      deleteChapter
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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

.subjects-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.subject-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.subject-card h3 {
  color: #333;
  margin-bottom: 1rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.subject-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.subject-table th,
.subject-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.subject-table th {
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

.btn-add-chapter {
  background-color: #667eea;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-add-subject {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
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

.loading, .error {
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

.no-data {
  text-align: center;
  color: #666;
  font-style: italic;
}

.no-subjects {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-style: italic;
}
</style> 