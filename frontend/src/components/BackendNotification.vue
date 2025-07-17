<template>
  <div v-if="!isDismissed" class="backend-notification">
    <div class="notification-content">
      <div class="notification-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
      </div>
      <div class="notification-text">
        <h4 class="notification-title">Frontend Demo Notice (You can safely cut this!)</h4>
        <p class="notification-message">
          This is a frontend-only demo for showcase purposes. The complete application with full backend functionality,
          including face recognition, database operations, and real-time attendance tracking, is available in my
          <a href="https://github.com/Lusan-sapkota/Face-Recognition-Based-Attendance-System" target="_blank"
            rel="noopener noreferrer" class="github-link">
            GitHub repository
          </a>
        </p>
      </div>
      <button @click="dismiss" class="dismiss-btn" title="Dismiss notification">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDismissed = ref(false)

const dismiss = () => {
  isDismissed.value = true
  // Store dismissal state in localStorage
  localStorage.setItem('backend-notification-dismissed', 'true')
  // Remove body padding
  document.body.style.paddingTop = '0'
}

onMounted(() => {
  // Check if notification was previously dismissed
  const dismissed = localStorage.getItem('backend-notification-dismissed')
  if (dismissed === 'true') {
    isDismissed.value = true
  } else {
    // Add padding to body to prevent content overlap
    // Increased padding to account for taller notification
    document.body.style.paddingTop = '80px'
  }
})
</script>

<style scoped>
.backend-notification {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.95) 0%, rgba(255, 152, 0, 0.95) 100%);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 193, 7, 0.3);
  box-shadow: 0 4px 20px rgba(255, 193, 7, 0.2);
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.notification-content {
  display: flex;
  align-items: center;
  flex-direction: row !important;
  gap: 16px;
  padding: 15px 18px;
  max-width: 1200px;
  margin: 0 auto;
}

.notification-icon {
  width: 24px;
  height: 24px;
  color: #92400e;
  flex-shrink: 0;
}

.notification-icon svg {
  width: 100%;
  height: 100%;
}

.notification-text {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #92400e;
  margin: 0 0 4px 0;
}

.notification-message {
  font-size: 0.8rem;
  color: #92400e;
  margin: 0;
  line-height: 1.4;
}

.github-link {
  color: #92400e;
  text-decoration: underline;
  font-weight: 600;
  transition: color 0.2s ease;
}

.github-link:hover {
  color: #78350f;
}

.dismiss-btn {
  background: none;
  border: none;
  color: #92400e;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.dismiss-btn:hover {
  background: rgba(146, 64, 14, 0.1);
  color: #78350f;
}

.dismiss-btn svg {
  width: 16px;
  height: 16px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .notification-content {
    padding: 18px 16px;
    gap: 12px;
  }

  .notification-title {
    font-size: 0.8rem;
  }

  .notification-message {
    font-size: 0.75rem;
  }

  .notification-icon {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .notification-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 20px 16px;
  }

  .dismiss-btn {
    align-self: flex-end;
    margin-top: -8px;
  }
}
</style>