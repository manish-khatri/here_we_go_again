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
      <div class="page-header">
        <div class="row align-items-center">
          <div class="col">
            <h1 class="page-title">
              <i class="bi bi-collection me-3"></i>Subject Management
            </h1>
            <p class="page-subtitle text-muted">Manage your subjects and chapters efficiently</p>
          </div>
          <div class="col-auto">
            <button @click="showNewSubjectModal = true" class="btn btn-primary btn-lg">
              <i class="bi bi-plus-circle me-2"></i>Add Subject
            </button>
          </div>
        </div>
      </div>
      
      <div v-if="quizStore.loading" class="loading-state">
        <div class="loading-content">
          <div class="loading-spinner">
            <div class="spinner"></div>
          </div>
          <h4 class="loading-text">Loading Subjects</h4>
          <p class="loading-subtitle">Please wait while we fetch your data...</p>
        </div>
      </div>
      
      <div v-else-if="quizStore.error" class="error-state">
        <div class="alert alert-danger border-0 shadow-sm" role="alert">
          <div class="d-flex align-items-center">
            <i class="bi bi-exclamation-triangle-fill me-3 fs-4"></i>
            <div>
              <h6 class="mb-1">Something went wrong!</h6>
              <small>{{ quizStore.error }}</small>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="subjects-section">
        <div class="row g-4" v-if="filteredSubjects.length > 0">
          <div class="col-xl-4 col-lg-6 col-md-6" v-for="subject in filteredSubjects" :key="subject.sub_id">
            <div class="subject-card">
              <div class="subject-header">
                <div class="subject-info">
                  <div class="subject-icon">
                    <i class="bi bi-book"></i>
                  </div>
                  <div>
                    <h5 class="subject-title">{{ subject.sub_name }}</h5>
                    <p class="subject-meta">{{ subject.chapters?.length || 0 }} chapters</p>
                  </div>
                </div>
                <div class="subject-actions">
                  <button @click="openNewChapterModal(subject.sub_id)" 
                          class="btn btn-primary btn-sm">
                    <i class="bi bi-plus"></i>
                  </button>
                </div>
              </div>
              
              <div class="chapters-list">
                <div v-if="subject.chapters?.length > 0">
                  <div class="chapter-item" v-for="chapter in subject.chapters" :key="chapter.chp_id">
                    <div class="chapter-info">
                      <div class="chapter-name">{{ chapter.chp_name }}</div>
                      <div class="chapter-desc">{{ chapter.chp_desc }}</div>
                    </div>
                    <div class="chapter-meta">
                      <span class="question-count">{{ chapter.questionCount || 0 }}</span>
                      <div class="chapter-actions">
                        <button @click="editChapter(chapter)" class="action-btn edit-btn">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button @click="deleteChapter(chapter.chp_id)" class="action-btn delete-btn">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-chapters">
                  <i class="bi bi-inbox"></i>
                  <span>No chapters yet</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <div class="empty-content">
            <div class="empty-icon">
              <i class="bi bi-collection"></i>
            </div>
            <h3 class="empty-title">No Subjects Found</h3>
            <p class="empty-subtitle">Get started by creating your first subject</p>
            <button @click="showNewSubjectModal = true" class="btn btn-primary btn-lg">
              <i class="bi bi-plus-circle me-2"></i>Create Subject
            </button>
          </div>
        </div>
      </div>
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

    <!-- New/Edit Chapter Modal -->
    <div v-if="showNewChapterModal" class="modal-overlay" @click="closeChapterModal">
      <div class="modal-content" @click.stop>
        <h3>{{ selectedChapterId ? 'Edit Chapter' : 'New Chapter' }}</h3>
        <form @submit.prevent="saveChapter" class="modal-form">
          <div class="form-group">
            <label for="chapter-id">Chapter ID</label>
            <input 
              type="text" 
              id="chapter-id" 
              v-model="newChapter.chp_id" 
              :disabled="selectedChapterId" 
              required 
            />
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
            <button type="submit" class="btn btn-primary">
              {{ selectedChapterId ? 'Update' : 'Save' }}
            </button>
            <button type="button" @click="closeChapterModal" class="btn btn-secondary">Cancel</button>
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
    const selectedChapterId = ref(null)
    
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
        closeChapterModal()
      } else {
        alert('Failed to add chapter: ' + result.error)
      }
    }

    const updateChapter = async () => {
      try {
        const response = await fetch(`/api/chapters/${selectedChapterId.value}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            chp_name: newChapter.value.name,
            chp_desc: newChapter.value.description
          })
        })

        if (response.ok) {
          alert('Chapter updated successfully!')
          closeChapterModal()
          // Refresh the subjects list
          await quizStore.fetchSubjects()
        } else {
          const error = await response.json()
          alert(`Failed to update chapter: ${error.error}`)
        }
      } catch (error) {
        console.error('Error updating chapter:', error)
        alert('Failed to update chapter. Please try again.')
      }
    }

    const saveChapter = async () => {
      if (selectedChapterId.value) {
        await updateChapter()
      } else {
        await addNewChapter()
      }
    }

    const closeChapterModal = () => {
      showNewChapterModal.value = false
      newChapter.value = { chp_id: '', name: '', description: '' }
      selectedSubjectId.value = null
      selectedChapterId.value = null
    }

    const openNewChapterModal = (subjectId) => {
      // Clear any existing data
      newChapter.value = { chp_id: '', name: '', description: '' }
      selectedChapterId.value = null
      selectedSubjectId.value = subjectId
      showNewChapterModal.value = true
    }

    const editChapter = (chapter) => {
      // Open edit modal with chapter data
      newChapter.value = {
        chp_id: chapter.chp_id,
        name: chapter.chp_name,
        description: chapter.chp_desc
      }
      selectedChapterId.value = chapter.chp_id
      showNewChapterModal.value = true
    }

    const deleteChapter = async (chapterId) => {
      if (confirm('Are you sure you want to delete this chapter? This will also delete all associated quizzes and questions.')) {
        try {
          const response = await fetch(`/api/chapters/${chapterId}`, {
            method: 'DELETE'
          })

          if (response.ok) {
            alert('Chapter deleted successfully!')
            // Refresh the subjects list
            await quizStore.fetchSubjects()
          } else {
            const error = await response.json()
            alert(`Failed to delete chapter: ${error.error}`)
          }
        } catch (error) {
          console.error('Error deleting chapter:', error)
          alert('Failed to delete chapter. Please try again.')
        }
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
      selectedChapterId,
      newSubject,
      newChapter,
      authStore,
      quizStore,
      filteredSubjects,
      logout,
      addNewSubject,
      addNewChapter,
      saveChapter,
      openNewChapterModal,
      closeChapterModal,
      editChapter,
      deleteChapter
    }
  }
}
</script>

<style scoped>
/* Admin Dashboard Styling */
.admin-dashboard {
  min-height: 100vh;
  background: #f8f9fa;
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

.page-header {
  margin-bottom: 3rem;
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.page-title {
  color: #374151;
  margin-bottom: 0.5rem;
  font-weight: 700;
  font-size: 2.5rem;
  display: flex;
  align-items: center;
}

.page-title i {
  color: #667eea;
}

.page-subtitle {
  font-size: 1.1rem;
  margin-bottom: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.loading-content {
  text-align: center;
  max-width: 300px;
}

.loading-spinner {
  margin-bottom: 2rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: #374151;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.loading-subtitle {
  color: #6b7280;
  margin-bottom: 0;
}

/* Error State */
.error-state {
  margin-bottom: 2rem;
}

/* Subject Cards */
.subjects-section {
  animation: fadeInUp 0.6s ease-out;
}

.subject-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
}

.subject-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.subject-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subject-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.subject-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.subject-title {
  margin-bottom: 0.25rem;
  font-weight: 600;
  font-size: 1.3rem;
}

.subject-meta {
  margin-bottom: 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

.subject-actions .btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  border-radius: 8px;
  padding: 0.5rem;
  transition: all 0.3s ease;
}

.subject-actions .btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Chapters List */
.chapters-list {
  padding: 1.5rem;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
}

.chapter-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.chapter-item:last-child {
  margin-bottom: 0;
}

.chapter-info {
  flex: 1;
}

.chapter-name {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.25rem;
}

.chapter-desc {
  color: #6b7280;
  font-size: 0.9rem;
}

.chapter-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.question-count {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.chapter-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.edit-btn {
  background: #10b981;
  color: white;
}

.edit-btn:hover {
  background: #059669;
  transform: scale(1.1);
}

.delete-btn {
  background: #ef4444;
  color: white;
}

.delete-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.empty-chapters {
  text-align: center;
  padding: 2rem;
  color: #6b7280;
  background: #f8f9fa;
  border-radius: 12px;
}

.empty-chapters i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

/* Empty State */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-content {
  text-align: center;
  max-width: 400px;
  padding: 2rem;
}

.empty-icon {
  margin-bottom: 2rem;
}

.empty-icon i {
  font-size: 5rem;
  color: #d1d5db;
}

.empty-title {
  color: #374151;
  margin-bottom: 1rem;
  font-weight: 600;
}

.empty-subtitle {
  color: #6b7280;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

/* Buttons */
.btn {
  border: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
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
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content h3 {
  margin-bottom: 1.5rem;
  color: #374151;
  font-weight: 700;
  text-align: center;
}

.modal-form .form-group {
  margin-bottom: 1.5rem;
}

.modal-form label {
  display: block;
  margin-bottom: 0.75rem;
  color: #374151;
  font-weight: 600;
}

.modal-form input,
.modal-form textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.modal-form input:focus,
.modal-form textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.modal-form input:disabled {
  background-color: #f3f4f6;
  color: #6b7280;
  cursor: not-allowed;
}

.modal-form textarea {
  resize: vertical;
  min-height: 100px;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  padding: 0.75rem 1.5rem;
}

.btn-secondary:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  
  .page-header {
    padding: 1.5rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .subject-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .chapter-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .chapter-meta {
    align-self: stretch;
    justify-content: space-between;
  }
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