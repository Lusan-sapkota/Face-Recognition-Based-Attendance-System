<template>
  <div class="login-page">
    <div class="container">
      <div class="login-container">
        <div class="login-card card">
          <div class="login-header">
            <div class="login-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <circle cx="12" cy="16" r="1"></circle>
                <path d="m7 11 0 0a5 5 0 0 1 10 0"></path>
              </svg>
            </div>
            <h1 class="login-title gradient-text">
              {{ isAdminLogin ? 'Admin Login' : 'User Login' }}
            </h1>
            <p class="login-subtitle">
              {{ isAdminLogin ? 'Enter admin credentials to access the dashboard' : 'Enter your username and password' }}
            </p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <!-- Username field for user login -->
            <div v-if="!isAdminLogin" class="input-group">
              <label for="username" class="input-label">Username</label>
              <input
                id="username"
                v-model="username"
                type="text"
                class="input-field"
                placeholder="Enter your username"
                required
              />
            </div>

            <div class="input-group">
              <label for="password" class="input-label">Password</label>
              <input
                id="password"
                v-model="password"
                type="password"
                class="input-field"
                :placeholder="isAdminLogin ? 'Enter admin password' : 'Enter your password'"
                required
              />
            </div>

            <button 
              type="submit" 
              class="btn btn-primary login-btn"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="spinner"></span>
              {{ isLoading ? 'Signing In...' : 'Sign In' }}
            </button>

            <div v-if="error" class="error-message">
              {{ error }}
            </div>
          </form>

          <div class="login-footer">
            <p class="footer-text">
              <RouterLink to="/" class="footer-link">← Back to Home</RouterLink>
            </p>
            <p v-if="!isAdminLogin" class="footer-text">
              <RouterLink to="/admin/login" class="footer-link">Admin Access →</RouterLink>
            </p>
            <p v-else class="footer-text">
              <RouterLink to="/login" class="footer-link">← User Login</RouterLink>
            </p>
          </div>
        </div>

        <div class="login-info">
          <div class="info-card card">
            <h3 class="info-title">Dashboard Features</h3>
            <ul class="info-list">
              <li class="info-item">
                <div class="info-icon">✓</div>
                Real-time attendance monitoring
              </li>
              <li class="info-item">
                <div class="info-icon">✓</div>
                Student & employee management
              </li>
              <li class="info-item">
                <div class="info-icon">✓</div>
                Advanced analytics & reports
              </li>
              <li class="info-item">
                <div class="info-icon">✓</div>
                Notice board management
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/counter'
import { authAPI } from '../services/api'

interface Props {
  userType?: 'admin' | 'user'
}

const props = withDefaults(defineProps<Props>(), {
  userType: 'user'
})

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const error = ref('')

const isAdminLogin = computed(() => props.userType === 'admin')

const handleLogin = async () => {
  // Validation
  if (isAdminLogin.value) {
    if (!password.value) {
      error.value = 'Please enter admin password'
      return
    }
  } else {
    if (!username.value || !password.value) {
      error.value = 'Please enter both username and password'
      return
    }
  }

  isLoading.value = true
  error.value = ''

  try {
    let response
    
    if (isAdminLogin.value) {
      response = await authAPI.adminLogin(password.value)
    } else {
      response = await authAPI.userLogin(username.value, password.value)
    }
    
    const { access_token, role, user } = response.data
    
    authStore.login(access_token, role, user)
    
    if (role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/dashboard')
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || 'Invalid credentials. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  max-width: 1000px;
  width: 100%;
  align-items: center;
}

.login-card {
  padding: 40px;
  max-width: 400px;
  width: 100%;
  margin: 0 auto;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  padding: 20px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-icon svg {
  width: 40px;
  height: 40px;
  color: white;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.login-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

.login-form {
  margin-bottom: 32px;
}

.login-btn {
  width: 100%;
  padding: 16px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 8px;
  position: relative;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 16px;
  padding: 12px 16px;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid var(--danger-color);
  border-radius: 8px;
  color: var(--danger-color);
  font-size: 14px;
  text-align: center;
}

.login-footer {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid var(--card-border);
}

.footer-text {
  color: var(--text-secondary);
  font-size: 14px;
}

.footer-link {
  color: var(--accent-color);
  text-decoration: none;
  font-weight: 500;
}

.footer-link:hover {
  text-decoration: underline;
}

/* Info Card */
.info-card {
  padding: 40px;
}

.info-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.info-list {
  list-style: none;
  padding: 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  color: var(--text-secondary);
}

.info-icon {
  width: 24px;
  height: 24px;
  background: var(--success-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .login-container {
    grid-template-columns: 1fr;
    gap: 40px;
    max-width: 500px;
  }
}

@media (max-width: 768px) {
  .login-page {
    padding: 20px 0;
  }
  
  .login-card,
  .info-card {
    padding: 24px;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>
