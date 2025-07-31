import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useQuizStore = defineStore('quiz', () => {
  // State
  const subjects = ref([])
  const quizzes = ref([])
  const upcomingQuizzes = ref([])
  const userScores = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const getSubjectById = computed(() => (id) => {
    return subjects.value.find(subject => subject.sub_id === id)
  })

  const getChapterById = computed(() => (id) => {
    for (const subject of subjects.value) {
      const chapter = subject.chapters.find(ch => ch.chp_id === id)
      if (chapter) return chapter
    }
    return null
  })

  const getQuizById = computed(() => (id) => {
    return quizzes.value.find(quiz => quiz.q_id === id)
  })

  const getUpcomingQuizById = computed(() => (id) => {
    return upcomingQuizzes.value.find(quiz => quiz.q_id === id)
  })

  // Actions
  const addSubject = async (subjectData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch('/api/subjects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sub_id: subjectData.sub_id || Date.now().toString(),
          sub_name: subjectData.name,
          sub_desc: subjectData.description
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        await fetchSubjects() // Refresh subjects list
        return { success: true, subject: data }
      } else {
        throw new Error(data.error || 'Failed to add subject')
      }
    } catch (error) {
      console.error('Add subject error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const addChapter = async (subjectId, chapterData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch(`/api/subjects/${subjectId}/chapters`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chp_id: chapterData.chp_id || Date.now().toString(),
          chp_name: chapterData.name,
          chp_desc: chapterData.description
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        await fetchSubjects() // Refresh subjects list
        return { success: true, chapter: data }
      } else {
        throw new Error(data.error || 'Failed to add chapter')
      }
    } catch (error) {
      console.error('Add chapter error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const addQuiz = async (quizData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch(`/api/chapters/${quizData.chapterId}/quizzes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          q_id: quizData.q_id || Date.now().toString(),
          q_name: quizData.name,
          sub_id: quizData.subjectId,
          date_of_quiz: quizData.date,
          time_dur: quizData.duration,
          remarks: quizData.remarks
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        await fetchQuizzes() // Refresh quizzes list
        return { success: true, quiz: data }
      } else {
        throw new Error(data.error || 'Failed to add quiz')
      }
    } catch (error) {
      console.error('Add quiz error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const addQuestion = async (quizId, questionData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch(`/api/quizzes/${quizId}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ques_id: questionData.ques_id || Date.now().toString(),
          sub_id: questionData.subjectId,
          chp_id: questionData.chapterId,
          statement: questionData.statement,
          options: questionData.options,
          answer: questionData.correctOption.toString()
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        return { success: true, question: data }
      } else {
        throw new Error(data.error || 'Failed to add question')
      }
    } catch (error) {
      console.error('Add question error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const submitQuizScore = async (quizId, answers) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch(`/api/quizzes/${quizId}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        await fetchUserScores() // Refresh scores
        return { success: true, score: data }
      } else {
        throw new Error(data.error || 'Failed to submit quiz')
      }
    } catch (error) {
      console.error('Submit score error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const fetchSubjects = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch('/api/subjects')
      const data = await response.json()
      
      if (response.ok) {
        subjects.value = data
        return { success: true }
      } else {
        throw new Error(data.error || 'Failed to fetch subjects')
      }
    } catch (error) {
      console.error('Fetch subjects error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const fetchQuizzes = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch('/api/admin/quizzes')
      const data = await response.json()
      
      if (response.ok) {
        quizzes.value = data
        return { success: true }
      } else {
        throw new Error(data.error || 'Failed to fetch quizzes')
      }
    } catch (error) {
      console.error('Fetch quizzes error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const fetchUpcomingQuizzes = async () => {
    console.log('fetchUpcomingQuizzes called in store')
    try {
      loading.value = true
      error.value = null
      
      // Use the public quizzes endpoint
      console.log('Making request to /api/quizzes')
      const response = await fetch('/api/quizzes')
      console.log('Response status:', response.status, response.ok)
      const data = await response.json()
      console.log('Raw API data:', data)
      
      if (response.ok) {
        upcomingQuizzes.value = data.map(quiz => ({
          q_id: quiz.q_id,
          q_name: quiz.q_name,
          questionCount: quiz.questionCount || 0,
          date_of_quiz: quiz.date_of_quiz,
          time_dur: quiz.time_dur,
          subject: quiz.subject,
          chapter: quiz.chapter,
          chp_id: quiz.chp_id,
          sub_id: quiz.sub_id,
          remarks: quiz.remarks
        }))
        console.log('Mapped quizzes:', upcomingQuizzes.value)
        return { success: true }
      } else {
        throw new Error(data.error || 'Failed to fetch upcoming quizzes')
      }
    } catch (error) {
      console.error('Fetch upcoming quizzes error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const fetchUserScores = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch('/api/scores')
      const data = await response.json()
      
      if (response.ok) {
        userScores.value = data
        return { success: true }
      } else {
        throw new Error(data.error || 'Failed to fetch user scores')
      }
    } catch (error) {
      console.error('Fetch user scores error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  const startQuiz = async (quizId) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await fetch(`/api/quizzes/${quizId}/start`)
      const data = await response.json()
      
      if (response.ok) {
        return { success: true, quiz: data }
      } else {
        throw new Error(data.error || 'Failed to start quiz')
      }
    } catch (error) {
      console.error('Start quiz error:', error)
      error.value = error.message
      return { success: false, error: error.message }
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    subjects,
    quizzes,
    upcomingQuizzes,
    userScores,
    loading,
    error,
    
    // Getters
    getSubjectById,
    getChapterById,
    getQuizById,
    getUpcomingQuizById,
    
    // Actions
    addSubject,
    addChapter,
    addQuiz,
    addQuestion,
    submitQuizScore,
    fetchSubjects,
    fetchQuizzes,
    fetchUpcomingQuizzes,
    fetchUserScores,
    startQuiz
  }
}) 