<template>
    <div v-if="isDemoMode()" class="demo-banner">
        <div class="demo-content">
            <div class="demo-icon">🎯</div>
            <div class="demo-text">
                <span class="demo-title">Demo Mode Active</span>
                <span class="demo-subtitle">You're viewing realistic demo data. All features are fully
                    functional!</span>
            </div>
            <div class="demo-credentials">
                <div class="credential-item">
                    <span class="credential-label">Try logging in as:</span>
                    <code class="credential-value">alice.johnson / demo123</code>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { isDemoMode } from '../services/mockAuth'
</script>

<style scoped>
.demo-banner {
    background: linear-gradient(135deg, #8A2BE2 0%, #4ecdc4 100%);
    color: white;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.demo-content {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.demo-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.demo-text {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    flex: 1;
    min-width: 200px;
}

.demo-title {
    font-weight: 700;
    font-size: 0.875rem;
}

.demo-subtitle {
    font-size: 0.75rem;
    opacity: 0.9;
}

.demo-credentials {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-shrink: 0;
}

.credential-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.1);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
}

.credential-label {
    opacity: 0.9;
}

.credential-value {
    background: rgba(0, 0, 0, 0.2);
    padding: 0.125rem 0.5rem;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.7rem;
}

/* Responsive Design */
@media (max-width: 768px) {
    .demo-content {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
    }

    .demo-credentials {
        width: 100%;
        justify-content: center;
    }

    .credential-item {
        flex-direction: column;
        gap: 0.25rem;
        text-align: center;
    }
}
</style>