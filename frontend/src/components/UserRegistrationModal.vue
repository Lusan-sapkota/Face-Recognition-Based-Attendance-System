<template>
  <div class="registration-modal-overlay" v-if="show" @click.self="closeModal">
    <div class="registration-modal">
      <div class="modal-header">
        <h2 class="modal-title">
          <i class="title-icon">{{ props.existingUser ? '📸' : '👤➕' }}</i>
          {{ props.existingUser ? 'Capture User Face' : 'Register New User' }}
        </h2>
        <button @click="closeModal" class="close-btn">
          <i class="close-icon">✖️</i>
        </button>
      </div>

      <div class="modal-body">
        <div class="registration-form">
          <!-- Step Indicator -->
          <div class="step-indicator" v-if="!isFaceCaptureMode">
            <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
              <span class="step-number">1</span>
              <span class="step-label">User Details</span>
            </div>
            <div class="step-divider"></div>
            <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
              <span class="step-number">2</span>
              <span class="step-label">Face Capture</span>
            </div>
            <div class="step-divider"></div>
            <div class="step" :class="{ active: currentStep >= 3 }">
              <span class="step-number">3</span>
              <span class="step-label">Complete</span>
            </div>
          </div>

          <!-- Face Capture Mode Header -->
          <div v-if="isFaceCaptureMode" class="face-capture-header">
            <div class="user-info">
              <h3>Capturing face for: {{ formData.name }}</h3>
              <p>ID: {{ formData.user_id }} | Type: {{ formData.type }}</p>
            </div>
          </div>

          <!-- Step 1: User Details (hidden for existing users) -->
          <div v-if="currentStep === 1 && !isFaceCaptureMode" class="form-step">
            <div class="form-grid">
              <div class="form-field">
                <label class="field-label">👤 Full Name</label>
                <input 
                  v-model="formData.name" 
                  type="text" 
                  class="field-input"
                  placeholder="Enter full name"
                  required
                />
              </div>

              <div class="form-field">
                <label class="field-label">🆔 User ID</label>
                <input 
                  v-model="formData.user_id" 
                  type="text" 
                  class="field-input"
                  placeholder="Enter user ID"
                  required
                />
              </div>

              <div class="form-field">
                <label class="field-label">👨‍🎓 Username</label>
                <input 
                  v-model="formData.username" 
                  type="text" 
                  class="field-input"
                  placeholder="Enter username"
                  required
                />
              </div>

              <div class="form-field">
                <label class="field-label">🔒 Password</label>
                <input 
                  v-model="formData.password" 
                  type="password" 
                  class="field-input"
                  placeholder="Enter password"
                  required
                />
              </div>

              <div class="form-field">
                <label class="field-label">👥 User Type</label>
                <select v-model="formData.type" class="field-input" required>
                  <option value="">Select user type</option>
                  <option value="student">Student</option>
                  <option value="teacher">Teacher</option>
                  <option value="staff">Staff</option>
                </select>
              </div>

              <div class="form-field">
                <label class="field-label">🏫 Class/Section</label>
                <input 
                  v-model="formData.class_section" 
                  type="text" 
                  class="field-input"
                  placeholder="e.g., CS 4th E"
                />
              </div>
            </div>

            <div class="form-actions">
              <button @click="closeModal" class="btn-secondary">Cancel</button>
              <button @click="nextStep" :disabled="!isStep1Valid" class="btn-primary">
                Next: Face Capture
              </button>
            </div>
          </div>

          <!-- Step 2: Face Capture -->
          <div v-if="currentStep === 2 || isFaceCaptureMode" class="form-step">
            <div class="face-capture-section">
              <div class="capture-header">
                <h3 class="capture-title">Face Registration</h3>
                <p class="capture-description">
                  Please position your face in the camera frame for face registration
                </p>
              </div>

              <div class="camera-container" :class="{ 'scanning': isScanning }">
                <video 
                  ref="videoRef" 
                  v-show="isCameraActive && !captureComplete"
                  class="camera-feed"
                  autoplay 
                  muted
                  playsinline
                ></video>
                
                <canvas 
                  ref="canvasRef" 
                  v-show="false"
                  class="capture-canvas"
                ></canvas>
                
                <!-- Status Overlay -->
                <div class="status-overlay" v-if="!isCameraActive || captureComplete">
                  <div class="status-indicator" :class="statusClass">
                    <div class="status-icon">{{ statusIcon }}</div>
                    <div class="status-text">{{ statusMessage }}</div>
                  </div>
                </div>
                
                <!-- Face Detection Frame -->
                <div class="face-frame" v-if="isCameraActive && !captureComplete">
                  <div class="frame-corner tl"></div>
                  <div class="frame-corner tr"></div>
                  <div class="frame-corner bl"></div>
                  <div class="frame-corner br"></div>
                </div>

                <!-- Scanning Animation -->
                <div class="scanning-overlay" v-if="isScanning">
                  <div class="scanner-line"></div>
                  <div class="scanning-text">Registering face...</div>
                </div>
              </div>

              <div class="capture-instructions">
                <div v-if="!isCameraActive && !captureComplete && !cameraError" class="instruction">
                  📸 Click "Start Camera" to begin face registration
                </div>
                <div v-else-if="cameraError" class="instruction error">
                  ❌ {{ cameraError }}
                </div>
                <div v-else-if="isCameraActive && !isScanning && !captureComplete" class="instruction">
                  📹 Position your face in the frame and click "Capture Face"
                </div>
                <div v-else-if="isScanning" class="instruction">
                  ⏳ Processing face data... Please stay still
                </div>
                <div v-else-if="captureComplete && captureSuccess" class="instruction success">
                  ✅ Face registered successfully!
                </div>
                <div v-else-if="captureComplete && !captureSuccess" class="instruction error">
                  ❌ Face registration failed. Please try again.
                </div>
              </div>

              <div class="capture-actions">
                <button @click="previousStep" class="btn-secondary" :disabled="isScanning">
                  ← Back
                </button>

                <button 
                  v-if="!isCameraActive && !captureComplete" 
                  @click="startCamera" 
                  :disabled="isLoading"
                  class="btn-primary"
                >
                  <span v-if="isLoading" class="loading-spinner"></span>
                  {{ isLoading ? 'Starting Camera...' : '📸 Start Camera' }}
                </button>
                
                <button 
                  v-if="isCameraActive && !isScanning && !captureComplete" 
                  @click="captureAndRegister" 
                  class="btn-success"
                >
                  📷 Capture Face
                </button>
                
                <button 
                  v-if="captureComplete && captureSuccess" 
                  @click="completeRegistration"
                  class="btn-primary"
                >
                  Complete Registration →
                </button>
                
                <button 
                  v-if="captureComplete && !captureSuccess" 
                  @click="resetCapture"
                  class="btn-warning"
                >
                  🔄 Try Again
                </button>
              </div>
            </div>
          </div>

          <!-- Step 3: Complete -->
          <div v-if="currentStep === 3" class="form-step">
            <div class="completion-section">
              <div class="success-animation">
                <div class="check-circle">
                  <div class="check-mark">✓</div>
                </div>
              </div>
              
              <h3 class="completion-title">Registration Complete!</h3>
              <p class="completion-message">
                User {{ formData.name }} has been successfully registered with face recognition.
              </p>
              
              <div class="user-summary">
                <div class="summary-item">
                  <span class="summary-label">Name:</span>
                  <span class="summary-value">{{ formData.name }}</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label">User ID:</span>
                  <span class="summary-value">{{ formData.user_id }}</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label">Type:</span>
                  <span class="summary-value">{{ formData.type }}</span>
                </div>
                <div class="summary-item">
                  <span class="summary-label">Class/Section:</span>
                  <span class="summary-value">{{ formData.class_section || 'N/A' }}</span>
                </div>
              </div>

              <div class="completion-actions">
                <button @click="registerAnother" class="btn-secondary">
                  ➕ Register Another User
                </button>
                <button @click="closeModal" class="btn-primary">
                  ✓ Done
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { adminAPI } from '../services/api'

// Props and Events
interface Props {
  show: boolean
  existingUser?: {
    id: string
    name: string
    user_id: string
    type: string
    class_section?: string
  } | null
}

const props = defineProps<Props>()
const emit = defineEmits(['close', 'success'])

// Reactive State
const currentStep = ref(1)
const isLoading = ref(false)
const isScanning = ref(false)
const isCameraActive = ref(false)
const captureComplete = ref(false)
const captureSuccess = ref(false)
const cameraError = ref('')
const statusMessage = ref('')

// Form Data
const formData = ref({
  name: '',
  user_id: '',
  username: '',
  password: '',
  type: '',
  class_section: ''
})

// Camera References
const videoRef = ref<HTMLVideoElement>()
const canvasRef = ref<HTMLCanvasElement>()
const mediaStream = ref<MediaStream>()

// Computed Properties
const isStep1Valid = computed(() => {
  if (props.existingUser) {
    // For existing users (face capture mode), skip step 1 validation
    return true
  }
  return formData.value.name && 
         formData.value.user_id && 
         formData.value.username && 
         formData.value.password && 
         formData.value.type
})

const isFaceCaptureMode = computed(() => !!props.existingUser)

// Initialize form data when existing user is provided
const initializeFormData = () => {
  if (props.existingUser) {
    formData.value = {
      name: props.existingUser.name,
      user_id: props.existingUser.user_id,
      username: props.existingUser.id, // Use existing username/id
      password: '', // Don't change password
      type: props.existingUser.type,
      class_section: props.existingUser.class_section || ''
    }
    // Skip to face capture step
    currentStep.value = 2
  } else {
    // Reset for new user
    formData.value = {
      name: '',
      user_id: '',
      username: '',
      password: '',
      type: '',
      class_section: ''
    }
    currentStep.value = 1
  }
}

const statusClass = computed(() => {
  if (captureComplete.value) {
    return captureSuccess.value ? 'success' : 'error'
  }
  if (cameraError.value) return 'error'
  if (isLoading.value) return 'loading'
  return 'info'
})

const statusIcon = computed(() => {
  if (captureComplete.value) {
    return captureSuccess.value ? '✅' : '❌'
  }
  if (cameraError.value) return '❌'
  if (isLoading.value) return '⏳'
  return '📸'
})

// Methods
const closeModal = () => {
  stopCamera()
  resetForm()
  emit('close')
}

const resetForm = () => {
  if (props.existingUser) {
    // Don't reset for existing user, just initialize properly
    initializeFormData()
  } else {
    currentStep.value = 1
    formData.value = {
      name: '',
      user_id: '',
      username: '',
      password: '',
      type: '',
      class_section: ''
    }
  }
  resetCapture()
}

const resetCapture = () => {
  isScanning.value = false
  captureComplete.value = false
  captureSuccess.value = false
  cameraError.value = ''
  statusMessage.value = ''
}

const nextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  }
}

const previousStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    if (currentStep.value === 1) {
      stopCamera()
      resetCapture()
    }
  }
}

const startCamera = async () => {
  try {
    isLoading.value = true
    cameraError.value = ''
    statusMessage.value = 'Starting camera...'

    const constraints = {
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: 'user'
      },
      audio: false
    }

    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    
    if (videoRef.value) {
      videoRef.value.srcObject = mediaStream.value
      await videoRef.value.play()
      isCameraActive.value = true
      statusMessage.value = 'Camera ready'
    }
  } catch (error: any) {
    console.error('Camera error:', error)
    cameraError.value = 'Failed to access camera. Please check permissions.'
    statusMessage.value = 'Camera access failed'
  } finally {
    isLoading.value = false
  }
}

const stopCamera = () => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
    mediaStream.value = undefined
  }
  isCameraActive.value = false
}

const captureAndRegister = async () => {
  if (!videoRef.value || !canvasRef.value) return

  try {
    isScanning.value = true
    statusMessage.value = 'Capturing and registering face...'

    // Capture image from video
    const canvas = canvasRef.value
    const video = videoRef.value
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    
    const ctx = canvas.getContext('2d')
    if (!ctx) throw new Error('Canvas context not available')
    
    ctx.drawImage(video, 0, 0)
    const imageData = canvas.toDataURL('image/jpeg', 0.8)

    // Register user first (only for new users)
    if (!props.existingUser) {
      await adminAPI.registerUser(formData.value)
    }

    // Then register face with scan_face API
    const faceResponse = await adminAPI.scanFace({
      image: imageData.split(',')[1], // Remove data:image/jpeg;base64, prefix
      user_id: formData.value.user_id,
      name: formData.value.name
    })

    if (faceResponse.data.success) {
      captureSuccess.value = true
      statusMessage.value = props.existingUser 
        ? 'Face captured successfully!' 
        : 'Face registered successfully!'
    } else {
      captureSuccess.value = false
      statusMessage.value = faceResponse.data.message || 'Face registration failed'
    }

  } catch (error: any) {
    console.error('Registration error:', error)
    captureSuccess.value = false
    statusMessage.value = error.response?.data?.message || 'Registration failed'
  } finally {
    isScanning.value = false
    captureComplete.value = true
  }
}

const completeRegistration = () => {
  stopCamera()
  currentStep.value = 3
}

const registerAnother = () => {
  resetForm()
  emit('success', `User ${formData.value.name} registered successfully!`)
}

// Watch for modal visibility and existing user changes
watch(() => props.show, (newShow) => {
  if (newShow) {
    initializeFormData()
  } else {
    stopCamera()
    resetForm()
  }
})

watch(() => props.existingUser, () => {
  if (props.show) {
    initializeFormData()
  }
})
</script>

<style scoped>
.registration-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 2rem;
}

.registration-modal {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 24px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.modal-body {
  padding: 2rem;
}

/* Step Indicator */
.step-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 3rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  color: white;
}

.step.completed .step-number {
  background: #22c55e;
  color: white;
}

.step-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.step.active .step-label {
  color: white;
}

.step-divider {
  width: 60px;
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  margin: 0 1rem;
}

/* Form Fields */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.field-input {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.field-input:focus {
  outline: none;
  border-color: #4ecdc4;
  box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.2);
  background: rgba(255, 255, 255, 0.08);
}

.field-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

/* Camera Section */
.face-capture-section {
  text-align: center;
}

.capture-header {
  margin-bottom: 2rem;
}

.capture-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.5rem;
}

.capture-description {
  color: rgba(255, 255, 255, 0.7);
}

.camera-container {
  position: relative;
  width: 100%;
  max-width: 480px;
  height: 360px;
  margin: 0 auto 2rem;
  border-radius: 16px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.camera-feed {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  color: white;
}

.status-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.status-text {
  font-size: 1.125rem;
  font-weight: 500;
}

.face-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200px;
  height: 200px;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.frame-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 3px solid #4ecdc4;
}

.frame-corner.tl {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
}

.frame-corner.tr {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
}

.frame-corner.bl {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
}

.frame-corner.br {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
}

.scanning-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(78, 205, 196, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.scanner-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #4ecdc4, transparent);
  animation: scan 2s ease-in-out infinite;
}

@keyframes scan {
  0%, 100% { transform: translateY(-100px); }
  50% { transform: translateY(100px); }
}

.scanning-text {
  margin-top: 1rem;
  color: white;
  font-weight: 600;
}

/* Instructions */
.capture-instructions {
  margin-bottom: 2rem;
}

.instruction {
  padding: 1rem;
  border-radius: 12px;
  font-weight: 500;
}

.instruction.error {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

.instruction.success {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #86efac;
}

.instruction:not(.error):not(.success) {
  background: rgba(78, 205, 196, 0.1);
  border: 1px solid rgba(78, 205, 196, 0.3);
  color: rgba(255, 255, 255, 0.9);
}

/* Actions */
.form-actions,
.capture-actions,
.completion-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary,
.btn-success,
.btn-warning {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.btn-success {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.btn-primary:hover,
.btn-success:hover,
.btn-warning:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-primary:disabled,
.btn-secondary:disabled {
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

/* Completion Section */
.completion-section {
  text-align: center;
}

.success-animation {
  margin-bottom: 2rem;
}

.check-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  animation: bounceIn 0.8s ease;
}

@keyframes bounceIn {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.check-mark {
  font-size: 2rem;
  color: white;
  font-weight: bold;
}

.completion-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.completion-message {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
}

.user-summary {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: left;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.summary-item:last-child {
  border-bottom: none;
}

.summary-label {
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.summary-value {
  color: white;
  font-weight: 600;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
