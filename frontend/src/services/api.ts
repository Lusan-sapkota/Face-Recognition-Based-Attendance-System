import axios from 'axios'

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
  adminLogin: (password: string) => api.post('/admin/login', { password }),
  userLogin: (username: string, password: string) => api.post('/user/login', { username, password }),
  // Legacy login for backward compatibility
  login: (password: string) => api.post('/login', { password }),
}

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getAttendance: () => api.get('/attendance'),
  startAttendance: () => api.post('/attendance/start'),
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
  getUsers: () => api.get('/admin/users'),
  deleteUser: (userId: string) => api.delete(`/admin/users/${userId}`),
  updateUser: (userId: string, userData: any) => api.put(`/admin/users/${userId}`, userData),
  updateUserPassword: (userId: string, password: string) => 
    api.put(`/admin/users/${userId}/password`, { password }),
  resetPassword: (userId: string, password: string) => 
    api.put(`/admin/users/${userId}/password`, { password }),
  getNotices: () => api.get('/admin/notices'),
  createNotice: (notice: { title: string; content: string; priority?: string }) => 
    api.post('/admin/notices', notice),
  deleteNotice: (noticeId: string) => api.delete(`/admin/notices/${noticeId}`),
  getAttendanceHistory: () => api.get('/admin/attendance-history'),
  
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
  getAnalytics: () => api.get('/admin/analytics'),
  getRecentActivity: () => api.get('/admin/recent-activity'), // New endpoint
}

export const analyticsAPI = {
  getAttendanceTrends: () => api.get('/analytics/attendance-trends'),
}

export const profileAPI = {
  getUserProfile: (userId: string) => api.get(`/profile/${userId}`),
}

export const userAPI = {
  login: (credentials: { username: string; password: string }) => 
    api.post('/user/login', credentials),
  getMyAttendance: () => api.get('/user/attendance'),
  getMyProfile: () => api.get('/user/profile'),
  getNotices: () => api.get('/user/notices'),
  markAttendance: () => api.post('/user/mark-attendance'),
  markAttendanceWithImage: (data: { image: string }) => api.post('/user/mark-attendance-with-image', data),
  startFaceScan: () => api.post('/user/start-face-scan'),
  getMyAnalytics: () => api.get('/user/analytics'), // New endpoint
}

export default api
