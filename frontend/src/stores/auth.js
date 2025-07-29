import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const userRole = ref(null) // 'admin' or 'user'

  // Getters
  const isAdmin = computed(() => userRole.value === 'admin')
  const isCustomer = computed(() => userRole.value === 'customer')
  const currentUser = computed(() => user.value)

  // Actions
  const login = async (email, password) => {
    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        // Success - user authenticated
        const userData = {
          id: data.id,
          email: data.email,
          role: data.role,
          token: data.token
        }

        user.value = userData
        userRole.value = data.role
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('isAuthenticated', 'true')
        localStorage.setItem('authToken', data.token)

        return { success: true, user: userData }
      } else {
        // Error response
        return { success: false, error: data.error || data.message || 'Login failed' }
      }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const register = async (userData) => {
    try {
      const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: userData.email,
          name: userData.fullName,
          password: userData.password,
          role: 'customer' // New users are always customers
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        // Success - user registered
        const newUser = {
          email: userData.email,
          name: userData.fullName,
          role: 'customer'
        }

        user.value = newUser
        userRole.value = 'customer'
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('user', JSON.stringify(newUser))
        localStorage.setItem('isAuthenticated', 'true')

        return { success: true, user: newUser }
      } else {
        // Error response
        return { success: false, error: data.error || 'Registration failed' }
      }
    } catch (error) {
      console.error('Registration error:', error)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const logout = () => {
    user.value = null
    userRole.value = null
    isAuthenticated.value = false

    // Clear localStorage
    localStorage.removeItem('user')
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('authToken')
  }

  const checkAuth = () => {
    const storedUser = localStorage.getItem('user')
    const storedAuth = localStorage.getItem('isAuthenticated')

    if (storedUser && storedAuth === 'true') {
      const userData = JSON.parse(storedUser)
      user.value = userData
      userRole.value = userData.role
      isAuthenticated.value = true
      return true
    }
    return false
  }

      return {
      // State
      user,
      isAuthenticated,
      userRole,
      
      // Getters
      isAdmin,
      isCustomer,
      currentUser,
      
      // Actions
      login,
      register,
      logout,
      checkAuth
    }
}) 