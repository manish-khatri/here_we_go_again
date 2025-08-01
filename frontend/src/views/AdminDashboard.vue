<template>
  <div class="admin-dashboard">
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
          <router-link to="/admin/dashboard" class="nav-link active">
            <i class="bi bi-house"></i>
            Dashboard
          </router-link>
          <router-link to="/admin/quiz" class="nav-link">
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
              placeholder="Search subjects..."
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
            <h1>Subject Management</h1>
            <p>Manage your subjects and chapters efficiently</p>
          </div>
          <button @click="showNewSubjectModal = true" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i>
            Add Subject
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="quizStore.loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading subjects...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="quizStore.error" class="error-state">
          <i class="bi bi-exclamation-triangle"></i>
          <h3>Oops! Something went wrong</h3>
          <p>{{ quizStore.error }}</p>
          <button @click="refreshSubjects" class="btn btn-primary">
            Try Again
          </button>
        </div>

        <!-- Subjects Section -->
        <div v-else class="subjects-section">
          <div class="section-header">
            <h2>Subjects</h2>
            <span class="subject-count">{{ filteredSubjects.length }} subjects</span>
          </div>

          <div v-if="filteredSubjects.length === 0" class="empty-state">
            <i class="bi bi-book"></i>
            <h3>No subjects available</h3>
            <p>Create your first subject to get started.</p>
            <button @click="showNewSubjectModal = true" class="btn btn-primary">
              <i class="bi bi-plus-circle"></i>
              Add First Subject
            </button>
          </div>

          <div v-else class="subjects-grid">
            <div 
              v-for="subject in filteredSubjects" 
              :key="subject.sub_id" 
              class="subject-card"
            >
              <div class="subject-header">
                <div class="subject-info">
                  <div class="subject-icon">
                    <i class="bi bi-book"></i>
                  </div>
                  <div>
                    <h3 class="subject-title">{{ subject.sub_name }}</h3>
                    <p class="subject-meta">{{ subject.chapters?.length || 0 }} chapters</p>
                  </div>
                </div>
                <button @click="openNewChapterModal(subject.sub_id)" class="btn btn-primary btn-sm">
                  <i class="bi bi-plus"></i>
                  Add Chapter
                </button>
              </div>
              
              <div class="chapters-section">
                <div v-if="subject.chapters?.length > 0" class="chapters-list">
                  <div 
                    v-for="chapter in subject.chapters" 
                    :key="chapter.chp_id" 
                    class="chapter-item"
                  >
                    <div class="chapter-info">
                      <h4 class="chapter-name">{{ chapter.chp_name }}</h4>
                      <p class="chapter-desc">{{ chapter.chp_desc }}</p>
                      <div class="chapter-meta">
                        <span class="question-count">
                          <i class="bi bi-question-circle"></i>
                          {{ chapter.questionCount || 0 }} questions
                        </span>
                      </div>
                    </div>
                    <div class="chapter-actions">
                      <button @click="editChapter(chapter)" class="btn btn-secondary btn-sm">
                        <i class="bi bi-pencil"></i>
                        Edit
                      </button>
                      <button @click="deleteChapter(chapter.chp_id)" class="btn btn-danger btn-sm">
                        <i class="bi bi-trash"></i>
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
                
                <div v-else class="no-chapters">
                  <i class="bi bi-folder-plus"></i>
                  <p>No chapters yet</p>
                  <button @click="openNewChapterModal(subject.sub_id)" class="btn btn-outline-primary btn-sm">
                    Add Chapter
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- New Subject Modal -->
    <div v-if="showNewSubjectModal" class="modal" @click="showNewSubjectModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Add New Subject</h3>
          <button @click="showNewSubjectModal = false" class="close-btn">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="addSubject" class="subject-form">
            <div class="form-group">
              <label class="form-label">Subject Name</label>
              <input 
                type="text" 
                class="form-control"
                v-model="newSubject.name" 
                placeholder="Enter subject name"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea 
                class="form-control"
                v-model="newSubject.description" 
                placeholder="Enter subject description"
                rows="3"
              ></textarea>
            </div>
            
            <div class="modal-footer">
              <button type="button" @click="showNewSubjectModal = false" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="addingSubject">
                <div v-if="addingSubject" class="spinner"></div>
                <span v-else>Add Subject</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- New Chapter Modal -->
    <div v-if="showNewChapterModal" class="modal" @click="showNewChapterModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Add New Chapter</h3>
          <button @click="showNewChapterModal = false" class="close-btn">
            <i class="bi bi-x"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="addChapter" class="chapter-form">
            <div class="form-group">
              <label class="form-label">Chapter Name</label>
              <input 
                type="text" 
                class="form-control"
                v-model="newChapter.name" 
                placeholder="Enter chapter name"
                required
              />
            </div>
            
            <div class="form-group">
              <label class="form-label">Description</label>
              <textarea 
                class="form-control"
                v-model="newChapter.description" 
                placeholder="Enter chapter description"
                rows="3"
              ></textarea>
            </div>
            
            <div class="modal-footer">
              <button type="button" @click="showNewChapterModal = false" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="addingChapter">
                <div v-if="addingChapter" class="spinner"></div>
                <span v-else>Add Chapter</span>
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
import { useQuizStore } from '@/stores/quizStore'
import { useRouter } from 'vue-router'

export default {
  name: 'AdminDashboard',
  setup() {
    const quizStore = useQuizStore()
    const router = useRouter()
    
    const searchQuery = ref('')
    const showNewSubjectModal = ref(false)
    const showNewChapterModal = ref(false)
    const selectedSubjectId = ref(null)
    const addingSubject = ref(false)
    const addingChapter = ref(false)
    
    const newSubject = ref({
      name: '',
      description: ''
    })
    
    const newChapter = ref({
      name: '',
      description: ''
    })

    const filteredSubjects = computed(() => {
      if (!searchQuery.value) return quizStore.subjects
      return quizStore.subjects.filter(subject =>
        subject.sub_name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    })

    const logout = () => {
      // Clear any stored authentication data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }

    const refreshSubjects = () => {
      quizStore.fetchSubjects()
    }

    const addSubject = async () => {
      addingSubject.value = true
      try {
        await quizStore.addSubject(newSubject.value)
        showNewSubjectModal.value = false
        newSubject.value = { name: '', description: '' }
      } catch (error) {
        console.error('Error adding subject:', error)
      } finally {
        addingSubject.value = false
      }
    }

    const openNewChapterModal = (subjectId) => {
      selectedSubjectId.value = subjectId
      showNewChapterModal.value = true
      newChapter.value = { name: '', description: '' }
    }

    const addChapter = async () => {
      addingChapter.value = true
      try {
        await quizStore.addChapter({
          ...newChapter.value,
          sub_id: selectedSubjectId.value
        })
        showNewChapterModal.value = false
        newChapter.value = { name: '', description: '' }
      } catch (error) {
        console.error('Error adding chapter:', error)
      } finally {
        addingChapter.value = false
      }
    }

    const editChapter = (chapter) => {
      // Implement edit functionality
      console.log('Edit chapter:', chapter)
    }

    const deleteChapter = async (chapterId) => {
      if (confirm('Are you sure you want to delete this chapter?')) {
        try {
          await quizStore.deleteChapter(chapterId)
        } catch (error) {
          console.error('Error deleting chapter:', error)
        }
      }
    }

    onMounted(() => {
      quizStore.fetchSubjects()
    })

    return {
      quizStore,
      searchQuery,
      showNewSubjectModal,
      showNewChapterModal,
      newSubject,
      newChapter,
      addingSubject,
      addingChapter,
      filteredSubjects,
      logout,
      refreshSubjects,
      addSubject,
      openNewChapterModal,
      addChapter,
      editChapter,
      deleteChapter
    }
  }
}
</script>

<style scoped>
/* Modern Admin Dashboard Design */
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 100%);
}

/* Header */
.header {
  background: var(--white);
  box-shadow: var(--shadow);
  border-bottom: 1px solid var(--gray-200);
  padding: 0 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 0;
}

.header-left .logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-dark);
}

.header-left .logo i {
  margin-right: 0.75rem;
  font-size: 1.75rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text);
  text-decoration: none;
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover,
.nav-link.active {
  background: var(--primary-light);
  color: var(--primary-dark);
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
  font-size: 1rem;
}

.search-box input {
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  background: var(--white);
  font-size: 0.875rem;
  width: 250px;
  transition: all 0.2s ease;
}

.search-box input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(168, 213, 232, 0.1);
}

.user-menu {
  position: relative;
}

.user-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--text);
  font-weight: 500;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.user-btn:hover {
  background: var(--primary-light);
  color: var(--primary-dark);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--white);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--gray-200);
  min-width: 150px;
  z-index: 100;
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
  border: none;
  background: none;
  color: var(--text);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: var(--gray-100);
  color: var(--error);
}

/* Main Content */
.main {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.container {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.page-title p {
  color: var(--text-light);
  font-size: 1rem;
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-state .spinner {
  margin: 0 auto 1rem;
}

.loading-state p {
  color: var(--text-light);
  font-size: 1rem;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 4rem 2rem;
}

.error-state i {
  font-size: 3rem;
  color: var(--error);
  margin-bottom: 1rem;
}

.error-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.error-state p {
  color: var(--text-light);
  margin-bottom: 1.5rem;
}

/* Subjects Section */
.subjects-section {
  margin-top: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
}

.subject-count {
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
}

.empty-state i {
  font-size: 4rem;
  color: var(--text-light);
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: var(--text-light);
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

/* Subjects Grid */
.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background: var(--white);
  border-radius: 16px;
  box-shadow: var(--shadow);
  border: 1px solid var(--gray-100);
  overflow: hidden;
  transition: all 0.2s ease;
}

.subject-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: var(--primary-light);
  border-bottom: 1px solid var(--gray-200);
}

.subject-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.subject-icon {
  width: 50px;
  height: 50px;
  background: var(--primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--white);
  font-size: 1.5rem;
}

.subject-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.subject-meta {
  color: var(--text-light);
  font-size: 0.875rem;
  margin: 0;
}

/* Chapters Section */
.chapters-section {
  padding: 1.5rem;
}

.chapters-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--gray-50);
  border-radius: 8px;
  border: 1px solid var(--gray-200);
}

.chapter-info {
  flex: 1;
}

.chapter-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 0.25rem;
}

.chapter-desc {
  color: var(--text-light);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.chapter-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.question-count {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: var(--primary-light);
  color: var(--primary-dark);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
}

.chapter-actions {
  display: flex;
  gap: 0.5rem;
}

.no-chapters {
  text-align: center;
  padding: 2rem;
  color: var(--text-light);
}

.no-chapters i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  display: block;
}

.no-chapters p {
  margin-bottom: 1rem;
}

/* Modal Styles */
.modal {
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
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1.5rem 0;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--text-light);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--gray-100);
  color: var(--text);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(168, 213, 232, 0.1);
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 0 1.5rem 1.5rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 0;
  }
  
  .nav {
    margin-left: 0;
  }
  
  .header-right {
    width: 100%;
    justify-content: space-between;
  }
  
  .search-box input {
    width: 200px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }
  
  .subjects-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    padding: 0 1rem;
  }
  
  .search-box input {
    width: 150px;
  }
  
  .subject-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .chapter-item {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .nav {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .header-right {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box input {
    width: 100%;
  }
}
</style> 