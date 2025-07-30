<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Welcome to Quiz Master Login</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Username (E-mail)</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            required 
            placeholder="Enter your email"
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required 
            placeholder="Enter your password"
          />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">Login</button>
          <button type="button" @click="showRegister = true" class="btn btn-secondary">
            Create new user?
          </button>
        </div>
      </form>
    </div>

    <!-- Registration Modal -->
    <div v-if="showRegister" class="modal-overlay" @click="showRegister = false">
      <div class="modal-content" @click.stop>
        <h3>Welcome to Quiz Master Registration</h3>
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="reg-email">User name (E-mail)</label>
            <input type="email" id="reg-email" v-model="regEmail" required />
          </div>
          <div class="form-group">
            <label for="reg-password">Password</label>
            <input type="password" id="reg-password" v-model="regPassword" required />
          </div>
          <div class="form-group">
            <label for="full-name">Full name</label>
            <input type="text" id="full-name" v-model="fullName" required />
          </div>
          <div class="form-group">
            <label for="qualification">Qualification</label>
            <input type="text" id="qualification" v-model="qualification" required />
          </div>
          <div class="form-group">
            <label for="dob">Date of Birth</label>
            <input type="date" id="dob" v-model="dateOfBirth" required />
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Submit</button>
            <button type="button" @click="showRegister = false" class="btn btn-secondary">
              Existing user?
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const email = ref('')
    const password = ref('')
    const showRegister = ref(false)
    
    // Registration form data
    const regEmail = ref('')
    const regPassword = ref('')
    const fullName = ref('')
    const qualification = ref('')
    const dateOfBirth = ref('')

    const handleLogin = async () => {
      try {
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
          alert('Login failed: ' + result.error)
        }
      } catch (error) {
        console.error('Login error:', error)
        alert('Login failed. Please try again.')
      }
    }

    const handleRegister = async () => {
      try {
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
          alert('Registration failed: ' + result.error)
        }
      } catch (error) {
        console.error('Registration error:', error)
        alert('Registration failed. Please try again.')
      }
    }

    return {
      email,
      password,
      showRegister,
      regEmail,
      regPassword,
      fullName,
      qualification,
      dateOfBirth,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-actions {
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
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover {
  background-color: #5a6fd8;
}

.btn-secondary {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background-color: #e9ecef;
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
  max-height: 90vh;
  overflow-y: auto;
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