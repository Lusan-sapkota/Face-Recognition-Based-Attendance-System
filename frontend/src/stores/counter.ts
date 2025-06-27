import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userRole = ref(localStorage.getItem('userRole') || '')
  const currentUser = ref(JSON.parse(localStorage.getItem('currentUser') || 'null'))
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userRole.value === 'admin')
  const user = computed(() => currentUser.value) // Alias for compatibility

  function login(authToken: string, role: string, user?: any) {
    token.value = authToken
    userRole.value = role
    currentUser.value = user || null
    localStorage.setItem('token', authToken)
    localStorage.setItem('userRole', role)
    if (user) {
      localStorage.setItem('currentUser', JSON.stringify(user))
    }
  }

  function logout() {
    token.value = ''
    userRole.value = ''
    currentUser.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userRole')
    localStorage.removeItem('currentUser')
  }

  return { token, userRole, currentUser, user, isAuthenticated, isAdmin, login, logout }
})

interface DashboardStats {
  total_registered: number
  today_attendance: number
  students_present: number
  employees_present: number
  attendance_data: any[]
}

interface Notice {
  id: number
  title: string
  content: string
  created_at: string
  created_by: string
}

export const useDashboardStore = defineStore('dashboard', () => {
  const stats = ref<DashboardStats>({
    total_registered: 0,
    today_attendance: 0,
    students_present: 0,
    employees_present: 0,
    attendance_data: [],
  })

  const notices = ref<Notice[]>([])
  const isLoading = ref(false)

  function setStats(newStats: DashboardStats) {
    stats.value = newStats
  }

  function setNotices(newNotices: Notice[]) {
    notices.value = newNotices
  }

  function setLoading(loading: boolean) {
    isLoading.value = loading
  }

  return { stats, notices, isLoading, setStats, setNotices, setLoading }
})
