<template>
  <transition name="toast" appear>
    <div v-if="show" class="notification-toast" :class="type">
      <div class="toast-icon">
        {{ getIcon() }}
      </div>
      <div class="toast-content">
        <h4 class="toast-title">{{ title }}</h4>
        <p class="toast-message">{{ message }}</p>
      </div>
      <button @click="close" class="toast-close">
        ✕
      </button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show: boolean
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
}

const props = withDefaults(defineProps<Props>(), {
  duration: 5000
})

const emit = defineEmits(['close'])

const getIcon = () => {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  }
  return icons[props.type]
}

const close = () => {
  emit('close')
}

// Auto close after duration
if (props.show && props.duration > 0) {
  setTimeout(() => {
    close()
  }, props.duration)
}
</script>

<style scoped>
.notification-toast {
  position: fixed;
  top: 20px;
  right: 20px;
  max-width: 400px;
  background: var(--card-background);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  z-index: 10000;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  backdrop-filter: blur(10px);
}

.notification-toast.success {
  border-left: 4px solid #22c55e;
}

.notification-toast.error {
  border-left: 4px solid #ef4444;
}

.notification-toast.warning {
  border-left: 4px solid #f59e0b;
}

.notification-toast.info {
  border-left: 4px solid #3b82f6;
}

.toast-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 4px 0;
}

.toast-message {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.4;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-primary);
}

/* Transition animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

@media (max-width: 640px) {
  .notification-toast {
    left: 20px;
    right: 20px;
    max-width: none;
  }
}
</style>
