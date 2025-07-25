import axios from 'axios'
import { mockAuthAPI, mockDashboardAPI, mockAdminAPI, mockUserAPI, isDemoMode } from './mockAuth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  adminLogin: (password: string) => {
    if (isDemoMode()) {
      return mockAuthAPI.adminLogin(password)
    }
    return api.post('/admin/login', { password })
  },
  userLogin: (username: string, password: string) => {
    if (isDemoMode()) {
      return mockAuthAPI.userLogin(username, password)
    }
    return api.post('/user/login', { username, password })
  },
  // Legacy login for backward compatibility
  login: (password: string) => api.post('/login', { password }),
}

export const dashboardAPI = {
  getStats: () => {
    if (isDemoMode()) {
      return mockDashboardAPI.getStats()
    }
    return api.get('/dashboard/stats')
  },
  getAttendance: () => {
    if (isDemoMode()) {
      return mockDashboardAPI.getAttendance()
    }
    return api.get('/attendance')
  },
  startAttendance: () => {
    if (isDemoMode()) {
      return mockDashboardAPI.startAttendance()
    }
    return api.post('/attendance/start')
  },
}

export const adminAPI = {
  registerUser: (userData: {
    name: string
    user_id: string
    username: string
    password: string
    type: string
    class_section?: string
  }) => api.post('/admin/register', userData),
  captureUserFaces: (userData: { user_id: string; name: string }) => 
    api.post('/admin/capture-face', userData),
  scanFace: (imageData: { image: string; user_id?: string; name?: string }) => 
    api.post('/admin/scan-face', imageData),
  checkFaceDetection: () => api.post('/admin/check-face-detection'),
  testCamera: () => api.post('/admin/test-camera'),
  getUsers: () => {
    if (isDemoMode()) {
      return mockAdminAPI.getUsers()
    }
    return api.get('/admin/users')
  },
  deleteUser: (userId: string) => api.delete(`/admin/users/${userId}`),
  updateUser: (userId: string, userData: any) => api.put(`/admin/users/${userId}`, userData),
  updateUserPassword: (userId: string, password: string) => 
    api.put(`/admin/users/${userId}/password`, { password }),
  resetPassword: (userId: string, password: string) => 
    api.put(`/admin/users/${userId}/password`, { password }),
  getNotices: () => {
    if (isDemoMode()) {
      return mockAdminAPI.getNotices()
    }
    return api.get('/admin/notices')
  },
  createNotice: (notice: { title: string; content: string; priority?: string }) => 
    api.post('/admin/notices', notice),
  deleteNotice: (noticeId: string) => api.delete(`/admin/notices/${noticeId}`),
  getAttendanceHistory: () => {
    if (isDemoMode()) {
      return mockAdminAPI.getAttendanceHistory()
    }
    return api.get('/admin/attendance-history')
  },
  
  // Backup and Export functions
  backupDatabase: () => api.post('/admin/backup/database'),
  exportToJson: () => api.post('/admin/export/json'),
  exportToCsv: (date?: string) => api.post('/admin/export/csv', { date }),
  downloadFile: (filename: string) => {
    return api.get(`/admin/download/${filename}`, {
      responseType: 'blob',
      headers: {
        'Accept': 'application/octet-stream',
      },
    })
  },
  
  // Class Management APIs
  saveClassConfig: (config: any) => api.post('/admin/class-config', config),
  saveTimeSettings: (settings: any) => api.post('/admin/time-settings', settings),
  getActiveClasses: () => api.get('/admin/active-classes'),
  getAnalytics: () => {
    if (isDemoMode()) {
      return mockAdminAPI.getAnalytics()
    }
    return api.get('/admin/analytics')
  },
  getRecentActivity: () => {
    if (isDemoMode()) {
      return mockAdminAPI.getRecentActivity()
    }
    return api.get('/admin/recent-activity')
  },
  
  // Demo Data Management
  populateDemoData: () => api.post('/admin/populate-demo-data'),
  getDemoSummary: () => api.get('/admin/demo-summary'),
}

export const analyticsAPI = {
  getAttendanceTrends: () => api.get('/analytics/attendance-trends'),
}

export const userAPI = {
  login: (credentials: { username: string; password: string }) => 
    api.post('/user/login', credentials),
  getMyAttendance: () => {
    if (isDemoMode()) {
      return mockUserAPI.getMyAttendance()
    }
    return api.get('/user/my-attendance')
  },
  getMyProfile: () => {
    if (isDemoMode()) {
      return mockUserAPI.getMyProfile()
    }
    return api.get('/user/my-profile')
  },
  getUserAnalytics: () => {
    if (isDemoMode()) {
      return mockUserAPI.getUserAnalytics()
    }
    return api.get('/user/analytics')
  },
  getUserNotices: () => {
    if (isDemoMode()) {
      return mockUserAPI.getUserNotices()
    }
    return api.get('/user/notices')
  },
  getNotices: () => {
    if (isDemoMode()) {
      return mockUserAPI.getUserNotices()
    }
    return api.get('/user/notices')
  },
  markAttendance: () => {
    if (isDemoMode()) {
      return mockUserAPI.markAttendance()
    }
    return api.post('/user/mark-attendance')
  },
  markAttendanceWithImage: (data: { image: string }) => api.post('/user/mark-attendance-with-image', data),
  startFaceScan: () => api.post('/user/start-face-scan'),
  getMyAnalytics: () => {
    if (isDemoMode()) {
      return mockUserAPI.getUserAnalytics()
    }
    return api.get('/user/analytics')
  },
  getAttendanceStats: () => {
    if (isDemoMode()) {
      return mockUserAPI.getAttendanceStats()
    }
    return api.get('/user/attendance-stats')
  },
}

export const profileAPI = {
  getUserProfile: (userId: string) => api.get(`/profile/${userId}`),
}

export default api
