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
                <input v-model="formData.name" type="text" class="field-input" placeholder="Enter full name" required />
              </div>

              <div class="form-field">
                <label class="field-label">🆔 User ID</label>
                <input v-model="formData.user_id" type="text" class="field-input" placeholder="Enter user ID"
                  required />
              </div>

              <div class="form-field">
                <label class="field-label">👨‍🎓 Username</label>
                <input v-model="formData.username" type="text" class="field-input" placeholder="Enter username"
                  required />
              </div>

              <div class="form-field">
                <label class="field-label">🔒 Password</label>
                <input v-model="formData.password" type="password" class="field-input" placeholder="Enter password"
                  required />
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
                <input v-model="formData.class_section" type="text" class="field-input" placeholder="e.g., CS 4th E" />
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
                  We need to capture 3 photos of your face for better recognition accuracy
                </p>

                <!-- Photo Progress Indicator -->
                <div class="photo-progress" v-if="isCameraActive || capturedPhotos.length > 0">
                  <div class="progress-title">Photo Progress</div>
                  <div class="progress-photos">
                    <div v-for="i in 3" :key="i" class="progress-photo" :class="{
                      'captured': i <= capturedPhotos.length,
                      'current': i === capturedPhotos.length + 1 && isCameraActive && !isCapturing,
                      'capturing': i === capturedPhotos.length + 1 && isCapturing
                    }">
                      <div class="photo-number">{{ i }}</div>
                      <div class="photo-status">
                        <span v-if="i <= capturedPhotos.length">✓</span>
                        <span v-else-if="i === capturedPhotos.length + 1 && isCapturing"
                          class="capturing-spinner"></span>
                        <span v-else>📷</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="camera-container" :class="{ 'scanning': isCapturing, 'countdown': countdownActive }">
                <video ref="videoRef" v-show="isCameraActive && !allPhotosComplete" class="camera-feed" autoplay muted
                  playsinline></video>

                <canvas ref="canvasRef" v-show="false" class="capture-canvas"></canvas>

                <!-- Status Overlay -->
                <div class="status-overlay" v-if="!isCameraActive || allPhotosComplete">
                  <div class="status-indicator" :class="statusClass">
                    <div class="status-icon">{{ statusIcon }}</div>
                    <div class="status-text">{{ statusMessage }}</div>
                  </div>
                </div>

                <!-- Face Detection Frame -->
                <div class="face-frame" v-if="isCameraActive && !allPhotosComplete && !countdownActive">
                  <div class="frame-corner tl"></div>
                  <div class="frame-corner tr"></div>
                  <div class="frame-corner bl"></div>
                  <div class="frame-corner br"></div>
                  <div class="frame-instruction">Position your face here</div>
                </div>

                <!-- Countdown Overlay -->
                <div class="countdown-overlay" v-if="countdownActive">
                  <div class="countdown-circle">
                    <div class="countdown-number">{{ countdownNumber }}</div>
                  </div>
                  <div class="countdown-text">Get ready...</div>
                </div>

                <!-- Capturing Animation -->
                <div class="capturing-overlay" v-if="isCapturing && !countdownActive">
                  <div class="capture-flash"></div>
                  <div class="capturing-text">📸 Capturing photo {{ capturedPhotos.length + 1 }}/3</div>
                </div>

                <!-- Photo Preview -->
                <div class="photo-preview" v-if="allPhotosComplete && capturedPhotos.length > 0">
                  <div class="preview-title">Captured Photos</div>
                  <div class="preview-grid">
                    <div v-for="(photo, index) in capturedPhotos" :key="index" class="preview-item">
                      <img :src="photo" :alt="`Photo ${index + 1}`" class="preview-image" />
                      <div class="preview-label">Photo {{ index + 1 }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="capture-instructions">
                <div v-if="!isCameraActive && capturedPhotos.length === 0 && !cameraError" class="instruction">
                  📸 Click "Start Camera" to begin capturing 3 photos for face registration
                </div>
                <div v-else-if="cameraError" class="instruction error">
                  ❌ {{ cameraError }}
                </div>
                <div v-else-if="isCameraActive && !isCapturing && !countdownActive && capturedPhotos.length < 3"
                  class="instruction">
                  📹 Position your face in the frame and click "Capture Photo {{ capturedPhotos.length + 1 }}/3"
                </div>
                <div v-else-if="countdownActive" class="instruction">
                  ⏰ Get ready! Photo will be taken in {{ countdownNumber }} seconds
                </div>
                <div v-else-if="isCapturing" class="instruction">
                  📸 Hold still... Capturing photo {{ capturedPhotos.length + 1 }}/3
                </div>
                <div v-else-if="allPhotosComplete && !isProcessing" class="instruction success">
                  ✅ All 3 photos captured! Click "Register Face" to complete registration
                </div>
                <div v-else-if="isProcessing" class="instruction">
                  ⏳ Processing face data and training model... Please wait
                </div>
                <div v-else-if="registrationComplete && registrationSuccess" class="instruction success">
                  ✅ Face registered successfully!
                </div>
                <div v-else-if="registrationComplete && !registrationSuccess" class="instruction error">
                  ❌ Face registration failed. Please try again.
                </div>
              </div>

              <div class="capture-actions">
                <button @click="previousStep" class="btn-secondary"
                  :disabled="isCapturing || isProcessing || countdownActive">
                  ← Back
                </button>

                <button v-if="!isCameraActive && capturedPhotos.length === 0" @click="startCamera" :disabled="isLoading"
                  class="btn-primary">
                  <span v-if="isLoading" class="loading-spinner"></span>
                  {{ isLoading ? 'Starting Camera...' : '📸 Start Camera' }}
                </button>

                <button v-if="isCameraActive && !isCapturing && !countdownActive && capturedPhotos.length < 3"
                  @click="startPhotoCapture" class="btn-success">
                  📷 Capture Photo {{ capturedPhotos.length + 1 }}/3
                </button>

                <button v-if="allPhotosComplete && !isProcessing && !registrationComplete"
                  @click="registerFaceWithPhotos" class="btn-primary">
                  🎯 Register Face
                </button>

                <button v-if="registrationComplete && registrationSuccess" @click="completeRegistration"
                  class="btn-primary">
                  Complete Registration →
                </button>

                <button
                  v-if="(allPhotosComplete && !registrationSuccess) || (registrationComplete && !registrationSuccess)"
                  @click="resetCapture" class="btn-warning">
                  🔄 Try Again
                </button>

                <button v-if="capturedPhotos.length > 0 && capturedPhotos.length < 3 && !isCapturing"
                  @click="resetCapture" class="btn-secondary">
                  🔄 Start Over
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

// New 3-photo capture state
const capturedPhotos = ref<string[]>([])
const isCapturing = ref(false)
const countdownActive = ref(false)
const countdownNumber = ref(3)
const allPhotosComplete = ref(false)
const isProcessing = ref(false)
const registrationComplete = ref(false)
const registrationSuccess = ref(false)

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

  // Reset 3-photo capture state
  capturedPhotos.value = []
  isCapturing.value = false
  countdownActive.value = false
  countdownNumber.value = 3
  allPhotosComplete.value = false
  isProcessing.value = false
  registrationComplete.value = false
  registrationSuccess.value = false
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

// New 3-photo capture methods
const startPhotoCapture = async () => {
  if (!videoRef.value || !canvasRef.value) return

  // Start countdown
  countdownActive.value = true
  countdownNumber.value = 3

  const countdown = setInterval(() => {
    countdownNumber.value--
    if (countdownNumber.value <= 0) {
      clearInterval(countdown)
      countdownActive.value = false
      capturePhoto()
    }
  }, 1000)
}

const capturePhoto = async () => {
  if (!videoRef.value || !canvasRef.value) return

  try {
    isCapturing.value = true

    // Capture image from video
    const canvas = canvasRef.value
    const video = videoRef.value
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    const ctx = canvas.getContext('2d')
    if (!ctx) throw new Error('Canvas context not available')

    ctx.drawImage(video, 0, 0)
    const imageData = canvas.toDataURL('image/jpeg', 0.8)

    // Add to captured photos
    capturedPhotos.value.push(imageData)

    // Check if we have all 3 photos
    if (capturedPhotos.value.length >= 3) {
      allPhotosComplete.value = true
      stopCamera()
    }

    // Small delay for visual feedback
    await new Promise(resolve => setTimeout(resolve, 1000))

  } catch (error) {
    console.error('Photo capture error:', error)
  } finally {
    isCapturing.value = false
  }
}

const registerFaceWithPhotos = async () => {
  if (capturedPhotos.value.length < 3) return

  try {
    isProcessing.value = true
    statusMessage.value = 'Processing face data and training model...'

    // Register user first (only for new users)
    if (!props.existingUser) {
      await adminAPI.registerUser(formData.value)
    }

    // Register each photo with the scan_face API
    let successCount = 0

    for (let i = 0; i < capturedPhotos.value.length; i++) {
      try {
        const faceResponse = await adminAPI.scanFace({
          image: capturedPhotos.value[i].split(',')[1], // Remove data:image/jpeg;base64, prefix
          user_id: formData.value.user_id,
          name: formData.value.name
        })

        if (faceResponse.data.success) {
          successCount++
        }

        // Small delay between requests
        await new Promise(resolve => setTimeout(resolve, 500))

      } catch (error) {
        console.error(`Error registering photo ${i + 1}:`, error)
      }
    }

    // Check if registration was successful
    if (successCount > 0) {
      registrationSuccess.value = true
      statusMessage.value = `Face registered successfully with ${successCount}/3 photos!`
    } else {
      registrationSuccess.value = false
      statusMessage.value = 'Face registration failed. Please try again.'
    }

  } catch (error: any) {
    console.error('Registration error:', error)
    registrationSuccess.value = false
    statusMessage.value = error.response?.data?.message || 'Registration failed'
  } finally {
    isProcessing.value = false
    registrationComplete.value = true
  }
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

  0%,
  100% {
    transform: translateY(-100px);
  }

  50% {
    transform: translateY(100px);
  }
}

.scanning-text {
  margin-top: 1rem;
  color: white;
  font-weight: 600;
}

/* Photo Progress Indicator */
.photo-progress {
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.progress-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1rem;
  text-align: center;
}

.progress-photos {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.progress-photo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  min-width: 60px;
}

.progress-photo.captured {
  background: rgba(34, 197, 94, 0.2);
  border-color: rgba(34, 197, 94, 0.5);
}

.progress-photo.current {
  background: rgba(78, 205, 196, 0.2);
  border-color: rgba(78, 205, 196, 0.5);
  animation: pulse 2s ease-in-out infinite;
}

.progress-photo.capturing {
  background: rgba(138, 43, 226, 0.2);
  border-color: rgba(138, 43, 226, 0.5);
  animation: capturing 1s ease-in-out infinite;
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }
}

@keyframes capturing {

  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }

  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.photo-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
}

.progress-photo.captured .photo-number {
  background: #22c55e;
}

.progress-photo.current .photo-number {
  background: #4ecdc4;
}

.progress-photo.capturing .photo-number {
  background: #8A2BE2;
}

.photo-status {
  font-size: 1rem;
}

.capturing-spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* Face Frame Instruction */
.frame-instruction {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

/* Countdown Overlay */
.countdown-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.countdown-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  animation: countdownPulse 1s ease-in-out infinite;
}

@keyframes countdownPulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }
}

.countdown-number {
  font-size: 3rem;
  font-weight: bold;
  color: white;
}

.countdown-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
}

/* Capturing Overlay */
.capturing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(138, 43, 226, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.capture-flash {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: white;
  opacity: 0;
  animation: flash 0.3s ease-out;
}

@keyframes flash {
  0% {
    opacity: 0;
  }

  50% {
    opacity: 0.8;
  }

  100% {
    opacity: 0;
  }
}

.capturing-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Photo Preview */
.photo-preview {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  margin-top: 1rem;
}

.preview-title {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
  text-align: center;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.preview-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.preview-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.preview-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
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
  flex-wrap: wrap;
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
  min-width: 120px;
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
.btn-secondary:disabled,
.btn-success:disabled,
.btn-warning:disabled {
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
  0% {
    transform: scale(0);
  }

  50% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1);
  }
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

/* Face Capture Header */
.face-capture-header {
  text-align: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info h3 {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.user-info p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .registration-modal-overlay {
    padding: 1rem;
  }

  .registration-modal {
    max-width: 100%;
    max-height: 95vh;
  }

  .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .modal-title {
    font-size: 1.25rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .camera-container {
    max-width: 100%;
    height: 280px;
  }

  .step-indicator {
    margin-bottom: 2rem;
  }

  .step-divider {
    width: 40px;
    margin: 0 0.5rem;
  }

  .progress-photos {
    gap: 0.5rem;
  }

  .progress-photo {
    min-width: 50px;
    padding: 0.5rem;
  }

  .preview-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
  }

  .preview-image {
    width: 60px;
    height: 60px;
  }

  .form-actions,
  .capture-actions,
  .completion-actions {
    flex-direction: column;
    align-items: center;
  }

  .btn-primary,
  .btn-secondary,
  .btn-success,
  .btn-warning {
    width: 100%;
    max-width: 280px;
  }

  .countdown-circle {
    width: 100px;
    height: 100px;
  }

  .countdown-number {
    font-size: 2.5rem;
  }

  .frame-instruction {
    font-size: 0.625rem;
    padding: 0.25rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .registration-modal-overlay {
    padding: 0.5rem;
  }

  .modal-header {
    padding: 1rem;
  }

  .modal-body {
    padding: 1rem;
  }

  .camera-container {
    height: 240px;
  }

  .step-indicator {
    flex-direction: column;
    gap: 1rem;
  }

  .step-divider {
    width: 2px;
    height: 20px;
    margin: 0;
  }

  .progress-photos {
    flex-direction: row;
    justify-content: space-around;
  }

  .countdown-circle {
    width: 80px;
    height: 80px;
  }

  .countdown-number {
    font-size: 2rem;
  }

  .capturing-text {
    font-size: 1rem;
  }
}

/* Theme Support with CSS Custom Properties */
:root {
  --modal-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  --modal-border: rgba(255, 255, 255, 0.1);
  --text-primary: white;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.5);
  --accent-primary: linear-gradient(135deg, #8A2BE2, #4ecdc4);
  --accent-secondary: rgba(78, 205, 196, 0.2);
  --success-color: #22c55e;
  --error-color: #ef4444;
  --warning-color: #f59e0b;
  --overlay-bg: rgba(0, 0, 0, 0.8);
  --input-bg: rgba(255, 255, 255, 0.05);
  --input-border: rgba(255, 255, 255, 0.2);
  --input-focus: #4ecdc4;
}

/* Dark theme adjustments */
@media (prefers-color-scheme: dark) {
  :root {
    --modal-bg: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    --overlay-bg: rgba(0, 0, 0, 0.9);
  }
}

/* Light theme support */
@media (prefers-color-scheme: light) {
  :root {
    --modal-bg: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    --modal-border: rgba(0, 0, 0, 0.1);
    --text-primary: #1a202c;
    --text-secondary: rgba(26, 32, 44, 0.7);
    --text-muted: rgba(26, 32, 44, 0.5);
    --overlay-bg: rgba(255, 255, 255, 0.9);
    --input-bg: rgba(0, 0, 0, 0.05);
    --input-border: rgba(0, 0, 0, 0.2);
  }

  .registration-modal {
    background: var(--modal-bg);
    color: var(--text-primary);
  }

  .field-input {
    color: var(--text-primary);
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

uctions {
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
  0% {
    transform: scale(0);
  }

  50% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1);
  }
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
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>
