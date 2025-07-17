<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title gradient-text">
              Smart Attendance System
            </h1>
            <p class="hero-subtitle">
              Experience the future of attendance tracking with our AI-powered face recognition technology. 
              Secure, accurate, and efficient attendance management for educational institutions and workplaces.
            </p>
            <div class="hero-actions">
              <RouterLink to="/login" class="btn btn-primary hero-btn">
                Get Started
              </RouterLink>
              <button @click="scrollToFeatures" class="btn btn-secondary hero-btn">
                Learn More
              </button>
            </div>
          </div>
          <div class="hero-visual">
            <div class="floating-card">
              <div class="face-scan-animation">
                <div class="scan-line"></div>
                <div class="face-outline"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title gradient-text">Why Choose RecognizeMe?</h2>
          <p class="section-subtitle">
            Cutting-edge technology meets simplicity for seamless attendance management
          </p>
        </div>
        
        <div class="grid grid-cols-3 features-grid">
          <div class="feature-card card fade-in">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4"></path>
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
            </div>
            <h3 class="feature-title">99.9% Accuracy</h3>
            <p class="feature-description">
              Advanced AI algorithms ensure precise face recognition with minimal false positives
            </p>
          </div>

          <div class="feature-card card fade-in">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <circle cx="12" cy="16" r="1"></circle>
                <path d="m7 11 0 0a5 5 0 0 1 10 0"></path>
              </svg>
            </div>
            <h3 class="feature-title">Secure & Private</h3>
            <p class="feature-description">
              Your biometric data is encrypted and stored securely with enterprise-grade security
            </p>
          </div>

          <div class="feature-card card fade-in">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
              </svg>
            </div>
            <h3 class="feature-title">Lightning Fast</h3>
            <p class="feature-description">
              Process attendance in under 2 seconds with real-time face recognition technology
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats">
      <div class="container">
        <div class="grid grid-cols-4 stats-grid">
          <div class="stat-item text-center fade-in">
            <div class="stat-number gradient-text">5000+</div>
            <div class="stat-label">Active Users</div>
          </div>
          <div class="stat-item text-center fade-in">
            <div class="stat-number gradient-text">99.9%</div>
            <div class="stat-label">Accuracy Rate</div>
          </div>
          <div class="stat-item text-center fade-in">
            <div class="stat-number gradient-text">1M+</div>
            <div class="stat-label">Attendance Records</div>
          </div>
          <div class="stat-item text-center fade-in">
            <div class="stat-number gradient-text">24/7</div>
            <div class="stat-label">System Uptime</div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title gradient-text">How It Works</h2>
          <p class="section-subtitle">Simple, fast, and reliable attendance tracking in 3 easy steps</p>
        </div>
        
        <div class="steps">
          <div class="step fade-in">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3 class="step-title">Register Your Face</h3>
              <p class="step-description">
                Quick and secure facial data capture using advanced computer vision technology
              </p>
            </div>
          </div>
          
          <div class="step fade-in">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3 class="step-title">Look at Camera</h3>
              <p class="step-description">
                Simply face the camera for instant recognition and attendance marking
              </p>
            </div>
          </div>
          
          <div class="step fade-in">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3 class="step-title">Attendance Recorded</h3>
              <p class="step-description">
                Automatic attendance logging with timestamp and comprehensive reporting
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Demo Section -->
    <section class="demo">
      <div class="container">
        <div class="demo-content">
          <div class="demo-header text-center">
            <h2 class="section-title gradient-text">Try the Demo</h2>
            <p class="section-subtitle">
              Experience the full functionality with our demo credentials
            </p>
          </div>
          
          <div class="demo-cards">
            <div class="demo-card card">
              <div class="demo-card-header">
                <div class="demo-icon user-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                  </svg>
                </div>
                <h3 class="demo-title">User Demo</h3>
              </div>
              <div class="demo-credentials">
                <div class="credential-item">
                  <span class="credential-label">Username:</span>
                  <code class="credential-value">demo_user</code>
                </div>
                <div class="credential-item">
                  <span class="credential-label">Password:</span>
                  <code class="credential-value">demo123</code>
                </div>
              </div>
              <RouterLink to="/login" class="btn btn-secondary demo-btn">
                Try User Demo
              </RouterLink>
            </div>

            <div class="demo-card card">
              <div class="demo-card-header">
                <div class="demo-icon admin-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
                  </svg>
                </div>
                <h3 class="demo-title">Admin Demo</h3>
              </div>
              <div class="demo-credentials">
                <div class="credential-item">
                  <span class="credential-label">Password:</span>
                  <code class="credential-value">admin123</code>
                </div>
              </div>
              <RouterLink to="/admin/login" class="btn btn-primary demo-btn">
                Try Admin Demo
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Backend Notice Section -->
    <section class="backend-notice">
      <div class="container">
        <div class="notice-card card">
          <div class="notice-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M12 6v6l4 2"></path>
            </svg>
          </div>
          <div class="notice-content">
            <h3 class="notice-title">Frontend Demo Notice</h3>
            <p class="notice-text">
              This is a frontend-only demo for showcase purposes. The complete application with full backend functionality, 
              including face recognition, database operations, and real-time attendance tracking, is available in our 
              GitHub repository.
            </p>
            <div class="notice-actions">
              <a 
                href="https://github.com/Lusan-sapkota/Face-Recognition-Based-Attendance-System" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="btn btn-outline github-btn"
              >
                <svg viewBox="0 0 24 24" fill="currentColor" class="github-icon">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                View Full Project
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta">
      <div class="container">
        <div class="cta-content text-center">
          <h2 class="cta-title gradient-text">Ready to Transform Your Attendance System?</h2>
          <p class="cta-subtitle">
            Join thousands of organizations already using RecognizeMe for their attendance needs
          </p>
          <RouterLink to="/login" class="btn btn-primary cta-btn">
            Start Now - It's Free
          </RouterLink>
        </div>
      </div>
    </section>
    
    <!-- Admin Access Footer -->
    <footer class="admin-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-links">
            <RouterLink to="/faq" class="footer-link">
              Frequently Asked Questions
            </RouterLink>
          </div>
          <div class="admin-access">
            <RouterLink to="/admin/login" class="admin-link">
              Administrator Access
            </RouterLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const scrollToFeatures = () => {
  const element = document.getElementById('features')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
/* Hero Section */
.hero {
  padding: 80px 0 120px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at center, rgba(0, 191, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 24px;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 40px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-btn {
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
}

/* Hero Visual */
.floating-card {
  position: relative;
  background: var(--card-background);
  backdrop-filter: blur(20px);
  border: 1px solid var(--card-border);
  border-radius: 24px;
  padding: 60px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.face-scan-animation {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.face-outline {
  width: 100%;
  height: 100%;
  border: 3px solid var(--accent-color);
  border-radius: 50%;
  position: relative;
  opacity: 0.7;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, var(--gradient-start) 50%, transparent 100%);
  animation: scan 2s ease-in-out infinite;
}

@keyframes scan {
  0% { transform: translateY(0); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(200px); opacity: 0; }
}

/* Features Section */
.features {
  padding: 120px 0;
  background: rgba(255, 255, 255, 0.02);
}

.section-header {
  text-align: center;
  margin-bottom: 80px;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  gap: 40px;
}

.feature-card {
  text-align: center;
  padding: 40px 24px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.feature-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 24px;
  padding: 16px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Stats Section */
.stats {
  padding: 80px 0;
}

.stats-grid {
  gap: 40px;
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 1rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* How It Works */
.how-it-works {
  padding: 120px 0;
  background: rgba(255, 255, 255, 0.02);
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 60px;
  max-width: 800px;
  margin: 0 auto;
}

.step {
  display: flex;
  align-items: center;
  gap: 40px;
}

.step:nth-child(even) {
  flex-direction: row-reverse;
}

.step-number {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-primary);
}

.step-description {
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Demo Section */
.demo {
  padding: 120px 0;
  background: rgba(255, 255, 255, 0.02);
}

.demo-content {
  max-width: 1000px;
  margin: 0 auto;
}

.demo-header {
  margin-bottom: 60px;
}

.demo-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.demo-card {
  padding: 40px 32px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 20px;
}

.demo-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.4);
}

.demo-card-header {
  margin-bottom: 32px;
}

.demo-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  padding: 16px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.demo-icon.user-icon {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
}

.demo-icon.admin-icon {
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
}

.demo-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.demo-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.demo-credentials {
  margin-bottom: 32px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.credential-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.credential-item:last-child {
  margin-bottom: 0;
}

.credential-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.credential-value {
  background: rgba(0, 191, 255, 0.1);
  color: var(--accent-color);
  padding: 6px 12px;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid rgba(0, 191, 255, 0.2);
}

.demo-btn {
  width: 100%;
  padding: 16px 24px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  transition: all 0.3s ease;
}

/* Backend Notice Section */
.backend-notice {
  padding: 80px 0;
}

.notice-card {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  padding: 40px;
  max-width: 900px;
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1) 0%, rgba(255, 152, 0, 0.1) 100%);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.notice-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ffc107 0%, #ff9800 100%);
}

.notice-icon {
  width: 48px;
  height: 48px;
  padding: 12px;
  background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notice-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.notice-content {
  flex: 1;
}

.notice-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.notice-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 24px;
  font-size: 0.95rem;
}

.notice-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.github-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.3s ease;
  text-decoration: none;
}

.github-icon {
  width: 18px;
  height: 18px;
}

/* CTA Section */
.cta {
  padding: 120px 0;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.cta-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 40px;
}

.cta-btn {
  padding: 20px 40px;
  font-size: 18px;
  font-weight: 600;
}

/* Admin Footer */
.admin-footer {
  padding: 20px 0;
  background: rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 20px;
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85em;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.footer-link:hover {
  opacity: 1;
  color: var(--primary-color);
}

.admin-access {
  text-align: center;
}

.admin-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85em;
  opacity: 0.7;
  transition: all 0.3s ease;
}

.admin-link:hover {
  opacity: 1;
  color: var(--primary-color);
}

/* Enhanced Responsive Design - Mobile First Approach */

/* Base Mobile Styles (320px+) */
.home {
  min-height: 100vh;
  overflow-x: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}

/* Hero Section - Mobile First */
.hero {
  padding: 60px 0 80px;
  position: relative;
  overflow: hidden;
  min-height: 70vh;
  display: flex;
  align-items: center;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at center, rgba(0, 191, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  align-items: center;
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-text {
  order: 2;
  width: 100%;
}

.hero-visual {
  order: 1;
  width: 100%;
  max-width: 280px;
}

.hero-title {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 2rem;
  max-width: 100%;
}

.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.hero-btn {
  padding: 0.875rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  width: 100%;
  text-align: center;
  border-radius: 12px;
  transition: all 0.3s ease;
}

/* Hero Visual */
.floating-card {
  position: relative;
  background: var(--card-background);
  backdrop-filter: blur(20px);
  border: 1px solid var(--card-border);
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: float 6s ease-in-out infinite;
  width: 100%;
  max-width: 280px;
  margin: 0 auto;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-15px); }
}

.face-scan-animation {
  position: relative;
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.face-outline {
  width: 100%;
  height: 100%;
  border: 3px solid var(--accent-color);
  border-radius: 50%;
  position: relative;
  opacity: 0.7;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent 0%, var(--gradient-start) 50%, transparent 100%);
  animation: scan 2s ease-in-out infinite;
}

@keyframes scan {
  0% { transform: translateY(0); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(120px); opacity: 0; }
}

/* Features Section */
.features {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.02);
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  max-width: 100%;
  margin: 0 auto;
  line-height: 1.6;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 16px;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.feature-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1.5rem;
  padding: 12px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.feature-description {
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Stats Section */
.stats {
  padding: 60px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.05);
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  display: block;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* How It Works */
.how-it-works {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.02);
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  max-width: 100%;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
  padding: 2rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.step:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.05);
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
  box-shadow: 0 8px 25px rgba(0, 191, 255, 0.3);
}

.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.step-description {
  color: var(--text-secondary);
  line-height: 1.6;
  font-size: 0.95rem;
  max-width: 400px;
}

/* CTA Section */
.cta {
  padding: 80px 0;
}

.cta-content {
  max-width: 100%;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.cta-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-btn {
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  display: inline-block;
}

/* Admin Footer */
.admin-footer {
  padding: 1.5rem 0;
  background: rgba(0, 0, 0, 0.1);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: center;
  align-items: center;
}

.footer-links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85em;
  opacity: 0.7;
  transition: all 0.3s ease;
  padding: 0.5rem;
}

.footer-link:hover {
  opacity: 1;
  color: var(--primary-color);
}

.admin-access {
  text-align: center;
}

.admin-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85em;
  opacity: 0.7;
  transition: all 0.3s ease;
  padding: 0.5rem;
}

.admin-link:hover {
  opacity: 1;
  color: var(--primary-color);
}

/* Tablet Styles (576px+) */
@media (min-width: 576px) {
  .container {
    padding: 0 1.5rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.125rem;
  }
  
  .hero-actions {
    flex-direction: row;
    max-width: 400px;
    gap: 1rem;
  }
  
  .hero-btn {
    width: auto;
    padding: 1rem 2rem;
  }
  
  .floating-card {
    padding: 3rem;
    max-width: 320px;
  }
  
  .face-scan-animation {
    width: 150px;
    height: 150px;
  }
  
  @keyframes scan {
    0% { transform: translateY(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(150px); opacity: 0; }
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .section-subtitle {
    font-size: 1.125rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
  
  .stat-label {
    font-size: 0.9rem;
  }
  
  .feature-icon {
    width: 56px;
    height: 56px;
    padding: 14px;
  }
  
  .feature-icon svg {
    width: 28px;
    height: 28px;
  }
  
  .feature-title {
    font-size: 1.375rem;
  }
  
  .step-number {
    width: 70px;
    height: 70px;
    font-size: 1.75rem;
  }
  
  .step-title {
    font-size: 1.375rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
  
  .cta-subtitle {
    font-size: 1.125rem;
  }
  
  .cta-btn {
    width: auto;
    padding: 1.25rem 2.5rem;
    font-size: 1.125rem;
  }
  
  .footer-content {
    flex-direction: row;
    justify-content: space-between;
  }
}

/* Large Tablet Styles (768px+) */
@media (min-width: 768px) {
  .container {
    padding: 0 2rem;
  }
  
  .hero {
    padding: 80px 0 100px;
    min-height: 80vh;
  }
  
  .hero-content {
    flex-direction: row;
    gap: 3rem;
    text-align: left;
    align-items: center;
  }
  
  .hero-text {
    order: 1;
    flex: 1;
  }
  
  .hero-visual {
    order: 2;
    flex: 0 0 auto;
    max-width: 350px;
  }
  
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1.25rem;
    max-width: 90%;
  }
  
  .hero-actions {
    justify-content: flex-start;
    max-width: none;
  }
  
  .floating-card {
    padding: 3.5rem;
    max-width: 350px;
  }
  
  .face-scan-animation {
    width: 180px;
    height: 180px;
  }
  
  @keyframes scan {
    0% { transform: translateY(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(180px); opacity: 0; }
  }
  
  .features {
    padding: 100px 0;
  }
  
  .section-header {
    margin-bottom: 4rem;
  }
  
  .section-title {
    font-size: 2.25rem;
  }
  
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5rem;
  }
  
  .feature-card {
    padding: 2.5rem 2rem;
  }
  
  .feature-icon {
    width: 64px;
    height: 64px;
    padding: 16px;
  }
  
  .feature-icon svg {
    width: 32px;
    height: 32px;
  }
  
  .feature-title {
    font-size: 1.5rem;
  }
  
  .stats {
    padding: 80px 0;
  }
  
  .stat-number {
    font-size: 3rem;
  }
  
  .how-it-works {
    padding: 100px 0;
  }
  
  .steps {
    max-width: 800px;
    gap: 4rem;
  }
  
  .step {
    flex-direction: row;
    text-align: left;
    gap: 2rem;
    padding: 2.5rem;
  }
  
  .step:nth-child(even) {
    flex-direction: row-reverse;
  }
  
  .step-number {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .step-content {
    flex: 1;
  }
  
  .step-title {
    font-size: 1.5rem;
  }
  
  .cta {
    padding: 100px 0;
  }
  
  .cta-title {
    font-size: 2.25rem;
  }
  
  .cta-btn {
    font-size: 1.25rem;
    padding: 1.5rem 3rem;
  }
}

/* Desktop Styles (1024px+) */
@media (min-width: 1024px) {
  .container {
    padding: 0 2.5rem;
  }
  
  .hero {
    min-height: 85vh;
  }
  
  .hero-content {
    gap: 4rem;
  }
  
  .hero-title {
    font-size: 3.5rem;
  }
  
  .hero-subtitle {
    max-width: 85%;
  }
  
  .floating-card {
    padding: 4rem;
    max-width: 400px;
  }
  
  .face-scan-animation {
    width: 200px;
    height: 200px;
  }
  
  @keyframes scan {
    0% { transform: translateY(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(200px); opacity: 0; }
  }
  
  .section-title {
    font-size: 2.5rem;
  }
  
  .features-grid {
    gap: 3rem;
  }
  
  .feature-card {
    padding: 3rem 2.5rem;
  }
  
  .steps {
    gap: 5rem;
  }
  
  .step {
    padding: 3rem;
    gap: 2.5rem;
  }
  
  .cta-title {
    font-size: 2.5rem;
  }
}

/* Large Desktop Styles (1200px+) */
@media (min-width: 1200px) {
  .container {
    max-width: 1200px;
    padding: 0 3rem;
  }
  
  .hero {
    padding: 100px 0 120px;
  }
  
  .hero-content {
    gap: 5rem;
  }
  
  .floating-card {
    padding: 5rem;
  }
  
  .features {
    padding: 120px 0;
  }
  
  .section-header {
    margin-bottom: 5rem;
  }
  
  .features-grid {
    gap: 3.5rem;
  }
  
  .feature-card {
    padding: 3.5rem 3rem;
  }
  
  .how-it-works {
    padding: 120px 0;
  }
  
  .cta {
    padding: 120px 0;
  }
  
  .cta-content {
    max-width: 800px;
  }
}

/* Extra Large Desktop Styles (1400px+) */
@media (min-width: 1400px) {
  .container {
    max-width: 1400px;
  }
  
  .hero-content {
    gap: 6rem;
  }
  
  .features-grid {
    gap: 4rem;
  }
  
  .feature-card {
    padding: 4rem 3.5rem;
  }
}

/* Landscape Mobile Support */
@media (max-width: 767px) and (orientation: landscape) {
  .hero {
    min-height: 90vh;
    padding: 40px 0 60px;
  }
  
  .hero-content {
    flex-direction: row;
    gap: 2rem;
  }
  
  .hero-text {
    flex: 1;
  }
  
  .hero-visual {
    flex: 0 0 auto;
    max-width: 250px;
  }
  
  .floating-card {
    padding: 2rem;
  }
  
  .face-scan-animation {
    width: 100px;
    height: 100px;
  }
  
  @keyframes scan {
    0% { transform: translateY(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(100px); opacity: 0; }
  }
  
  .hero-title {
    font-size: 2.25rem;
  }
  
  .hero-actions {
    flex-direction: row;
    gap: 1rem;
  }
  
  .hero-btn {
    width: auto;
    padding: 0.75rem 1.5rem;
    font-size: 0.9rem;
  }
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .floating-card {
    animation: none;
  }
  
  .scan-line {
    animation: none;
    opacity: 0.5;
  }
  
  .feature-card,
  .stat-item,
  .step {
    transition: none;
  }
  
  .feature-card:hover,
  .stat-item:hover,
  .step:hover {
    transform: none;
  }
}

/* High Contrast Mode Support */
@media (prefers-contrast: high) {
  .hero::before {
    display: none;
  }
  
  .floating-card,
  .feature-card,
  .stat-item,
  .step {
    border: 2px solid currentColor;
  }
  
  .feature-icon,
  .step-number {
    border: 2px solid white;
  }
}

/* Print Styles */
@media print {
  .hero::before,
  .floating-card,
  .admin-footer {
    display: none;
  }
  
  .hero {
    padding: 20px 0;
    page-break-after: always;
  }
  
  .hero-content {
    flex-direction: column;
    text-align: center;
  }
  
  .features,
  .stats,
  .how-it-works,
  .cta {
    padding: 20px 0;
    page-break-inside: avoid;
  }
  
  .features-grid,
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .step {
    flex-direction: column;
    text-align: center;
    page-break-inside: avoid;
  }
}
</style>
