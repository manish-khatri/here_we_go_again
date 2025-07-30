<template>
  <div class="login-container">
    <div class="container-fluid">
      <div class="row min-vh-100">
        <!-- Left side - Branding/Welcome -->
        <div class="col-lg-6 d-none d-lg-flex welcome-section">
          <div class="welcome-content">
            <div class="brand-logo mb-4">
              <i class="bi bi-mortarboard-fill display-2 text-white"></i>
            </div>
            <h1 class="display-4 text-white fw-bold mb-4">Quiz Master</h1>
            <p class="lead text-white-50 mb-4">
              Enhance your learning experience with our comprehensive quiz platform. 
              Test your knowledge, track your progress, and excel in your studies.
            </p>
            <div class="feature-highlights">
              <div class="feature-item d-flex align-items-center mb-3">
                <i class="bi bi-check-circle-fill text-success me-3"></i>
                <span class="text-white">Interactive Quiz Experience</span>
              </div>
              <div class="feature-item d-flex align-items-center mb-3">
                <i class="bi bi-check-circle-fill text-success me-3"></i>
                <span class="text-white">Real-time Progress Tracking</span>
              </div>
              <div class="feature-item d-flex align-items-center mb-3">
                <i class="bi bi-check-circle-fill text-success me-3"></i>
                <span class="text-white">Comprehensive Subject Coverage</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right side - Login Form -->
        <div class="col-lg-6 d-flex align-items-center justify-content-center login-section">
          <div class="login-form-container">
            <div class="text-center mb-5">
              <div class="d-lg-none mb-3">
                <i class="bi bi-mortarboard-fill display-4 text-primary"></i>
              </div>
              <h2 class="fw-bold text-dark mb-2">Welcome Back!</h2>
              <p class="text-muted">Please sign in to your account</p>
            </div>
            
            <div v-if="error" class="alert alert-danger border-0 shadow-sm" role="alert">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              {{ error }}
            </div>
            
            <form @submit.prevent="handleLogin" novalidate class="login-form">
              <div class="mb-4">
                <label for="email" class="form-label fw-semibold text-dark">Email Address</label>
                <div class="input-group">
                  <span class="input-group-text border-end-0 bg-transparent">
                    <i class="bi bi-envelope text-muted"></i>
                  </span>
                  <input 
                    type="email" 
                    id="email" 
                    class="form-control border-start-0 form-control-lg"
                    :class="emailError ? 'is-invalid' : ''"
                    v-model="email" 
                    @blur="validateEmail"
                    required 
                    placeholder="Enter your email address"
                  />
                  <div v-if="emailError" class="invalid-feedback">
                    {{ emailError }}
                  </div>
                </div>
              </div>
              
              <div class="mb-4">
                <label for="password" class="form-label fw-semibold text-dark">Password</label>
                <div class="input-group">
                  <span class="input-group-text border-end-0 bg-transparent">
                    <i class="bi bi-lock text-muted"></i>
                  </span>
                  <input 
                    type="password" 
                    id="password" 
                    class="form-control border-start-0 form-control-lg"
                    :class="passwordError ? 'is-invalid' : ''"
                    v-model="password" 
                    @blur="validatePassword"
                    required 
                    placeholder="Enter your password"
                  />
                  <div v-if="passwordError" class="invalid-feedback">
                    {{ passwordError }}
                  </div>
                </div>
              </div>
              
              <div class="d-grid gap-3 mb-4">
                <button type="submit" class="btn btn-primary btn-lg fw-semibold py-3" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
              </div>
              
              <div class="text-center">
                <p class="text-muted mb-3">Don't have an account?</p>
                <button type="button" @click="showRegister = true" class="btn btn-outline-primary btn-lg px-4">
                  <i class="bi bi-person-plus me-2"></i>Create Account
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Registration Modal -->
    <div v-if="showRegister" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Master Registration</h5>
            <button type="button" class="btn-close" @click="closeRegister"></button>
          </div>
          <div class="modal-body">
            <div v-if="regError" class="alert alert-danger" role="alert">
              {{ regError }}
            </div>
            
            <form @submit.prevent="handleRegister" novalidate id="registerForm">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="reg-email" class="form-label">User name (E-mail)</label>
                    <input 
                      type="email" 
                      id="reg-email" 
                      class="form-control"
                      :class="regEmailError ? 'is-invalid' : ''"
                      v-model="regEmail" 
                      @blur="validateRegEmail"
                      required 
                    />
                    <div v-if="regEmailError" class="invalid-feedback">
                      {{ regEmailError }}
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="reg-password" class="form-label">Password</label>
                    <input 
                      type="password" 
                      id="reg-password" 
                      class="form-control"
                      :class="regPasswordError ? 'is-invalid' : ''"
                      v-model="regPassword" 
                      @blur="validateRegPassword"
                      required 
                    />
                    <div v-if="regPasswordError" class="invalid-feedback">
                      {{ regPasswordError }}
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="full-name" class="form-label">Full name</label>
                    <input 
                      type="text" 
                      id="full-name" 
                      class="form-control"
                      :class="fullNameError ? 'is-invalid' : ''"
                      v-model="fullName" 
                      @blur="validateFullName"
                      required 
                    />
                    <div v-if="fullNameError" class="invalid-feedback">
                      {{ fullNameError }}
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="qualification" class="form-label">Qualification</label>
                    <input 
                      type="text" 
                      id="qualification" 
                      class="form-control"
                      :class="qualificationError ? 'is-invalid' : ''"
                      v-model="qualification" 
                      @blur="validateQualification"
                      required 
                    />
                    <div v-if="qualificationError" class="invalid-feedback">
                      {{ qualificationError }}
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="dob" class="form-label">Date of Birth</label>
                <input 
                  type="date" 
                  id="dob" 
                  class="form-control"
                  :class="dobError ? 'is-invalid' : ''"
                  v-model="dateOfBirth" 
                  @blur="validateDob"
                  required 
                />
                <div v-if="dobError" class="invalid-feedback">
                  {{ dobError }}
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeRegister">
              Existing user?
            </button>
            <button type="submit" form="registerForm" class="btn btn-primary" :disabled="regLoading">
              <span v-if="regLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              {{ regLoading ? 'Registering...' : 'Submit' }}
            </button>
          </div>
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
    const showRegister = ref(false)
    const regEmail = ref('')
    const regPassword = ref('')
    const fullName = ref('')
    const qualification = ref('')
    const dateOfBirth = ref('')
    const regLoading = ref(false)
    const regError = ref('')
    const regEmailError = ref('')
    const regPasswordError = ref('')
    const fullNameError = ref('')
    const qualificationError = ref('')
    const dobError = ref('')

    // Validation methods
    const validateEmail = () => {
      emailError.value = validateField(email.value, [validators.required, validators.email])
    }

    const validatePassword = () => {
      passwordError.value = validateField(password.value, [validators.required])
    }

    const validateRegEmail = async () => {
      regEmailError.value = validateField(regEmail.value, [validators.required, validators.email])
      if (!regEmailError.value) {
        const uniqueError = await validateEmailUniqueness(regEmail.value)
        regEmailError.value = uniqueError
      }
    }

    const validateRegPassword = () => {
      regPasswordError.value = validateField(regPassword.value, [validators.required, validators.password])
    }

    const validateFullName = () => {
      fullNameError.value = validateField(fullName.value, [validators.required, validators.minLength(2)])
    }

    const validateQualification = () => {
      qualificationError.value = validateField(qualification.value, [validators.required])
    }

    const validateDob = () => {
      dobError.value = validateField(dateOfBirth.value, [validators.required])
      if (!dobError.value) {
        const today = new Date()
        const birth = new Date(dateOfBirth.value)
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
      // Validate all fields
      await validateRegEmail()
      validateRegPassword()
      validateFullName()
      validateQualification()
      validateDob()
      
      if (regEmailError.value || regPasswordError.value || fullNameError.value || 
          qualificationError.value || dobError.value) {
        return
      }

      try {
        regLoading.value = true
        regError.value = ''
        
        const userData = {
          email: regEmail.value,
          password: regPassword.value,
          fullName: fullName.value,
          qualification: qualification.value,
          dateOfBirth: dateOfBirth.value
        }
        
        const result = await authStore.register(userData)
        if (result.success) {
          // New users are always customers, so redirect to user dashboard
          router.push('/user/dashboard')
          showRegister.value = false
        } else {
          regError.value = result.error || 'Registration failed'
        }
      } catch (error) {
        console.error('Registration error:', error)
        regError.value = 'Registration failed. Please try again.'
      } finally {
        regLoading.value = false
      }
    }

    const closeRegister = () => {
      showRegister.value = false
      // Reset form and errors
      regEmail.value = ''
      regPassword.value = ''
      fullName.value = ''
      qualification.value = ''
      dateOfBirth.value = ''
      regError.value = ''
      regEmailError.value = ''
      regPasswordError.value = ''
      fullNameError.value = ''
      qualificationError.value = ''
      dobError.value = ''
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
      showRegister,
      regEmail,
      regPassword,
      fullName,
      qualification,
      dateOfBirth,
      regLoading,
      regError,
      regEmailError,
      regPasswordError,
      fullNameError,
      qualificationError,
      dobError,
      
      // Methods
      handleLogin,
      handleRegister,
      closeRegister,
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
/* Login Container */
.login-container {
  min-height: 100vh;
  background: #f8f9fa;
}

/* Welcome Section (Left Side) */
.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.welcome-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
  opacity: 0.3;
}

.welcome-content {
  position: relative;
  z-index: 2;
  padding: 4rem 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.brand-logo {
  text-align: center;
}

.feature-highlights {
  margin-top: 2rem;
}

.feature-item {
  font-size: 1.1rem;
}

/* Login Section (Right Side) */
.login-section {
  background: white;
  padding: 2rem;
}

.login-form-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
}

/* Form Styling */
.login-form {
  margin-top: 1rem;
}

.form-label {
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.input-group {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  background: white;
}

.input-group:focus-within {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-group-text {
  border: none;
  padding: 1rem;
  background: transparent;
}

.form-control {
  border: none;
  padding: 1rem 1rem 1rem 0.5rem;
  background: transparent;
  font-size: 1rem;
}

.form-control:focus {
  box-shadow: none;
  background: transparent;
}

.form-control-lg {
  font-size: 1rem;
}

/* Button Styling */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: transparent;
}

.btn-outline-primary:hover {
  background: #667eea;
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* Alert Styling */
.alert-danger {
  border-radius: 12px;
  border: none;
  background: #fef2f2;
  color: #dc2626;
  border-left: 4px solid #dc2626;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .login-form-container {
    max-width: 500px;
  }
  
  .login-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  
  .login-section .login-form-container {
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  }
  
  .login-section h2,
  .login-section .form-label {
    color: #374151;
  }
}

@media (max-width: 575.98px) {
  .login-form-container {
    padding: 1.5rem;
    margin: 1rem;
  }
  
  .welcome-content {
    padding: 2rem 1.5rem;
  }
}

/* Animation */
.login-form-container {
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

/* Input validation styling */
.is-invalid {
  border-color: #dc3545 !important;
}

.invalid-feedback {
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding-left: 1rem;
}

/* Loading state */
.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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
  border-radius: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.register-form .form-actions {
  flex-direction: column;
}
</style> 