import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useQuizStore = defineStore('quiz', () => {
  // State
  const subjects = ref([
    {
      sub_id: '1',
      sub_name: 'Physics',
      sub_desc: 'Study of matter and energy',
      chapters: [
        { chp_id: '1', chp_name: 'Force', questionCount: 15 },
        { chp_id: '2', chp_name: 'EMF', questionCount: 12 }
      ]
    },
    {
      sub_id: '2',
      sub_name: 'App Dev-I',
      sub_desc: 'Application Development Fundamentals',
      chapters: [
        { chp_id: '3', chp_name: 'HTML', questionCount: 20 },
        { chp_id: '4', chp_name: 'CSS', questionCount: 18 }
      ]
    }
  ])

  const quizzes = ref([
    {
      q_id: '1',
      q_name: 'Quiz1 (CSS)',
      chp_id: '4',
      sub_id: '2',
      date_of_quiz: '2024-01-15',
      time_dur: '00:10',
      questions: [
        { ques_id: '1', statement: 'What is the purpose of CSS classes?' },
        { ques_id: '2', statement: 'How do you apply internal CSS styles?' }
      ]
    },
    {
      q_id: '2',
      q_name: 'Quiz2 (HTML)',
      chp_id: '3',
      sub_id: '2',
      date_of_quiz: '2024-01-20',
      time_dur: '00:15',
      questions: [
        { ques_id: '3', statement: 'What does the <b> element do?' },
        { ques_id: '4', statement: 'How many heading levels are available in HTML?' },
        { ques_id: '5', statement: 'What is the purpose of the <form> element?' }
      ]
    }
  ])

  const upcomingQuizzes = ref([
    {
      q_id: '1',
      questionCount: 5,
      date_of_quiz: '2024-01-15',
      time_dur: '00:10',
      subject: 'Mathematics',
      chapter: 'Random Variables'
    },
    {
      q_id: '2',
      questionCount: 10,
      date_of_quiz: '2024-01-20',
      time_dur: '00:10',
      subject: 'Physics',
      chapter: 'Force'
    },
    {
      q_id: '3',
      questionCount: 15,
      date_of_quiz: '2024-01-25',
      time_dur: '00:30',
      subject: 'Chemistry',
      chapter: 'Organic Chemistry'
    }
  ])

  const userScores = ref([
    {
      score_id: '1',
      q_id: '1',
      user_id: 'C0',
      time_stamp: '2024-01-10T10:30:00',
      total_score: 3
    },
    {
      score_id: '2',
      q_id: '2',
      user_id: 'C0',
      time_stamp: '2024-01-05T14:20:00',
      total_score: 12
    },
    {
      score_id: '3',
      q_id: '3',
      user_id: 'C0',
      time_stamp: '2023-12-28T09:15:00',
      total_score: 8
    },
    {
      score_id: '4',
      q_id: '4',
      user_id: 'C0',
      time_stamp: '2023-12-20T16:45:00',
      total_score: 16
    }
  ])

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
      // TODO: Replace with actual API call
      const newSubject = {
        sub_id: Date.now().toString(),
        sub_name: subjectData.name,
        sub_desc: subjectData.description,
        chapters: []
      }
      
      subjects.value.push(newSubject)
      return { success: true, subject: newSubject }
    } catch (error) {
      console.error('Add subject error:', error)
      return { success: false, error: error.message }
    }
  }

  const addChapter = async (subjectId, chapterData) => {
    try {
      // TODO: Replace with actual API call
      const subject = subjects.value.find(s => s.sub_id === subjectId)
      if (!subject) {
        throw new Error('Subject not found')
      }

      const newChapter = {
        chp_id: Date.now().toString(),
        chp_name: chapterData.name,
        chp_desc: chapterData.description,
        questionCount: 0
      }

      subject.chapters.push(newChapter)
      return { success: true, chapter: newChapter }
    } catch (error) {
      console.error('Add chapter error:', error)
      return { success: false, error: error.message }
    }
  }

  const addQuiz = async (quizData) => {
    try {
      // TODO: Replace with actual API call
      const newQuiz = {
        q_id: Date.now().toString(),
        q_name: `Quiz${quizzes.value.length + 1}`,
        chp_id: quizData.chapterId,
        sub_id: quizData.subjectId,
        date_of_quiz: quizData.date,
        time_dur: quizData.duration,
        questions: []
      }

      quizzes.value.push(newQuiz)
      return { success: true, quiz: newQuiz }
    } catch (error) {
      console.error('Add quiz error:', error)
      return { success: false, error: error.message }
    }
  }

  const addQuestion = async (quizId, questionData) => {
    try {
      // TODO: Replace with actual API call
      const quiz = quizzes.value.find(q => q.q_id === quizId)
      if (!quiz) {
        throw new Error('Quiz not found')
      }

      const newQuestion = {
        ques_id: Date.now().toString(),
        statement: questionData.statement,
        options: questionData.options,
        answer: questionData.correctOption.toString()
      }

      quiz.questions.push(newQuestion)
      return { success: true, question: newQuestion }
    } catch (error) {
      console.error('Add question error:', error)
      return { success: false, error: error.message }
    }
  }

  const submitQuizScore = async (quizId, score) => {
    try {
      // TODO: Replace with actual API call
      const newScore = {
        score_id: Date.now().toString(),
        q_id: quizId,
        user_id: score.userId,
        time_stamp: new Date().toISOString(),
        total_score: score.correctAnswers
      }

      userScores.value.push(newScore)
      return { success: true, score: newScore }
    } catch (error) {
      console.error('Submit score error:', error)
      return { success: false, error: error.message }
    }
  }

  const fetchSubjects = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/subjects')
      // const data = await response.json()
      // subjects.value = data
      return { success: true }
    } catch (error) {
      console.error('Fetch subjects error:', error)
      return { success: false, error: error.message }
    }
  }

  const fetchQuizzes = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/quizzes')
      // const data = await response.json()
      // quizzes.value = data
      return { success: true }
    } catch (error) {
      console.error('Fetch quizzes error:', error)
      return { success: false, error: error.message }
    }
  }

  const fetchUpcomingQuizzes = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/upcoming-quizzes')
      // const data = await response.json()
      // upcomingQuizzes.value = data
      return { success: true }
    } catch (error) {
      console.error('Fetch upcoming quizzes error:', error)
      return { success: false, error: error.message }
    }
  }

  const fetchUserScores = async () => {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch('/api/user-scores')
      // const data = await response.json()
      // userScores.value = data
      return { success: true }
    } catch (error) {
      console.error('Fetch user scores error:', error)
      return { success: false, error: error.message }
    }
  }

  return {
    // State
    subjects,
    quizzes,
    upcomingQuizzes,
    userScores,
    
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
    fetchUserScores
  }
}) 