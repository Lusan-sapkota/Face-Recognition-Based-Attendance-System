<template>
  <div class="modern-dashboard">
    <!-- Animated Background -->
    <div class="background-animation">
      <div class="floating-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="orb orb-4"></div>
        <div class="orb orb-5"></div>
      </div>
      <div class="grid-overlay"></div>
    </div>

    <div class="dashboard-container">
      <!-- Ultra Modern Header -->
      <header class="dashboard-header">
        <div class="header-content">
          <div class="user-greeting">
            <div class="greeting-avatar">
              <div class="avatar-circle">
                <span class="avatar-text">{{ getInitials(authStore.user?.name || 'U') }}</span>
                <div class="avatar-ring"></div>
              </div>
              <div class="online-indicator"></div>
            </div>
            <div class="greeting-text">
              <h1 class="welcome-title">
                {{ getGreeting() }}, {{ authStore.user?.name || 'User' }}!
              </h1>
              <p class="role-subtitle">
                <span class="role-chip" :class="authStore.isAdmin ? 'admin' : 'student'">
                  {{ authStore.isAdmin ? 'Administrator' : 'Student' }}
                </span>
                <span class="date-display">{{ getCurrentDate() }}</span>
              </p>
            </div>
          </div>

          <div class="header-actions">
            <div v-if="!authStore.isAdmin" class="stats-preview">
              <div class="stat-mini">
                <span class="stat-number">{{ personalStats.attendanceRate }}%</span>
                <span class="stat-text">Attendance</span>
              </div>
              <div class="stat-mini">
                <span class="stat-number">{{ personalStats.attendedDays }}</span>
                <span class="stat-text">Days Present</span>
              </div>
            </div>

            <div class="action-buttons">
              <button v-if="!authStore.isAdmin" @click="openCameraModal" class="primary-action-btn">
                <div class="btn-icon">
                  <i class="icon-camera">📸</i>
                  <div class="pulse-effect"></div>
                </div>
                <span class="btn-text">Mark Attendance</span>
              </button>

              <button v-if="authStore.isAdmin" @click="openUserRegistrationModal" class="primary-action-btn admin-btn">
                <div class="btn-icon">
                  <i class="icon-user-plus">👤➕</i>
                </div>
                <span class="btn-text">Register User</span>
              </button>

              <button class="secondary-action-btn" @click="refreshData">
                <i class="icon-refresh">🔄</i>
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Advanced Stats Dashboard -->
      <section class="stats-dashboard">
        <div v-if="isLoading" class="loading-container">
          <div class="modern-loader">
            <div class="loader-ring"></div>
            <div class="loader-text">Loading Dashboard...</div>
          </div>
        </div>

        <div v-else class="stats-grid">
          <div v-for="(stat, index) in getStatsConfig" :key="index" class="stat-card"
            :style="{ '--delay': index * 0.1 + 's' }">
            <div class="stat-background">
              <div class="stat-pattern"></div>
            </div>
            <div class="stat-content">
              <div class="stat-icon-container">
                <div class="stat-icon">{{ stat.icon }}</div>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-change" :class="stat.changeType">
                  {{ stat.change }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Enhanced Navigation Tabs -->
      <nav class="modern-nav">
        <div class="nav-wrapper">
          <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" class="nav-tab"
            :class="{ active: activeTab === tab.id }">
            <span class="tab-icon">{{ tab.icon }}</span>
            <span class="tab-label">{{ tab.label }}</span>
            <div class="tab-highlight"></div>
          </button>
        </div>
      </nav>

      <!-- Dynamic Tab Content -->
      <main class="tab-content-area">
        <!-- Analytics Tab -->
        <div v-if="activeTab === 'analytics'" class="tab-content analytics-tab">
          <div class="content-grid">
            <!-- Enhanced Chart Section -->
            <div class="chart-panel">
              <div class="panel-header">
                <h3 class="panel-title">
                  <i class="title-icon">📊</i>
                  Attendance Analytics
                </h3>
                <div class="panel-controls">
                  <button class="control-btn">📅 Filter</button>
                  <button class="control-btn">📤 Export</button>
                </div>
              </div>

              <div class="chart-area">
                <div v-if="attendanceChart.length > 0" class="modern-chart">
                  <div v-for="(month, index) in attendanceChart" :key="index" class="chart-column" :style="{
                    height: month.percentage + '%',
                    animationDelay: (index * 0.1) + 's'
                  }" @mouseover="showChartTooltip(month, $event)" @mouseleave="hideChartTooltip">
                    <div class="column-fill"></div>
                    <div class="column-label">{{ month.month.slice(0, 3) }}</div>
                    <div class="column-value">{{ month.days }}</div>
                  </div>
                </div>
                <div v-else class="empty-chart">
                  <div class="empty-illustration">
                    <i class="empty-icon">�</i>
                    <h4>No Data Available</h4>
                    <p>Start attending classes to see your analytics</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Weekly Heatmap -->
            <div class="heatmap-panel">
              <div class="panel-header">
                <h3 class="panel-title">
                  <i class="title-icon">🗓️</i>
                  Weekly Pattern
                </h3>
              </div>

              <div class="heatmap-container">
                <div v-for="day in weeklyPattern" :key="day.name" class="day-heatmap">
                  <div class="day-header">
                    <span class="day-name">{{ day.name }}</span>
                    <span class="day-percentage">{{ day.percentage }}%</span>
                  </div>
                  <div class="day-progress-bar">
                    <div class="progress-fill" :style="{ width: day.percentage + '%' }"
                      :class="getProgressClass(day.percentage)"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Activity Timeline -->
          <div class="timeline-panel">
            <div class="panel-header">
              <h3 class="panel-title">
                <i class="title-icon">⏱️</i>
                {{ authStore.isAdmin ? 'Recent System Activity' : 'Your Recent Activity' }}
              </h3>
              <button class="control-btn" @click="refreshActivity">🔄 Refresh</button>
            </div>

            <div class="timeline-container">
              <div v-for="activity in recentActivity.slice(0, 8)"
                :key="authStore.isAdmin ? `${activity.user_id}-${activity.date}` : activity.date" class="timeline-item">
                <div class="timeline-marker" :class="activity.status"></div>
                <div class="timeline-content">
                  <div class="activity-meta">
                    <span v-if="authStore.isAdmin" class="activity-user">{{ activity.user_name || 'Unknown User'
                      }}</span>
                    <span class="activity-time">{{ formatTime(activity.time) }}</span>
                    <span class="activity-date">{{ formatDate(activity.date) }}</span>
                  </div>
                  <div class="activity-details">
                    <span class="status-indicator" :class="activity.status">
                      {{ activity.status === 'present' ? '✅ Present' : '❌ Absent' }}
                    </span>
                    <span v-if="authStore.isAdmin && activity.user_type" class="user-type">
                      {{ activity.user_type }}
                    </span>
                  </div>
                </div>
              </div>

              <div v-if="recentActivity.length === 0" class="empty-timeline">
                <div class="empty-illustration">
                  <i class="empty-icon">📅</i>
                  <h4>No Recent Activity</h4>
                  <p>{{ authStore.isAdmin ? 'System activity will appear here' : 'Your activity will appear here' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Notices Tab -->
        <div v-if="activeTab === 'notices'" class="tab-content notices-tab">
          <div class="notices-container">
            <!-- Enhanced Notices Header -->
            <div class="notices-header">
              <div class="header-content">
                <h2 class="notices-title">
                  <div class="title-icon-wrapper">
                    <i class="title-icon">📢</i>
                    <div class="notification-pulse"></div>
                  </div>
                  Important Announcements
                </h2>
              </div>

              <div class="notices-actions">
                <div class="notices-filters">
                  <button class="filter-btn" :class="{ active: noticeFilter === 'all' }" @click="noticeFilter = 'all'">
                    All
                  </button>
                  <button class="filter-btn" :class="{ active: noticeFilter === 'recent' }"
                    @click="noticeFilter = 'recent'">
                    Recent
                  </button>
                  <button class="filter-btn" :class="{ active: noticeFilter === 'important' }"
                    @click="noticeFilter = 'important'">
                    Important
                  </button>
                  <button v-if="authStore.isAdmin" @click="createNotice" class="create-notice-btn">
                    <i class="btn-icon">➕</i>
                    <span>Create Notice</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Notices Grid -->
            <div class="notices-grid">
              <div v-for="(notice, index) in filteredNotices" :key="notice.id" class="notice-card"
                :style="{ '--delay': index * 0.1 + 's' }">
                <div class="notice-background">
                  <div class="notice-pattern"></div>
                </div>

                <div class="notice-header">
                  <div class="notice-meta">
                    <div class="notice-priority" :class="notice.priority">
                      <i class="priority-icon">{{ getPriorityIcon(notice.priority) }}</i>
                    </div>
                    <div class="notice-info">
                      <h4 class="notice-title">{{ notice.title }}</h4>
                      <div class="notice-details">
                        <span class="notice-date">{{ formatDate(notice.created_at) }}</span>
                        <span class="notice-separator">•</span>
                        <span class="notice-author">{{ notice.created_by || 'System' }}</span>
                      </div>
                    </div>
                  </div>

                  <div class="notice-actions">
                    <button class="notice-action-btn bookmark" :class="{ active: notice.bookmarked }"
                      @click="toggleBookmark(notice)" title="Bookmark">
                      📑
                    </button>
                    <button class="notice-action-btn share" @click="shareNotice(notice)" title="Share">
                      📤
                    </button>
                    <button v-if="authStore.isAdmin" class="notice-action-btn delete" @click="deleteNotice(notice)"
                      title="Delete">
                      �️
                    </button>
                  </div>
                </div>

                <div class="notice-content">
                  <p class="notice-text" :class="{ expanded: notice.expanded }">
                    {{ notice.content }}
                  </p>

                  <button v-if="notice.content.length > 150" @click="toggleNoticeExpansion(notice)"
                    class="read-more-btn">
                    {{ notice.expanded ? 'Show Less' : 'Read More' }}
                  </button>
                </div>

                <div class="notice-footer">
                  <div class="notice-tags">
                    <span v-for="tag in notice.tags || []" :key="tag" class="notice-tag">
                      {{ tag }}
                    </span>
                  </div>

                  <div class="notice-engagement">
                    <button class="engagement-btn">
                      <i class="engagement-icon">👀</i>
                      <span>{{ notice.views || 0 }}</span>
                    </button>
                    <button class="engagement-btn" @click="toggleLike(notice)">
                      <i class="engagement-icon">👍</i>
                      <span>{{ notice.likes || 0 }}</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-if="filteredNotices.length === 0" class="empty-notices">
                <div class="empty-illustration">
                  <div class="empty-icon-wrapper">
                    <i class="empty-icon">📢</i>
                    <div class="empty-icon-bg"></div>
                  </div>
                  <h4 class="empty-title">No Announcements Found</h4>
                  <p class="empty-description">
                    {{ noticeFilter === 'all' ? 'There are no announcements at the moment.' : `No ${noticeFilter}
                    announcements available.` }}
                  </p>
                  <button v-if="authStore.isAdmin" @click="createNotice" class="empty-action-btn">
                    ➕ Create First Notice
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Tab (Student) -->
        <div v-if="activeTab === 'profile' && !authStore.isAdmin" class="tab-content profile-tab">
          <div class="profile-layout">
            <!-- Enhanced Profile Card -->
            <div class="profile-main">
              <div class="profile-header">
                <div class="profile-avatar-large">
                  <div class="avatar-container">
                    <div class="avatar-circle-large">
                      {{ getInitials(authStore.user?.name || 'U') }}
                    </div>
                    <div class="avatar-status online"></div>
                  </div>
                </div>
                <div class="profile-info">
                  <h2 class="profile-name">{{ authStore.user?.name || 'Unknown User' }}</h2>
                  <p class="profile-role">{{ formatRole(authStore.user?.type || 'user') }}</p>
                  <div class="profile-badges">
                    <span class="badge active">Active</span>
                    <span class="badge verified">Verified</span>
                  </div>
                </div>
              </div>

              <div class="profile-details">
                <div class="detail-row">
                  <span class="detail-label">🆔 Student ID</span>
                  <span class="detail-value">{{ authStore.user?.id || 'N/A' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">👤 Username</span>
                  <span class="detail-value">{{ authStore.user?.username || 'N/A' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">🏫 Class/Section</span>
                  <span class="detail-value">{{ authStore.user?.class_section || 'N/A' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">📅 Registered</span>
                  <span class="detail-value">{{ formatDate(authStore.user?.registered_date || '') }}</span>
                </div>
              </div>
            </div>

            <!-- Profile Statistics -->
            <div class="profile-stats">
              <div class="stats-header">
                <h3 class="stats-title">
                  <i class="title-icon">📊</i>
                  Your Statistics
                </h3>
              </div>

              <div class="stats-items">
                <div class="stat-item">
                  <div class="stat-icon">🔥</div>
                  <div class="stat-data">
                    <span class="stat-number">{{ profileStats.consecutiveDays }}</span>
                    <span class="stat-text">Day Streak</span>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon">⏰</div>
                  <div class="stat-data">
                    <span class="stat-number">{{ profileStats.avgDailyTime }}</span>
                    <span class="stat-text">Avg Time</span>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon">🏆</div>
                  <div class="stat-data">
                    <span class="stat-number">{{ profileStats.bestMonth }}</span>
                    <span class="stat-text">Best Month</span>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon">📱</div>
                  <div class="stat-data">
                    <span class="stat-number">{{ profileStats.totalLogins }}</span>
                    <span class="stat-text">Total Logins</span>
                  </div>
                </div>
              </div>

              <!-- Achievements -->
              <div class="achievements-section">
                <h4 class="achievements-title">🏅 Achievements</h4>
                <div class="achievements-grid">
                  <div v-for="achievement in achievements" :key="achievement.id" class="achievement-item"
                    :title="achievement.description">
                    <div class="achievement-icon">{{ achievement.icon }}</div>
                    <span class="achievement-name">{{ achievement.name }}</span>
                  </div>

                  <div v-if="achievements.length === 0" class="no-achievements">
                    <div class="achievement-icon">🏆</div>
                    <span class="achievement-name">Keep Going!</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Management Tab (Admin) -->
        <div v-if="activeTab === 'management' && authStore.isAdmin" class="tab-content management-tab">
          <div class="management-layout">
            <!-- Management Header -->
            <div class="management-header">
              <div class="header-content">
                <h2 class="section-title">
                  <div class="title-icon-wrapper">
                    <i class="title-icon">⚙️</i>
                    <div class="icon-glow"></div>
                  </div>
                  System Management Center
                </h2>
                <p class="section-subtitle">Configure settings, manage users, and monitor system performance</p>
              </div>
              <div class="header-stats">
                <div class="quick-stat">
                  <span class="stat-number">{{ users.length }}</span>
                  <span class="stat-label">Total Users</span>
                </div>
                <div class="quick-stat">
                  <span class="stat-number">{{ dashboardStats.attendanceRate }}%</span>
                  <span class="stat-label">Attendance Rate</span>
                </div>
                <div class="quick-stat">
                  <span class="stat-number">{{ notices.length }}</span>
                  <span class="stat-label">Active Notices</span>
                </div>
              </div>
            </div>

            <!-- Management Grid -->
            <div class="management-grid">
              <!-- System Configuration Card -->
              <div class="config-section">
                <div class="config-card">
                  <div class="card-header">
                    <h3 class="card-title">
                      <i class="title-icon">⚙️</i>
                      System Configuration
                    </h3>
                    <div class="card-status">
                      <span class="status-dot active"></span>
                      <span class="status-text">Active</span>
                    </div>
                  </div>

                  <div class="config-form">
                    <div class="form-grid">
                      <div class="form-field">
                        <label class="field-label">🎓 Program/Degree</label>
                        <select v-model="classConfig.program" class="field-input">
                          <option value="bachelors">Bachelor's</option>
                          <option value="masters">Master's</option>
                          <option value="diploma">Diploma</option>
                        </select>
                      </div>

                      <div class="form-field">
                        <label class="field-label">📚 Semester/Year</label>
                        <select v-model="classConfig.semester" class="field-input">
                          <option value="1st">1st Semester</option>
                          <option value="2nd">2nd Semester</option>
                          <option value="3rd">3rd Semester</option>
                          <option value="4th">4th Semester</option>
                          <option value="5th">5th Semester</option>
                          <option value="6th">6th Semester</option>
                          <option value="7th">7th Semester</option>
                          <option value="8th">8th Semester</option>
                        </select>
                      </div>

                      <div class="form-field">
                        <label class="field-label">🏫 Section</label>
                        <input v-model="classConfig.section" type="text" class="field-input"
                          placeholder="e.g., A, B, C" />
                      </div>

                      <div class="form-field">
                        <label class="field-label">📖 Subject/Course</label>
                        <input v-model="classConfig.subject" type="text" class="field-input"
                          placeholder="e.g., Computer Science" />
                      </div>
                    </div>

                    <button @click="saveClassConfig" class="save-btn">
                      💾 Save Configuration
                    </button>
                  </div>
                </div>

                <!-- Time Settings -->
                <div class="time-card">
                  <div class="card-header">
                    <h3 class="card-title">
                      <i class="title-icon">⏰</i>
                      Time Settings
                    </h3>
                    <div class="status-indicator active">Active</div>
                  </div>

                  <div class="time-form">
                    <div class="time-grid">
                      <div class="time-field">
                        <label class="field-label">🕘 Class Start Time</label>
                        <input v-model="timeSettings.startTime" type="time" class="field-input" />
                      </div>

                      <div class="time-field">
                        <label class="field-label">⏱️ Grace Period</label>
                        <div class="input-group">
                          <input v-model="timeSettings.gracePeriod" type="number" min="0" max="30"
                            class="field-input" />
                          <span class="input-suffix">minutes</span>
                        </div>
                      </div>

                      <div class="time-field">
                        <label class="field-label">🚫 Late Cutoff</label>
                        <input v-model="timeSettings.cutoffTime" type="time" class="field-input" />
                      </div>

                      <div class="time-field">
                        <label class="field-label">📵 Auto Absent After</label>
                        <select v-model="timeSettings.autoAbsent" class="field-input">
                          <option value="30">30 minutes</option>
                          <option value="60">1 hour</option>
                          <option value="120">2 hours</option>
                          <option value="0">Never</option>
                        </select>
                      </div>
                    </div>

                    <button @click="saveTimeSettings" class="save-btn">
                      ⚡ Apply Settings
                    </button>
                  </div>
                </div>
              </div>

              <!-- User Management Section -->
              <div class="users-section">
                <div class="users-card">
                  <div class="card-header">
                    <h3 class="card-title">
                      <i class="title-icon">👥</i>
                      Manage Users
                    </h3>
                    <div class="card-actions">
                      <button @click="loadUsers" class="action-btn">🔄 Refresh</button>
                      <button @click="openUserRegistrationModal" class="action-btn primary">➕ Add User</button>
                    </div>
                  </div>

                  <div v-if="loadingUsers" class="loading-container">
                    <div class="loader"></div>
                    <span>Loading users...</span>
                  </div>

                  <div v-else class="users-table-container">
                    <table class="users-table" v-if="users.length > 0">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Name</th>
                          <th>Type</th>
                          <th>Class/Section</th>
                          <th>Face Data</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="user in users" :key="user.id" class="user-row">
                          <td class="user-id">{{ user.id }}</td>
                          <td class="user-name">{{ user.name }}</td>
                          <td class="user-type">
                            <span class="type-badge" :class="user.type">{{ user.type }}</span>
                          </td>
                          <td class="user-class">{{ user.class_section || 'N/A' }}</td>
                          <td class="user-face-status">
                            <span class="face-badge"
                              :class="{ 'has-face': user.has_face_data, 'no-face': !user.has_face_data }">
                              {{ user.has_face_data ? 'Yes' : 'No' }}
                            </span>
                          </td>
                          <td class="user-actions">
                            <button v-if="!user.has_face_data" @click="captureUserFace(user)"
                              class="action-btn-small capture" title="Capture Face">
                              📸
                            </button>
                            <button @click="editUser(user)" class="action-btn-small edit" title="Edit User">
                              ✏️
                            </button>
                            <button @click="deleteUser(user)" class="action-btn-small delete" title="Delete User">
                              🗑️
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <div v-else class="empty-users">
                      <div class="empty-illustration enhanced-empty-users">
                        <div class="empty-icon-bg"></div>
                        <i class="empty-icon">👥</i>
                        <h4 class="empty-title">No Users Found</h4>
                        <p class="empty-description">Add users to see them listed here.</p>
                        <button @click="openUserRegistrationModal" class="add-user-btn enhanced-add-user-btn" style="
                        background: linear-gradient(135deg, #4ecdc4, #45b7d1);
                        color: white;
                        border: none;
                        padding: 1.25rem 2.5rem;
                        border-radius: 18px;
                        font-weight: 700;
                        font-size: 1rem;
                        cursor: pointer;
                        transition: all 0.3s ease;
                        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
                      " @mouseover="handleAddUserMouseOver" @mouseout="handleAddUserMouseOut">
                          ➕ Add First User
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Active Classes -->
              <div class="classes-section">
                <div class="classes-card">
                  <div class="card-header">
                    <h3 class="card-title">
                      <i class="title-icon">🏫</i>
                      Today's Classes
                    </h3>
                    <div class="card-actions">
                      <button @click="refreshClasses" class="action-btn">🔄</button>
                      <button class="action-btn primary">➕ Add Class</button>
                    </div>
                  </div>

                  <div class="classes-grid">
                    <div v-for="cls in activeClasses" :key="cls.id" class="class-card">
                      <div class="class-header">
                        <div class="class-info">
                          <h4 class="class-name">{{ cls.name }}</h4>
                          <p class="class-details">{{ cls.program }} {{ cls.semester }} - Section {{ cls.section }}</p>
                        </div>
                        <div class="class-status" :class="getClassStatus(cls)">
                          {{ getClassStatusText(cls) }}
                        </div>
                      </div>

                      <div class="class-time">
                        <span class="time-range">{{ cls.startTime }} - {{ cls.endTime }}</span>
                      </div>

                      <div class="class-attendance">
                        <div class="attendance-bar">
                          <div class="attendance-fill" :style="{ width: cls.rate + '%' }"></div>
                        </div>
                        <span class="attendance-text">{{ cls.present }}/{{ cls.total }} ({{ cls.rate }}%)</span>
                      </div>

                      <button @click="openAttendance(cls)" class="class-action-btn">
                        📋 Take Attendance
                      </button>
                    </div>

                    <div v-if="activeClasses.length === 0" class="empty-classes">
                      <div class="empty-illustration">
                        <i class="empty-icon">🏫</i>
                        <h4>No Active Classes</h4>
                        <p>Set up class schedules to see them here</p>
                        <button class="setup-btn">⚙️ Setup Classes</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Enhanced Camera Modal -->
    <CameraModal :show="showCameraModal" @close="closeCameraModal" @success="onAttendanceSuccess" />

    <!-- User Registration Modal -->
    <UserRegistrationModal :show="showUserRegistrationModal" :existing-user="transformedUserToCapture"
      @close="closeUserRegistrationModal" @success="onUserRegistrationSuccess" />

    <!-- Chart Tooltip -->
    <div v-if="chartTooltip.show" class="chart-tooltip" :style="chartTooltip.style">
      <div class="tooltip-content">
        <div class="tooltip-title">{{ chartTooltip.title }}</div>
        <div class="tooltip-value">{{ chartTooltip.value }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore, useDashboardStore } from '../stores/counter'
import { useRouter } from 'vue-router'
import { userAPI, dashboardAPI, adminAPI } from '../services/api'
import CameraModal from '../components/CameraModal.vue'
import UserRegistrationModal from '../components/UserRegistrationModal.vue'

// Interfaces
interface Notice {
  id: number
  title: string
  content: string
  created_at: string
  created_by: string
  priority?: 'low' | 'medium' | 'high' | 'urgent'
  bookmarked?: boolean
  expanded?: boolean
  tags?: string[]
  views?: number
  likes?: number
  liked?: boolean
}

interface User {
  id: number
  name: string
  email: string
  type: 'student' | 'teacher' | 'staff' | 'admin'
  status: 'active' | 'inactive'
  created_at: string
  last_seen?: string
  class_section?: string
  has_face_data?: boolean
  user_id?: string
}

interface UserStats {
  totalDays: number
  attendedDays: number
  attendanceRate: number
  thisMonth: number
}

interface ActivityRecord {
  date: string
  time: string
  status: 'present' | 'absent'
  user_id?: string
  user_name?: string
  user_type?: string
}

interface Achievement {
  id: string
  name: string
  icon: string
  description: string
}

interface AttendanceRecord {
  Name: string
  Roll: number
  Time: string
  Type?: string
}

interface ClassConfig {
  program: string
  semester: string
  section: string
  subject: string
}

interface TimeSettings {
  startTime: string
  gracePeriod: number
  cutoffTime: string
  autoAbsent: number
}

interface ChartTooltip {
  show: boolean
  title: string
  value: string
  style: Record<string, string>
}

// Store initialization
const router = useRouter()
const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

// Reactive state
const activeTab = ref<string>('analytics')
const isLoading = ref<boolean>(false)
const showCameraModal = ref<boolean>(false)
const showUserRegistrationModal = ref<boolean>(false)
const loadingUsers = ref<boolean>(false)
const users = ref<User[]>([])
const userToCapture = ref<User | null>(null)
const notices = ref<Notice[]>([])
const attendanceData = ref<AttendanceRecord[]>([])

// Enhanced notice features
const noticeFilter = ref<string>('all')

// Chart tooltip state
const chartTooltip = ref<ChartTooltip>({
  show: false,
  title: '',
  value: '',
  style: {}
})

const personalStats = ref<UserStats>({
  totalDays: 0,
  attendedDays: 0,
  attendanceRate: 0,
  thisMonth: 0
})

const profileStats = ref({
  totalLogins: 0,
  consecutiveDays: 0,
  bestMonth: 'N/A',
  avgDailyTime: '0h 0m'
})

// Initialize with empty data - will be populated from API
const attendanceChart = ref<any[]>([])
const weeklyPattern = ref<any[]>([])
const recentActivity = ref<ActivityRecord[]>([])
const achievements = ref<Achievement[]>([])

// Class management data (Admin)
const classConfig = ref<ClassConfig>({
  program: 'bachelors',
  semester: '4th',
  section: 'E',
  subject: ''
})

const timeSettings = ref<TimeSettings>({
  startTime: '09:00',
  gracePeriod: 15,
  cutoffTime: '09:30',
  autoAbsent: 60
})

const activeClasses = ref<any[]>([])

// Dashboard Stats with real-time percentage changes
const dashboardStats = ref({
  totalUsers: 0,
  totalPresent: 0,
  absentToday: 0,
  attendanceRate: 0
})

const previousDashboardStats = ref({
  totalUsers: 0,
  totalPresent: 0,
  absentToday: 0,
  attendanceRate: 0
})

const statsPercentageChanges = ref({
  totalUsers: '+0.0%',
  totalPresent: '+0.0%',
  absentToday: '+0.0%',
  attendanceRate: '+0.0%'
})

// Define tabs for navigation
const tabs = computed(() => {
  if (authStore.isAdmin) {
    return [
      { id: 'analytics', label: 'System Analytics', icon: '📊' },
      { id: 'notices', label: 'Notices', icon: '📢' },
      { id: 'management', label: 'Management', icon: '⚙️' }
    ]
  } else {
    return [
      { id: 'analytics', label: 'My Analytics', icon: '📈' },
      { id: 'notices', label: 'Notices', icon: '📢' },
      { id: 'profile', label: 'Profile', icon: '👤' }
    ]
  }
})

// Get stats configuration based on user role
const getStatsConfig = computed(() => {
  if (authStore.isAdmin) {
    return [
      {
        icon: '👥',
        value: dashboardStats.value.totalUsers,
        label: 'Total Users',
        change: statsPercentageChanges.value.totalUsers,
        changeType: statsPercentageChanges.value.totalUsers.startsWith('+') ? 'positive' : 'negative',
        trend: '↗️',
        trendDirection: 'up',
        chartHeight: '60%'
      },
      {
        icon: '✅',
        value: dashboardStats.value.totalPresent,
        label: 'Present Today',
        change: statsPercentageChanges.value.totalPresent,
        changeType: statsPercentageChanges.value.totalPresent.startsWith('+') ? 'positive' : 'negative',
        trend: '↗️',
        trendDirection: 'up',
        chartHeight: '75%'
      },
      {
        icon: '❌',
        value: dashboardStats.value.absentToday,
        label: 'Absent Today',
        change: statsPercentageChanges.value.absentToday,
        changeType: statsPercentageChanges.value.absentToday.startsWith('+') ? 'negative' : 'positive',
        trend: '↘️',
        trendDirection: 'down',
        chartHeight: '40%'
      },
      {
        icon: '📊',
        value: `${dashboardStats.value.attendanceRate}%`,
        label: 'Attendance Rate',
        change: statsPercentageChanges.value.attendanceRate,
        changeType: statsPercentageChanges.value.attendanceRate.startsWith('+') ? 'positive' : 'negative',
        trend: '↗️',
        trendDirection: 'up',
        chartHeight: '85%'
      }
    ]
  } else {
    return [
      {
        icon: '📅',
        value: personalStats.value.totalDays,
        label: 'Total Days',
        change: statsPercentageChanges.value.totalUsers,
        changeType: statsPercentageChanges.value.totalUsers.startsWith('+') ? 'positive' : 'negative',
        trend: '📈',
        trendDirection: 'up',
        chartHeight: '60%'
      },
      {
        icon: '✅',
        value: personalStats.value.attendedDays,
        label: 'Days Present',
        change: statsPercentageChanges.value.totalPresent,
        changeType: statsPercentageChanges.value.totalPresent.startsWith('+') ? 'positive' : 'negative',
        trend: '✅',
        trendDirection: 'up',
        chartHeight: '70%'
      },
      {
        icon: '📊',
        value: `${personalStats.value.attendanceRate}%`,
        label: 'Attendance Rate',
        change: statsPercentageChanges.value.attendanceRate,
        changeType: statsPercentageChanges.value.attendanceRate.startsWith('+') ? 'positive' : 'negative',
        trend: '📈',
        trendDirection: 'up',
        chartHeight: '85%'
      }
    ]
  }
})

// Computed properties for enhanced features
const filteredNotices = computed(() => {
  const now = new Date()
  const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)

  switch (noticeFilter.value) {
    case 'recent':
      return notices.value.filter(notice => new Date(notice.created_at) >= oneWeekAgo)
    case 'important':
      return notices.value.filter(notice => notice.priority === 'high' || notice.priority === 'urgent')
    default:
      return notices.value
  }
})

// Transform user object for UserRegistrationModal compatibility
const transformedUserToCapture = computed(() => {
  if (!userToCapture.value) return null

  return {
    id: userToCapture.value.id.toString(),
    name: userToCapture.value.name,
    user_id: userToCapture.value.user_id || userToCapture.value.id.toString(),
    type: userToCapture.value.type === 'student' ? 'student' : 'employee',
    class_section: userToCapture.value.class_section
  }
})

// Helper functions
const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase()
}

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 17) return 'Good Afternoon'
  return 'Good Evening'
}

const getCurrentDate = () => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatTime = (timeString: string) => {
  if (!timeString) return 'N/A'
  return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRole = (type: string) => {
  const roles: { [key: string]: string } = {
    student: 'Student',
    teacher: 'Teacher',
    staff: 'Staff Member',
    admin: 'Administrator'
  }
  return roles[type] || 'User'
}

const getProgressClass = (percentage: number) => {
  if (percentage >= 80) return 'high'
  if (percentage >= 60) return 'medium'
  return 'low'
}

const getClassStatus = (cls: any) => {
  const now = new Date()
  const startTime = new Date(`${now.toDateString()} ${cls.startTime}`)
  const endTime = new Date(`${now.toDateString()} ${cls.endTime}`)

  if (now < startTime) return 'upcoming'
  if (now > endTime) return 'completed'
  return 'active'
}

const getClassStatusText = (cls: any) => {
  const status = getClassStatus(cls)
  switch (status) {
    case 'upcoming': return 'Upcoming'
    case 'active': return 'In Progress'
    case 'completed': return 'Completed'
    default: return 'Unknown'
  }
}

// Chart tooltip methods
const showChartTooltip = (data: any, event: MouseEvent) => {
  chartTooltip.value = {
    show: true,
    title: data.month,
    value: `${data.days} days (${data.percentage}%)`,
    style: {
      left: event.clientX + 10 + 'px',
      top: event.clientY - 10 + 'px'
    }
  }
}

const hideChartTooltip = () => {
  chartTooltip.value.show = false
}

// Modal methods
const openCameraModal = () => {
  showCameraModal.value = true
}

const closeCameraModal = () => {
  showCameraModal.value = false
}

const openUserRegistrationModal = () => {
  showUserRegistrationModal.value = true
}

const closeUserRegistrationModal = () => {
  showUserRegistrationModal.value = false
}

const onAttendanceSuccess = async (message: string) => {
  // Show success message
  alert(message)

  // Reload user data to update stats
  await loadUserData()

  // Close modal
  closeCameraModal()
}

const onUserRegistrationSuccess = async (message: string) => {
  // Show success message
  alert(message)

  // Reload admin data to update stats
  if (authStore.isAdmin) {
    await loadDashboardData()
  }

  // Close modal
  closeUserRegistrationModal()
}

// Data loading methods
const loadUserData = async () => {
  try {
    isLoading.value = true

    // Load real-time dashboard stats with percentage changes
    await loadDashboardStats()

    // Load user attendance data
    const attendanceResponse = await userAPI.getMyAttendance()
    const attendanceData = attendanceResponse.data

    // Calculate personal stats
    personalStats.value = {
      totalDays: attendanceData.total_days || 0,
      attendedDays: attendanceData.attended_days || 0,
      attendanceRate: attendanceData.attendance_rate || 0,
      thisMonth: attendanceData.this_month || 0
    }

    // Load profile stats and achievements
    try {
      const profileResponse = await userAPI.getMyProfile()
      profileStats.value = {
        totalLogins: profileResponse.data.total_logins || 0,
        consecutiveDays: profileResponse.data.consecutive_days || 0,
        bestMonth: profileResponse.data.best_month || 'N/A',
        avgDailyTime: profileResponse.data.avg_daily_time || '0h 0m'
      }

      // Load achievements from profile
      if (profileResponse.data.achievements) {
        achievements.value = profileResponse.data.achievements
      }
    } catch (error) {
      console.error('Error loading profile stats:', error)
    }

    // Load notices
    try {
      const noticesResponse = await userAPI.getNotices()
      notices.value = noticesResponse.data.notices || []
    } catch (error) {
      console.error('Error loading notices:', error)
    }

    // Load user analytics (charts and patterns)
    try {
      const analyticsResponse = await userAPI.getMyAnalytics()
      if (analyticsResponse.data) {
        // Monthly attendance chart
        if (analyticsResponse.data.monthly_trend) {
          attendanceChart.value = analyticsResponse.data.monthly_trend
        }

        // Weekly pattern
        if (analyticsResponse.data.weekly_pattern) {
          weeklyPattern.value = analyticsResponse.data.weekly_pattern
        }

        // Recent activity from analytics
        if (analyticsResponse.data.recent_activity) {
          recentActivity.value = analyticsResponse.data.recent_activity
        }
      }
    } catch (error) {
      console.error('Error loading user analytics:', error)
      // Set default empty charts if API fails
      attendanceChart.value = []
      weeklyPattern.value = [
        { name: 'Mon', percentage: 0 },
        { name: 'Tue', percentage: 0 },
        { name: 'Wed', percentage: 0 },
        { name: 'Thu', percentage: 0 },
        { name: 'Fri', percentage: 0 },
        { name: 'Sat', percentage: 0 },
        { name: 'Sun', percentage: 0 }
      ]
    }

  } catch (error) {
    console.error('Error loading user data:', error)
    // Use fallback data if API fails
    personalStats.value = {
      totalDays: 0,
      attendedDays: 0,
      attendanceRate: 0,
      thisMonth: 0
    }
  } finally {
    isLoading.value = false
  }
}

const loadDashboardData = async () => {
  try {
    isLoading.value = true
    dashboardStore.setLoading(true)

    // Load real-time dashboard stats with percentage changes
    await loadDashboardStats()

    // Load admin stats
    const statsResponse = await dashboardAPI.getStats()
    dashboardStore.setStats(statsResponse.data)

    // For admin, show all users' attendance, not their own
    attendanceData.value = statsResponse.data.attendance_data || []

    // Set admin stats differently
    personalStats.value = {
      totalDays: statsResponse.data.total_registered || 0,
      attendedDays: statsResponse.data.today_attendance || 0,
      attendanceRate: Math.round((statsResponse.data.today_attendance / Math.max(statsResponse.data.total_registered, 1)) * 100),
      thisMonth: statsResponse.data.students_present + statsResponse.data.employees_present || 0
    }

    // Load notices
    const noticesResponse = await adminAPI.getNotices()
    dashboardStore.setNotices(noticesResponse.data.notices || [])
    notices.value = noticesResponse.data.notices || []

    // Load system analytics data
    try {
      const analyticsResponse = await adminAPI.getAnalytics()
      if (analyticsResponse.data) {
        // System-wide monthly trend
        if (analyticsResponse.data.monthly_trend) {
          attendanceChart.value = analyticsResponse.data.monthly_trend
        }

        // System-wide weekly pattern
        if (analyticsResponse.data.weekly_pattern) {
          weeklyPattern.value = analyticsResponse.data.weekly_pattern
        }

        // System-wide recent activity (all users)
        if (analyticsResponse.data.recent_system_activity) {
          recentActivity.value = analyticsResponse.data.recent_system_activity
        }
      }
    } catch (error) {
      console.error('Error loading analytics:', error)
      // Set default empty charts for admin
      attendanceChart.value = []
      weeklyPattern.value = [
        { name: 'Mon', percentage: 0 },
        { name: 'Tue', percentage: 0 },
        { name: 'Wed', percentage: 0 },
        { name: 'Thu', percentage: 0 },
        { name: 'Fri', percentage: 0 },
        { name: 'Sat', percentage: 0 },
        { name: 'Sun', percentage: 0 }
      ]
    }

    // Load recent system activity if not in analytics
    if (recentActivity.value.length === 0) {
      try {
        const recentResponse = await adminAPI.getRecentActivity()
        recentActivity.value = recentResponse.data.activities || []
      } catch (error) {
        console.error('Error loading recent activity:', error)
      }
    }

    // Load active classes for admin
    try {
      const classesResponse = await adminAPI.getActiveClasses()
      activeClasses.value = classesResponse.data.classes || []
    } catch (error) {
      console.error('Error loading active classes:', error)
      activeClasses.value = []
    }

    // Load users for admin
    await loadUsers()

  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    isLoading.value = false
    dashboardStore.setLoading(false)
  }
}

// Activity refresh function
const refreshActivity = async () => {
  try {
    if (authStore.isAdmin) {
      // Reload system analytics for admin
      const analyticsResponse = await adminAPI.getAnalytics()
      if (analyticsResponse.data?.recent_system_activity) {
        recentActivity.value = analyticsResponse.data.recent_system_activity
      }
    } else {
      // Reload user analytics for students
      const analyticsResponse = await userAPI.getMyAnalytics()
      if (analyticsResponse.data?.recent_activity) {
        recentActivity.value = analyticsResponse.data.recent_activity
      }
    }
  } catch (error) {
    console.error('Error refreshing activity:', error)
  }
}

// User management methods
const loadUsers = async () => {
  if (!authStore.isAdmin) return

  try {
    loadingUsers.value = true
    const response = await adminAPI.getUsers()
    users.value = response.data.users || []
  } catch (error: any) {
    console.error('Error loading users:', error)
    alert(error.response?.data?.message || 'Error loading users')
  } finally {
    loadingUsers.value = false
  }
}

const captureUserFace = (user: User) => {
  // Set the user to capture face for and open registration modal in capture mode
  userToCapture.value = user
  showUserRegistrationModal.value = true
}

const editUser = async (user: User) => {
  // For now, show user details - could expand to edit modal
  const newPassword = prompt(`Enter new password for ${user.name} (leave empty to keep current):`)
  if (newPassword !== null && newPassword.trim() !== '') {
    try {
      await adminAPI.updateUserPassword(user.id.toString(), newPassword.trim())
      alert('Password updated successfully!')
    } catch (error: any) {
      console.error('Error updating password:', error)
      alert(error.response?.data?.message || 'Error updating password')
    }
  }
}

const deleteUser = async (user: User) => {
  if (!confirm(`Are you sure you want to delete user "${user.name}"? This action cannot be undone.`)) {
    return
  }

  try {
    await adminAPI.deleteUser(user.id.toString())
    alert('User deleted successfully!')

    // Reload users list
    await loadUsers()
  } catch (error: any) {
    console.error('Error deleting user:', error)
    alert(error.response?.data?.message || 'Error deleting user')
  }
}

const refreshData = async () => {
  if (authStore.isAdmin) {
    await Promise.all([
      loadDashboardData(),
      loadUsers()
    ])
  } else {
    await loadUserData()
  }
}

// Notice management methods
const getPriorityIcon = (priority?: string) => {
  const icons: { [key: string]: string } = {
    low: '📌',
    normal: '📋',
    high: '⚠️',
    urgent: '🚨'
  }
  return icons[priority || 'normal'] || '📋'
}

const toggleBookmark = (notice: Notice) => {
  notice.bookmarked = !notice.bookmarked
}

const shareNotice = (notice: Notice) => {
  // Implement share functionality
  if (navigator.share) {
    navigator.share({
      title: notice.title,
      text: notice.content,
      url: window.location.href
    })
  } else {
    // Fallback: copy to clipboard
    navigator.clipboard.writeText(`${notice.title}\n\n${notice.content}`)
    alert('Notice copied to clipboard!')
  }
}

const deleteNotice = async (notice: Notice) => {
  if (!confirm('Are you sure you want to delete this notice?')) return

  try {
    await adminAPI.deleteNotice(notice.id.toString())
    notices.value = notices.value.filter(n => n.id !== notice.id)
    alert('Notice deleted successfully!')
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error deleting notice')
  }
}

const toggleNoticeExpansion = (notice: Notice) => {
  notice.expanded = !notice.expanded
}

const toggleLike = (notice: Notice) => {
  notice.likes = (notice.likes || 0) + (notice.liked ? -1 : 1)
  notice.liked = !notice.liked
}

const createNotice = () => {
  // Open notice creation modal or redirect to admin panel
  router.push('/admin?tab=notices&action=create')
}

// Class management methods (Admin)
const saveClassConfig = async () => {
  try {
    await adminAPI.saveClassConfig(classConfig.value)
    alert('Class configuration saved successfully!')
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error saving class configuration')
  }
}

const saveTimeSettings = async () => {
  try {
    await adminAPI.saveTimeSettings(timeSettings.value)
    alert('Time settings saved successfully!')
  } catch (error: any) {
    alert(error.response?.data?.message || 'Error saving time settings')
  }
}

const refreshClasses = async () => {
  try {
    const response = await adminAPI.getActiveClasses()
    activeClasses.value = response.data.classes || []
  } catch (error) {
    console.error('Error refreshing classes:', error)
  }
}

const openAttendance = (cls: any) => {
  // Navigate to attendance taking for specific class
  router.push(`/admin?class=${cls.id}&action=attendance`)
}

// Percentage change calculation
const calculatePercentageChange = (current: number, previous: number): string => {
  if (previous === 0) return current > 0 ? '+100%' : '+0.0%'
  const change = ((current - previous) / previous) * 100
  const sign = change >= 0 ? '+' : ''
  return `${sign}${change.toFixed(1)}%`
}

// Load dashboard stats with real-time changes
const loadDashboardStats = async () => {
  try {
    // Store previous stats for comparison
    previousDashboardStats.value = { ...dashboardStats.value }

    if (authStore.isAdmin) {
      // Load admin stats
      const response = await dashboardAPI.getStats()
      const data = response.data

      dashboardStats.value = {
        totalUsers: data.total_users || 0,
        totalPresent: data.present_today || 0,
        absentToday: data.absent_today || 0,
        attendanceRate: data.attendance_rate || 0
      }
    } else {
      // Load user-specific stats
      const response = await userAPI.getMyAnalytics()
      const data = response.data

      dashboardStats.value = {
        totalUsers: data.total_classmates || personalStats.value.totalDays,
        totalPresent: data.present_today || personalStats.value.attendedDays,
        absentToday: data.absent_today || 0,
        attendanceRate: data.attendance_rate || personalStats.value.attendanceRate
      }
    }

    // Calculate percentage changes
    statsPercentageChanges.value = {
      totalUsers: calculatePercentageChange(dashboardStats.value.totalUsers, previousDashboardStats.value.totalUsers),
      totalPresent: calculatePercentageChange(dashboardStats.value.totalPresent, previousDashboardStats.value.totalPresent),
      absentToday: calculatePercentageChange(dashboardStats.value.absentToday, previousDashboardStats.value.absentToday),
      attendanceRate: calculatePercentageChange(dashboardStats.value.attendanceRate, previousDashboardStats.value.attendanceRate)
    }
  } catch (error) {
    console.error('Error loading dashboard stats:', error)
  }
}

// Add event handlers for Add User button hover
const handleAddUserMouseOver = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  target.style.background = 'linear-gradient(135deg, #45b7d1, #3b9dd8)'
}
const handleAddUserMouseOut = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  target.style.background = 'linear-gradient(135deg, #4ecdc4, #45b7d1)'
}

// Load data when component mounts
onMounted(() => {
  if (authStore.isAdmin) {
    loadDashboardData()
  } else {
    loadUserData()
  }
})
</script>

<style scoped>
/* Modern Dashboard Styles */
.modern-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  overflow-x: hidden;
}

/* Background Animation */
.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.floating-orbs {
  position: absolute;
  width: 100%;
  height: 100%;
}

.orb {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(78, 205, 196, 0.1), rgba(255, 107, 107, 0.05));
  animation: float 15s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  top: 60%;
  right: 10%;
  animation-delay: -5s;
}

.orb-3 {
  width: 150px;
  height: 150px;
  bottom: 20%;
  left: 60%;
  animation-delay: -10s;
}

.orb-4 {
  width: 100px;
  height: 100px;
  top: 30%;
  right: 30%;
  animation-delay: -15s;
}

.orb-5 {
  width: 250px;
  height: 250px;
  bottom: 10%;
  right: 5%;
  animation-delay: -20s;
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }

  25% {
    transform: translateY(-20px) rotate(90deg);
  }

  50% {
    transform: translateY(10px) rotate(180deg);
  }

  75% {
    transform: translateY(-15px) rotate(270deg);
  }
}

.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(78, 205, 196, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(78, 205, 196, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% {
    transform: translate(0, 0);
  }

  100% {
    transform: translate(50px, 50px);
  }
}

/* Dashboard Container */
.dashboard-container {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

/* Ultra Modern Header - Responsive */
.dashboard-header {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  padding: 2rem;
  margin-bottom: 3rem;
  position: relative;
  overflow: hidden;
}

.dashboard-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 300% 100%;
  animation: gradientFlow 3s ease-in-out infinite;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.user-greeting {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.greeting-avatar {
  position: relative;
}

.avatar-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.avatar-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  z-index: 2;
}

.avatar-ring {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border: 2px solid rgba(78, 205, 196, 0.5);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.online-indicator {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 16px;
  height: 16px;
  background: #22c55e;
  border: 3px solid #1a1a2e;
  border-radius: 50%;
  animation: blink 2s infinite;
}

@keyframes pulse {

  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

@keyframes blink {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.7;
  }
}

.greeting-text {
  flex: 1;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradientFlow 4s ease-in-out infinite;
  margin-bottom: 0.5rem;
  line-height: 1.2;
  word-break: break-word;
  overflow-wrap: break-word;
}

.role-subtitle {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.role-chip {
  background: rgba(78, 205, 196, 0.2);
  color: #4ecdc4;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  border: 1px solid rgba(78, 205, 196, 0.3);
}

.role-chip.admin {
  background: rgba(255, 107, 107, 0.2);
  color: #8A2BE2;
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.date-display {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

.header-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1rem;
}

.stats-preview {
  display: flex;
  gap: 1rem;
}

.stat-mini {
  text-align: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  min-width: 70px;
}

.stat-number {
  display: block;
  font-size: 1.25rem;
  font-weight: bold;
  color: white;
}

.stat-text {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.primary-action-btn {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.primary-action-btn.admin-btn {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4, #45b7d1);
}

.primary-action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
}

.btn-icon {
  position: relative;
}

.pulse-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s infinite;
}

.secondary-action-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.secondary-action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

/* Advanced Stats Dashboard */
.stats-dashboard {
  margin-bottom: 3rem;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.modern-loader {
  text-align: center;
}

.loader-ring {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(78, 205, 196, 0.2);
  border-top: 4px solid #4ecdc4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.loader-text {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  transition: all 0.4s ease;
  animation: slideUp 0.6s ease var(--delay);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.stat-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.stat-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.1;
}

.stat-pattern {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 70% 30%, rgba(78, 205, 196, 0.1), transparent 50%);
}

.stat-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stat-icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-trend {
  font-size: 1.5rem;
}

.stat-info {
  text-align: right;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.25rem;
}

.stat-change {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

.stat-change.positive {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.stat-change.negative {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.stat-chart-mini {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 60px;
  height: 40px;
}

.chart-line {
  width: 100%;
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.3), rgba(69, 183, 209, 0.3));
  border-radius: 4px 4px 0 0;
  transition: height 0.8s ease;
}

/* Enhanced Navigation */
.modern-nav {
  margin-bottom: 3rem;
}

.nav-wrapper {
  display: flex;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 0.5rem;
  gap: 0.5rem;
  overflow-x: auto;
}

.nav-tab {
  flex: 1;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  padding: 1rem 2rem;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  white-space: nowrap;
}

.nav-tab.active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  box-shadow: 0 4px 20px rgba(78, 205, 196, 0.2);
}

.nav-tab:hover:not(.active) {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
}

.tab-highlight {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.nav-tab.active .tab-highlight {
  width: 80%;
}

/* Tab Content Area */
.tab-content-area {
  min-height: 600px;
}

.tab-content {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 1024px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .chart-panel,
  .heatmap-panel,
  .timeline-panel {
    padding: 1.5rem;
    border-radius: 18px;
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .chart-panel,
  .heatmap-panel,
  .timeline-panel {
    padding: 1rem;
    border-radius: 14px;
  }

  .panel-header {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 1rem 0.5rem;
  }

  .panel-title {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .content-grid {
    gap: 0.5rem;
    margin-bottom: 1rem;
  }

  .chart-panel,
  .heatmap-panel,
  .timeline-panel {
    padding: 0.5rem;
    border-radius: 10px;
  }

  .panel-title {
    font-size: 0.85rem;
  }
}

/* Panel Styles */
.chart-panel,
.heatmap-panel,
.timeline-panel,
.notices-container,
.profile-main,
.profile-stats,
.config-section,
.classes-section {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
}

.panel-header,
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.panel-title,
.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.panel-controls,
.card-actions {
  display: flex;
  gap: 0.5rem;
}

.control-btn,
.action-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover,
.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.action-btn.primary {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  border: none;
}

/* Chart Area */
.chart-area {
  padding: 2rem;
  height: 400px;
}

.modern-chart {
  display: flex;
  align-items: end;
  gap: 1rem;
  height: 100%;
  padding: 1rem 0;
}

.chart-column {
  flex: 1;
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  border-radius: 8px 8px 0 0;
  position: relative;
  min-height: 20px;
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: center;
  cursor: pointer;
  transition: all 0.4s ease;
  animation: chartGrow 0.8s ease var(--delay);
}

@keyframes chartGrow {
  from {
    height: 0;
  }

  to {
    height: var(--final-height);
  }
}

.chart-column:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 10px 25px rgba(78, 205, 196, 0.3);
}

.column-fill {
  width: 100%;
  height: 100%;
  background: inherit;
  border-radius: inherit;
}

.column-label {
  position: absolute;
  bottom: -25px;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.column-value {
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.empty-chart,
.empty-timeline,
.empty-notices,
.empty-classes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.empty-illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

/* Heatmap */
.heatmap-container {
  padding: 2rem;
}

.day-heatmap {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  transition: all 0.3s ease;
}

.day-heatmap:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(5px);
}

.day-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 100px;
}

.day-name {
  font-weight: 600;
  color: white;
}

.day-percentage {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.8);
}

.day-progress-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s ease;
}

.progress-fill.high {
  background: linear-gradient(90deg, #22c55e, #16a34a);
}

.progress-fill.medium {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-fill.low {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

/* Timeline */
.timeline-container {
  padding: 2rem;
  max-height: 500px;
  overflow-y: auto;
}

.timeline-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border-left: 4px solid #4ecdc4;
  transition: all 0.3s ease;
}

.timeline-item:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(5px);
}

.timeline-marker {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 0.5rem;
  flex-shrink: 0;
}

.timeline-marker.present {
  background: #22c55e;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
}

.timeline-marker.absent {
  background: #ef4444;
  box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
}

.timeline-content {
  flex: 1;
}

.activity-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.activity-user {
  font-weight: 600;
  color: white;
}

.activity-time {
  color: rgba(255, 255, 255, 0.8);
}

.activity-date {
  color: rgba(255, 255, 255, 0.6);
}

.activity-details {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status-indicator {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-indicator.present {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.status-indicator.absent {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.user-type {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Enhanced Notices Section Styling - Complete Redesign */
.notices-tab {
  animation: fadeInUp 0.6s ease;
  padding: 0;
}

.notices-container {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 28px;
  padding: 2.5rem;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.notices-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 400% 100%;
  animation: gradientFlow 4s ease-in-out infinite;
}

.notices-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  gap: 2rem;
}

.notices-header .header-content {
  flex: 1;
  min-width: 0;
}

.notices-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.75rem;
  line-height: 1.2;
}

.title-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
}

.title-icon-wrapper .title-icon {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.5rem;
  position: relative;
  z-index: 2;
}

.notification-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70px;
  height: 70px;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s infinite;
}

.section-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.4;
}

.notices-actions {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: flex-end;
  flex-shrink: 0;
}

@media (max-width: 1024px) {
  .notices-actions {
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }

  .admin-actions {
    flex-direction: row;
    gap: 0.75rem;
  }

  .notices-filters[data-v-336c5134] {
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 0.75rem;
    flex-direction: row;
  }

  .welcome-title[data-v-336c5134] {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .notices-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    margin-top: 1rem;
  }

  .admin-actions {
    flex-direction: column;
    gap: 0.5rem;
    align-items: stretch;
  }

  .create-notice-btn {
    width: 100%;
    justify-content: center;
    font-size: 0.9rem;
    padding: 0.75rem 1rem;
  }

  .notices-filters {
    gap: 0.5rem;
    padding: 0.5rem;
    align-items: stretch;
  }

  .filter-btn {
    width: 100%;
    text-align: center;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .notices-actions {
    gap: 0.5rem;
    margin-top: 0.5rem;
  }

  .admin-actions {
    gap: 0.25rem;
  }

  .create-notice-btn {
    font-size: 0.85rem;
    padding: 0.5rem 0.5rem;
    border-radius: 12px;
  }

  .notices-filters {
    padding: 0.25rem;
    border-radius: 12px;
  }

  .filter-btn {
    font-size: 0.8rem;
    padding: 0.5rem 0.5rem;
    border-radius: 10px;
  }
}

.notices-filters {
  display: flex;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.75rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.filter-btn {
  padding: 0.875rem 1.75rem;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.9rem;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
}

.filter-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.filter-btn:hover::before {
  left: 100%;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.filter-btn.active {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  color: white;
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.3);
  transform: translateY(-1px);
}

.admin-actions {
  display: flex;
  gap: 1rem;
}

.create-notice-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 18px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 700;
  font-size: 0.95rem;
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.3);
  position: relative;
  overflow: hidden;
}

.create-notice-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.create-notice-btn:hover::before {
  left: 100%;
}

.create-notice-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(34, 197, 94, 0.4);
  background: linear-gradient(135deg, #16a34a, #15803d);
}

/* Enhanced Notice Cards */
.notices-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
  gap: 2rem;
  animation: fadeInUp 0.6s ease;
}

.notice-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 24px;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  animation: slideInUp 0.7s ease var(--delay);
}

.notice-card:hover {
  transform: translateY(-12px) scale(1.02);
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(78, 205, 196, 0.4);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.notice-background {
  position: absolute;
  top: -100%;
  right: -100%;
  width: 300%;
  height: 300%;
  pointer-events: none;
}

.notice-pattern {
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.08) 0%, transparent 60%);
  animation: floatPattern 12s ease-in-out infinite;
}

@keyframes floatPattern {

  0%,
  100% {
    transform: rotate(0deg) translateY(0px);
    opacity: 0.6;
  }

  33% {
    transform: rotate(120deg) translateY(-30px);
    opacity: 0.8;
  }

  66% {
    transform: rotate(240deg) translateY(-15px);
    opacity: 0.4;
  }
}

.notice-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  position: relative;
  z-index: 2;
  gap: 1rem;
}

.notice-meta {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  flex: 1;
  min-width: 0;
}

.notice-priority {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 16px;
  font-size: 1.5rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.notice-priority:hover {
  transform: scale(1.1);
}

.notice-priority.low {
  background: rgba(107, 114, 128, 0.2);
  border: 2px solid rgba(107, 114, 128, 0.4);
  color: #9ca3af;
}

.notice-priority.normal {
  background: rgba(59, 130, 246, 0.2);
  border: 2px solid rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.notice-priority.high {
  background: rgba(245, 158, 11, 0.2);
  border: 2px solid rgba(245, 158, 11, 0.4);
  color: #f59e0b;
}

.notice-priority.urgent {
  background: rgba(239, 68, 68, 0.2);
  border: 2px solid rgba(239, 68, 68, 0.4);
  color: #ef4444;
  animation: urgentPulse 2s infinite;
}

@keyframes urgentPulse {

  0%,
  100% {
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    transform: scale(1);
  }

  50% {
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
    transform: scale(1.05);
  }
}

.notice-info {
  flex: 1;
  min-width: 0;
}

.notice-title {
  color: white;
  font-size: 1.4rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  line-height: 1.3;
  word-wrap: break-word;
}

.notice-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  flex-wrap: wrap;
}

.notice-date {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.notice-separator {
  color: rgba(255, 255, 255, 0.4);
}

.notice-author {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
}

.notice-actions {
  display: flex;
  gap: 0.75rem;
  flex-shrink: 0;
}

.notice-action-btn {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.875rem;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  height: 44px;
  position: relative;
  overflow: hidden;
}

.notice-action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: all 0.3s ease;
  transform: translate(-50%, -50%);
}

.notice-action-btn:hover::before {
  width: 100%;
  height: 100%;
}

.notice-action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.notice-action-btn.bookmark.active {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.4);
  color: #f59e0b;
  box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
}

.notice-action-btn.share:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.notice-action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

.notice-content {
  position: relative;
  z-index: 2;
  margin-bottom: 2rem;
}

.notice-text {
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.7;
  margin: 0;
  font-size: 1rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  transition: all 0.4s ease;
}

.notice-text.expanded {
  -webkit-line-clamp: unset;
  overflow: visible;
  display: block;
}

.read-more-btn {
  background: none;
  border: none;
  color: #4ecdc4;
  cursor: pointer;
  font-weight: 600;
  margin-top: 1rem;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  position: relative;
}

.read-more-btn::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #4ecdc4, #45b7d1);
  transition: width 0.3s ease;
}

.read-more-btn:hover::after {
  width: 100%;
}

.read-more-btn:hover {
  color: #45b7d1;
  transform: translateX(2px);
}

.notice-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
  gap: 1rem;
  flex-wrap: wrap;
}

.notice-tags {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.notice-tag {
  background: rgba(78, 205, 196, 0.15);
  color: #4ecdc4;
  padding: 0.4rem 1rem;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 600;
  border: 1px solid rgba(78, 205, 196, 0.3);
  transition: all 0.3s ease;
}

.notice-tag:hover {
  background: rgba(78, 205, 196, 0.25);
  transform: translateY(-1px);
}

.notice-engagement {
  display: flex;
  gap: 1.5rem;
}

.engagement-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  padding: 0.6rem 0.8rem;
  border-radius: 12px;
  font-weight: 500;
}

.engagement-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  transform: translateY(-1px);
}

/* Empty States Enhanced */
.empty-notices {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 2rem;
  text-align: center;
}

.empty-icon-wrapper {
  position: relative;
  margin-bottom: 2rem;
}

.empty-icon {
  font-size: 5rem;
  color: rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
}

.empty-icon-bg {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s infinite;
}

.empty-title {
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.empty-description {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
  margin: 0 0 2.5rem 0;
  max-width: 500px;
  line-height: 1.5;
}

.empty-action-btn {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  color: white;
  border: none;
  padding: 1.25rem 2.5rem;
  border-radius: 18px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
}

.empty-action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(78, 205, 196, 0.4);
}

/* Enhanced Management Section Styling */
.management-tab {
  animation: fadeInUp 0.6s ease;
}

.management-layout {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.management-header {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 28px;
  padding: 2.5rem;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.management-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 400% 100%;
  animation: gradientFlow 4s ease-in-out infinite;
}

.management-header .header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 2rem;
}

.management-header .section-title {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin: 0;
  line-height: 1.2;
}

.title-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
}

.title-icon-wrapper .title-icon {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.5rem;
  position: relative;
  z-index: 2;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s infinite;
}

.header-stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.quick-stat {
  text-align: center;
  background: rgba(255, 255, 255, 0.06);
  padding: 1.5rem 2rem;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  min-width: 120px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.quick-stat::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.1), transparent);
  transition: left 0.5s ease;
}

.quick-stat:hover::before {
  left: 100%;
}

.quick-stat:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(78, 205, 196, 0.4);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.quick-stat .stat-number {
  display: block;
  font-size: 1.75rem;
  font-weight: 800;
  color: #4ecdc4;
  margin-bottom: 0.5rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.quick-stat .stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

/* Management Grid */
.management-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2.5rem;
  margin-bottom: 2.5rem;
}

.config-section,
.time-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.config-section:hover,
.time-card:hover {
  border-color: rgba(78, 205, 196, 0.3);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-dot.active {
  background: #22c55e;
  box-shadow: 0 0 10px rgba(34, 197, 94, 0.5);
}

.status-text {
  color: #22c55e;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-indicator {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-indicator.active {
  animation: pulse 3s infinite;
}

/* Forms */
.config-form,
.time-form {
  padding: 2rem;
}

.form-grid,
.time-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-field,
.time-field {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.field-label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.field-input {
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  padding: 1rem 1.25rem;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.field-input:focus {
  outline: none;
  border-color: rgba(78, 205, 196, 0.5);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 20px rgba(78, 205, 196, 0.2);
}

.field-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.input-group {
  display: flex;
  align-items: center;
  position: relative;
}

.input-group .field-input {
  flex: 1;
  border-radius: 14px 0 0 14px;
}

.input-suffix {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-left: none;
  border-radius: 0 14px 14px 0;
  padding: 1rem 1.25rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 500;
}

.save-btn {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  color: white;
  border: none;
  padding: 1.25rem 2.5rem;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
  position: relative;
  overflow: hidden;
}

.save-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.save-btn:hover::before {
  left: 100%;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(78, 205, 196, 0.4);
  background: linear-gradient(135deg, #45b7d1, #3b9dd8);
}

/* User Management Section */
.users-section,
.classes-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.75rem 1.5rem;
  border-radius: 14px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.action-btn.primary {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  border: none;
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
}

.action-btn.primary:hover {
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
}

/* Users Table */
.users-table-container {
  padding: 2rem;
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  overflow: hidden;
}

.users-table th {
  background: rgba(255, 255, 255, 0.05);
  padding: 1.25rem 1rem;
  text-align: left;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.users-table td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
}

.user-row {
  transition: all 0.3s ease;
}

.user-row:hover {
  background: rgba(255, 255, 255, 0.03);
}

.user-id {
  font-weight: 700;
  color: #4ecdc4;
}

.user-name {
  font-weight: 600;
  color: white;
}

.type-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.type-badge.student {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.type-badge.teacher {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.type-badge.admin {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.face-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.face-badge.has-face {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.face-badge.no-face {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn-small {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.6rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn-small:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.action-btn-small.capture:hover {
  background: rgba(59, 130, 246, 0.2);
  border-color: rgba(59, 130, 246, 0.4);
  color: #3b82f6;
}

.action-btn-small.edit:hover {
  background: rgba(245, 158, 11, 0.2);
  border-color: rgba(245, 158, 11, 0.4);
  color: #f59e0b;
}

.action-btn-small.delete:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ef4444;
}

/* Enhanced Profile Section Styling */
.profile-tab {
  animation: fadeInUp 0.6s ease;
}

.profile-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2.5rem;
}

.profile-main {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 28px;
  padding: 0;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  backdrop-filter: blur(15px);
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.profile-main:hover {
  border-color: rgba(78, 205, 196, 0.4);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

.profile-header {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(78, 205, 196, 0.15));
  padding: 2.5rem;
  display: flex;
  align-items: center;
  gap: 2.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
}

.profile-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4);
  background-size: 400% 100%;
  animation: gradientFlow 4s ease-in-out infinite;
}

.profile-avatar-large {
  position: relative;
  flex-shrink: 0;
}

.avatar-container {
  position: relative;
}

.avatar-circle-large {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 800;
  color: white;
  position: relative;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.15);
  transition: all 0.4s ease;
  box-shadow: 0 8px 30px rgba(78, 205, 196, 0.3);
}

.avatar-circle-large:hover {
  transform: scale(1.05) rotate(5deg);
  box-shadow: 0 12px 40px rgba(78, 205, 196, 0.4);
}

.avatar-status {
  position: absolute;
  bottom: 15px;
  right: 15px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 4px solid #1a1a2e;
  transition: all 0.3s ease;
}

.avatar-status.online {
  background: #22c55e;
  animation: pulse 2s infinite;
  box-shadow: 0 0 15px rgba(34, 197, 94, 0.5);
}

.profile-info {
  flex: 1;
  min-width: 0;
}

.profile-name {
  font-size: 2.25rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.75rem;
  line-height: 1.2;
  word-wrap: break-word;
}

.profile-role {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.profile-badges {
  display: flex;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.badge {
  padding: 0.75rem 1.25rem;
  border-radius: 16px;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
}

.badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.badge.active {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
  border: 2px solid rgba(34, 197, 94, 0.4);
}

.badge.verified {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
  border: 2px solid rgba(59, 130, 246, 0.4);
}

.profile-details {
  padding: 2.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  transition: all 0.3s ease;
  border-radius: 12px;
}

.detail-row:hover {
  background: rgba(255, 255, 255, 0.03);
  padding-left: 1.25rem;
  padding-right: 1.25rem;
  transform: translateX(5px);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.detail-value {
  color: white;
  font-weight: 700;
  font-size: 1rem;
}

/* Enhanced Profile Stats */
.profile-stats {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 24px;
  padding: 0;
  border: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  backdrop-filter: blur(10px);
  height: fit-content;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.profile-stats:hover {
  border-color: rgba(78, 205, 196, 0.4);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.stats-header {
  padding: 2rem 2.5rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stats-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.4rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.stats-items {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.05), transparent);
  transition: left 0.5s ease;
}

.stat-item:hover::before {
  left: 100%;
}

.stat-item:hover {
  background: rgba(255, 255, 255, 0.07);
  transform: translateX(8px);
  border-color: rgba(78, 205, 196, 0.4);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
}

.stat-icon {
  font-size: 2rem;
  background: rgba(78, 205, 196, 0.15);
  padding: 1rem;
  border-radius: 16px;
  border: 2px solid rgba(78, 205, 196, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.stat-item:hover .stat-icon {
  transform: scale(1.1);
  background: rgba(78, 205, 196, 0.25);
}

.stat-data {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-data .stat-number {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.25rem;
}

.stat-data .stat-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

/* Enhanced Achievements Section */
.achievements-section {
  margin-top: 2.5rem;
  padding-top: 2.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.achievements-title {
  color: white;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1.25rem;
}

.achievement-item {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 2rem 1.25rem;
  text-align: center;
  transition: all 0.4s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.achievement-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.1), transparent);
  transition: left 0.6s ease;
}

.achievement-item:hover::before {
  left: 100%;
}

.achievement-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.4);
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.achievement-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: block;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
}

.achievement-item:hover .achievement-icon {
  transform: scale(1.1);
}

.achievement-name {
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  position: relative;
  z-index: 2;
  line-height: 1.3;
}

.no-achievements {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.03);
  border: 2px dashed rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

/* Responsive Design - Mobile First Approach */
@media (max-width: 1400px) {
  .notices-grid {
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  }

  .management-grid {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }

  .profile-layout {
    grid-template-columns: 1fr 350px;
  }
}

@media (max-width: 1200px) {
  .dashboard-container {
    padding: 1.5rem;
  }

  .notices-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }

  .management-grid {
    grid-template-columns: 1fr;
  }

  .profile-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .header-stats {
    flex-direction: column;
    gap: 1.5rem;
  }

  .quick-stat {
    min-width: auto;
  }
}

@media (max-width: 1024px) {
  .notices-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .notices-actions {
    width: 100%;
    justify-content: space-between;
    align-items: center;
  }

  .management-header .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .header-stats {
    width: 100%;
    flex-direction: row;
    justify-content: space-between;
  }

  .form-grid,
  .time-grid {
    grid-template-columns: 1fr;
  }

  .users-table-container {
    overflow-x: auto;
  }

  .users-table {
    min-width: 600px;
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }

  .notices-grid {
    grid-template-columns: 1fr;
  }

  .notice-card {
    padding: 2rem;
  }

  .management-header,
  .notices-container {
    padding: 2rem;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 2rem;
    padding: 2rem;
  }

  .profile-name {
    font-size: 2rem;
  }

  .avatar-circle-large {
    width: 120px;
    height: 120px;
    font-size: 2.5rem;
  }

  .notices-header {
    text-align: center;
  }

  .notice-meta {
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    text-align: center;
  }

  .notice-actions {
    margin-top: 1rem;
    justify-content: center;
  }

  .achievements-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }

  .header-stats {
    flex-direction: column;
    gap: 1rem;
  }

  .quick-stat {
    padding: 1.25rem 1.5rem;
  }

  .card-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-btn {
    text-align: center;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 0.75rem;
  }

  .notices-container,
  .management-header {
    padding: 1.5rem;
    border-radius: 20px;
  }

  .notice-card {
    padding: 1.5rem;
    border-radius: 16px;
  }

  .notices-title,
  .management-header .section-title {
    font-size: 1.5rem;
  }

  .title-icon-wrapper {
    width: 50px;
    height: 50px;
  }

  .title-icon-wrapper .title-icon {
    font-size: 2rem;
  }

  .profile-header {
    padding: 1.5rem;
  }

  .profile-name {
    font-size: 1.75rem;
  }

  .avatar-circle-large {
    width: 100px;
    height: 100px;
    font-size: 2rem;
  }

  .notices-filters {
    gap: 0.5rem;
    padding: 0.5rem;
  }

  .filter-btn {
    text-align: center;
    padding: 0.75rem 1.25rem;
  }

  .notice-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .notice-engagement {
    justify-content: center;
    width: 100%;
  }

  .form-grid,
  .time-grid {
    gap: 1rem;
  }

  .field-input {
    padding: 0.875rem 1rem;
  }

  .save-btn {
    padding: 1rem 2rem;
    font-size: 0.95rem;
  }

  .stats-items {
    padding: 2rem;
    gap: 1.5rem;
  }

  .stat-item {
    padding: 1.25rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .stat-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .achievements-grid {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  }

  .achievement-item {
    padding: 1.5rem 1rem;
  }

  .users-table th,
  .users-table td {
    padding: 1rem 0.5rem;
    font-size: 0.85rem;
  }

  .action-btn-small {
    min-width: 32px;
    height: 32px;
    padding: 0.5rem;
    font-size: 0.9rem;
  }

  .content-grid[data-v-336c5134] {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .panel-title {
    font-size: 0.75rem;
  }

}

@media (max-width: 360px) {
  .notices-grid {
    gap: 1.5rem;
  }

  .notice-card {
    padding: 1.25rem;
  }

  .notices-title {
    font-size: 1.25rem;
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .profile-name {
    font-size: 1.5rem;
  }

  .avatar-circle-large {
    width: 80px;
    height: 80px;
    font-size: 1.5rem;
  }

  .management-grid {
    gap: 1.5rem;
  }

  .quick-stat {
    padding: 1rem;
  }

  .quick-stat .stat-number {
    font-size: 1.5rem;
  }
}

/* Animation Keyframes */
@keyframes gradientFlow {

  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* Loading States */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  flex-direction: column;
  gap: 1rem;
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(78, 205, 196, 0.2);
  border-top: 4px solid #4ecdc4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Chart Tooltip */
.chart-tooltip {
  position: fixed;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  pointer-events: none;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.tooltip-title {
  font-weight: 600;
  color: #4ecdc4;
}

.tooltip-value {
  font-weight: 500;
}
</style>

/* ===== RESPONSIVE HEADER FIXES ===== */

/* Tablet and smaller screens */
@media (max-width: 1024px) {
.dashboard-header {
padding: 1.5rem;
margin-bottom: 2rem;
border-radius: 20px;
}

.header-content {
gap: 1.5rem;
}

.welcome-title {
font-size: 2rem;
}

.avatar-circle {
width: 60px;
height: 60px;
}

.avatar-text {
font-size: 1.25rem;
}

.stats-preview {
gap: 0.75rem;
}

.stat-mini {
min-width: 60px;
padding: 0.5rem;
}

.primary-action-btn {
padding: 0.75rem 1.5rem;
}
}

/* Mobile landscape and tablet portrait */
@media (max-width: 768px) {
.dashboard-header {
padding: 1.25rem;
margin-bottom: 1.5rem;
border-radius: 16px;
}

.header-content {
flex-direction: column;
align-items: stretch;
gap: 1.5rem;
}

.user-greeting {
flex-direction: column;
align-items: center;
text-align: center;
gap: 1rem;
}

.greeting-text {
width: 100%;
}

.welcome-title {
font-size: 1.75rem;
text-align: center;
line-height: 1.3;
}

.role-subtitle {
justify-content: center;
flex-wrap: wrap;
gap: 0.75rem;
}

.header-actions {
align-items: center;
width: 100%;
}

.stats-preview {
width: 100%;
justify-content: center;
margin-bottom: 1rem;
}

.action-buttons {
width: 100%;
justify-content: center;
flex-wrap: wrap;
gap: 0.75rem;
}

.primary-action-btn {
flex: 1;
min-width: 200px;
max-width: 300px;
justify-content: center;
}

.secondary-action-btn {
width: 48px;
height: 48px;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
}
}

/* Mobile portrait */
@media (max-width: 480px) {
.dashboard-header {
padding: 1rem;
margin-bottom: 1rem;
border-radius: 12px;
}

.header-content {
gap: 1rem;
}

.user-greeting {
gap: 0.75rem;
}

.avatar-circle {
width: 50px;
height: 50px;
}

.avatar-text {
font-size: 1rem;
}

.online-indicator {
width: 12px;
height: 12px;
border-width: 2px;
}

.welcome-title {
font-size: 1.5rem;
line-height: 1.4;
}

.role-subtitle {
font-size: 0.875rem;
gap: 0.5rem;
}

.role-chip {
padding: 0.375rem 0.75rem;
font-size: 0.75rem;
border-radius: 16px;
}

.date-display {
font-size: 0.75rem;
}

.stats-preview {
gap: 0.5rem;
}

.stat-mini {
min-width: 50px;
padding: 0.5rem 0.375rem;
}

.stat-number {
font-size: 1rem;
}

.stat-text {
font-size: 0.625rem;
}

.action-buttons {
flex-direction: column;
gap: 0.5rem;
}

.primary-action-btn {
width: 100%;
min-width: auto;
max-width: none;
padding: 1rem;
font-size: 0.875rem;
}

.btn-text {
font-size: 0.875rem;
}

.secondary-action-btn {
width: 100%;
height: 44px;
border-radius: 12px;
font-size: 1.25rem;
}
}

/* Very small screens */
@media (max-width: 360px) {
.dashboard-header {
padding: 0.75rem;
}

.welcome-title {
font-size: 1.25rem;
word-break: break-word;
hyphens: auto;
}

.role-subtitle {
flex-direction: column;
align-items: center;
gap: 0.375rem;
}

.stats-preview {
flex-direction: column;
gap: 0.375rem;
}

.stat-mini {
width: 100%;
display: flex;
justify-content: space-between;
align-items: center;
padding: 0.5rem 0.75rem;
}

.stat-number {
font-size: 1.125rem;
}

.stat-text {
font-size: 0.75rem;
}
}

/* Landscape orientation on mobile */
@media (max-width: 768px) and (orientation: landscape) {
.dashboard-header {
padding: 1rem 1.25rem;
}

.header-content {
flex-direction: row;
align-items: center;
}

.user-greeting {
flex-direction: row;
text-align: left;
flex: 1;
}

.welcome-title {
font-size: 1.5rem;
text-align: left;
}

.role-subtitle {
justify-content: flex-start;
}

.header-actions {
flex-direction: row;
align-items: center;
width: auto;
}

.stats-preview {
margin-bottom: 0;
margin-right: 1rem;
}

.action-buttons {
flex-direction: row;
width: auto;
}

.primary-action-btn {
flex: none;
min-width: 160px;
}
}

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
.dashboard-header::before {
height: 1px;
}

.avatar-ring {
border-width: 1px;
}

.online-indicator {
border-width: 2px;
}
}

/* Accessibility - Reduced motion */
@media (prefers-reduced-motion: reduce) {
.welcome-title,
.avatar-ring,
.online-indicator,
.pulse-effect {
animation: none !important;
}

.primary-action-btn:hover,
.secondary-action-btn:hover {
transform: none !important;
}
}

/* Dark mode adjustments for header */
@media (prefers-color-scheme: light) {
.dashboard-header {
background: rgba(0, 0, 0, 0.02);
border: 1px solid rgba(0, 0, 0, 0.08);
}

.welcome-title {
background: linear-gradient(135deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
}

.role-subtitle {
color: rgba(0, 0, 0, 0.8);
}

.date-display {
color: rgba(0, 0, 0, 0.6);
}

.stat-number {
color: #1a1a2e;
}

.stat-text {
color: rgba(0, 0, 0, 0.7);
}
}

/* Touch device optimizations */
@media (hover: none) and (pointer: coarse) {
.primary-action-btn,
.secondary-action-btn {
min-height: 48px;
touch-action: manipulation;
}

.primary-action-btn:active {
transform: scale(0.98);
}

.secondary-action-btn:active {
transform: scale(0.95);
}

.stat-mini {
min-height: 44px;
}
}

/* Container width adjustments */
@media (max-width: 1200px) {
.dashboard-container {
padding: 0 1.5rem;
}
}

@media (max-width: 768px) {
.dashboard-container {
padding: 0 1rem;
}
}

@media (max-width: 480px) {
.dashboard-container {
padding: 0 0.75rem;
}
}