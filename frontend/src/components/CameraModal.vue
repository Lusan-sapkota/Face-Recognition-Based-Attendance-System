<template>
  <div class="modal-overlay" v-if="show" @click.self="closeModal">
    <div class="modal-container">
      <div class="modal-header">
        <h3 class="modal-title">
          <span class="camera-emoji">📸</span>
          Face Recognition Attendance
        </h3>
        <button @click="closeModal" class="modal-close">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="camera-section">
          <!-- Camera Feed -->
          <div class="camera-container" :class="{ 'scanning': isScanning }">
            <video 
              ref="videoRef" 
              v-show="isCameraActive && !isComplete"
              class="camera-feed"
              autoplay 
              muted
            ></video>
            
            <canvas 
              ref="canvasRef" 
              v-show="false"
              class="capture-canvas"
            ></canvas>
            
            <!-- Status Overlay -->
            <div class="status-overlay" v-if="!isCameraActive || isComplete">
              <div class="status-indicator" :class="statusClass">
                <div class="status-icon">{{ statusIcon }}</div>
                <div class="status-text">{{ statusMessage }}</div>
              </div>
            </div>
            
            <!-- Scanning Animation -->
            <div class="scanning-animation" v-if="isScanning && isCameraActive">
              <div class="scanner-line"></div>
              <div class="scanner-corners">
                <div class="corner corner-tl"></div>
                <div class="corner corner-tr"></div>
                <div class="corner corner-bl"></div>
                <div class="corner corner-br"></div>
              </div>
              <div class="scanning-text">Scanning face...</div>
            </div>
            
            <!-- Face Detection Frame -->
            <div class="face-frame" v-if="isCameraActive && !isComplete"></div>
          </div>
          
          <div class="instructions">
            <p v-if="!isCameraActive && !isComplete && !cameraError">
              Click "Start Camera" to begin face recognition attendance.
            </p>
            <p v-else-if="cameraError" class="error-text">
              {{ cameraError }}
            </p>
            <p v-else-if="isCameraActive && !isScanning && !isComplete">
              Position your face within the frame and click "Capture" when ready.
            </p>
            <p v-else-if="isScanning">
              Processing... Please keep your face steady in the frame.
            </p>
            <p v-else-if="isComplete && scanSuccess" class="success-text">
              ✅ Face recognized successfully! Your attendance has been marked.
            </p>
            <p v-else-if="isComplete && !scanSuccess" class="error-text">
              ❌ Face recognition failed. Please try again or contact admin.
            </p>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button 
          v-if="!isCameraActive && !isComplete" 
          @click="startCamera" 
          :disabled="isLoading"
          class="btn btn-primary"
        >
          <span v-if="isLoading" class="spinner"></span>
          {{ isLoading ? 'Starting Camera...' : 'Start Camera' }}
        </button>
        
        <button 
          v-if="isCameraActive && !isScanning && !isComplete" 
          @click="captureAndRecognize" 
          class="btn btn-success"
        >
          📸 Capture & Recognize
        </button>
        
        <button 
          v-if="isComplete" 
          @click="resetModal"
          class="btn btn-primary"
        >
          {{ scanSuccess ? 'Continue' : 'Try Again' }}
        </button>
        
        <button @click="closeModal" class="btn btn-secondary">
          {{ isComplete ? 'Close' : 'Cancel' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onUnmounted } from 'vue'
import { userAPI } from '@/services/api'

// Props
interface Props {
  show: boolean
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  close: []
  success: [message: string]
}>()

// Reactive state
const isLoading = ref(false)
const isCameraActive = ref(false)
const isScanning = ref(false)
const isComplete = ref(false)
const scanSuccess = ref(false)
const scanMessage = ref('')
const cameraError = ref('')

// Refs
const videoRef = ref<HTMLVideoElement | null>(null)
const canvasRef = ref<HTMLCanvasElement | null>(null)
const streamRef = ref<MediaStream | null>(null)

// Timeout refs for cleanup
const cameraStartTimeout = ref<any>(null)
const scanningTimeout = ref<any>(null)
const autoRecoveryTimeout = ref<any>(null)

// Computed properties
const statusClass = computed(() => {
  if (cameraError.value) return 'error'
  if (isComplete.value) {
    return scanSuccess.value ? 'success' : 'error'
  }
  if (isScanning.value) return 'scanning'
  if (isCameraActive.value) return 'ready'
  return 'waiting'
})

const statusIcon = computed(() => {
  if (cameraError.value) return '❌'
  if (isComplete.value) {
    return scanSuccess.value ? '✅' : '❌'
  }
  if (isScanning.value) return '🔍'
  if (isCameraActive.value) return '�'
  return '📷'
})

const statusMessage = computed(() => {
  if (cameraError.value) return 'Camera Error'
  if (isComplete.value) {
    return scanMessage.value
  }
  if (isScanning.value) return 'Processing face...'
  if (isCameraActive.value) return 'Camera Ready'
  return 'Click to start camera'
})

// Methods
const clearAllTimeouts = () => {
  if (cameraStartTimeout.value) {
    clearTimeout(cameraStartTimeout.value)
    cameraStartTimeout.value = null
  }
  if (scanningTimeout.value) {
    clearTimeout(scanningTimeout.value)
    scanningTimeout.value = null
  }
  if (autoRecoveryTimeout.value) {
    clearTimeout(autoRecoveryTimeout.value)
    autoRecoveryTimeout.value = null
  }
}

const startCamera = async () => {
  isLoading.value = true
  cameraError.value = ''
  clearAllTimeouts()
  
  // Set timeout for camera startup
  cameraStartTimeout.value = setTimeout(() => {
    if (isLoading.value) {
      isLoading.value = false
      cameraError.value = 'Camera startup timed out. Please try again.'
    }
  }, 10000) // 10 second timeout for camera startup
  
  try {
    // Request camera permission and start video stream
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: 'user'
      },
      audio: false
    })
    
    streamRef.value = stream
    
    await nextTick()
    
    if (videoRef.value) {
      videoRef.value.srcObject = stream
      
      // Wait for video to be ready
      await new Promise((resolve, reject) => {
        const timeoutId = setTimeout(() => {
          reject(new Error('Video ready timeout'))
        }, 5000)
        
        videoRef.value!.onloadedmetadata = () => {
          clearTimeout(timeoutId)
          resolve(null)
        }
        
        videoRef.value!.onerror = () => {
          clearTimeout(timeoutId)
          reject(new Error('Video load error'))
        }
      })
      
      await videoRef.value.play()
      isCameraActive.value = true
      
      // Clear the startup timeout on success
      if (cameraStartTimeout.value) {
        clearTimeout(cameraStartTimeout.value)
        cameraStartTimeout.value = null
      }
    }
    
  } catch (error: any) {
    console.error('Camera access error:', error)
    if (error.name === 'NotAllowedError') {
      cameraError.value = 'Camera access denied. Please allow camera permissions and try again.'
    } else if (error.name === 'NotFoundError') {
      cameraError.value = 'No camera found. Please ensure a camera is connected.'
    } else if (error.name === 'NotReadableError') {
      cameraError.value = 'Camera is already in use by another application.'
    } else if (error.message.includes('timeout')) {
      cameraError.value = 'Camera startup timed out. Please try again.'
    } else {
      cameraError.value = 'Unable to access camera. Please check your browser settings.'
    }
  } finally {
    isLoading.value = false
    if (cameraStartTimeout.value) {
      clearTimeout(cameraStartTimeout.value)
      cameraStartTimeout.value = null
    }
  }
}

const stopCamera = () => {
  clearAllTimeouts()
  
  if (streamRef.value) {
    streamRef.value.getTracks().forEach(track => track.stop())
    streamRef.value = null
  }
  if (videoRef.value) {
    videoRef.value.srcObject = null
  }
  isCameraActive.value = false
}

const captureImage = (): string | null => {
  if (!videoRef.value || !canvasRef.value) return null
  
  const canvas = canvasRef.value
  const video = videoRef.value
  
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  const ctx = canvas.getContext('2d')
  if (!ctx) return null
  
  ctx.drawImage(video, 0, 0)
  return canvas.toDataURL('image/jpeg', 0.8)
}

const captureAndRecognize = async () => {
  isScanning.value = true
  isComplete.value = false
  scanSuccess.value = false
  cameraError.value = ''
  
  // Set timeout for scanning process
  scanningTimeout.value = setTimeout(() => {
    if (isScanning.value) {
      isScanning.value = false
      isComplete.value = true
      scanSuccess.value = false
      scanMessage.value = 'Face recognition timed out. Please try again.'
      
      // Auto-recovery: reset to camera ready state after 3 seconds
      autoRecoveryTimeout.value = setTimeout(() => {
        if (!scanSuccess.value && isComplete.value) {
          resetModal()
        }
      }, 3000)
    }
  }, 15000) // 15 second timeout for face recognition
  
  try {
    // Capture image from video
    const imageData = captureImage()
    if (!imageData) {
      throw new Error('Failed to capture image')
    }
    
    // Send image to backend for face recognition
    const response = await userAPI.markAttendanceWithImage({
      image: imageData
    })
    
    // Clear scanning timeout on success
    if (scanningTimeout.value) {
      clearTimeout(scanningTimeout.value)
      scanningTimeout.value = null
    }
    
    if (response.data.success) {
      scanSuccess.value = true
      scanMessage.value = response.data.message
      emit('success', response.data.message)
      stopCamera()
    } else {
      scanSuccess.value = false
      scanMessage.value = response.data.message || 'Face recognition failed'
      
      // Auto-recovery for failed recognition
      autoRecoveryTimeout.value = setTimeout(() => {
        if (!scanSuccess.value && isComplete.value) {
          resetModal()
        }
      }, 5000) // Auto-retry after 5 seconds
    }
  } catch (error: any) {
    scanSuccess.value = false
    scanMessage.value = error.response?.data?.message || 'Face recognition failed. Please try again.'
    console.error('Face recognition error:', error)
    
    // Auto-recovery for errors
    autoRecoveryTimeout.value = setTimeout(() => {
      if (!scanSuccess.value && isComplete.value) {
        resetModal()
      }
    }, 5000)
  } finally {
    isScanning.value = false
    isComplete.value = true
    
    // Clear scanning timeout
    if (scanningTimeout.value) {
      clearTimeout(scanningTimeout.value)
      scanningTimeout.value = null
    }
  }
}

const resetModal = () => {
  isScanning.value = false
  isComplete.value = false
  scanSuccess.value = false
  scanMessage.value = ''
  cameraError.value = ''
  
  if (scanSuccess.value) {
    closeModal()
  }
}

const closeModal = () => {
  stopCamera()
  
  // Reset all state
  isLoading.value = false
  isCameraActive.value = false
  isScanning.value = false
  isComplete.value = false
  scanSuccess.value = false
  scanMessage.value = ''
  cameraError.value = ''
  
  emit('close')
}

// Cleanup on unmount
onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-container {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
  animation: modalSlideIn 0.3s ease;
  position: relative;
}

@keyframes modalSlideIn {
  from { 
    transform: scale(0.9) translateY(-20px);
    opacity: 0;
  }
  to { 
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.modal-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #8A2BE2, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 300% 100%;
  animation: gradientShift 3s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.02);
}

.modal-title {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.camera-emoji {
  font-size: 1.8rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.modal-close {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
  transition: all 0.3s ease;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(90deg);
}

.modal-body {
  padding: 2rem;
}

.camera-section {
  text-align: center;
}

.camera-container {
  position: relative;
  width: 100%;
  max-width: 480px;
  height: 360px;
  margin: 0 auto 2rem;
  border-radius: 20px;
  overflow: hidden;
  background: #000;
  border: 3px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.camera-container.scanning {
  border-color: #4ecdc4;
  box-shadow: 0 0 30px rgba(78, 205, 196, 0.4);
}

.camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 17px;
}

.capture-canvas {
  display: none;
}

.status-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
}

.status-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.status-indicator.waiting {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.3);
}

.status-indicator.ready {
  background: rgba(78, 205, 196, 0.1);
  border: 2px solid rgba(78, 205, 196, 0.5);
}

.status-indicator.scanning {
  background: rgba(69, 183, 209, 0.1);
  border: 2px solid #45b7d1;
  box-shadow: 0 0 20px rgba(69, 183, 209, 0.3);
}

.status-indicator.success {
  background: rgba(34, 197, 94, 0.1);
  border: 2px solid #22c55e;
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

.status-indicator.error {
  background: rgba(239, 68, 68, 0.1);
  border: 2px solid #ef4444;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}

.status-icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  animation: iconPulse 2s infinite;
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.status-text {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
}

.face-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200px;
  height: 200px;
  transform: translate(-50%, -50%);
  border: 3px solid rgba(78, 205, 196, 0.6);
  border-radius: 50%;
  animation: framePulse 2s infinite;
}

@keyframes framePulse {
  0%, 100% { 
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.6;
  }
  50% { 
    transform: translate(-50%, -50%) scale(1.05);
    opacity: 1;
  }
}

.scanning-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  border-radius: 17px;
  overflow: hidden;
}

.scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, #4ecdc4, transparent);
  animation: scan 2s linear infinite;
  box-shadow: 0 0 10px #4ecdc4;
}

.scanner-corners {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  bottom: 20px;
}

.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 3px solid #4ecdc4;
  animation: cornerGlow 2s infinite;
}

@keyframes cornerGlow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.corner-tl {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.corner-tr {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.corner-bl {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

.corner-br {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.scanning-text {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  color: #4ecdc4;
  font-weight: 600;
  font-size: 14px;
  animation: textPulse 1s infinite;
}

@keyframes textPulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

@keyframes scan {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(350px);
  }
}

.instructions {
  font-size: 1rem;
  line-height: 1.6;
  margin-top: 1rem;
  min-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.instructions p {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
}

.success-text {
  color: #22c55e !important;
  font-weight: 600;
}

.error-text {
  color: #ef4444 !important;
  font-weight: 600;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  justify-content: flex-end;
  background: rgba(255, 255, 255, 0.02);
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #8A2BE2 0%, #4ecdc4 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(255, 107, 107, 0.5);
}

.btn-success {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(34, 197, 94, 0.3);
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(34, 197, 94, 0.5);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.9);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-container {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
  
  .camera-container {
    height: 280px;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1.5rem;
  }
  
  .modal-title {
    font-size: 1.25rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
