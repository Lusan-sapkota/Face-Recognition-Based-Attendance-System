// Mock authentication service for frontend-only demo
export const mockAuthAPI = {
  adminLogin: async (password: string) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (password === 'admin123') {
      return {
        data: {
          access_token: 'mock-admin-token',
          role: 'admin',
          user: {
            id: 'admin',
            name: 'Demo Admin',
            type: 'admin'
          }
        }
      }
    } else {
      throw {
        response: {
          data: {
            message: 'Invalid admin credentials'
          }
        }
      }
    }
  },

  userLogin: async (username: string, password: string) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (username === 'demo_user' && password === 'demo123') {
      return {
        data: {
          access_token: 'mock-user-token',
          role: 'user',
          user: {
            id: 'demo_user',
            name: 'Demo User',
            type: 'student',
            class_section: 'Demo Class'
          }
        }
      }
    } else {
      throw {
        response: {
          data: {
            message: 'Invalid credentials'
          }
        }
      }
    }
  }
}

// Mock dashboard data
export const mockDashboardAPI = {
  getStats: async () => {
    await new Promise(resolve => setTimeout(resolve, 800))
    return {
      data: {
        total_users: 25,
        today_attendance: 18,
        present_today: 18,
        absent_today: 7,
        students_present: 15,
        employees_present: 3,
        attendance_rate: 72.0,
        attendance_data: [
          { Name: 'Demo User', Roll: 'demo_user', Time: '09:15:30', Type: 'student' },
          { Name: 'John Doe', Roll: 'john_001', Time: '09:20:15', Type: 'student' },
          { Name: 'Jane Smith', Roll: 'jane_002', Time: '09:25:45', Type: 'teacher' }
        ]
      }
    }
  },

  getAttendance: async () => {
    await new Promise(resolve => setTimeout(resolve, 600))
    return {
      data: {
        attendance: [
          { Name: 'Demo User', Roll: 'demo_user', Time: '09:15:30', Type: 'student' },
          { Name: 'John Doe', Roll: 'john_001', Time: '09:20:15', Type: 'student' },
          { Name: 'Jane Smith', Roll: 'jane_002', Time: '09:25:45', Type: 'teacher' },
          { Name: 'Bob Wilson', Roll: 'bob_003', Time: '09:30:20', Type: 'student' },
          { Name: 'Alice Brown', Roll: 'alice_004', Time: '09:35:10', Type: 'staff' }
        ]
      }
    }
  },

  startAttendance: async () => {
    await new Promise(resolve => setTimeout(resolve, 2000))
    return {
      data: {
        message: 'Demo: Face recognition attendance completed',
        recognized_users: ['demo_user', 'john_001']
      }
    }
  }
}

// Mock admin data
export const mockAdminAPI = {
  getUsers: async () => {
    await new Promise(resolve => setTimeout(resolve, 800))
    return {
      data: {
        users: [
          {
            id: 'demo_user',
            name: 'Demo User',
            username: 'demo_user',
            type: 'student',
            class_section: 'Demo Class',
            registered_date: '2024-01-15',
            has_face_data: true,
            has_password: true
          },
          {
            id: 'john_001',
            name: 'John Doe',
            username: 'john_doe',
            type: 'student',
            class_section: 'CS 4th A',
            registered_date: '2024-01-16',
            has_face_data: true,
            has_password: true
          },
          {
            id: 'jane_002',
            name: 'Jane Smith',
            username: 'jane_smith',
            type: 'teacher',
            class_section: 'Computer Science',
            registered_date: '2024-01-17',
            has_face_data: false,
            has_password: true
          }
        ]
      }
    }
  },

  getNotices: async () => {
    await new Promise(resolve => setTimeout(resolve, 600))
    return {
      data: {
        notices: [
          {
            id: 1,
            title: 'Welcome to Demo Mode',
            content: 'This is a frontend-only demo. Full functionality available in the complete system.',
            priority: 'high',
            created_date: '2024-07-18',
            created_by: 'admin'
          },
          {
            id: 2,
            title: 'System Maintenance',
            content: 'Demo system is running smoothly. All features are simulated.',
            priority: 'normal',
            created_date: '2024-07-17',
            created_by: 'admin'
          }
        ]
      }
    }
  },

  getAttendanceHistory: async () => {
    await new Promise(resolve => setTimeout(resolve, 800))
    return {
      data: {
        history: {
          '07_18_25': [
            { user_id: 'demo_user', name: 'Demo User', time: '09:15:30', type: 'student' },
            { user_id: 'john_001', name: 'John Doe', time: '09:20:15', type: 'student' }
          ],
          '07_17_25': [
            { user_id: 'demo_user', name: 'Demo User', time: '09:10:45', type: 'student' },
            { user_id: 'jane_002', name: 'Jane Smith', time: '09:25:30', type: 'teacher' }
          ]
        }
      }
    }
  },

  getAnalytics: async () => {
    await new Promise(resolve => setTimeout(resolve, 1000))
    return {
      data: {
        total_users: 25,
        total_attendance_records: 150,
        average_daily_attendance: 18,
        attendance_trends: [
          { date: '07_14_25', total: 16, students: 14, employees: 2 },
          { date: '07_15_25', total: 19, students: 16, employees: 3 },
          { date: '07_16_25', total: 17, students: 15, employees: 2 },
          { date: '07_17_25', total: 20, students: 17, employees: 3 },
          { date: '07_18_25', total: 18, students: 15, employees: 3 }
        ]
      }
    }
  },

  getRecentActivity: async () => {
    await new Promise(resolve => setTimeout(resolve, 600))
    return {
      data: {
        recent_activity: [
          {
            type: 'attendance',
            user_id: 'demo_user',
            user_name: 'Demo User',
            timestamp: '2024-07-18 09:15:30',
            action: 'Marked attendance'
          },
          {
            type: 'attendance',
            user_id: 'john_001',
            user_name: 'John Doe',
            timestamp: '2024-07-18 09:20:15',
            action: 'Marked attendance'
          }
        ]
      }
    }
  }
}

// Check if we're in demo mode (frontend-only)
export const isDemoMode = () => {
  // Explicitly set demo mode
  if (import.meta.env.VITE_DEMO_MODE === 'true') {
    return true
  }
  
  // Auto-detect demo mode when no API URL is provided or it's localhost
  const apiUrl = import.meta.env.VITE_API_BASE_URL
  if (!apiUrl || apiUrl.includes('localhost') || apiUrl.includes('127.0.0.1')) {
    return true
  }
  
  return false
}