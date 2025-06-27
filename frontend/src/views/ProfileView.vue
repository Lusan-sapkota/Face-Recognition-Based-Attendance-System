<template>
  <div class="profile">
    <div class="container">
      <div class="profile-header">
        <button @click="goBack" class="btn btn-secondary back-btn">
          ← Back
        </button>
        <h1 class="profile-title gradient-text">User Profile</h1>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Loading profile...</p>
      </div>

      <div v-else-if="user" class="profile-content">
        <!-- User Info Card -->
        <div class="profile-info card">
          <div class="profile-avatar">
            <div class="avatar-placeholder">
              {{ user.name.charAt(0).toUpperCase() }}
            </div>
          </div>
          
          <div class="user-details">
            <h2 class="user-name">{{ user.name }}</h2>
            <div class="user-meta">
              <span class="user-id">ID: {{ user.id }}</span>
              <span class="user-type" :class="`type-${user.type}`">{{ user.type }}</span>
            </div>
            <div v-if="user.class_section" class="user-class">
              Class/Section: {{ user.class_section }}
            </div>
            <div class="registration-date">
              Registered: {{ formatDate(user.registered_date) }}
            </div>
          </div>
        </div>

        <!-- Attendance Statistics -->
        <div class="attendance-stats">
          <div class="grid grid-cols-3 stats-grid">
            <div class="stat-card card">
              <div class="stat-icon">📅</div>
              <div class="stat-value">{{ attendanceHistory.length }}</div>
              <div class="stat-label">Total Days</div>
            </div>
            
            <div class="stat-card card">
              <div class="stat-icon">📈</div>
              <div class="stat-value">{{ attendanceRate }}%</div>
              <div class="stat-label">Attendance Rate</div>
            </div>
            
            <div class="stat-card card">
              <div class="stat-icon">⏰</div>
              <div class="stat-value">{{ averageTime }}</div>
              <div class="stat-label">Avg Check-in</div>
            </div>
          </div>
        </div>

        <!-- Attendance History -->
        <div class="attendance-history card">
          <div class="section-header">
            <h3 class="section-title">Attendance History</h3>
            <div class="history-filter">
              <select v-model="filterPeriod" class="filter-select">
                <option value="all">All Time</option>
                <option value="month">This Month</option>
                <option value="week">This Week</option>
              </select>
            </div>
          </div>

          <div v-if="filteredAttendance.length > 0" class="history-list">
            <div class="history-table-container">
              <table class="table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Check-in Time</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="record in filteredAttendance" :key="`${record.date}-${record.time}`">
                    <td>{{ formatAttendanceDate(record.date) }}</td>
                    <td>{{ record.time }}</td>
                    <td>
                      <span class="status-badge" :class="getStatusClass(record.time)">
                        {{ getStatus(record.time) }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div v-else class="empty-attendance">
            <div class="empty-icon">📊</div>
            <h4 class="empty-title">No attendance records</h4>
            <p class="empty-description">
              {{ filterPeriod === 'all' ? 'No attendance records found for this user' : `No records for ${filterPeriod}` }}
            </p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="quick-actions card">
          <h3 class="section-title">Quick Actions</h3>
          <div class="actions-grid">
            <button @click="exportData" class="action-btn">
              <div class="action-icon">📥</div>
              <span>Export Data</span>
            </button>
            
            <button @click="viewCalendar" class="action-btn">
              <div class="action-icon">📅</div>
              <span>View Calendar</span>
            </button>
            
            <button @click="generateReport" class="action-btn">
              <div class="action-icon">📊</div>
              <span>Generate Report</span>
            </button>
            
            <button v-if="authStore.isAdmin" @click="editUser" class="action-btn">
              <div class="action-icon">✏️</div>
              <span>Edit User</span>
            </button>
          </div>
        </div>
      </div>

      <div v-else class="error-state">
        <div class="error-icon">❌</div>
        <h3 class="error-title">User Not Found</h3>
        <p class="error-description">The requested user profile could not be found.</p>
        <button @click="goBack" class="btn btn-primary">Go Back</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/counter'
import { profileAPI } from '../services/api'

interface User {
  name: string
  id: string
  type: 'student' | 'employee'
  class_section?: string
  registered_date: string
}

interface AttendanceRecord {
  date: string
  time: string
  name: string
}

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const user = ref<User | null>(null)
const attendanceHistory = ref<AttendanceRecord[]>([])
const loading = ref(true)
const filterPeriod = ref('all')

const userId = route.params.id as string

// Computed properties
const attendanceRate = computed(() => {
  if (attendanceHistory.value.length === 0) return 0
  // Simplified calculation - in real app, you'd compare with expected attendance days
  const expectedDays = 30 // Example: last 30 days
  return Math.min(100, Math.round((attendanceHistory.value.length / expectedDays) * 100))
})

const averageTime = computed(() => {
  if (attendanceHistory.value.length === 0) return '--:--'
  
  const times = attendanceHistory.value.map((record: AttendanceRecord) => {
    const [hours, minutes] = record.time.split(':').map(Number)
    return hours * 60 + minutes // Convert to minutes
  })
  
  const avgMinutes = times.reduce((sum, time) => sum + time, 0) / times.length
  const hours = Math.floor(avgMinutes / 60)
  const minutes = Math.round(avgMinutes % 60)
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
})

const filteredAttendance = computed(() => {
  if (filterPeriod.value === 'all') return attendanceHistory.value
  
  const now = new Date()
  const filtered = attendanceHistory.value.filter((record: AttendanceRecord) => {
    const recordDate = parseAttendanceDate(record.date)
    
    if (filterPeriod.value === 'week') {
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
      return recordDate >= weekAgo
    } else if (filterPeriod.value === 'month') {
      const monthAgo = new Date(now.getFullYear(), now.getMonth() - 1, now.getDate())
      return recordDate >= monthAgo
    }
    
    return true
  })
  
  return filtered.sort((a: any, b: any) => {
    const dateA = parseAttendanceDate(a.date)
    const dateB = parseAttendanceDate(b.date)
    return dateB.getTime() - dateA.getTime() // Most recent first
  })
})

// Methods
const loadUserProfile = async () => {
  try {
    loading.value = true
    const response = await profileAPI.getUserProfile(userId)
    user.value = response.data.user
    attendanceHistory.value = response.data.attendance_history || []
  } catch (error) {
    console.error('Error loading user profile:', error)
    user.value = null
  } finally {
    loading.value = false
  }
}

const parseAttendanceDate = (dateString: string) => {
  // Parse MM_DD_YY format
  const [month, day, year] = dateString.split('_').map(Number)
  return new Date(2000 + year, month - 1, day)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatAttendanceDate = (dateString: string) => {
  const date = parseAttendanceDate(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getStatus = (time: string) => {
  const [hours, minutes] = time.split(':').map(Number)
  const timeInMinutes = hours * 60 + minutes
  
  // Assuming work/school starts at 9:00 AM (540 minutes)
  if (timeInMinutes <= 540) return 'On Time'
  if (timeInMinutes <= 570) return 'Late' // Up to 9:30 AM
  return 'Very Late'
}

const getStatusClass = (time: string) => {
  const status = getStatus(time)
  return {
    'status-on-time': status === 'On Time',
    'status-late': status === 'Late',
    'status-very-late': status === 'Very Late'
  }
}

const goBack = () => {
  router.go(-1)
}

const exportData = () => {
  // Implement data export
  alert('Export feature coming soon!')
}

const viewCalendar = () => {
  alert('Calendar view coming soon!')
}

const generateReport = () => {
  alert('Report generation coming soon!')
}

const editUser = () => {
  alert('User editing coming soon!')
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.profile {
  padding: 40px 0;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 40px;
}

.back-btn {
  padding: 8px 16px;
}

.profile-title {
  font-size: 2.5rem;
  font-weight: 700;
}

/* Profile Info */
.profile-info {
  display: flex;
  align-items: center;
  gap: 32px;
  padding: 40px;
  margin-bottom: 32px;
}

.profile-avatar {
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 700;
  color: white;
}

.user-details {
  flex: 1;
}

.user-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.user-id {
  font-size: 16px;
  color: var(--text-secondary);
  font-weight: 500;
}

.user-type {
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
  text-transform: capitalize;
}

.type-student {
  background: rgba(0, 191, 255, 0.2);
  color: var(--accent-color);
}

.type-employee {
  background: rgba(138, 43, 226, 0.2);
  color: var(--gradient-end);
}

.user-class,
.registration-date {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 8px;
}

/* Stats */
.attendance-stats {
  margin-bottom: 32px;
}

.stats-grid {
  gap: 24px;
}

.stat-card {
  text-align: center;
  padding: 32px 24px;
}

.stat-icon {
  font-size: 32px;
  margin-bottom: 16px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 8px;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Attendance History */
.attendance-history {
  padding: 32px;
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.filter-select {
  padding: 8px 16px;
  background: var(--input-background);
  border: 1px solid var(--input-border);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
}

.history-table-container {
  max-height: 400px;
  overflow-y: auto;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.status-on-time {
  background: rgba(0, 255, 127, 0.2);
  color: var(--success-color);
}

.status-late {
  background: rgba(255, 215, 0, 0.2);
  color: var(--warning-color);
}

.status-very-late {
  background: rgba(255, 107, 107, 0.2);
  color: var(--danger-color);
}

/* Empty States */
.empty-attendance {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-description {
  color: var(--text-secondary);
  font-size: 14px;
}

/* Quick Actions */
.quick-actions {
  padding: 32px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  background: var(--input-background);
  border: 1px solid var(--input-border);
  border-radius: 12px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: var(--card-background);
  transform: translateY(-2px);
}

.action-icon {
  font-size: 24px;
}

.action-btn span {
  font-size: 14px;
  font-weight: 500;
}

/* Error State */
.error-state {
  text-align: center;
  padding: 80px 20px;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.error-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.error-description {
  color: var(--text-secondary);
  font-size: 16px;
  margin-bottom: 24px;
}

/* Loading */
.loading {
  text-align: center;
  padding: 80px 20px;
}

.loading p {
  margin-top: 16px;
  color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 1024px) {
  .profile-info {
    flex-direction: column;
    text-align: center;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .profile {
    padding: 20px 0;
  }
  
  .profile-title {
    font-size: 2rem;
  }
  
  .profile-info,
  .attendance-history,
  .quick-actions {
    padding: 24px 16px;
  }
  
  .user-name {
    font-size: 1.5rem;
  }
  
  .user-meta {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>
