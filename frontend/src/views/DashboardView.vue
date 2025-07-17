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
            :style="{ '--delay': index * 0.3 + 's' }">
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
          </button>
        </div>
      </nav>

      <!-- Dynamic Tab Content -->
      <main class="tab-content-area">
        <!-- Analytics Tab -->
        <div v-if="activeTab === 'analytics'" class="tab-content analytics-tab">
          <!-- Loading State for Analytics -->
          <div v-if="analyticsLoading" class="analytics-loading">
            <div class="loading-grid">
              <div class="loading-card">
                <div class="loading-shimmer"></div>
                <div class="loading-text">Loading Charts...</div>
              </div>
              <div class="loading-card">
                <div class="loading-shimmer"></div>
                <div class="loading-text">Loading Patterns...</div>
              </div>
              <div class="loading-card">
                <div class="loading-shimmer"></div>
                <div class="loading-text">Loading Activity...</div>
              </div>
            </div>
          </div>

          <div v-else class="content-grid">
            <!-- Ultra Modern Chart Section -->
            <section class="advanced-chart-panel chart-section">
              <div class="panel-header-advanced">
                <div class="header-left">
                  <h3 class="panel-title">
                    <div class="title-icon-container">
                      <div class="icon-glow-effect"></div>
                      <i class="title-icon">📊</i>
                    </div>
                    {{ authStore.isAdmin ? 'System Analytics Dashboard' : 'Personal Analytics Hub' }}
                  </h3>

                </div>
                <div class="panel-controls-advanced">
                  <div class="control-group">
                    <button class="control-btn-modern" @click="filterChart">
                      <span>Filter</span>
                      <div class="btn-ripple"></div>
                    </button>
                    <button class="control-btn-modern" @click="exportChart">
                      <span>Export</span>
                      <div class="btn-ripple"></div>
                    </button>
                    <button class="control-btn-modern primary" @click="refreshAnalytics">
                      <span>Refresh</span>
                      <div class="btn-ripple"></div>
                    </button>
                  </div>
                </div>
              </div>

              <div class="chart-area-advanced">
                <div v-if="attendanceChart.length > 0" class="sophisticated-chart">
                  <!-- Chart Header with Advanced Legend -->
                  <div class="chart-header-advanced">
                    <div class="chart-title-section">
                      <h4 class="chart-title">Monthly Attendance Trend</h4>
                      <div class="chart-metrics">
                        <div class="metric-item">
                          <span class="metric-label">Avg Rate</span>
                          <span class="metric-value">{{ calculateAverageRate() }}%</span>
                        </div>
                        <div class="metric-item">
                          <span class="metric-label">Peak Month</span>
                          <span class="metric-value">{{ getPeakMonth() }}</span>
                        </div>
                        <div class="metric-item">
                          <span class="metric-label">Trend</span>
                          <span class="metric-value trend-up">↗ +5.2%</span>
                        </div>
                      </div>
                    </div>
                    <div class="chart-legend-advanced">
                      <div class="legend-item-advanced">
                        <div class="legend-indicator primary-gradient"></div>
                        <span>{{ authStore.isAdmin ? 'Total Attendance' : 'Your Attendance' }}</span>
                      </div>
                      <div class="legend-item-advanced">
                        <div class="legend-indicator secondary-gradient"></div>
                        <span>Target Goal</span>
                      </div>
                    </div>
                  </div>

                  <!-- Advanced Chart Container -->
                  <div class="chart-container-advanced">
                    <!-- Y-Axis with Grid Lines -->
                    <div class="chart-y-axis-advanced">
                      <div class="y-label-advanced" v-for="(label, index) in ['100%', '75%', '50%', '25%', '0%']"
                        :key="index">
                        <span class="label-text">{{ label }}</span>
                        <div class="grid-line" :style="{ opacity: index === 4 ? 0.3 : 0.1 }"></div>
                      </div>
                    </div>

                    <!-- Chart Bars with Advanced Styling -->
                    <div class="chart-bars-advanced">
                      <div v-for="(month, index) in filteredChartData" :key="index" class="chart-column-advanced"
                        :style="{
                          animationDelay: (index * 0.15) + 's',
                          '--column-index': index
                        }" @mouseover="showAdvancedTooltip(month, $event, index)" @mouseleave="hideChartTooltip">

                        <!-- Background Column -->
                        <div class="column-background"></div>

                        <!-- Main Data Column -->
                        <div class="column-bar-advanced">
                          <div class="column-fill-advanced" :style="{
                            height: getChartHeight(month) + '%',
                            background: getAdvancedGradient(month, index),
                            '--fill-height': getChartHeight(month) + '%'
                          }">
                            <!-- Animated Fill Effect -->
                            <div class="fill-animation"></div>
                            <!-- Glow Effect -->
                            <div class="column-glow"></div>
                            <!-- Data Point -->
                            <div class="data-point">
                              <div class="point-pulse"></div>
                            </div>
                          </div>
                        </div>

                        <!-- Target Line -->
                        <div class="target-line" :style="{ bottom: '75%' }"></div>

                        <!-- Column Labels -->
                        <div class="column-label-advanced">{{ getChartLabel(month) }}</div>
                        <div class="column-value-advanced">
                          <span class="value-number">{{ getChartValue(month) }}</span>
                          <span class="value-unit">{{ authStore.isAdmin ? 'users' : 'days' }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Chart Overlay Effects -->
                    <div class="chart-overlay">
                      <div class="gradient-overlay"></div>
                      <div class="particle-effect">
                        <div v-for="i in 20" :key="i" class="particle" :style="{ '--delay': i * 0.1 + 's' }"></div>
                      </div>
                    </div>
                  </div>

                  <!-- Chart Footer with Insights -->
                  <div class="chart-footer-advanced">
                    <div class="insight-cards">
                      <div class="insight-card">
                        <div class="insight-icon">📈</div>
                        <div class="insight-content">
                          <span class="insight-title">Growth Rate</span>
                          <span class="insight-value">+12.5%</span>
                        </div>
                      </div>
                      <div class="insight-card">
                        <div class="insight-icon">🎯</div>
                        <div class="insight-content">
                          <span class="insight-title">Goal Achievement</span>
                          <span class="insight-value">87%</span>
                        </div>
                      </div>
                      <div class="insight-card">
                        <div class="insight-icon">⚡</div>
                        <div class="insight-content">
                          <span class="insight-title">Performance</span>
                          <span class="insight-value">Excellent</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Empty State -->
                <div v-else class="empty-chart-advanced">
                  <div class="empty-illustration-advanced">
                    <div class="empty-icon-container">
                      <div class="icon-background"></div>
                      <div class="empty-icon-animated">📊</div>
                      <div class="icon-particles">
                        <div v-for="i in 8" :key="i" class="icon-particle" :style="{ '--delay': i * 0.2 + 's' }"></div>
                      </div>
                    </div>
                    <h4 class="empty-title">No Analytics Data Available</h4>
                    <p class="empty-description">
                      {{ authStore.isAdmin ? 'System analytics will appear here once data is collected' : 'Start attending classes to see your personalized analytics dashboard' }}
                    </p>
                    <button class="empty-action-btn-advanced" @click="refreshAnalytics">
                      <i class="btn-icon">🔄</i>
                      <span>Refresh Data</span>
                      <div class="btn-shine"></div>
                    </button>
                  </div>
                </div>
              </div>
          </div>

          <!-- Weekly Attendance Pattern Panel -->
          <section class="weekly-attendance-panel">
            <!-- Panel Header -->
            <header class="panel-header-modern">
              <div class="header-content">
                <div class="title-section">
                  <div class="title-icon-wrapper">
                    <div class="icon-glow-effect"></div>
                    <i class="title-icon">🗓️</i>
                  </div>
                  <div class="title-text">
                    <h3 class="panel-title">Weekly Attendance Pattern</h3>
                    <p class="panel-subtitle">Track your weekly attendance trends</p>
                  </div>
                </div>

                <div class="header-controls">
                  <div class="control-group">
                    <button class="control-btn-modern" @click="toggleWeeklyView">
                      <span>{{ weeklyViewMode }}</span>
                      <div class="btn-ripple"></div>
                    </button>
                    <button class="control-btn-modern secondary" @click="refreshAnalytics">
                      <i class="btn-icon">🔄</i>
                      <span>Refresh</span>
                    </button>
                  </div>
                </div>
              </div>
            </header>

            <!-- Panel Content -->
            <div class="panel-content">
              <!-- Weekly Pattern Carousel -->
              <div v-if="weeklyPattern.length > 0" class="weekly-carousel-container">
                <!-- Carousel Navigation -->
                <div class="carousel-navigation">
                  <button class="nav-btn nav-prev" @click="slideWeeklyCards('prev')"
                    :disabled="currentSlideIndex === 0">
                    <i class="nav-icon">‹</i>
                  </button>

                  <div class="slide-indicators">
                    <div v-for="(indicator, index) in slideIndicators" :key="index" class="slide-indicator"
                      :class="{ active: index === currentSlideIndex }" @click="goToSlide(index)"></div>
                  </div>

                  <button class="nav-btn nav-next" @click="slideWeeklyCards('next')"
                    :disabled="currentSlideIndex >= slideIndicators.length - 1">
                    <i class="nav-icon">›</i>
                  </button>
                </div>

                <!-- Carousel Wrapper -->
                <div class="carousel-wrapper" ref="carouselWrapper" @touchstart="handleTouchStart"
                  @touchend="handleTouchEnd">
                  <div class="weekly-carousel-track"
                    :style="{ transform: `translateX(-${currentSlideIndex * slideWidth}%)` }" ref="carouselTrack">
                    <div v-for="(day, index) in weeklyPattern" :key="day.name || day.day"
                      class="day-card carousel-slide" :style="{ animationDelay: (index * 0.1) + 's' }">
                      <!-- Day Header -->
                      <div class="day-header">
                        <div class="day-info">
                          <h4 class="day-name">{{ getDayName(day) }}</h4>
                          <div class="day-badge" :class="getProgressClass(getDayPercentage(day))">
                            {{ getDayPercentage(day) }}%
                          </div>
                        </div>
                        <div class="day-trend" :class="getDayPercentage(day) > 50 ? 'positive' : 'negative'">
                          {{ getDayPercentage(day) > 50 ? '↗' : '↘' }}
                        </div>
                      </div>

                      <!-- Progress Section -->
                      <div class="progress-section">
                        <div class="progress-bar-container">
                          <div class="progress-bar-track">
                            <div class="progress-bar-fill" :style="{
                              width: getDayPercentage(day) + '%',
                              background: getProgressGradient(getDayPercentage(day))
                            }">
                              <div class="progress-glow"></div>
                              <div class="progress-shine"></div>
                            </div>
                          </div>
                        </div>

                        <div class="progress-stats">
                          <div class="stat-item">
                            <span class="stat-value">{{ getDayCount(day) }}</span>
                            <span class="stat-label">days</span>
                          </div>
                        </div>
                      </div>

                      <!-- Day Details -->
                      <div class="day-details">
                        <div class="detail-row">
                          <span class="detail-label">Avg Time</span>
                          <span class="detail-value">{{ day.avgTime || '2h 15m' }}</span>
                        </div>
                        <div class="detail-row">
                          <span class="detail-label">Status</span>
                          <span class="detail-value status" :class="getProgressClass(getDayPercentage(day))">
                            {{ getDayPercentage(day) > 75 ? 'Excellent' : getDayPercentage(day) > 50 ? 'Good' : 'Needs Improvement' }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Carousel Info -->
                <div class="carousel-info">
                  <span class="slide-counter">
                    {{ currentSlideIndex + 1 }} / {{ slideIndicators.length }}
                  </span>
                  <div class="carousel-controls">
                    <button class="control-btn-mini" @click="toggleAutoSlide">
                      <i class="control-icon">{{ autoSlideEnabled ? '⏸️' : '▶️' }}</i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Empty State -->
              <div v-else class="empty-state">
                <div class="empty-illustration">
                  <div class="empty-icon-container">
                    <div class="empty-icon-bg"></div>
                    <div class="empty-icon">🗓️</div>
                    <div class="icon-particles">
                      <div v-for="i in 6" :key="i" class="particle" :style="{ '--delay': i * 0.2 + 's' }"></div>
                    </div>
                  </div>
                  <div class="empty-content">
                    <h4 class="empty-title">No Weekly Data Available</h4>
                    <p class="empty-description">Weekly attendance patterns will appear here once data is collected
                    </p>
                    <button class="empty-action-btn" @click="refreshAnalytics">
                      <i class="btn-icon">🔄</i>
                      <span>Refresh Data</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Performance Insights Panel -->
          <div class="insights-panel">
            <div class="panel-header">
              <h3 class="panel-title">
                <i class="title-icon">💡</i>
                Performance Insights
              </h3>
            </div>

            <div class="insights-container">
              <div v-if="performanceInsights" class="insights-grid">
                <div class="insight-card">
                  <div class="insight-icon">🎯</div>
                  <div class="insight-content">
                    <h4>Attendance Goal</h4>
                    <p>{{ performanceInsights.goal || 'Maintain consistent attendance' }}</p>
                  </div>
                </div>
                <div class="insight-card">
                  <div class="insight-icon">📈</div>
                  <div class="insight-content">
                    <h4>Trend Analysis</h4>
                    <p>{{ performanceInsights.trend || 'Your attendance is improving' }}</p>
                  </div>
                </div>
                <div class="insight-card">
                  <div class="insight-icon">🏆</div>
                  <div class="insight-content">
                    <h4>Achievement</h4>
                    <p>{{ performanceInsights.achievement || 'Keep up the great work!' }}</p>
                  </div>
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
      </main>
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

              <button v-if="notice.content.length > 150" @click="toggleNoticeExpansion(notice)" class="read-more-btn">
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
                    <input v-model="classConfig.section" type="text" class="field-input" placeholder="e.g., A, B, C" />
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
                      <input v-model="timeSettings.gracePeriod" type="number" min="0" max="30" class="field-input" />
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
  </div>

  <!-- Chart Filter Modal -->
  <div v-if="showFilterModal" class="modal-overlay" @click="showFilterModal = false">
    <div class="filter-modal" @click.stop>
      <div class="modal-header">
        <h3 class="modal-title">
          <i class="modal-icon">🔍</i>
          Chart Filters
        </h3>
        <button class="modal-close" @click="showFilterModal = false">✕</button>
      </div>

      <div class="modal-content">
        <div class="filter-section">
          <label class="filter-label">Date Range</label>
          <select v-model="chartFilters.dateRange" class="filter-select">
            <option value="all">All Time</option>
            <option value="last3months">Last 3 Months</option>
            <option value="last6months">Last 6 Months</option>
            <option value="thisyear">This Year</option>
          </select>
        </div>

        <div class="filter-section">
          <label class="filter-label">Minimum Attendance (%)</label>
          <div class="range-container">
            <input type="range" v-model="chartFilters.attendanceThreshold" min="0" max="100" step="5"
              class="filter-range">
            <span class="range-value">{{ chartFilters.attendanceThreshold }}%</span>
          </div>
        </div>

        <div class="filter-section">
          <label class="filter-label">Sort By</label>
          <select v-model="chartFilters.sortBy" class="filter-select">
            <option value="date">Date</option>
            <option value="attendance">Attendance Rate</option>
            <option value="alphabetical">Alphabetical</option>
          </select>
        </div>

        <div class="filter-section">
          <label class="filter-label">Sort Order</label>
          <div class="radio-group">
            <label class="radio-option">
              <input type="radio" v-model="chartFilters.sortOrder" value="asc">
              <span class="radio-text">Ascending</span>
            </label>
            <label class="radio-option">
              <input type="radio" v-model="chartFilters.sortOrder" value="desc">
              <span class="radio-text">Descending</span>
            </label>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="modal-btn secondary" @click="resetChartFilters">
          <i class="btn-icon">🔄</i>
          Reset
        </button>
        <button class="modal-btn primary" @click="applyChartFilters">
          <i class="btn-icon">✓</i>
          Apply Filters
        </button>
      </div>
    </div>
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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
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

interface WeeklyPatternDay {
  name?: string
  day?: string
  count?: number
  average?: number
  percentage?: number
}

// Store initialization
const router = useRouter()
const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

// Reactive state
const activeTab = ref<string>('analytics')
const isLoading = ref<boolean>(false)
const analyticsLoading = ref<boolean>(false)
const noticesLoading = ref<boolean>(false)
const managementLoading = ref<boolean>(false)
const showCameraModal = ref<boolean>(false)
const showUserRegistrationModal = ref<boolean>(false)
const loadingUsers = ref<boolean>(false)
const users = ref<User[]>([])
const userToCapture = ref<User | null>(null)
const notices = ref<Notice[]>([])
const attendanceData = ref<AttendanceRecord[]>([])

// Enhanced analytics features
const weeklyViewMode = ref<string>('Percentage')
const performanceInsights = ref<any>(null)

// Carousel functionality
const currentSlideIndex = ref<number>(0)
const slideWidth = ref<number>(100)
const autoSlideEnabled = ref<boolean>(false)
const autoSlideInterval = ref<NodeJS.Timeout | null>(null)
const carouselWrapper = ref<HTMLElement | null>(null)
const carouselTrack = ref<HTMLElement | null>(null)

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
const analytics = ref<any>(null)

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

const getHeatmapProgressClass = (percentage: number) => {
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

// Advanced Chart Methods
const calculateAverageRate = () => {
  if (attendanceChart.value.length === 0) return 0
  const total = attendanceChart.value.reduce((sum, month) => sum + getChartHeight(month), 0)
  return Math.round(total / attendanceChart.value.length)
}

const getPeakMonth = () => {
  if (attendanceChart.value.length === 0) return 'N/A'
  const peak = attendanceChart.value.reduce((max, month) =>
    getChartHeight(month) > getChartHeight(max) ? month : max
  )
  return getChartLabel(peak)
}

const getAdvancedGradient = (month: any, index: number) => {
  const percentage = getChartHeight(month)
  const hue = 180 + (percentage * 1.8) // Blue to green spectrum
  const saturation = 70 + (percentage * 0.3)
  const lightness = 45 + (percentage * 0.2)

  return `linear-gradient(135deg, 
    hsl(${hue}, ${saturation}%, ${lightness}%) 0%,
    hsl(${hue + 20}, ${saturation + 10}%, ${lightness + 10}%) 50%,
    hsl(${hue + 40}, ${saturation + 20}%, ${lightness + 20}%) 100%)`
}

// Enhanced Chart Tooltip
const showAdvancedTooltip = (data: any, event: MouseEvent, index: number) => {
  const percentage = getChartHeight(data)
  const value = getChartValue(data)
  const label = getChartLabel(data)

  chartTooltip.value = {
    show: true,
    title: `${label} Analytics`,
    value: `${value} ${authStore.isAdmin ? 'attendances' : 'days'} (${Math.round(percentage)}%)`,
    style: {
      left: event.clientX + 15 + 'px',
      top: event.clientY - 15 + 'px'
    }
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

// Enhanced Analytics Methods
const refreshAnalytics = async () => {
  analyticsLoading.value = true
  try {
    if (authStore.isAdmin) {
      const analyticsResponse = await adminAPI.getAnalytics()
      if (analyticsResponse.data) {
        attendanceChart.value = analyticsResponse.data.monthly_trend || []
        weeklyPattern.value = analyticsResponse.data.weekly_pattern || []
        recentActivity.value = analyticsResponse.data.recent_system_activity || []
      }
    } else {
      const analyticsResponse = await userAPI.getUserAnalytics()
      if (analyticsResponse.data) {
        attendanceChart.value = analyticsResponse.data.monthly_trend || []
        weeklyPattern.value = analyticsResponse.data.day_frequency || []
        recentActivity.value = analyticsResponse.data.recent_attendance || []
        performanceInsights.value = analyticsResponse.data.performance_insights || null
      }
    }
  } catch (error) {
    console.error('Error refreshing analytics:', error)
  } finally {
    analyticsLoading.value = false
  }
}

// Chart filtering state
const showFilterModal = ref<boolean>(false)
const chartFilters = ref({
  dateRange: 'all', // 'all', 'last3months', 'last6months', 'thisyear'
  attendanceThreshold: 0, // minimum attendance percentage
  sortBy: 'date', // 'date', 'attendance', 'alphabetical'
  sortOrder: 'asc' // 'asc', 'desc'
})

const filteredChartData = computed(() => {
  let data = [...attendanceChart.value]

  // Apply date range filter
  if (chartFilters.value.dateRange !== 'all') {
    const now = new Date()
    let cutoffDate = new Date()

    switch (chartFilters.value.dateRange) {
      case 'last3months':
        cutoffDate.setMonth(now.getMonth() - 3)
        break
      case 'last6months':
        cutoffDate.setMonth(now.getMonth() - 6)
        break
      case 'thisyear':
        cutoffDate = new Date(now.getFullYear(), 0, 1)
        break
    }

    data = data.filter(item => {
      const itemDate = new Date(item.month || item.date || '2024-01-01')
      return itemDate >= cutoffDate
    })
  }

  // Apply attendance threshold filter
  if (chartFilters.value.attendanceThreshold > 0) {
    data = data.filter(item => {
      const percentage = getChartHeight(item)
      return percentage >= chartFilters.value.attendanceThreshold
    })
  }

  // Apply sorting
  data.sort((a, b) => {
    let aValue, bValue

    switch (chartFilters.value.sortBy) {
      case 'attendance':
        aValue = getChartHeight(a)
        bValue = getChartHeight(b)
        break
      case 'alphabetical':
        aValue = getChartLabel(a)
        bValue = getChartLabel(b)
        break
      case 'date':
      default:
        aValue = new Date(a.month || a.date || '2024-01-01').getTime()
        bValue = new Date(b.month || b.date || '2024-01-01').getTime()
        break
    }

    if (chartFilters.value.sortOrder === 'desc') {
      return aValue < bValue ? 1 : -1
    }
    return aValue > bValue ? 1 : -1
  })

  return data
})

const filterChart = () => {
  showFilterModal.value = true
}

const applyChartFilters = () => {
  // The computed property will automatically update the chart
  showFilterModal.value = false
}

const resetChartFilters = () => {
  chartFilters.value = {
    dateRange: 'all',
    attendanceThreshold: 0,
    sortBy: 'date',
    sortOrder: 'asc'
  }
}

const exportChart = () => {
  // Implement chart export logic
  console.log('Export chart functionality')
}

const toggleWeeklyView = () => {
  weeklyViewMode.value = weeklyViewMode.value === 'Percentage' ? 'Count' : 'Percentage'
}

// Carousel functionality
const slideIndicators = computed(() => {
  if (!weeklyPattern.value.length) return []
  const cardsPerSlide = getCardsPerSlide()
  return Array.from({ length: Math.ceil(weeklyPattern.value.length / cardsPerSlide) }, (_, i) => i)
})

const getCardsPerSlide = () => {
  if (typeof window === 'undefined') return 3
  const width = window.innerWidth
  if (width < 480) return 1
  if (width < 768) return 2
  if (width < 1024) return 2
  return 3
}

const slideWeeklyCards = (direction: 'prev' | 'next') => {
  const maxIndex = slideIndicators.value.length - 1

  if (direction === 'next' && currentSlideIndex.value < maxIndex) {
    currentSlideIndex.value++
  } else if (direction === 'prev' && currentSlideIndex.value > 0) {
    currentSlideIndex.value--
  }

  updateSlideWidth()
}

const goToSlide = (index: number) => {
  currentSlideIndex.value = index
  updateSlideWidth()
}

const updateSlideWidth = () => {
  const cardsPerSlide = getCardsPerSlide()
  slideWidth.value = 100 / cardsPerSlide
}

const toggleAutoSlide = () => {
  autoSlideEnabled.value = !autoSlideEnabled.value

  if (autoSlideEnabled.value) {
    startAutoSlide()
  } else {
    stopAutoSlide()
  }
}

const startAutoSlide = () => {
  if (autoSlideInterval.value) clearInterval(autoSlideInterval.value)

  autoSlideInterval.value = setInterval(() => {
    const maxIndex = slideIndicators.value.length - 1
    if (currentSlideIndex.value >= maxIndex) {
      currentSlideIndex.value = 0
    } else {
      currentSlideIndex.value++
    }
    updateSlideWidth()
  }, 4000)
}

const stopAutoSlide = () => {
  if (autoSlideInterval.value) {
    clearInterval(autoSlideInterval.value)
    autoSlideInterval.value = null
  }
}

// Handle window resize for responsive carousel
const handleCarouselResize = () => {
  updateSlideWidth()
  // Reset to first slide if current slide is out of bounds
  const maxIndex = slideIndicators.value.length - 1
  if (currentSlideIndex.value > maxIndex) {
    currentSlideIndex.value = 0
  }
}

// Touch/Swipe functionality for mobile
let touchStartX = 0
let touchEndX = 0

const handleTouchStart = (e: TouchEvent) => {
  touchStartX = e.changedTouches[0].screenX
}

const handleTouchEnd = (e: TouchEvent) => {
  touchEndX = e.changedTouches[0].screenX
  handleSwipeGesture()
}

const handleSwipeGesture = () => {
  const swipeThreshold = 50
  const swipeDistance = touchStartX - touchEndX

  if (Math.abs(swipeDistance) > swipeThreshold) {
    if (swipeDistance > 0) {
      // Swipe left - next slide
      slideWeeklyCards('next')
    } else {
      // Swipe right - previous slide
      slideWeeklyCards('prev')
    }
  }
}

// Chart helper methods
const getChartHeight = (month: any) => {
  if (authStore.isAdmin) {
    // For admin, use attendance numbers and scale them properly
    const maxAttendance = Math.max(...attendanceChart.value.map(m => m.attendance || m.students || 0))
    const currentValue = month.attendance || month.students || 0
    return maxAttendance > 0 ? Math.min((currentValue / maxAttendance) * 100, 100) : 0
  } else {
    // For users, treat attendance as days and scale to percentage
    const maxDays = 31 // Maximum days in a month
    const currentDays = month.attendance || month.days || 0
    return Math.min((currentDays / maxDays) * 100, 100)
  }
}

const getChartGradient = (month: any) => {
  const percentage = getChartHeight(month)
  if (percentage >= 80) return 'linear-gradient(135deg, #22c55e, #16a34a)'
  if (percentage >= 60) return 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
  if (percentage >= 40) return 'linear-gradient(135deg, #f59e0b, #d97706)'
  return 'linear-gradient(135deg, #ef4444, #dc2626)'
}

const getChartLabel = (month: any) => {
  if (month.month) {
    // Handle full month names like "Aug 2024"
    const parts = month.month.split(' ')
    return parts[0] // Return just "Aug"
  }
  return month.name || 'N/A'
}

const getChartValue = (month: any) => {
  if (authStore.isAdmin) {
    return month.attendance || month.students || 0
  } else {
    return month.attendance || month.days || 0
  }
}

// Weekly pattern helper methods
const getDayName = (day: any) => {
  return day.day || day.name || 'Unknown'
}

const getDayPercentage = (day: any) => {
  if (weeklyViewMode.value === 'Count') {
    return Math.min((day.count || day.average || 0) * 10, 100)
  }
  return day.percentage || ((day.count || day.average || 0) / 5) * 100
}

const getDayCount = (day: any) => {
  return day.count || day.average || 0
}

const getProgressGradient = (percentage: number) => {
  if (percentage >= 80) return 'linear-gradient(90deg, #22c55e, #16a34a)'
  if (percentage >= 60) return 'linear-gradient(90deg, #3b82f6, #1d4ed8)'
  if (percentage >= 40) return 'linear-gradient(90deg, #f59e0b, #d97706)'
  return 'linear-gradient(90deg, #ef4444, #dc2626)'
}

const getProgressClass = (percentage: number) => {
  if (percentage >= 80) return 'excellent'
  if (percentage >= 60) return 'good'
  if (percentage >= 40) return 'average'
  return 'poor'
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
      const analyticsResponse = await userAPI.getUserAnalytics()
      if (analyticsResponse.data?.recent_attendance) {
        recentActivity.value = analyticsResponse.data.recent_attendance.map(item => ({
          ...item,
          status: 'present',
          user_name: authStore.user?.name || 'You'
        }))
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

  // Initialize carousel
  updateSlideWidth()

  // Add window resize listener for responsive carousel
  window.addEventListener('resize', handleCarouselResize)
})

// Cleanup on unmount
onUnmounted(() => {
  // Remove window resize listener
  window.removeEventListener('resize', handleCarouselResize)

  // Stop auto slide if running
  stopAutoSlide()
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

/* Advanced Chart Panel Styles */
.advanced-chart-panel {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.advanced-chart-panel:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
  border-color: rgba(78, 205, 196, 0.3);
}

.panel-header-advanced {
  justify-content: space-between;
  align-items: flex-start;
  padding: 2.5rem 3rem 1.5rem;
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.05), rgba(69, 183, 209, 0.05));
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
}

.panel-header-advanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 400% 100%;
  animation: gradientFlow 4s ease-in-out infinite;
}

.header-left {
  flex: 1;
}

.title-icon-container {
  position: relative;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-glow-effect {
  position: absolute;
  width: 60px;
  height: 60px;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s infinite;
}

.panel-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
}

.panel-controls-advanced {
  display: flex;
  align-items: center;
}

.control-group {
  display: flex;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.5rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.control-btn-modern {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.control-btn-modern.primary {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  border: none;
  color: white;
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
}

.control-btn-modern:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.control-btn-modern.primary:hover {
  box-shadow: 0 8px 30px rgba(78, 205, 196, 0.5);
}

.btn-ripple {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: all 0.5s ease;
}

.control-btn-modern:active .btn-ripple {
  width: 100%;
  height: 100%;
}

/* Chart Area Advanced */
.chart-area-advanced {
  padding: 0;
  min-height: 500px;
}

.sophisticated-chart {
  padding: 2rem 3rem 3rem;
}

.chart-header-advanced {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  gap: 2rem;
}

.chart-title-section {
  flex: 1;
}

.chart-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.chart-metrics {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.metric-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metric-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
}

.metric-value.trend-up {
  color: #22c55e;
}

.chart-legend-advanced {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.legend-item-advanced {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.legend-indicator {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  position: relative;
}

.legend-indicator.primary-gradient {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
}

.legend-indicator.secondary-gradient {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

/* Advanced Chart Container */
.chart-container-advanced {
  position: relative;
  height: 350px;
  margin: 2rem 0;
  display: flex;
  align-items: end;
  gap: 1rem;
}

.chart-y-axis-advanced {
  display: flex;
  flex-direction: column-reverse;
  justify-content: space-between;
  height: 100%;
  width: 60px;
  position: relative;
}

.y-label-advanced {
  display: flex;
  align-items: center;
  position: relative;
  height: 20%;
}

.label-text {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  width: 50px;
  text-align: right;
}

.grid-line {
  position: absolute;
  left: 55px;
  right: -2000px;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  pointer-events: none;
}

.chart-bars-advanced {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: end;
  gap: 1rem;
  position: relative;
  z-index: 2;
}

.chart-column-advanced {
  flex: 1;
  height: 100%;
  position: relative;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: columnRise 1s ease var(--delay);
}

@keyframes columnRise {
  from {
    transform: translateY(100%) scaleY(0);
    opacity: 0;
  }

  to {
    transform: translateY(0) scaleY(1);
    opacity: 1;
  }
}

.chart-column-advanced:hover {
  transform: translateY(-8px) scale(1.05);
  z-index: 10;
}

.column-background {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.column-bar-advanced {
  position: relative;
  height: 100%;
  display: flex;
  align-items: end;
}

.column-fill-advanced {
  width: 100%;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  animation: fillUp 1.5s ease var(--delay);
}

@keyframes fillUp {
  from {
    height: 0% !important;
  }

  to {
    height: var(--fill-height);
  }
}

.fill-animation {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }

  100% {
    left: 100%;
  }
}

.column-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: inherit;
  border-radius: 14px;
  filter: blur(8px);
  opacity: 0.5;
  z-index: -1;
}

.data-point {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 16px;
  background: white;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.point-pulse {
  width: 8px;
  height: 8px;
  background: #4ecdc4;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.target-line {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  border-radius: 1px;
  opacity: 0.7;
  z-index: 1;
}

.target-line::before {
  content: 'Target';
  position: absolute;
  right: 0;
  top: -20px;
  font-size: 0.7rem;
  color: #f59e0b;
  font-weight: 600;
}

.column-label-advanced {
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
  white-space: nowrap;
}

.column-value-advanced {
  position: absolute;
  bottom: -55px;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.value-number {
  font-size: 1rem;
  font-weight: 800;
  color: white;
}

.value-unit {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Chart Overlay Effects */
.chart-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.gradient-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to top, rgba(78, 205, 196, 0.05), transparent);
  border-radius: 0 0 12px 12px;
}

.particle-effect {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: rgba(78, 205, 196, 0.6);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite var(--delay);
}

.particle:nth-child(odd) {
  background: rgba(69, 183, 209, 0.6);
}

@keyframes float {

  0%,
  100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 0;
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  50% {
    transform: translateY(-100px) translateX(20px) scale(1.2);
    opacity: 0.8;
  }
}

/* Chart Footer */
.chart-footer-advanced {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.insight-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.insight-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.insight-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.1), transparent);
  transition: left 0.5s ease;
}

.insight-card:hover::before {
  left: 100%;
}

.insight-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.3);
  transform: translateY(-2px);
}

.insight-icon {
  font-size: 1.5rem;
  background: rgba(78, 205, 196, 0.15);
  padding: 0.75rem;
  border-radius: 12px;
  border: 1px solid rgba(78, 205, 196, 0.3);
}

.insight-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.insight-title {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.insight-value {
  font-size: 1.25rem;
  font-weight: 800;
  color: white;
}

/* Enhanced Empty State */
.empty-chart-advanced {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 3rem;
}

.empty-illustration-advanced {
  text-align: center;
  max-width: 400px;
}

.empty-icon-container {
  position: relative;
  margin-bottom: 2rem;
  display: inline-block;
}

.icon-background {
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

.empty-icon-animated {
  font-size: 4rem;
  color: rgba(255, 255, 255, 0.4);
  position: relative;
  z-index: 2;
  animation: bounce 2s infinite;
}

@keyframes bounce {

  0%,
  20%,
  50%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-10px);
  }

  60% {
    transform: translateY(-5px);
  }
}

.icon-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.icon-particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(78, 205, 196, 0.6);
  border-radius: 50%;
  animation: particleFloat 4s ease-in-out infinite var(--delay);
}

@keyframes particleFloat {

  0%,
  100% {
    transform: translate(0, 0) scale(1);
    opacity: 0;
  }

  50% {
    transform: translate(var(--x, 30px), var(--y, -30px)) scale(1.5);
    opacity: 1;
  }
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.empty-description {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 2rem;
}

.empty-action-btn-advanced {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 16px;
  cursor: pointer;
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.3);
}

.btn-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.empty-action-btn-advanced:hover .btn-shine {
  left: 100%;
}

.empty-action-btn-advanced:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(78, 205, 196, 0.4);
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

/* Weekly Attendance Pattern Panel */
.weekly-attendance-panel {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.weekly-attendance-panel:hover {
  transform: translateY(-5px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
  border-color: rgba(78, 205, 196, 0.3);
}

/* Panel Header Modern */
.panel-header-modern {
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.05), rgba(69, 183, 209, 0.05));
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  position: relative;
  padding: 2.5rem 3rem 2rem;
}

.panel-header-modern::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 400% 100%;
  animation: gradientFlow 4s ease-in-out infinite;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.title-icon-wrapper {
  position: relative;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title-icon-wrapper .title-icon {
  font-size: 2rem;
  z-index: 2;
  position: relative;
}

.title-text {
  flex: 1;
}

.panel-title {
  font-size: 1.75rem;
  font-weight: 800;
  color: white;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.panel-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  margin: 0;
  font-weight: 500;
}

.header-controls {
  display: flex;
  align-items: center;
}

.control-btn-modern.secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.control-btn-modern.secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Panel Content */
.panel-content {
  padding: 2.5rem 3rem 3rem;
}

/* Weekly Carousel Container */
.weekly-carousel-container {
  position: relative;
  overflow: hidden;
}

/* Carousel Navigation */
.carousel-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 0 1rem;
}

.nav-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 1.5rem;
  font-weight: bold;
  position: relative;
  overflow: hidden;
}

.nav-btn:hover:not(:disabled) {
  background: rgba(78, 205, 196, 0.2);
  border-color: rgba(78, 205, 196, 0.4);
  transform: scale(1.1);
  box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  transform: none;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.nav-btn:hover:not(:disabled)::before {
  left: 100%;
}

.nav-icon {
  z-index: 2;
  position: relative;
}

/* Slide Indicators */
.slide-indicators {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.slide-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.slide-indicator.active {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  transform: scale(1.3);
  box-shadow: 0 4px 12px rgba(78, 205, 196, 0.4);
}

.slide-indicator:hover:not(.active) {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

/* Carousel Wrapper */
.carousel-wrapper {
  overflow: hidden;
  border-radius: 20px;
  position: relative;
}

.weekly-carousel-track {
  display: flex;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 1.5rem;
}

/* Carousel Slide */
.carousel-slide {
  flex: 0 0 auto;
  width: calc(33.333% - 1rem);
  min-width: 320px;
}

/* Carousel Info */
.carousel-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.slide-counter {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
}

.carousel-controls {
  display: flex;
  gap: 0.5rem;
}

.control-btn-mini {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.control-btn-mini:hover {
  background: rgba(78, 205, 196, 0.2);
  border-color: rgba(78, 205, 196, 0.4);
  transform: scale(1.1);
}

.control-icon {
  font-size: 0.9rem;
}

/* Day Card */
.day-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideInUp 0.6s ease var(--delay);
  cursor: pointer;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.day-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.1), transparent);
  transition: left 0.5s ease;
}

.day-card:hover::before {
  left: 100%;
}

.day-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.3);
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

/* Day Header */
.day-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.day-info {
  flex: 1;
}

.day-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
}

.day-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  border: 1px solid;
}

.day-badge.high {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.3);
}

.day-badge.medium {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.3);
}

.day-badge.low {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.3);
}

.day-trend {
  font-size: 1.5rem;
  font-weight: bold;
  padding: 0.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.day-trend.positive {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.2);
}

.day-trend.negative {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

/* Progress Section */
.progress-section {
  margin-bottom: 1.5rem;
}

.progress-bar-container {
  margin-bottom: 1rem;
}

.progress-bar-track {
  height: 12px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.progress-bar-fill {
  height: 100%;
  border-radius: 6px;
  position: relative;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.progress-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: inherit;
  border-radius: 8px;
  filter: blur(4px);
  opacity: 0.6;
  z-index: -1;
}

.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: shine 2s infinite;
}

@keyframes shine {
  0% {
    left: -100%;
  }

  100% {
    left: 100%;
  }
}

.progress-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: white;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

/* Day Details */
.day-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.detail-value {
  font-size: 0.875rem;
  color: white;
  font-weight: 600;
}

.detail-value.status {
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value.status.high {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.detail-value.status.medium {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.detail-value.status.low {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

/* Empty State */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.empty-illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.empty-icon-container {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon-bg {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 3s infinite;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.7;
  z-index: 2;
}

.icon-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(78, 205, 196, 0.6);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite var(--delay);
}

.particle:nth-child(odd) {
  background: rgba(69, 183, 209, 0.6);
}

.empty-content {
  max-width: 300px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
}

.empty-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  line-height: 1.5;
  margin: 0 0 2rem 0;
}

.empty-action-btn {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.empty-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(78, 205, 196, 0.4);
}

.empty-action-btn .btn-icon {
  font-size: 1rem;
}

/* Responsive Design for Carousel */
@media (max-width: 1024px) {
  .carousel-slide {
    width: calc(50% - 0.75rem);
    min-width: 280px;
  }

  .panel-content {
    padding: 2rem;
  }

  .panel-header-modern {
    padding: 2rem;
  }

  .carousel-navigation {
    padding: 0 0.5rem;
  }

  .nav-btn {
    width: 45px;
    height: 45px;
    font-size: 1.3rem;
  }
}

@media (max-width: 768px) {
  .carousel-slide {
    width: calc(100% - 1rem);
    min-width: 250px;
  }

  .header-content {
    flex-direction: column;
    gap: 1.5rem;
  }

  .title-section {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .panel-content {
    padding: 1.5rem;
  }

  .panel-header-modern {
    padding: 1.5rem;
  }

  .day-card {
    padding: 1.5rem;
  }

  .carousel-navigation {
    margin-bottom: 1.5rem;
    padding: 0;
  }

  .nav-btn {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .slide-indicators {
    gap: 0.5rem;
  }

  .slide-indicator {
    width: 10px;
    height: 10px;
  }

  .carousel-info {
    margin-top: 1.5rem;
    padding: 0.75rem 1rem;
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .carousel-slide {
    width: 100%;
    min-width: 200px;
  }

  .panel-content {
    padding: 1rem;
  }

  .panel-header-modern {
    padding: 1rem;
  }

  .day-card {
    padding: 1rem;
  }

  .panel-title {
    font-size: 1.5rem;
  }

  .control-group {
    flex-direction: column;
    gap: 0.5rem;
  }

  .control-btn-modern {
    width: 100%;
    justify-content: center;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }

  .carousel-navigation {
    margin-bottom: 1rem;
  }

  .nav-btn {
    width: 35px;
    height: 35px;
    font-size: 1rem;
  }

  .slide-indicators {
    gap: 0.4rem;
  }

  .slide-indicator {
    width: 8px;
    height: 8px;
  }

  .carousel-info {
    margin-top: 1rem;
    padding: 0.5rem;
  }

  .slide-counter {
    font-size: 0.8rem;
  }

  .control-btn-mini {
    width: 35px;
    height: 35px;
    font-size: 0.8rem;
  }

  .day-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .day-info {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .day-trend {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .progress-stats {
    justify-content: center;
  }
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

/* Chart Filter Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.filter-modal {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 0;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow: hidden;
  animation: slideInUp 0.4s ease;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.02);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.modal-icon {
  font-size: 1.5rem;
}

.modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transform: rotate(90deg);
}

.modal-content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.filter-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
}

.filter-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  outline: none;
}

.filter-select:focus {
  border-color: #4ecdc4;
  box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.2);
}

.filter-select option {
  background: #1a1a1a;
  color: white;
}

.range-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.filter-range {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
}

.filter-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
  transition: all 0.3s ease;
}

.filter-range::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(78, 205, 196, 0.5);
}

.filter-range::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
}

.range-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4ecdc4;
  min-width: 50px;
  text-align: center;
  background: rgba(78, 205, 196, 0.1);
  padding: 0.25rem 0.75rem;
  border-radius: 8px;
}

.radio-group {
  display: flex;
  gap: 1rem;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.radio-option:hover {
  background: rgba(255, 255, 255, 0.05);
}

.radio-option input[type="radio"] {
  width: 18px;
  height: 18px;
  accent-color: #4ecdc4;
}

.radio-text {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.9);
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.02);
}

.modal-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.modal-btn.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.modal-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-1px);
}

.modal-btn.primary {
  background: linear-gradient(135deg, #4ecdc4, #45b7d1);
  color: white;
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
}

.modal-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
}

.modal-btn .btn-icon {
  font-size: 1rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive adjustments for filter modal */
@media (max-width: 768px) {
  .filter-modal {
    width: 95%;
    margin: 1rem;
  }

  .modal-header,
  .modal-content,
  .modal-footer {
    padding: 1rem 1.5rem;
  }

  .radio-group {
    flex-direction: column;
    gap: 0.5rem;
  }

  .modal-footer {
    flex-direction: column;
  }
}

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
@media (-webkit-min-device-pixel-ratio: 2),
(min-resolution: 192dpi) {
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
</style>
