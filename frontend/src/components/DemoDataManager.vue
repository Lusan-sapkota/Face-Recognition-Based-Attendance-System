<template>
    <div class="demo-data-manager">
        <div class="demo-header">
            <h2 class="demo-title">
                <i class="demo-icon">🎯</i>
                Demo Data Manager
            </h2>
            <p class="demo-description">
                Populate the system with realistic demo data for testing and demonstration purposes
            </p>
        </div>

        <div class="demo-stats" v-if="demoSummary">
            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.total_users }}</div>
                    <div class="stat-label">Total Users</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.students }}</div>
                    <div class="stat-label">Students</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">👨‍🏫</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.teachers }}</div>
                    <div class="stat-label">Teachers</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">👨‍💼</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.staff }}</div>
                    <div class="stat-label">Staff</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">📢</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.total_notices }}</div>
                    <div class="stat-label">Notices</div>
                </div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-content">
                    <div class="stat-number">{{ demoSummary.attendance_stats?.today_attendance || 0 }}</div>
                    <div class="stat-label">Today's Attendance</div>
                </div>
            </div>
        </div>

        <div class="demo-actions">
            <button @click="populateDemoData" :disabled="isLoading" class="btn-primary demo-btn">
                <span v-if="isLoading" class="loading-spinner"></span>
                <i v-else class="btn-icon">🚀</i>
                {{ isLoading ? 'Populating Demo Data...' : 'Populate Demo Data' }}
            </button>

            <button @click="refreshSummary" :disabled="isLoading" class="btn-secondary demo-btn">
                <i class="btn-icon">🔄</i>
                Refresh Summary
            </button>
        </div>

        <div v-if="populationResult" class="demo-result">
            <div class="result-header">
                <h3 class="result-title">
                    <i class="result-icon">✅</i>
                    Demo Data Population Complete
                </h3>
            </div>

            <div class="result-stats">
                <div class="result-item">
                    <span class="result-label">Users Created:</span>
                    <span class="result-value">{{ populationResult.result?.users_created || 0 }}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Attendance Records:</span>
                    <span class="result-value">{{ populationResult.result?.attendance_records || 0 }}</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Notices Created:</span>
                    <span class="result-value">{{ populationResult.result?.notices_created || 0 }}</span>
                </div>
            </div>

            <div class="demo-credentials">
                <h4 class="credentials-title">Demo Login Credentials</h4>
                <div class="credentials-grid">
                    <div class="credential-item admin">
                        <div class="credential-type">Admin Access</div>
                        <div class="credential-details">
                            <div class="credential-field">
                                <span class="field-label">Username:</span>
                                <code class="field-value">admin</code>
                            </div>
                            <div class="credential-field">
                                <span class="field-label">Password:</span>
                                <code class="field-value">admin123</code>
                            </div>
                        </div>
                    </div>

                    <div class="credential-item user">
                        <div class="credential-type">User Access</div>
                        <div class="credential-details">
                            <div class="credential-field">
                                <span class="field-label">Username:</span>
                                <code class="field-value">[any demo username]</code>
                            </div>
                            <div class="credential-field">
                                <span class="field-label">Password:</span>
                                <code class="field-value">demo123</code>
                            </div>
                        </div>
                    </div>

                    <div class="credential-item example">
                        <div class="credential-type">Example User</div>
                        <div class="credential-details">
                            <div class="credential-field">
                                <span class="field-label">Username:</span>
                                <code class="field-value">alice.johnson</code>
                            </div>
                            <div class="credential-field">
                                <span class="field-label">Password:</span>
                                <code class="field-value">demo123</code>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="error" class="demo-error">
            <div class="error-header">
                <i class="error-icon">❌</i>
                <span class="error-title">Error</span>
            </div>
            <p class="error-message">{{ error }}</p>
        </div>

        <div class="demo-info">
            <h3 class="info-title">
                <i class="info-icon">ℹ️</i>
                What Demo Data Includes
            </h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-item-icon">👥</div>
                    <div class="info-item-content">
                        <h4>Sample Users</h4>
                        <p>Students, teachers, and staff across different departments and classes</p>
                    </div>
                </div>

                <div class="info-item">
                    <div class="info-item-icon">📊</div>
                    <div class="info-item-content">
                        <h4>Attendance Records</h4>
                        <p>30 days of realistic attendance data with varying patterns</p>
                    </div>
                </div>

                <div class="info-item">
                    <div class="info-item-icon">📢</div>
                    <div class="info-item-content">
                        <h4>System Notices</h4>
                        <p>Sample announcements and notifications for demonstration</p>
                    </div>
                </div>

                <div class="info-item">
                    <div class="info-item-icon">📈</div>
                    <div class="info-item-content">
                        <h4>Analytics Data</h4>
                        <p>Rich analytics and reporting data for dashboard visualization</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminAPI } from '../services/api'

// Reactive state
const isLoading = ref(false)
interface DemoSummary {
    total_users: number
    students: number
    teachers: number
    staff: number
    total_notices: number
    attendance_stats?: {
        today_attendance: number
    }
}

const demoSummary = ref<DemoSummary | null>(null)
interface PopulationResult {
    result?: {
        users_created?: number
        attendance_records?: number
        notices_created?: number
    }
}
const populationResult = ref<PopulationResult | null>(null)
const error = ref('')

// Methods
const populateDemoData = async () => {
    try {
        isLoading.value = true
        error.value = ''
        populationResult.value = null

        const response = await adminAPI.populateDemoData()
        populationResult.value = response.data

        // Refresh summary after population
        await refreshSummary()

    } catch (err: any) {
        error.value = err.response?.data?.message || 'Failed to populate demo data'
        console.error('Demo data population error:', err)
    } finally {
        isLoading.value = false
    }
}

const refreshSummary = async () => {
    try {
        const response = await adminAPI.getDemoSummary()
        demoSummary.value = response.data.summary
    } catch (err: any) {
        console.error('Error fetching demo summary:', err)
        // Don't show error for summary fetch, just log it
    }
}

// Initialize
onMounted(() => {
    refreshSummary()
})
</script>

<style scoped>
.demo-data-manager {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 2rem;
    color: white;
    max-width: 1200px;
    margin: 0 auto;
}

.demo-header {
    text-align: center;
    margin-bottom: 2rem;
}

.demo-title {
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.demo-icon {
    font-size: 2rem;
}

.demo-description {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

.demo-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.stat-card:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.stat-icon {
    font-size: 2rem;
    opacity: 0.8;
}

.stat-content {
    flex: 1;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4ecdc4;
}

.stat-label {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-top: 0.25rem;
}

.demo-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.demo-btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    min-width: 180px;
    justify-content: center;
}

.btn-primary {
    background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
    color: white;
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.demo-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.demo-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}

.loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.demo-result {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.result-header {
    margin-bottom: 1rem;
}

.result-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #86efac;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.result-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.result-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.result-label {
    color: rgba(255, 255, 255, 0.8);
}

.result-value {
    font-weight: 600;
    color: #86efac;
}

.demo-credentials {
    margin-top: 1.5rem;
}

.credentials-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: white;
}

.credentials-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
}

.credential-item {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.credential-item.admin {
    border-color: rgba(138, 43, 226, 0.5);
}

.credential-item.user {
    border-color: rgba(78, 205, 196, 0.5);
}

.credential-item.example {
    border-color: rgba(34, 197, 94, 0.5);
}

.credential-type {
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: white;
}

.credential-field {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.field-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.875rem;
}

.field-value {
    background: rgba(0, 0, 0, 0.3);
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.875rem;
    color: #4ecdc4;
}

.demo-error {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 2rem;
}

.error-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.error-title {
    font-weight: 600;
    color: #fca5a5;
}

.error-message {
    color: #fca5a5;
    margin: 0;
}

.demo-info {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.info-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}

.info-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.info-item-icon {
    font-size: 1.5rem;
    opacity: 0.8;
    flex-shrink: 0;
}

.info-item-content h4 {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: white;
}

.info-item-content p {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.4;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .demo-data-manager {
        padding: 1.5rem;
    }

    .demo-stats {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }

    .demo-actions {
        flex-direction: column;
        align-items: center;
    }

    .demo-btn {
        width: 100%;
        max-width: 300px;
    }

    .credentials-grid {
        grid-template-columns: 1fr;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }
}
</style>