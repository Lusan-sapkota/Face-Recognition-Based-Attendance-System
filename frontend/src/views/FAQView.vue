<template>
  <div class="faq">
    <div class="container">
      <div class="faq-header">
        <h1 class="faq-title gradient-text">Frequently Asked Questions</h1>
        <p class="faq-subtitle">Find answers to common questions about our face recognition attendance system</p>
      </div>

      <div class="faq-content">
        <div class="faq-search">
          <div class="search-box">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search questions..." 
              class="search-input"
            />
            <div class="search-icon">🔍</div>
          </div>
        </div>

        <div class="faq-categories">
          <button 
            v-for="category in categories" 
            :key="category"
            @click="activeCategory = category"
            class="category-btn"
            :class="{ active: activeCategory === category }"
          >
            {{ category }}
          </button>
        </div>

        <div class="faq-items">
          <div 
            v-for="(faq, index) in filteredFAQs" 
            :key="index"
            class="faq-item card"
          >
            <div 
              class="faq-question" 
              @click="toggleFAQ(index)"
              :class="{ active: openFAQs.includes(index) }"
            >
              <h3>{{ faq.question }}</h3>
              <div class="faq-toggle">
                {{ openFAQs.includes(index) ? '−' : '+' }}
              </div>
            </div>
            <div 
              v-if="openFAQs.includes(index)" 
              class="faq-answer"
            >
              <div v-html="faq.answer"></div>
            </div>
          </div>
        </div>

        <div v-if="filteredFAQs.length === 0" class="no-results">
          <div class="no-results-icon">🤔</div>
          <h3>No questions found</h3>
          <p>Try adjusting your search terms or browse different categories</p>
        </div>
      </div>

      <!-- Contact Support -->
      <div class="support-section card">
        <div class="support-content">
          <h3>Still have questions?</h3>
          <p>Can't find what you're looking for? Our support team is here to help.</p>
          <div class="support-actions">
            <a href="mailto:support@recognizeme.com" class="btn btn-primary">
              Contact Support
            </a>
            <RouterLink to="/" class="btn btn-secondary">
              Back to Home
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface FAQ {
  question: string
  answer: string
  category: string
}

const searchQuery = ref('')
const activeCategory = ref('All')
const openFAQs = ref<number[]>([])

const categories = ['All', 'Getting Started', 'Security', 'Technical', 'Account', 'Troubleshooting']

const faqs: FAQ[] = [
  // Getting Started
  {
    question: "How does the face recognition attendance system work?",
    answer: "Our system uses advanced AI algorithms to capture and analyze facial features. When you register, we capture multiple images of your face to create a unique biometric template. During attendance marking, the system compares your live face with the stored template to verify your identity and mark attendance automatically.",
    category: "Getting Started"
  },
  {
    question: "How accurate is the face recognition system?",
    answer: "Our system boasts 99.9% accuracy rate. We use state-of-the-art deep learning models that can accurately identify faces even with changes in lighting, angles, and minor appearance changes like glasses or facial hair.",
    category: "Getting Started"
  },
  {
    question: "What do I need to get started?",
    answer: "To get started, you need:<ul><li>A device with a camera (laptop, desktop with webcam, or mobile device)</li><li>Good lighting conditions</li><li>Registration by an administrator</li><li>Your username and password for login</li></ul>",
    category: "Getting Started"
  },
  
  // Security
  {
    question: "Is my facial data secure?",
    answer: "Absolutely! We take security very seriously:<ul><li>All biometric data is encrypted using AES-256 encryption</li><li>Data is stored locally and never transmitted to external servers</li><li>We use secure hashing algorithms to protect your facial templates</li><li>Access is restricted to authorized administrators only</li></ul>",
    category: "Security"
  },
  {
    question: "Can someone use my photo to mark attendance?",
    answer: "No, our system includes advanced liveness detection that can distinguish between a real person and a photograph. It analyzes subtle facial movements, depth information, and other factors to ensure only live faces can mark attendance.",
    category: "Security"
  },
  {
    question: "What happens if I lose access to my account?",
    answer: "If you lose access to your account, contact your administrator immediately. They can reset your password and help you regain access. For security reasons, only administrators can modify user accounts.",
    category: "Security"
  },

  // Technical
  {
    question: "What browsers are supported?",
    answer: "Our system works best with modern browsers that support WebRTC for camera access:<ul><li>Chrome 60+ (recommended)</li><li>Firefox 55+</li><li>Safari 11+</li><li>Edge 79+</li></ul>Make sure to allow camera permissions when prompted.",
    category: "Technical"
  },
  {
    question: "Why is the camera not working?",
    answer: "If the camera isn't working, try these steps:<ol><li>Check if camera permissions are enabled for the website</li><li>Close other applications that might be using the camera</li><li>Refresh the page and try again</li><li>Check if your camera is properly connected</li><li>Try using a different browser</li></ol>",
    category: "Technical"
  },
  {
    question: "What are the minimum system requirements?",
    answer: "Minimum requirements:<ul><li>CPU: Dual-core 2.0 GHz or higher</li><li>RAM: 4GB minimum, 8GB recommended</li><li>Camera: 720p resolution minimum</li><li>Internet: Stable broadband connection</li><li>Browser: Modern browser with WebRTC support</li></ul>",
    category: "Technical"
  },

  // Account
  {
    question: "How do I update my profile information?",
    answer: "To update your profile:<ol><li>Log in to your dashboard</li><li>Navigate to the Profile section</li><li>Click 'Edit Profile' to modify your information</li><li>Save your changes</li></ol>Note: Some information like User ID may require administrator approval to change.",
    category: "Account"
  },
  {
    question: "Can I change my password?",
    answer: "Yes, you can change your password from your dashboard. Go to Profile → Security Settings → Change Password. If you've forgotten your current password, contact your administrator for a password reset.",
    category: "Account"
  },
  {
    question: "How do I view my attendance history?",
    answer: "You can view your attendance history from your dashboard. The Analytics section shows your attendance patterns, including:<ul><li>Daily attendance records</li><li>Monthly attendance statistics</li><li>Attendance trends and patterns</li><li>Detailed attendance reports</li></ul>",
    category: "Account"
  },

  // Troubleshooting
  {
    question: "Face recognition is not working properly. What should I do?",
    answer: "If face recognition isn't working:<ol><li>Ensure good lighting - avoid backlighting</li><li>Position your face directly in front of the camera</li><li>Remove any obstructions like hats or masks</li><li>Clean your camera lens</li><li>Try recapturing your face data with an administrator</li></ol>",
    category: "Troubleshooting"
  },
  {
    question: "The system says 'No face detected'. How to fix this?",
    answer: "This usually happens due to:<ul><li>Poor lighting conditions</li><li>Camera not properly positioned</li><li>Face too far from or too close to camera</li><li>Camera permissions not granted</li></ul>Try adjusting lighting, positioning, and camera settings.",
    category: "Troubleshooting"
  },
  {
    question: "Attendance marking is slow. How can I improve it?",
    answer: "To improve speed:<ul><li>Ensure stable internet connection</li><li>Use good lighting for faster face detection</li><li>Position yourself properly in front of camera</li><li>Close unnecessary browser tabs/applications</li><li>Clear browser cache if needed</li></ul>",
    category: "Troubleshooting"
  },
  {
    question: "I'm getting 'Network Error'. What does this mean?",
    answer: "Network errors usually indicate connectivity issues:<ol><li>Check your internet connection</li><li>Verify the server is running (for administrators)</li><li>Try refreshing the page</li><li>Check if firewall is blocking the application</li><li>Contact your administrator if the problem persists</li></ol>",
    category: "Troubleshooting"
  }
]

const filteredFAQs = computed(() => {
  let filtered = faqs

  // Filter by category
  if (activeCategory.value !== 'All') {
    filtered = filtered.filter(faq => faq.category === activeCategory.value)
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(faq => 
      faq.question.toLowerCase().includes(query) || 
      faq.answer.toLowerCase().includes(query)
    )
  }

  return filtered
})

const toggleFAQ = (index: number) => {
  const faqIndex = openFAQs.value.indexOf(index)
  if (faqIndex > -1) {
    openFAQs.value.splice(faqIndex, 1)
  } else {
    openFAQs.value.push(index)
  }
}
</script>

<style scoped>
.faq {
  padding: 40px 0;
  min-height: calc(100vh - 80px);
}

.faq-header {
  text-align: center;
  margin-bottom: 60px;
}

.faq-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.faq-subtitle {
  font-size: 1.2rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.faq-content {
  max-width: 800px;
  margin: 0 auto;
}

/* Search */
.faq-search {
  margin-bottom: 40px;
}

.search-box {
  position: relative;
  max-width: 400px;
  margin: 0 auto;
}

.search-input {
  width: 100%;
  padding: 16px 50px 16px 20px;
  border: 2px solid var(--border-color);
  border-radius: 50px;
  font-size: 16px;
  background: var(--input-background);
  color: var(--text-primary);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 191, 255, 0.1);
}

.search-icon {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: var(--text-secondary);
}

/* Categories */
.faq-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin-bottom: 40px;
}

.category-btn {
  padding: 10px 20px;
  border: 2px solid var(--border-color);
  border-radius: 25px;
  background: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-btn:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.category-btn.active {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

/* FAQ Items */
.faq-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 60px;
}

.faq-item {
  padding: 0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid transparent;
}

.faq-question:hover {
  background: rgba(0, 191, 255, 0.05);
}

.faq-question.active {
  background: rgba(0, 191, 255, 0.1);
  border-bottom-color: var(--border-color);
}

.faq-question h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
  padding-right: 16px;
}

.faq-toggle {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  font-size: 18px;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.faq-question.active .faq-toggle {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 24px 24px 24px;
  color: var(--text-secondary);
  line-height: 1.6;
  animation: fadeIn 0.3s ease;
}

.faq-answer :deep(ul),
.faq-answer :deep(ol) {
  margin: 12px 0;
  padding-left: 24px;
}

.faq-answer :deep(li) {
  margin-bottom: 8px;
}

/* No Results */
.no-results {
  text-align: center;
  padding: 60px 20px;
}

.no-results-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.no-results p {
  color: var(--text-secondary);
}

/* Support Section */
.support-section {
  padding: 40px;
  text-align: center;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
}

.support-content h3 {
  font-size: 1.5rem;
  margin-bottom: 12px;
}

.support-content p {
  margin-bottom: 24px;
  opacity: 0.9;
}

.support-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.support-actions .btn {
  min-width: 150px;
}

.support-actions .btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.support-actions .btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Responsive */
@media (max-width: 768px) {
  .faq {
    padding: 20px 0;
  }

  .faq-title {
    font-size: 2rem;
  }

  .faq-subtitle {
    font-size: 1rem;
  }

  .faq-categories {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 8px;
  }

  .category-btn {
    white-space: nowrap;
    flex-shrink: 0;
  }

  .faq-question {
    padding: 20px 16px;
  }

  .faq-answer {
    padding: 0 16px 20px 16px;
  }

  .support-section {
    padding: 24px 20px;
  }

  .support-actions {
    flex-direction: column;
    align-items: center;
  }

  .support-actions .btn {
    width: 100%;
    max-width: 250px;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
