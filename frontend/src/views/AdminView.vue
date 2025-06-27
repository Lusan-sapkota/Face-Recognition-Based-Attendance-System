<template>
  <div class="admin">
    <div class="container">
      <div class="admin-header">
        <h1 class="admin-title gradient-text">Admin Panel</h1>
        <p class="admin-subtitle">Manage users, notices, and system settings</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="admin-nav">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="nav-tab"
          :class="{ active: activeTab === tab.id }"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Register User Tab -->
      <div v-if="activeTab === 'register'" class="tab-content">
        <div class="register-section card">
          <div class="section-header">
            <h3 class="section-title">Register New User</h3>
            <p class="section-description">
              Register a new user and capture their face data for attendance tracking
            </p>
          </div>
          
          <div class="register-action">
            <button @click="openRegistrationModal" class="btn btn-primary btn-large">
              <span class="btn-icon">👤➕</span>
              <span class="btn-text">
                <strong>Open Registration Modal</strong>
                <small>Complete user registration with face capture</small>
              </span>
            </button>
          </div>
          
          <div v-if="Object.keys(users).length > 0" class="recent-registrations">
            <h4>Recent Registrations</h4>
            <div class="users-grid">
              <div v-for="(user, key) in Object.entries(users).slice(0, 6)" :key="key" class="user-preview-card">
                <div class="user-avatar">
                  {{ user[1].name.charAt(0).toUpperCase() }}
                </div>
                <div class="user-info">
                  <h5>{{ user[1].name }}</h5>
                  <p>{{ user[1].type }} • {{ user[1].id }}</p>
                  <span class="registration-date">{{ formatDate(user[1].registered_date) }}</span>
                </div>
                <button 
                  v-if="!hasUserFaceData(user[1])"
                  @click="openFaceCaptureModal(user[1])"
                  class="btn btn-sm btn-secondary"
                  title="Capture Face Data"
                >
                  📸
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Manage Users Tab -->
      <div v-if="activeTab === 'users'" class="tab-content">
        <div class="users-section card">
          <div class="section-header">
            <h3 class="section-title">Registered Users</h3>
            <div class="user-stats">
              <span class="stat-item">Total: {{ Object.keys(users).length }}</span>
              <span class="stat-item">Students: {{ studentCount }}</span>
              <span class="stat-item">Employees: {{ employeeCount }}</span>
            </div>
          </div>
          
          <div v-if="Object.keys(users).length > 0" class="users-table-container">
            <table class="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>ID</th>
                  <th>Type</th>
                  <th>Class/Section</th>
                  <th>Registered</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, key) in users" :key="key">
                  <td>{{ user.name }}</td>
                  <td>{{ user.id }}</td>
                  <td>
                    <span class="type-badge" :class="`type-${user.type}`">
                      {{ user.type }}
                    </span>
                  </td>
                  <td>{{ user.class_section || '-' }}</td>
                  <td>{{ formatDate(user.registered_date) }}</td>
                  <td>
                    <div class="action-buttons">
                      <button 
                        v-if="!hasUserFaceData(user)"
                        @click="openFaceCaptureModal(user)"
                        class="btn btn-secondary btn-sm"
                        title="Capture Face Data"
                      >
                        �
                      </button>
                      <button 
                        v-else
                        @click="openFaceCaptureModal(user)"
                        class="btn btn-info btn-sm"
                        title="Recapture Face Data"
                      >
                        🔄
                      </button>
                      <button 
                        @click="openEditModal(user)"
                        class="btn btn-primary btn-sm"
                        title="Edit User"
                      >
                        ✏️
                      </button>
                      <button 
                        @click="openPasswordModal(user)"
                        class="btn btn-warning btn-sm"
                        title="Reset Password"
                      >
                        🔑
                      </button>
                      <RouterLink 
                        :to="`/profile/${user.id}`"
                        class="btn btn-info btn-sm"
                        title="View Profile"
                      >
                        👤
                      </RouterLink>
                      <button 
                        @click="deleteUser(user)"
                        class="btn btn-danger btn-sm"
                        title="Delete User"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div v-else class="empty-state">
            <div class="empty-icon">👥</div>
            <h4 class="empty-title">No users registered yet</h4>
            <p class="empty-description">Start by registering your first user</p>
          </div>
        </div>
      </div>

      <!-- Notices Tab -->
      <div v-if="activeTab === 'notices'" class="tab-content">
        <div class="grid grid-cols-2 notices-grid">
          <div class="create-notice card">
            <h3 class="form-title">Create Notice</h3>
            <form @submit.prevent="createNotice">
              <div class="input-group">
                <label class="input-label">Title</label>
                <input 
                  v-model="newNotice.title" 
                  type="text" 
                  class="input-field" 
                  placeholder="Notice title"
                  required 
                />
              </div>
              
              <div class="input-group">
                <label class="input-label">Content</label>
                <textarea 
                  v-model="newNotice.content" 
                  class="input-field textarea" 
                  placeholder="Notice content..."
                  rows="5"
                  required
                ></textarea>
              </div>
              
              <button type="submit" class="btn btn-primary" :disabled="isCreatingNotice">
                <span v-if="isCreatingNotice" class="spinner"></span>
                {{ isCreatingNotice ? 'Creating...' : 'Post Notice' }}
              </button>
            </form>
          </div>
          
          <div class="notices-list card">
            <h3 class="form-title">Recent Notices</h3>
            <div v-if="notices.length > 0" class="notices-container">
              <div v-for="notice in notices" :key="notice.id" class="notice-item">
                <div class="notice-header">
                  <h4 class="notice-title">{{ notice.title }}</h4>
                  <span class="notice-date">{{ formatDate(notice.created_at) }}</span>
                </div>
                <p class="notice-content">{{ notice.content }}</p>
              </div>
            </div>
            <div v-else class="empty-state">
              <div class="empty-icon">📢</div>
              <h4 class="empty-title">No notices yet</h4>
              <p class="empty-description">Create your first notice</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Tab -->
      <div v-if="activeTab === 'analytics'" class="tab-content">
        <div class="analytics-section card">
          <h3 class="form-title">Attendance Analytics</h3>
          <div class="analytics-content">
            <!-- Summary Statistics -->
            <div class="analytics-stats">
              <div class="analytics-card">
                <h4>Total Users</h4>
                <div class="analytics-value">{{ totalUsers }}</div>
                <div class="analytics-trend">Registered Users</div>
              </div>
              <div class="analytics-card">
                <h4>This Week</h4>
                <div class="analytics-value">{{ weeklyAttendance }}</div>
                <div class="analytics-trend">Attendance Records</div>
              </div>
              <div class="analytics-card">
                <h4>This Month</h4>
                <div class="analytics-value">{{ monthlyAttendance }}</div>
                <div class="analytics-trend">Attendance Records</div>
              </div>
              <div class="analytics-card">
                <h4>Average Daily</h4>
                <div class="analytics-value">{{ dailyAverage }}%</div>
                <div class="analytics-trend">Attendance Rate</div>
              </div>
            </div>
            
            <!-- Date Filter -->
            <div class="date-filter">
              <label class="input-label">📅 Filter by Date Range:</label>
              <div class="date-inputs">
                <div class="date-group">
                  <label class="date-label">From:</label>
                  <input 
                    v-model="analyticsDateFrom" 
                    type="date" 
                    class="input-field date-input"
                    :max="analyticsDateTo || new Date().toISOString().split('T')[0]"
                  />
                </div>
                <div class="date-connector">to</div>
                <div class="date-group">
                  <label class="date-label">To:</label>
                  <input 
                    v-model="analyticsDateTo" 
                    type="date" 
                    class="input-field date-input"
                    :min="analyticsDateFrom"
                    :max="new Date().toISOString().split('T')[0]"
                  />
                </div>
                <button 
                  @click="filterAnalytics" 
                  class="btn btn-primary filter-btn"
                  :disabled="!analyticsDateFrom || !analyticsDateTo || isFilteringAnalytics"
                >
                  <span v-if="isFilteringAnalytics" class="spinner"></span>
                  {{ isFilteringAnalytics ? 'Filtering...' : '📊 Apply Filter' }}
                </button>
                <button 
                  @click="clearAnalyticsFilter" 
                  class="btn btn-secondary filter-btn"
                  v-if="analyticsDateFrom || analyticsDateTo"
                >
                  🔄 Clear
                </button>
              </div>
            </div>
            
            <!-- User Activity Chart -->
            <div class="chart-section">
              <h4>📈 User Activity Trends</h4>
              <div class="user-activity-chart">
                <div v-if="userActivityData.length > 0" class="activity-bars">
                  <div 
                    v-for="(activity, index) in userActivityData" 
                    :key="index"
                    class="activity-bar"
                    :style="{ 
                      height: Math.max(activity.percentage, 5) + '%',
                      background: getActivityBarColor(activity.percentage)
                    }"
                    :title="`${activity.name}: ${activity.attendance_count} days (${activity.percentage}%)`"
                  >
                    <span class="bar-label">{{ activity.name.split(' ')[0] }}</span>
                    <span class="bar-value">{{ activity.percentage }}%</span>
                  </div>
                </div>
                <div v-else class="no-data">
                  <div class="no-data-icon">📊</div>
                  <h4>No activity data available</h4>
                  <p>User activity will appear here once attendance is recorded</p>
                </div>
              </div>
            </div>
            
            <!-- Attendance History -->
            <div class="attendance-history">
              <h4>Recent Attendance History</h4>
              <div v-if="attendanceHistory && Object.keys(attendanceHistory).length > 0" class="history-container">
                <div v-for="(records, date) in attendanceHistory" :key="date" class="history-item">
                  <div class="history-header">
                    <span class="history-date">{{ formatDateKey(date) }}</span>
                    <span class="history-count">{{ records.length }} records</span>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state">
                <p>No attendance history available</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Backup & Export Tab -->
      <div v-if="activeTab === 'backup'" class="tab-content">
        <div class="backup-section">
          <div class="grid grid-cols-2 backup-grid">
            <!-- Database Backup -->
            <div class="backup-card card">
              <h3 class="form-title">Database Backup</h3>
              <p class="backup-description">
                Create a complete backup of the database including all users, attendance records, and notices.
              </p>
              <button 
                @click="backupDatabase" 
                :disabled="isBackingUp"
                class="btn btn-primary backup-btn"
              >
                {{ isBackingUp ? 'Creating Backup...' : 'Create Database Backup' }}
              </button>
            </div>

            <!-- Export to JSON -->
            <div class="backup-card card">
              <h3 class="form-title">Export to JSON</h3>
              <p class="backup-description">
                Export all data in JSON format for data analysis or migration purposes.
              </p>
              <button 
                @click="exportToJson" 
                :disabled="isExportingJson"
                class="btn btn-secondary backup-btn"
              >
                {{ isExportingJson ? 'Exporting...' : 'Export to JSON' }}
              </button>
            </div>

            <!-- Export Attendance CSV -->
            <div class="backup-card card">
              <h3 class="form-title">Export Attendance</h3>
              <p class="backup-description">
                Export attendance records in CSV format for spreadsheet analysis.
              </p>
              <div class="export-options">
                <select v-model="selectedExportDate" class="select-field">
                  <option value="">All Dates</option>
                  <option v-for="date in availableDates" :key="date" :value="date">
                    {{ formatDateOption(date) }}
                  </option>
                </select>
                <button 
                  @click="exportToCsv" 
                  :disabled="isExportingCsv"
                  class="btn btn-success backup-btn"
                >
                  {{ isExportingCsv ? 'Exporting...' : 'Export to CSV' }}
                </button>
              </div>
            </div>

            <!-- Recent Backups/Exports -->
            <div class="backup-card card">
              <h3 class="form-title">Recent Operations</h3>
              <div class="backup-list">
                <div v-if="recentOperations.length === 0" class="empty-state">
                  <p>No recent backup or export operations</p>
                </div>
                <div v-else>
                  <div 
                    v-for="operation in recentOperations" 
                    :key="operation.id"
                    class="backup-item"
                  >
                    <div class="backup-item-info">
                      <span class="backup-type">{{ operation.type }}</span>
                      <span class="backup-date">{{ formatDateTime(operation.timestamp) }}</span>
                    </div>
                    <button 
                      v-if="operation.downloadable"
                      @click="downloadFile(operation.filename)"
                      class="btn btn-sm btn-outline"
                    >
                      Download
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- User Registration Modal -->
  <UserRegistrationModal 
    :show="showRegistrationModal" 
    :existing-user="userForFaceCapture"
    @close="closeRegistrationModal"
    @success="onRegistrationSuccess"
  />

  <!-- Face Capture Modal -->
  <div v-if="showCaptureModal" class="modal-overlay" @click="closeCaptureModal">
    <div class="capture-modal" @click.stop>
      <div class="modal-header">
        <h3>Face Capture - {{ selectedUserForCapture?.name }}</h3>
        <button @click="closeCaptureModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="capture-status">
          <div class="status-indicator" :class="faceDetectionStatus.class">
            <div class="status-icon">{{ faceDetectionStatus.icon }}</div>
            <div class="status-text">{{ faceDetectionStatus.message }}</div>
          </div>
        </div>
        
        <div class="capture-progress" v-if="captureProgress.total > 0">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: (captureProgress.current / captureProgress.total) * 100 + '%' }"
            ></div>
          </div>
          <span class="progress-text">
            {{ captureProgress.current }} / {{ captureProgress.total }} images captured
          </span>
        </div>
        
        <div class="modal-actions">
          <button 
            @click="startCapture" 
            class="btn btn-primary"
            :disabled="isCapturing || !faceDetectionStatus.ready"
          >
            <span v-if="isCapturing" class="spinner"></span>
            {{ isCapturing ? 'Capturing...' : 'Start Capture' }}
          </button>
          <button @click="closeCaptureModal" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit User Modal -->
  <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
    <div class="edit-modal" @click.stop>
      <div class="modal-header">
        <h3>Edit User - {{ editingUser?.name }}</h3>
        <button @click="closeEditModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="saveUserEdit">
          <div class="input-group">
            <label class="input-label">Name</label>
            <input 
              v-model="editingUser!.name" 
              type="text" 
              class="input-field" 
              placeholder="Enter full name"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">User ID</label>
            <input 
              v-model="editingUser!.user_id" 
              type="text" 
              class="input-field" 
              placeholder="Enter unique ID"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">Username</label>
            <input 
              v-model="editingUser!.username" 
              type="text" 
              class="input-field" 
              placeholder="Enter username for login"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">Type</label>
            <select v-model="editingUser!.type" class="input-field" required>
              <option value="student">Student</option>
              <option value="employee">Employee</option>
            </select>
          </div>
          
          <div class="input-group" v-if="editingUser!.type === 'student'">
            <label class="input-label">Class/Section</label>
            <input 
              v-model="editingUser!.class_section" 
              type="text" 
              class="input-field" 
              placeholder="e.g., 10th Grade A"
            />
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary" :disabled="isUpdatingUser">
              <span v-if="isUpdatingUser" class="spinner"></span>
              {{ isUpdatingUser ? 'Updating...' : 'Update User' }}
            </button>
            <button @click="closeEditModal" class="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Reset Password Modal -->
  <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
    <div class="password-modal" @click.stop>
      <div class="modal-header">
        <h3>Reset Password - {{ resetPasswordUser?.name }}</h3>
        <button @click="closePasswordModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="input-group">
          <label class="input-label">New Password</label>
          <input 
            v-model="newPassword" 
            type="password" 
            class="input-field" 
            placeholder="Enter new password (min 6 characters)"
            minlength="6"
            required 
          />
        </div>
        
        <div class="modal-actions">
          <button @click="resetUserPassword" class="btn btn-primary" :disabled="isUpdatingPassword">
            <span v-if="isUpdatingPassword" class="spinner"></span>
            {{ isUpdatingPassword ? 'Updating...' : 'Reset Password' }}
          </button>
          <button @click="closePasswordModal" class="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Registration Modal -->
  <div v-if="showRegistrationModal" class="modal-overlay" @click="closeRegistrationModal">
    <div class="registration-modal" @click.stop>
      <div class="modal-header">
        <h3>Register User</h3>
        <button @click="closeRegistrationModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="registerUser">
          <div class="input-group">
            <label class="input-label">Name</label>
            <input 
              v-model="newUser.name" 
              type="text" 
              class="input-field" 
              placeholder="Enter full name"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">User ID</label>
            <input 
              v-model="newUser.user_id" 
              type="text" 
              class="input-field" 
              placeholder="Enter unique ID"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">Username</label>
            <input 
              v-model="newUser.username" 
              type="text" 
              class="input-field" 
              placeholder="Enter username for login"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">Password</label>
            <input 
              v-model="newUser.password" 
              type="password" 
              class="input-field" 
              placeholder="Enter password (min 6 characters)"
              minlength="6"
              required 
            />
          </div>
          
          <div class="input-group">
            <label class="input-label">Type</label>
            <select v-model="newUser.type" class="input-field" required>
              <option value="student">Student</option>
              <option value="employee">Employee</option>
            </select>
          </div>
          
          <div class="input-group" v-if="newUser.type === 'student'">
            <label class="input-label">Class/Section</label>
            <input 
              v-model="newUser.class_section" 
              type="text" 
              class="input-field" 
              placeholder="e.g., 10th Grade A"
            />
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn btn-primary" :disabled="isRegistering">
              <span v-if="isRegistering" class="spinner"></span>
              {{ isRegistering ? 'Registering...' : 'Register User' }}
            </button>
            <button @click="closeRegistrationModal" class="btn btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Notification Toast -->
  <NotificationToast
    :show="notification.show"
    :type="notification.type"
    :title="notification.title"
    :message="notification.message"
    @close="closeNotification"
  />
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { adminAPI } from '../services/api'
import UserRegistrationModal from '../components/UserRegistrationModal.vue'
import NotificationToast from '../components/NotificationToast.vue'

interface User {
  name: string
  id: string
  type: 'student' | 'employee'
  class_section?: string
  registered_date: string
  user_id?: string
  username?: string
}

interface Notice {
  id: number
  title: string
  content: string
  created_at: string
  created_by: string
}

interface FaceCaptureUser {
  id: string
  name: string
  user_id: string
  type: string
  class_section?: string
}

interface NewUser {
  name: string
  user_id: string
  username: string
  password: string
  type: 'student' | 'employee'
  class_section: string
}

interface NewNotice {
  title: string
  content: string
}

interface SelectedUser extends User {
  key: string
}

const activeTab = ref('register')
const showCaptureModal = ref(false)
const showEditModal = ref(false)
const showPasswordModal = ref(false)
const showRegistrationModal = ref(false)
const userForFaceCapture = ref<FaceCaptureUser | null>(null)
const faceDetectionStatus = ref({
  ready: false,
  message: 'Checking camera...',
  icon: '📷',
  class: 'checking'
})
const captureProgress = ref({
  current: 0,
  total: 0
})
let detectionInterval: any = null
const users = ref<Record<string, User>>({})
const notices = ref<Notice[]>([])
const attendanceHistory = ref<Record<string, any[]>>({})

const tabs = [
  { id: 'register', label: 'Register User' },
  { id: 'users', label: 'Manage Users' },
  { id: 'notices', label: 'Notices' },
  { id: 'analytics', label: 'Analytics' },
  { id: 'backup', label: 'Backup & Export' }
]

// User Registration
const newUser = ref<NewUser>({
  name: '',
  user_id: '',
  username: '',
  password: '',
  type: 'student',
  class_section: ''
})

const isRegistering = ref(false)
const isCapturing = ref(false)
const selectedUserForCapture = ref<SelectedUser | null>(null)

// User Management
const editingUser = ref<User | null>(null)
const selectedUserForPassword = ref<User | null>(null)
const resetPasswordUser = ref<User | null>(null)
const newPassword = ref('')
const isUpdatingUser = ref(false)
const isUpdatingPassword = ref(false)
const isProcessingUser = ref<string | null>(null)

// Notice Management
const newNotice = ref<NewNotice>({
  title: '',
  content: ''
})

const isCreatingNotice = ref(false)

// Backup & Export Management
const isBackingUp = ref(false)
const isExportingJson = ref(false)
const isExportingCsv = ref(false)
const selectedExportDate = ref('')
const recentOperations = ref<BackupOperation[]>([])
const availableDates = ref<string[]>([])

// Analytics
const analyticsDateFrom = ref('')
const analyticsDateTo = ref('')
const userActivityData = ref<any[]>([])
const isFilteringAnalytics = ref(false)

// Notification system
const notification = ref({
  show: false,
  type: 'info' as 'success' | 'error' | 'warning' | 'info',
  title: '',
  message: ''
})

const showNotification = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string) => {
  notification.value = {
    show: true,
    type,
    title,
    message
  }
}

const closeNotification = () => {
  notification.value.show = false
}

const filterAnalytics = async () => {
  if (!analyticsDateFrom.value || !analyticsDateTo.value) {
    showNotification('warning', 'Date Selection Required', 'Please select both start and end dates')
    return
  }
  
  isFilteringAnalytics.value = true
  try {
    const response = await adminAPI.getAnalytics()
    userActivityData.value = response.data.userActivity || []
    // Show success feedback
    showNotification('success', 'Analytics Filtered', 
      `Analytics filtered from ${formatDate(analyticsDateFrom.value)} to ${formatDate(analyticsDateTo.value)}`)
  } catch (error) {
    console.error('Error filtering analytics:', error)
    showNotification('error', 'Filter Error', 'Error filtering analytics. Please try again.')
  } finally {
    isFilteringAnalytics.value = false
  }
}

const clearAnalyticsFilter = async () => {
  analyticsDateFrom.value = ''
  analyticsDateTo.value = ''
  isFilteringAnalytics.value = true
  try {
    const response = await adminAPI.getAnalytics()
    userActivityData.value = response.data.userActivity || []
  } catch (error) {
    console.error('Error loading analytics:', error)
  } finally {
    isFilteringAnalytics.value = false
  }
}

interface BackupOperation {
  id: string
  type: string
  timestamp: string
  filename: string
  downloadable: boolean
}

// Computed Properties
const studentCount = computed(() => {
  return Object.values(users.value).filter((user: User) => user.type === 'student').length
})

const employeeCount = computed(() => {
  return Object.values(users.value).filter((user: User) => user.type === 'employee').length
})

const weeklyAttendance = computed(() => {
  // Calculate weekly attendance from history
  return Object.values(attendanceHistory.value).reduce((sum: number, records: any[]) => sum + records.length, 0)
})

const monthlyAttendance = computed(() => {
  // Calculate monthly attendance
  return weeklyAttendance.value // Simplified for demo
})

const dailyAverage = computed(() => {
  const totalDays = Object.keys(attendanceHistory.value).length
  const totalUsers = Object.keys(users.value).length
  if (totalDays > 0 && totalUsers > 0) {
    return Math.round((weeklyAttendance.value / (totalDays * totalUsers)) * 100)
  }
  return 0
})

const totalUsers = computed(() => {
  return Object.keys(users.value).length
})

// Methods
const loadUsers = async () => {
  try {
    const response = await adminAPI.getUsers()
    // Convert array to object for backward compatibility
    const usersArray = response.data.users || []
    const usersObject: Record<string, any> = {}
    usersArray.forEach((user: any, index: number) => {
      const key = `${user.name}_${user.id}`
      usersObject[key] = {
        ...user,
        key: key
      }
    })
    users.value = usersObject
  } catch (error) {
    console.error('Error loading users:', error)
  }
}

const loadNotices = async () => {
  try {
    const response = await adminAPI.getNotices()
    notices.value = response.data.notices
  } catch (error) {
    console.error('Error loading notices:', error)
  }
}

const loadAttendanceHistory = async () => {
  try {
    const response = await adminAPI.getAttendanceHistory()
    attendanceHistory.value = response.data.history
  } catch (error) {
    console.error('Error loading attendance history:', error)
  }
}

const refreshUsers = async () => {
  await loadUsers()
}

const startFaceDetection = async () => {
  console.log('Starting face detection...')
  try {
    const response = await adminAPI.checkFaceDetection()
    const data = response.data
    console.log('Face detection response:', data)
    
    if (data.face_detected && data.ready) {
      faceDetectionStatus.value = {
        ready: true,
        message: data.message,
        icon: '✅',
        class: 'ready'
      }
    } else if (data.face_detected && !data.ready) {
      faceDetectionStatus.value = {
        ready: false,
        message: data.message,
        icon: '⚠️',
        class: 'warning'
      }
    } else {
      faceDetectionStatus.value = {
        ready: false,
        message: data.message,
        icon: '❌',
        class: 'error'
      }
    }
  } catch (error: any) {
    console.error('Face detection error:', error)
    faceDetectionStatus.value = {
      ready: false,
      message: 'Camera error. Please check camera permissions and try again.',
      icon: '❌',
      class: 'error'
    }
  }
}

const closeCaptureModal = () => {
  showCaptureModal.value = false
  if (detectionInterval) {
    clearInterval(detectionInterval)
    detectionInterval = null
  }
  faceDetectionStatus.value = {
    ready: false,
    message: 'Checking camera...',
    icon: '📷',
    class: 'checking'
  }
  captureProgress.value = { current: 0, total: 0 }
}

const startCapture = async () => {
  if (!selectedUserForCapture.value || !faceDetectionStatus.value.ready) return

  isCapturing.value = true
  captureProgress.value = { current: 0, total: 3 }
  
  // Stop face detection during capture
  if (detectionInterval) {
    clearInterval(detectionInterval)
    detectionInterval = null
  }
  
  // Update status
  faceDetectionStatus.value = {
    ready: false,
    message: 'Capturing faces... Please stay still!',
    icon: '📸',
    class: 'capturing'
  }
  
  try {
    // Simulate real-time progress (since backend capture is very fast)
    const progressTimer = setInterval(() => {
      if (captureProgress.value.current < captureProgress.value.total) {
        captureProgress.value.current++
      }
    }, 800) // Update every 0.8 seconds
    
    const response = await adminAPI.captureUserFaces({
      user_id: selectedUserForCapture.value.id,
      name: selectedUserForCapture.value.name
    })
    
    clearInterval(progressTimer)
    captureProgress.value.current = captureProgress.value.total
    
    // Show success message
    faceDetectionStatus.value = {
      ready: true,
      message: 'Capture completed successfully!',
      icon: '🎉',
      class: 'success'
    }
    
    setTimeout(() => {
      alert(response.data.message)
      closeCaptureModal()
      selectedUserForCapture.value = null
      loadUsers() // Refresh the users list
    }, 1000)
    
  } catch (error: any) {
    faceDetectionStatus.value = {
      ready: false,
      message: error.response?.data?.message || 'Error capturing faces',
      icon: '❌',
      class: 'error'
    }
    alert(error.response?.data?.message || 'Error capturing faces')
  } finally {
    isCapturing.value = false
  }
}

// Legacy function - now opens modal
const captureFaces = async () => {
  console.log('Opening face capture modal...')
  showCaptureModal.value = true
  
  // Test camera first
  setTimeout(async () => {
    console.log('Testing camera...')
    try {
      const cameraResponse = await adminAPI.testCamera()
      console.log('Camera test response:', cameraResponse.data)
      
      if (cameraResponse.data.camera_available) {
        console.log('Camera is available, starting face detection...')
        startFaceDetection()
        
        // Check face detection every 2 seconds
        if (detectionInterval) {
          clearInterval(detectionInterval)
        }
        detectionInterval = setInterval(() => {
          console.log('Running periodic face detection...')
          startFaceDetection()
        }, 2000)
      } else {
        faceDetectionStatus.value = {
          ready: false,
          message: cameraResponse.data.message,
          icon: '❌',
          class: 'error'
        }
      }
    } catch (error) {
      console.error('Camera test failed:', error)
      faceDetectionStatus.value = {
        ready: false,
        message: 'Failed to test camera. Please check permissions.',
        icon: '❌',
        class: 'error'
      }
    }
  }, 500)  // Give modal time to render
}

const createNotice = async () => {
  if (!newNotice.value.title || !newNotice.value.content) {
    showNotification('warning', 'Missing Information', 'Please fill in all fields')
    return
  }

  isCreatingNotice.value = true
  try {
    await adminAPI.createNotice(newNotice.value)
    showNotification('success', 'Notice Created', 'Notice created successfully!')
    
    // Reset form
    newNotice.value = {
      title: '',
      content: ''
    }
    
    // Reload notices
    await loadNotices()
    
  } catch (error: any) {
    showNotification('error', 'Creation Failed', error.response?.data?.message || 'Error creating notice')
  } finally {
    isCreatingNotice.value = false
  }
}

// Backup and Export Functions
const backupDatabase = async () => {
  isBackingUp.value = true
  try {
    const response = await adminAPI.backupDatabase()
    showNotification('success', 'Backup Created', 'Database backup created successfully!')
    
    // Add to recent operations
    recentOperations.value.unshift({
      id: Date.now().toString(),
      type: 'Database Backup',
      timestamp: new Date().toISOString(),
      filename: response.data.backup_file.split('/').pop(),
      downloadable: true
    })
    
  } catch (error: any) {
    showNotification('error', 'Backup Failed', error.response?.data?.message || 'Error creating backup')
  } finally {
    isBackingUp.value = false
  }
}

const exportToJson = async () => {
  isExportingJson.value = true
  try {
    const response = await adminAPI.exportToJson()
    alert('Data exported to JSON successfully!')
    
    // Add to recent operations
    recentOperations.value.unshift({
      id: Date.now().toString(),
      type: 'JSON Export',
      timestamp: new Date().toISOString(),
      filename: response.data.export_file.split('/').pop(),
      downloadable: true
    })
    
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error exporting data')
  } finally {
    isExportingJson.value = false
  }
}

const exportToCsv = async () => {
  isExportingCsv.value = true
  try {
    const response = await adminAPI.exportToCsv(selectedExportDate.value || undefined)
    alert('Attendance data exported to CSV successfully!')
    
    // Add to recent operations
    recentOperations.value.unshift({
      id: Date.now().toString(),
      type: 'CSV Export',
      timestamp: new Date().toISOString(),
      filename: response.data.export_file.split('/').pop(),
      downloadable: true
    })
    
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error exporting CSV')
  } finally {
    isExportingCsv.value = false
  }
}

const downloadFile = async (filename: string) => {
  try {
    const response = await adminAPI.downloadFile(filename)
    
    // Create blob and download
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error downloading file')
  }
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}

const formatDateOption = (dateString: string) => {
  const date = new Date(dateString.replace(/_/g, '/'))
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const loadAvailableDates = () => {
  // Generate last 30 days as available dates for export
  const dates = []
  for (let i = 0; i < 30; i++) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    dates.push(date.toLocaleDateString('en-US', { month: '2-digit', day: '2-digit', year: '2-digit' }).replace(/\//g, '_'))
  }
  availableDates.value = dates
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatDateKey = (dateKey: string) => {
  // Convert MM_DD_YY to readable format
  const [month, day, year] = dateKey.split('_')
  return new Date(2000 + parseInt(year), parseInt(month) - 1, parseInt(day)).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

onMounted(() => {
  loadUsers()
  loadNotices()
  loadAttendanceHistory()
  loadAvailableDates()
})

// User Management Methods
const openEditModal = (user: User) => {
  editingUser.value = { ...user }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingUser.value = null
}

const saveUserEdit = async () => {
  if (!editingUser.value) return
  
  isUpdatingUser.value = true
  try {
    await adminAPI.updateUser(editingUser.value.id, editingUser.value)
    alert('User updated successfully!')
    await loadUsers()
    closeEditModal()
  } catch (error: any) {
    console.error('Error updating user:', error)
    alert(error.response?.data?.message || 'Failed to update user')
  } finally {
    isUpdatingUser.value = false
  }
}

const openPasswordModal = (user: User) => {
  resetPasswordUser.value = user
  newPassword.value = ''
  showPasswordModal.value = true
}

const closePasswordModal = () => {
  showPasswordModal.value = false
  resetPasswordUser.value = null
  newPassword.value = ''
}

const resetUserPassword = async () => {
  if (!resetPasswordUser.value || !newPassword.value) {
    alert('Please enter a new password')
    return
  }
  
  isUpdatingPassword.value = true
  try {
    await adminAPI.resetPassword(resetPasswordUser.value.id, newPassword.value)
    alert('Password reset successfully!')
    closePasswordModal()
  } catch (error: any) {
    console.error('Error resetting password:', error)
    alert(error.response?.data?.message || 'Failed to reset password')
  } finally {
    isUpdatingPassword.value = false
  }
}

const deleteUser = async (user: User) => {
  if (!confirm(`Are you sure you want to delete user "${user.name}"? This action cannot be undone.`)) {
    return
  }
  
  try {
    await adminAPI.deleteUser(user.id)
    showNotification('success', 'User Deleted', `User "${user.name}" deleted successfully!`)
    await loadUsers()
  } catch (error: any) {
    console.error('Error deleting user:', error)
    showNotification('error', 'Deletion Failed', error.response?.data?.message || 'Failed to delete user')
  }
}

const deleteUserWithLoading = async (user: User) => {
  if (!confirm(`Are you sure you want to delete user "${user.name}"? This action cannot be undone.`)) {
    return
  }
  
  isProcessingUser.value = user.id
  try {
    await adminAPI.deleteUser(user.id)
    showNotification('success', 'User Deleted', `User "${user.name}" deleted successfully!`)
    await loadUsers()
  } catch (error: any) {
    console.error('Error deleting user:', error)
    showNotification('error', 'Deletion Failed', error.response?.data?.message || 'Failed to delete user')
  } finally {
    isProcessingUser.value = null
  }
}

const viewUserProfile = (user: User) => {
  // TODO: Implement user profile view
  alert(`Profile for ${user.name} - Feature coming soon!`)
}

// Registration Modal Methods
const openRegistrationModal = () => {
  userForFaceCapture.value = null
  showRegistrationModal.value = true
}

const closeRegistrationModal = () => {
  showRegistrationModal.value = false
  userForFaceCapture.value = null
}

const openFaceCaptureModal = (user: any) => {
  userForFaceCapture.value = {
    id: user.id.toString(),
    name: user.name,
    user_id: user.id.toString(),
    type: user.type,
    class_section: user.class_section
  }
  showRegistrationModal.value = true
}

const hasUserFaceData = (user: any) => {
  // Check if user has face data based on user structure
  return user.has_face_data || false
}

const getActivityBarColor = (percentage: number) => {
  if (percentage >= 80) return 'linear-gradient(135deg, #22c55e, #16a34a)' // Green for high attendance
  if (percentage >= 60) return 'linear-gradient(135deg, #3b82f6, #1d4ed8)' // Blue for good attendance
  if (percentage >= 40) return 'linear-gradient(135deg, #f59e0b, #d97706)' // Orange for average attendance
  return 'linear-gradient(135deg, #ef4444, #dc2626)' // Red for low attendance
}

const registerUser = async () => {
  try {
    await adminAPI.registerUser(newUser.value)
    showNotification('success', 'User Registered', 'User registered successfully!')
    
    // Reset form
    newUser.value = {
      name: '',
      user_id: '',
      username: '',
      password: '',
      type: 'student',
      class_section: ''
    }
    
    closeRegistrationModal()
    await loadUsers()
  } catch (error: any) {
    showNotification('error', 'Registration Failed', error.response?.data?.message || 'Error registering user')
  }
}

const onRegistrationSuccess = async (message: string) => {
  showNotification('success', 'Registration Success', message)
  await loadUsers()
  closeRegistrationModal()
}
</script>

<style scoped>
.admin {
  padding: 40px 0;
}

.admin-header {
  text-align: center;
  margin-bottom: 40px;
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.admin-subtitle {
  color: var(--text-secondary);
  font-size: 1rem;
}

/* Navigation Tabs */
.admin-nav {
  display: flex;
  gap: 4px;
  margin-bottom: 40px;
  background: var(--input-background);
  padding: 4px;
  border-radius: 12px;
  overflow-x: auto;
}

.nav-tab {
  flex: 1;
  padding: 12px 24px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.nav-tab.active {
  background: var(--card-background);
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-tab:hover:not(.active) {
  color: var(--text-primary);
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.3s ease;
}

/* Register Grid */
.register-grid {
  gap: 32px;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

.register-form,
.capture-section,
.create-notice,
.notices-list,
.users-section,
.analytics-section {
  padding: 32px;
}

/* Capture Section */
.capture-area {
  text-align: center;
}

.capture-info {
  background: var(--input-background);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  text-align: left;
}

.capture-info p {
  margin-bottom: 8px;
  color: var(--text-secondary);
}

.capture-btn {
  width: 100%;
}

.no-user-selected {
  text-align: center;
  padding: 60px 20px;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* Users Section - Enhanced Management Styling */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 0;
  border-bottom: 2px solid var(--border-color);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 12px;
}

.section-title::before {
  content: '👥';
  font-size: 1.2rem;
}

.user-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.stat-item {
  font-size: 14px;
  color: var(--text-secondary);
  padding: 8px 16px;
  background: var(--input-background);
  border-radius: 20px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-item:hover {
  background: var(--card-background);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-item::before {
  content: '•';
  color: var(--accent-color);
  font-weight: bold;
}

.users-table-container {
  max-height: 600px;
  overflow-y: auto;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--card-background);
}

.table {
  width: 100%;
  border-collapse: collapse;
  background: transparent;
}

.table thead {
  background: var(--input-background);
  position: sticky;
  top: 0;
  z-index: 10;
}

.table th {
  padding: 16px 12px;
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 2px solid var(--border-color);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table td {
  padding: 16px 12px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
  vertical-align: middle;
}

.table tbody tr {
  transition: all 0.3s ease;
}

.table tbody tr:hover {
  background: var(--input-background);
  transform: scale(1.01);
}

.type-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-badge.type-student {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.type-badge.type-employee {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-sm {
  padding: 8px 12px;
  font-size: 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
}

.btn-sm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-primary.btn-sm {
  background: var(--primary-color);
  color: white;
}

.btn-secondary.btn-sm {
  background: var(--input-background);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.btn-info.btn-sm {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-warning.btn-sm {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.btn-danger.btn-sm {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-success.btn-sm {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

/* Notices */
.notices-grid {
  gap: 32px;
}

.textarea {
  resize: vertical;
  min-height: 120px;
}

.notices-container {
  max-height: 500px;
  overflow-y: auto;
}

.notice-item {
  padding: 16px;
  background: var(--input-background);
  border-radius: 8px;
  margin-bottom: 16px;
  border-left: 4px solid var(--accent-color);
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.notice-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.notice-date {
  font-size: 12px;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.notice-content {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
}

/* Analytics */
.analytics-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.analytics-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.analytics-card {
  text-align: center;
  padding: 24px;
  background: var(--input-background);
  border-radius: 12px;
}

.analytics-card h4 {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.analytics-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent-color);
}

.attendance-history {
  background: var(--input-background);
  padding: 24px;
  border-radius: 12px;
}

.attendance-history h4 {
  margin-bottom: 16px;
  color: var(--text-primary);
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--card-border);
}

.history-item:last-child {
  border-bottom: none;
}

.history-date {
  font-weight: 500;
  color: var(--text-primary);
}

.history-count {
  font-size: 14px;
  color: var(--text-secondary);
  padding: 4px 8px;
  background: var(--card-background);
  border-radius: 12px;
}

/* Registration Section Styles */
.register-section {
  padding: 32px;
  text-align: center;
}

.section-header {
  margin-bottom: 32px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.section-description {
  color: var(--text-secondary);
  font-size: 1rem;
  margin: 0;
}

.register-action {
  margin-bottom: 40px;
}

.btn-large {
  padding: 20px 32px;
  font-size: 1.1rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 16px;
  min-width: 300px;
}

.btn-icon {
  font-size: 1.5rem;
}

.btn-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.btn-text strong {
  font-weight: 600;
}

.btn-text small {
  font-size: 0.85rem;
  opacity: 0.8;
  font-weight: normal;
}

.recent-registrations {
  text-align: left;
}

.recent-registrations h4 {
  font-size: 1.2rem;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.user-preview-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--input-background);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-preview-card:hover {
  background: var(--card-background);
  transform: translateY(-2px);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
}

.user-info {
  flex: 1;
}

.user-info h5 {
  margin: 0 0 4px 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.user-info p {
  margin: 0 0 4px 0;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.registration-date {
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.8;
}

/* Enhanced Responsive Design - Mobile First Approach */

/* Base Mobile Styles (320px+) */
.admin {
  padding: 1rem 0;
  min-height: 100vh;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}

.admin-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.admin-subtitle {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.4;
}

/* Navigation Tabs - Mobile First */
.admin-nav {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 2rem;
  background: var(--input-background);
  padding: 0.25rem;
  border-radius: 12px;
  overflow-x: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.admin-nav::-webkit-scrollbar {
  display: none;
}

.nav-tab {
  flex: 1;
  min-width: fit-content;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 0.85rem;
  text-align: center;
}

.nav-tab.active {
  background: var(--card-background);
  color: var(--text-primary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.nav-tab:hover:not(.active) {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.05);
}

/* Tab Content */
.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Grid Layouts - Mobile First */
.register-grid,
.notices-grid,
.backup-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* Card Styles */
.card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

/* Form Elements */
.form-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.register-form,
.capture-section,
.create-notice,
.notices-list,
.users-section,
.analytics-section,
.backup-section {
  padding: 1.5rem;
}

/* Section Headers */
.section-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding: 1rem 0;
  border-bottom: 2px solid var(--border-color);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.section-title::before {
  content: '👥';
  font-size: 1.1rem;
}

.user-stats {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.stat-item {
  font-size: 0.8rem;
  color: var(--text-secondary);
  padding: 0.5rem 0.875rem;
  background: var(--input-background);
  border-radius: 16px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.375rem;
  white-space: nowrap;
}

.stat-item:hover {
  background: var(--card-background);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-item::before {
  content: '•';
  color: var(--accent-color);
  font-weight: bold;
}

/* Tables - Mobile First */
.users-table-container {
  max-height: 500px;
  overflow: auto;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background: var(--card-background);
}

.table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
  background: transparent;
  font-size: 0.85rem;
}

.table thead {
  background: var(--input-background);
  position: sticky;
  top: 0;
  z-index: 10;
}

.table th {
  padding: 0.875rem 0.5rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 2px solid var(--border-color);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table td {
  padding: 0.875rem 0.5rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
  vertical-align: middle;
}

.table tbody tr {
  transition: all 0.3s ease;
}

.table tbody tr:hover {
  background: var(--input-background);
}

/* Buttons - Mobile First */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.btn-sm {
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
}

.btn-sm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Type Badges */
.type-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 16px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.type-badge.type-student {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.type-badge.type-employee {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

/* Registration Section */
.register-section {
  padding: 2rem 1.5rem;
  text-align: center;
}

.register-action {
  margin-bottom: 2rem;
}

.btn-large {
  padding: 1.25rem 2rem;
  font-size: 1rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 350px;
  justify-content: center;
  text-align: center;
}

.btn-icon {
  font-size: 1.25rem;
}

.btn-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.25rem;
}

.btn-text strong {
  font-weight: 600;
}

.btn-text small {
  font-size: 0.8rem;
  opacity: 0.8;
  font-weight: normal;
}

.recent-registrations {
  text-align: left;
}

.recent-registrations h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.users-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.user-preview-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--input-background);
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
}

.user-preview-card:hover {
  background: var(--card-background);
  transform: translateY(-2px);
  border-color: var(--accent-color);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  flex-shrink: 0;
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-info h5 {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-info p {
  margin: 0 0 0.25rem 0;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.registration-date {
  font-size: 0.7rem;
  color: var(--text-secondary);
  opacity: 0.8;
}

/* Analytics */
.analytics-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.analytics-stats {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.analytics-card {
  text-align: center;
  padding: 1.5rem;
  background: var(--input-background);
  border-radius: 12px;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.analytics-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.analytics-card h4 {
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.analytics-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent-color);
}

/* Modals - Mobile First */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  padding: 1rem;
}

.capture-modal,
.edit-modal,
.registration-modal {
  background: var(--card-background);
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.modal-header h3 {
  margin: 0;
  color: white;
  font-size: 1.1rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 1rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
  flex-shrink: 0;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 1.5rem;
  max-height: calc(90vh - 80px);
  overflow-y: auto;
}

.modal-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.modal-actions .btn {
  min-width: 80px;
  padding: 0.75rem 1rem;
  font-size: 0.9rem;
}

/* Input Elements */
.input-group {
  margin-bottom: 1rem;
}

.input-label {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  display: block;
  font-size: 0.9rem;
}

.input-field,
.select-field {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--input-background);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input-field:focus,
.select-field:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 191, 255, 0.1);
}

/* Small Mobile (375px+) */
@media (min-width: 375px) {
  .container {
    padding: 0 1.25rem;
  }
  
  .admin-title {
    font-size: 2rem;
  }
  
  .nav-tab {
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }
  
  .btn-large {
    font-size: 1.05rem;
    padding: 1.5rem 2.25rem;
  }
  
  .users-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  
  .analytics-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Large Mobile (480px+) */
@media (min-width: 480px) {
  .admin {
    padding: 1.5rem 0;
  }
  
  .container {
    padding: 0 1.5rem;
  }
  
  .admin-header {
    padding: 2rem;
  }
  
  .section-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .user-stats {
    gap: 1rem;
  }
  
  .stat-item {
    font-size: 0.85rem;
    padding: 0.625rem 1rem;
  }
  
  .table {
    font-size: 0.9rem;
    min-width: 700px;
  }
  
  .table th,
  .table td {
    padding: 1rem 0.75rem;
  }
  
  .btn-sm {
    padding: 0.625rem 0.875rem;
    font-size: 0.8rem;
    min-width: 36px;
    height: 36px;
  }
  
  .modal-header h3 {
    font-size: 1.2rem;
  }
  
  .modal-actions {
    justify-content: center;
  }
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .admin {
    padding: 2rem 0;
  }
  
  .container {
    padding: 0 2rem;
  }
  
  .admin-header {
    margin-bottom: 3rem;
  }
  
  .admin-title {
    font-size: 2.5rem;
  }
  
  .admin-subtitle {
    font-size: 1rem;
  }
  
  .admin-nav {
    gap: 0.5rem;
    padding: 0.5rem;
    margin-bottom: 3rem;
  }
  
  .nav-tab {
    padding: 1rem 1.5rem;
    font-size: 1rem;
  }
  
  .register-grid,
  .notices-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
  
  .backup-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }
  
  .register-form,
  .capture-section,
  .create-notice,
  .notices-list,
  .users-section,
  .analytics-section,
  .backup-section {
    padding: 2rem;
  }
  
  .section-title {
    font-size: 1.4rem;
  }
  
  .analytics-stats {
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }
  
  .analytics-card {
    padding: 2rem;
  }
  
  .analytics-value {
    font-size: 2rem;
  }
  
  .users-table-container {
    max-height: 600px;
  }
  
  .table {
    font-size: 0.95rem;
    min-width: 800px;
  }
  
  .table th,
  .table td {
    padding: 1.25rem 1rem;
  }
  
  .btn-sm {
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
    min-width: 40px;
    height: 40px;
  }
  
  .action-buttons {
    gap: 0.75rem;
  }
  
  .users-grid {
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
  }
  
  .user-preview-card {
    padding: 1.25rem;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    font-size: 1.1rem;
  }
  
  .btn-large {
    width: auto;
    min-width: 300px;
  }
  
  .modal-overlay {
    padding: 2rem;
  }
  
  .modal-header {
    padding: 1.25rem 2rem;
  }
  
  .modal-body {
    padding: 2rem;
  }
  
  .modal-actions {
    justify-content: flex-end;
    gap: 1rem;
  }
  
  .close-btn {
    width: 32px;
    height: 32px;
    font-size: 24px;
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    padding: 0 2.5rem;
  }
  
  .admin-nav {
    justify-content: center;
    max-width: 800px;
    margin: 0 auto 3rem;
  }
  
  .register-grid {
    grid-template-columns: 2fr 1fr;
    gap: 3rem;
  }
  
  .notices-grid {
    grid-template-columns: 1fr 2fr;
    gap: 3rem;
  }
  
  .backup-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5rem;
  }
  
  .analytics-stats {
    gap: 2rem;
  }
  
  .analytics-card {
    padding: 2.5rem;
  }
  
  .table {
    min-width: 900px;
  }
  
  .users-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }
  
  .user-preview-card {
    padding: 1.5rem;
  }
  
  .register-section {
    padding: 3rem 2rem;
  }
  
  .btn-large {
    padding: 1.5rem 3rem;
    font-size: 1.125rem;
  }
}

/* Large Desktop (1200px+) */
@media (min-width: 1200px) {
  .container {
    max-width: 1400px;
    padding: 0 3rem;
  }
  
  .admin {
    padding: 3rem 0;
  }
  
  .admin-header {
    margin-bottom: 4rem;
  }
  
  .register-grid,
  .notices-grid,
  .backup-grid {
    gap: 3.5rem;
  }
  
  .table {
    min-width: 1000px;
    font-size: 1rem;
  }
  
  .analytics-card {
    padding: 3rem;
  }
  
  .analytics-value {
    font-size: 2.5rem;
  }
  
  .users-grid {
    grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  }
}

/* Extra Large Desktop (1400px+) */
@media (min-width: 1400px) {
  .backup-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .analytics-stats {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Landscape Mobile Support */
@media (max-width: 767px) and (orientation: landscape) {
  .admin-nav {
    flex-wrap: nowrap;
    overflow-x: auto;
  }
  
  .nav-tab {
    flex: 0 0 auto;
    min-width: 120px;
  }
  
  .modal-overlay {
    padding: 0.5rem;
  }
  
  .modal-body {
    max-height: calc(100vh - 120px);
  }
  
  .analytics-stats {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .card,
  .nav-tab,
  .btn-sm,
  .user-preview-card,
  .analytics-card {
    transition: none;
  }
  
  .card:hover,
  .user-preview-card:hover,
  .analytics-card:hover,
  .btn-sm:hover {
    transform: none;
  }
  
  .tab-content {
    animation: none;
  }
}

/* High Contrast Mode Support */
@media (prefers-contrast: high) {
  .card,
  .user-preview-card,
  .analytics-card,
  .modal-header {
    border: 2px solid currentColor;
  }
  
  .type-badge {
    border-width: 2px;
  }
}

/* Print Styles */
@media print {
  .admin-nav,
  .modal-overlay,
  .btn,
  .action-buttons {
    display: none !important;
  }
  
  .admin {
    padding: 0;
  }
  
  .card {
    border: 1px solid #000;
    background: white;
    break-inside: avoid;
  }
  
  .table {
    min-width: auto;
    font-size: 0.8rem;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
  }
}

/* Backup & Export Styles */
.backup-section {
  padding: 32px;
}

.backup-grid {
  gap: 24px;
}

.backup-card {
  padding: 24px;
  height: fit-content;
}

.backup-description {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin-bottom: 20px;
  line-height: 1.5;
}

.backup-btn {
  width: 100%;
  margin-top: 8px;
}

.export-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.select-field {
  background: var(--input-background);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 12px 16px;
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.select-field:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 191, 255, 0.1);
}

.backup-list {
  max-height: 300px;
  overflow-y: auto;
}

.backup-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.backup-item:last-child {
  border-bottom: none;
}

.backup-item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.backup-type {
  font-weight: 500;
  color: var(--text-primary);
}

.backup-date {
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.85rem;
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--primary-color);
  color: var(--primary-color);
}

.btn-outline:hover {
  background: var(--primary-color);
  color: white;
}

/* Face Capture Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.capture-modal {
  background: var(--card-background);
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.modal-header h3 {
  margin: 0;
  color: white;
  font-size: 1.2em;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 24px;
}

.capture-status {
  text-align: center;
  margin-bottom: 24px;
}

.status-indicator {
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
}

.status-indicator.checking {
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-indicator.ready {
  background: rgba(0, 255, 127, 0.1);
  border: 1px solid rgba(0, 255, 127, 0.3);
}

.status-indicator.warning {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.status-indicator.error {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.status-indicator.capturing {
  background: rgba(138, 43, 226, 0.1);
  border: 1px solid rgba(138, 43, 226, 0.3);
}

.status-indicator.success {
  background: rgba(0, 255, 127, 0.2);
  border: 1px solid rgba(0, 255, 127, 0.5);
}

.status-icon {
  font-size: 2em;
  margin-bottom: 8px;
}

.status-text {
  font-size: 1.1em;
  font-weight: 500;
  color: var(--text-primary);
}

.capture-progress {
  margin: 20px 0;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
  transition: width 0.5s ease;
  border-radius: 4px;
}

.progress-text {
  font-size: 0.9em;
  color: var(--text-secondary);
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.modal-actions .btn {
  min-width: 100px;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

/* Animation for status changes */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.status-indicator.checking .status-icon {
  animation: pulse 2s infinite;
}

.status-indicator.capturing .status-icon {
  animation: capture-flash 0.5s infinite alternate;
}

@keyframes capture-flash {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.1); opacity: 0.7; }
}

/* Registration Modal Styles */
.registration-modal {
  background: var(--card-background);
  border-radius: 16px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.modal-header h3 {
  margin: 0;
  color: white;
  font-size: 1.2em;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 24px;
}

.input-group {
  margin-bottom: 16px;
}

.input-label {
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 8px;
  display: block;
}

.input-field {
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--input-background);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 191, 255, 0.1);
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  font-weight: 500;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-primary:disabled {
  background: var(--primary-color);
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

/* Enhanced Date Filter Styles */
.date-filter {
  background: var(--input-background);
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.date-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.date-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.date-input {
  width: 160px;
}

.date-connector {
  font-weight: 500;
  color: var(--text-secondary);
  margin: 0 8px;
  align-self: end;
  margin-bottom: 12px;
}

.filter-btn {
  min-width: 120px;
  align-self: end;
  margin-bottom: 12px;
}

/* Enhanced Chart Section */
.chart-section {
  background: var(--input-background);
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.chart-section h4 {
  margin-bottom: 16px;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.user-activity-chart {
  background: var(--card-background);
  border-radius: 12px;
  padding: 24px;
  min-height: 300px;
}

.activity-bars {
  display: flex;
  align-items: end;
  gap: 12px;
  height: 250px;
  padding: 20px 0;
}

.activity-bar {
  flex: 1;
  min-height: 20px;
  border-radius: 8px 8px 0 0;
  position: relative;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.activity-bar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.bar-label {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  white-space: nowrap;
}

.bar-value {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.75rem;
  color: var(--text-primary);
  font-weight: 600;
  white-space: nowrap;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 250px;
  text-align: center;
}

.no-data-icon {
  font-size: 3rem;
  margin-bottom: 16px;
  opacity: 0.5;
}

.no-data h4 {
  color: var(--text-primary);
  margin-bottom: 8px;
  font-size: 1.1rem;
}

.no-data p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* Enhanced spinner animation */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 8px;
}

.mini-spinner {
  width: 12px;
  height: 12px;
  border: 1.5px solid rgba(255, 255, 255, 0.3);
  border-top: 1.5px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
