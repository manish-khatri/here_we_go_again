import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const userRole = ref(null) // 'admin' or 'customer'

  // Getters
  const isAdmin = computed(() => userRole.value === 'admin')
  const isCustomer = computed(() => userRole.value === 'customer')
  const currentUser = computed(() => user.value)

  // Actions
  const login = async (email, password) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_mail: email, 
          user_pass: password 
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        // Success - user authenticated
        const userData = {
          email: email,
          role: data.role[0] || 'customer', // Backend returns array of roles
          message: data.message
        }

        user.value = userData
        userRole.value = data.role[0] || 'customer'
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('isAuthenticated', 'true')

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

  const adminLogin = async (email, password) => {
    try {
      const response = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          user_mail: email, 
          user_pass: password 
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        // Success - admin authenticated
        const userData = {
          email: email,
          role: 'admin',
          message: data.message
        }

        user.value = userData
        userRole.value = 'admin'
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('user', JSON.stringify(userData))
        localStorage.setItem('isAuthenticated', 'true')

        return { success: true, user: userData }
      } else {
        // Error response
        return { success: false, error: data.error || data.message || 'Admin login failed' }
      }
    } catch (error) {
      console.error('Admin login error:', error)
      return { success: false, error: 'Network error. Please try again.' }
    }
  }

  const register = async (userData) => {
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_mail: userData.email,
          user_name: userData.fullName,
          user_pass: userData.password,
          qualification: userData.qualification,
          dob: userData.dateOfBirth,
          role: userData.qualification  // Send the role to backend
        })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        // Success - user registered
        const assignedRole = userData.qualification === 'admin' ? 'admin' : 'customer'
        const newUser = {
          email: userData.email,
          name: userData.fullName,
          role: assignedRole
        }

        user.value = newUser
        userRole.value = assignedRole
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

  const logout = async () => {
    try {
      // Call logout endpoint
      await fetch('/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local state regardless of API call success
      user.value = null
      userRole.value = null
      isAuthenticated.value = false

      // Clear localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('authToken')
    }
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
    adminLogin,
    register,
    logout,
    checkAuth
  }
}) 