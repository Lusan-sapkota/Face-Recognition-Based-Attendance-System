<template>
  <div id="app">
    <nav class="nav" v-if="!isLoginRoute">
      <div class="container nav-container">
        <RouterLink to="/" class="nav-brand">
          <img src="/logo.png" alt="RecognizeMe" class="logo" width="40" height="40" />
          <span class="gradient-text">{{ appName }}</span>
        </RouterLink>
        
        <ul class="nav-links">
          <li v-if="!authStore.isAuthenticated">
            <RouterLink to="/" class="nav-link">Home</RouterLink>
          </li>
          <li v-if="!authStore.isAuthenticated">
            <RouterLink to="/faq" class="nav-link">FAQ</RouterLink>
          </li>
          <li v-if="authStore.isAuthenticated">
            <RouterLink to="/dashboard" class="nav-link">Dashboard</RouterLink>
          </li>
          <li v-if="authStore.isAuthenticated && authStore.isAdmin">
            <RouterLink to="/admin" class="nav-link">Admin</RouterLink>
          </li>
          <li v-if="authStore.isAuthenticated">
            <button @click="logout" class="btn btn-secondary">Logout</button>
          </li>
          <li v-if="!authStore.isAuthenticated">
            <RouterLink to="/login" class="btn btn-primary">Login</RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/counter'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const appName = import.meta.env.VITE_APP_NAME || 'RecognizeMe'
const isLoginRoute = computed(() => 
  route.name === 'user-login' || route.name === 'admin-login'
)

const logout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.logo {
  border-radius: 8px;
  object-fit: contain;
}

.main-content {
  min-height: calc(100vh - 80px);
  padding: 24px 0;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 16px;
  }
  
  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .main-content {
    padding: 16px 0;
  }
}
</style>
