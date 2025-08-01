<template>
  <div class="login-page">
    <div class="login-container">
      <!-- Left Side - Branding -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-icon">
            <i class="bi bi-mortarboard-fill"></i>
          </div>
          <h1 class="brand-title">Quiz Master</h1>
          <p class="brand-subtitle">Empower your learning journey with intelligent assessments</p>
          <div class="features">
            <div class="feature">
              <i class="bi bi-check-circle"></i>
              <span>Smart Question Generation</span>
            </div>
            <div class="feature">
              <i class="bi bi-check-circle"></i>
              <span>Real-time Progress Tracking</span>
            </div>
            <div class="feature">
              <i class="bi bi-check-circle"></i>
              <span>Comprehensive Analytics</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side - Login Form -->
      <div class="form-section">
        <div class="form-container">
          <div class="form-header">
            <h2>Welcome Back</h2>
            <p>Sign in to continue your learning journey</p>
          </div>

          <div v-if="error" class="alert alert-error">
            <i class="bi bi-exclamation-triangle"></i>
            {{ error }}
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <div class="input-wrapper">
                <i class="bi bi-envelope input-icon"></i>
                <input 
                  type="email" 
                  class="form-control"
                  :class="emailError ? 'error' : ''"
                  v-model="email" 
                  @blur="validateEmail"
                  placeholder="Enter your email"
                  required
                />
              </div>
              <div v-if="emailError" class="error-message">{{ emailError }}</div>
            </div>

            <div class="form-group">
              <label class="form-label">Password</label>
              <div class="input-wrapper">
                <i class="bi bi-lock input-icon"></i>
                <input 
                  type="password" 
                  class="form-control"
                  :class="passwordError ? 'error' : ''"
                  v-model="password" 
                  @blur="validatePassword"
                  placeholder="Enter your password"
                  required
                />
              </div>
              <div v-if="passwordError" class="error-message">{{ passwordError }}</div>
            </div>

            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              <div v-if="loading" class="spinner"></div>
              <span v-else>Sign In</span>
            </button>
          </form>

          <div class="form-footer">
            <p>Don't have an account? 
              <button @click="showRegisterModal = true" class="link-btn">
                Create Account
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Register Modal -->
    <div v-if="showRegisterModal" class="modal" @click="showRegisterModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Create Account</h3>
          <button @click="showRegisterModal = false" class="close-btn">
            <i class="bi bi-x"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleRegister" class="register-form">
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input 
                  type="text" 
                  class="form-control"
                  v-model="registerData.firstName" 
                  required
                />
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input 
                  type="text" 
                  class="form-control"
                  v-model="registerData.lastName" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input 
                type="email" 
                class="form-control"
                v-model="registerData.email" 
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Password</label>
              <input 
                type="password" 
                class="form-control"
                v-model="registerData.password" 
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">Role</label>
              <select class="form-control" v-model="registerData.role" required>
                <option value="">Select Role</option>
                <option value="student">Student</option>
                <option value="admin" :disabled="adminExists">
                  {{ adminExists ? 'Admin (Already exists)' : 'Admin' }}
                </option>
              </select>
              <div v-if="adminExists" class="info-message">
                <i class="bi bi-info-circle"></i>
                Only one admin account is allowed. Admin role is disabled.
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Date of Birth</label>
              <input 
                type="date" 
                class="form-control"
                :class="dobError ? 'error' : ''"
                v-model="registerData.dateOfBirth" 
                required
              />
              <div v-if="dobError" class="error-message">{{ dobError }}</div>
            </div>

            <div class="modal-footer">
              <button type="button" @click="showRegisterModal = false" class="btn btn-secondary">
                Cancel
              </button>
              <button type="submit" class="btn btn-primary" :disabled="registerLoading">
                <div v-if="registerLoading" class="spinner"></div>
                <span v-else>Create Account</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { validators, validateField, validateEmailUniqueness } from '../utils/validation'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // Login form
    const email = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    const emailError = ref('')
    const passwordError = ref('')
    
    // Registration form
    const showRegisterModal = ref(false)
    const registerData = ref({
      firstName: '',
      lastName: '',
      email: '',
      password: '',
      role: '',
      dateOfBirth: ''
    })
    const registerLoading = ref(false)
    const registerError = ref('')
    const registerEmailError = ref('')
    const registerPasswordError = ref('')
    const fullNameError = ref('')
    const qualificationError = ref('')
    const dobError = ref('')
    const adminExists = ref(false)

    // Validation methods
    const validateEmail = () => {
      emailError.value = validateField(email.value, [validators.required, validators.email])
    }

    const validatePassword = () => {
      passwordError.value = validateField(password.value, [validators.required])
    }

    const validateRegEmail = async () => {
      registerEmailError.value = validateField(registerData.value.email, [validators.required, validators.email])
      if (!registerEmailError.value) {
        const uniqueError = await validateEmailUniqueness(registerData.value.email)
        registerEmailError.value = uniqueError
      }
    }

    const validateRegPassword = () => {
      registerPasswordError.value = validateField(registerData.value.password, [validators.required, validators.password])
    }

    const validateFullName = () => {
      fullNameError.value = validateField(registerData.value.firstName, [validators.required, validators.minLength(2)])
    }

    const validateQualification = () => {
      qualificationError.value = validateField(registerData.value.role, [validators.required])
      
      // Additional check for admin role
      if (!qualificationError.value && registerData.value.role === 'admin' && adminExists.value) {
        qualificationError.value = 'Admin account already exists. Please select Student role.'
      }
    }

    const validateDob = () => {
      dobError.value = validateField(registerData.value.dateOfBirth, [validators.required])
      if (!dobError.value) {
        const today = new Date()
        const birth = new Date(registerData.value.dateOfBirth)
        const age = today.getFullYear() - birth.getFullYear()
        if (age < 13) {
          dobError.value = 'Must be at least 13 years old'
        }
      }
    }

    const handleLogin = async () => {
      validateEmail()
      validatePassword()
      
      if (emailError.value || passwordError.value) {
        return
      }

      try {
        loading.value = true
        error.value = ''
        
        // Try admin login first, then regular login
        let result = await authStore.adminLogin(email.value, password.value)
        
        if (!result.success) {
          // If admin login fails, try regular login
          result = await authStore.login(email.value, password.value)
        }
        
        if (result.success) {
          // Redirect based on user role
          if (authStore.isAdmin) {
            router.push('/admin/dashboard')
          } else {
            router.push('/user/dashboard')
          }
        } else {
          error.value = result.error || 'Login failed'
        }
      } catch (error) {
        console.error('Login error:', error)
        error.value = 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const handleRegister = async () => {
      console.log('Registration started...')
      
      // Validate all fields
      await validateRegEmail()
      validateRegPassword()
      validateFullName()
      validateQualification()
      validateDob()
      
      console.log('Validation errors:', {
        email: registerEmailError.value,
        password: registerPasswordError.value,
        fullName: fullNameError.value,
        qualification: qualificationError.value,
        dob: dobError.value
      })
      
      if (registerEmailError.value || registerPasswordError.value || fullNameError.value || 
          qualificationError.value || dobError.value) {
        console.log('Validation failed, stopping registration')
        return
      }

      try {
        console.log('Starting registration API call...')
        registerLoading.value = true
        registerError.value = ''
        
        const userData = {
          email: registerData.value.email,
          password: registerData.value.password,
          fullName: registerData.value.firstName + ' ' + registerData.value.lastName,
          qualification: registerData.value.role,
          dateOfBirth: registerData.value.dateOfBirth
        }
        
        console.log('Registration data:', userData)
        
        const result = await authStore.register(userData)
        console.log('Registration result:', result)
        
        if (result.success) {
          // New users are always customers, so redirect to user dashboard
          router.push('/user/dashboard')
          showRegisterModal.value = false
        } else {
          registerError.value = result.error || 'Registration failed'
        }
      } catch (error) {
        console.error('Registration error:', error)
        registerError.value = 'Registration failed. Please try again.'
      } finally {
        registerLoading.value = false
      }
    }

    const closeRegister = () => {
      showRegisterModal.value = false
      // Reset form and errors
      registerData.value = {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        role: '',
        dateOfBirth: ''
      }
      registerError.value = ''
      registerEmailError.value = ''
      registerPasswordError.value = ''
      fullNameError.value = ''
      qualificationError.value = ''
      dobError.value = ''
    }

    const checkAdminExists = async () => {
      try {
        const response = await fetch('/api/check/admin-exists')
        if (response.ok) {
          const data = await response.json()
          adminExists.value = data.exists
        }
      } catch (error) {
        console.error('Error checking admin existence:', error)
      }
    }

    const openRegister = () => {
      console.log('Opening registration modal...')
      console.log('Current showRegister value:', showRegisterModal.value)
      checkAdminExists() // Check if admin exists when opening modal
      showRegisterModal.value = true
      console.log('New showRegister value:', showRegisterModal.value)
    }

    return {
      // Login form
      email,
      password,
      loading,
      error,
      emailError,
      passwordError,
      
      // Registration form
      showRegisterModal,
      registerData,
      registerLoading,
      registerError,
      registerEmailError,
      registerPasswordError,
      fullNameError,
      qualificationError,
      dobError,
      adminExists,
      
      // Methods
      handleLogin,
      handleRegister,
      closeRegister,
      openRegister,
      validateEmail,
      validatePassword,
      validateRegEmail,
      validateRegPassword,
      validateFullName,
      validateQualification,
      validateDob
    }
  }
}
</script>

<style scoped>
/* Modern Login Page Design */
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--white) 100%);
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1200px;
  width: 100%;
  background: var(--white);
  border-radius: 24px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  min-height: 600px;
}

/* Brand Section */
.brand-section {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.brand-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: center;
  color: var(--white);
  max-width: 400px;
}

.brand-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
}

.brand-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  letter-spacing: -0.025em;
}

.brand-subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  opacity: 0.9;
}

.feature i {
  font-size: 1.25rem;
  color: var(--success);
}

/* Form Section */
.form-section {
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.form-header p {
  color: var(--text-light);
  font-size: 1rem;
}

/* Form Styles */
.login-form {
  margin-bottom: 2rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: var(--text-light);
  font-size: 1.125rem;
  z-index: 1;
}

.form-control {
  padding-left: 3rem !important;
}

.form-control.error {
  border-color: var(--error);
}

.error-message {
  color: var(--error);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.info-message {
  color: var(--primary);
  font-size: 0.875rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-footer {
  text-align: center;
}

.form-footer p {
  color: var(--text-light);
  font-size: 0.875rem;
}

.link-btn {
  background: none;
  border: none;
  color: var(--primary-dark);
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  font-size: inherit;
}

.link-btn:hover {
  color: var(--primary);
}

/* Modal Styles */
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .login-container {
    grid-template-columns: 1fr;
    max-width: 500px;
  }
  
  .brand-section {
    padding: 2rem;
  }
  
  .form-section {
    padding: 2rem;
  }
}

@media (max-width: 640px) {
  .login-page {
    padding: 1rem;
  }
  
  .brand-section {
    padding: 1.5rem;
  }
  
  .form-section {
    padding: 1.5rem;
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}

/* Animation */
.form-container {
  animation: fadeInUp 0.6s ease-out;
}

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
</style> 