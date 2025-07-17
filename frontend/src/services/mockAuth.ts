// Mock authentication service for comprehensive frontend demo
const DEMO_USERS = [
  {
    username: 'alice.johnson',
    name: 'Alice Johnson',
    type: 'student',
    class_section: 'CS 4th Year A',
  },
  { username: 'bob.smith', name: 'Bob Smith', type: 'student', class_section: 'CS 4th Year A' },
  { username: 'carol.davis', name: 'Carol Davis', type: 'student', class_section: 'CS 4th Year B' },
  {
    username: 'david.wilson',
    name: 'David Wilson',
    type: 'student',
    class_section: 'EE 3rd Year A',
  },
  { username: 'emma.brown', name: 'Emma Brown', type: 'student', class_section: 'ME 2nd Year A' },
  {
    username: 'sarah.mitchell',
    name: 'Dr. Sarah Mitchell',
    type: 'teacher',
    class_section: 'Computer Science Dept',
  },
  {
    username: 'john.williams',
    name: 'Prof. John Williams',
    type: 'teacher',
    class_section: 'Electrical Engineering Dept',
  },
  {
    username: 'jennifer.adams',
    name: 'Jennifer Adams',
    type: 'staff',
    class_section: 'Administration',
  },
]

export const mockAuthAPI = {
  adminLogin: async (password: string) => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    if (password === 'admin123') {
      return {
        data: {
          access_token: 'mock-admin-token',
          role: 'admin',
          user: {
            id: 'admin',
            name: 'Demo Admin',
            type: 'admin',
          },
        },
      }
    } else {
      throw {
        response: {
          data: {
            message: 'Invalid admin credentials',
          },
        },
      }
    }
  },

  userLogin: async (username: string, password: string) => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Check demo users
    const user = DEMO_USERS.find((u) => u.username === username)

    if (user && password === 'demo123') {
      const userData = {
        id: username,
        name: user.name,
        type: user.type,
        class_section: user.class_section,
      }

      // Store current user data for personalized demo experience
      localStorage.setItem('currentUser', JSON.stringify(userData))

      return {
        data: {
          access_token: 'mock-user-token',
          role: 'user',
          user: userData,
        },
      }
    } else {
      throw {
        response: {
          data: {
            message: 'Invalid credentials',
          },
        },
      }
    }
  },
}

// Mock dashboard data
export const mockDashboardAPI = {
  getStats: async () => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        total_users: 25,
        today_attendance: 18,
        present_today: 18,
        absent_today: 7,
        students_present: 15,
        employees_present: 3,
        attendance_rate: 72.0,
        total_registered: 25,
        attendance_data: [
          { Name: 'Demo User', Roll: 'demo_user', Time: '09:15:30', Type: 'student' },
          { Name: 'John Doe', Roll: 'john_001', Time: '09:20:15', Type: 'student' },
          { Name: 'Jane Smith', Roll: 'jane_002', Time: '09:25:45', Type: 'teacher' },
        ],
      },
    }
  },

  getAttendance: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    return {
      data: {
        attendance: [
          { Name: 'Demo User', Roll: 'demo_user', Time: '09:15:30', Type: 'student' },
          { Name: 'John Doe', Roll: 'john_001', Time: '09:20:15', Type: 'student' },
          { Name: 'Jane Smith', Roll: 'jane_002', Time: '09:25:45', Type: 'teacher' },
          { Name: 'Bob Wilson', Roll: 'bob_003', Time: '09:30:20', Type: 'student' },
          { Name: 'Alice Brown', Roll: 'alice_004', Time: '09:35:10', Type: 'staff' },
        ],
      },
    }
  },

  startAttendance: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000))
    return {
      data: {
        message: 'Demo: Face recognition attendance completed',
        recognized_users: ['demo_user', 'john_001'],
      },
    }
  },
}

// Mock admin data
export const mockAdminAPI = {
  getUsers: async () => {
    await new Promise((resolve) => setTimeout(resolve, 800))
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
            has_password: true,
          },
          {
            id: 'john_001',
            name: 'John Doe',
            username: 'john_doe',
            type: 'student',
            class_section: 'CS 4th A',
            registered_date: '2024-01-16',
            has_face_data: true,
            has_password: true,
          },
          {
            id: 'jane_002',
            name: 'Jane Smith',
            username: 'jane_smith',
            type: 'teacher',
            class_section: 'Computer Science',
            registered_date: '2024-01-17',
            has_face_data: false,
            has_password: true,
          },
        ],
      },
    }
  },

  getNotices: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    return {
      data: {
        notices: [
          {
            id: 1,
            title: 'Welcome to Demo Mode',
            content:
              'This is a frontend-only demo. Full functionality available in the complete system.',
            priority: 'high',
            created_date: '2024-07-18',
            created_by: 'admin',
          },
          {
            id: 2,
            title: 'System Maintenance',
            content: 'Demo system is running smoothly. All features are simulated.',
            priority: 'normal',
            created_date: '2024-07-17',
            created_by: 'admin',
          },
        ],
      },
    }
  },

  getAttendanceHistory: async () => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        history: {
          '07_18_25': [
            { user_id: 'demo_user', name: 'Demo User', time: '09:15:30', type: 'student' },
            { user_id: 'john_001', name: 'John Doe', time: '09:20:15', type: 'student' },
          ],
          '07_17_25': [
            { user_id: 'demo_user', name: 'Demo User', time: '09:10:45', type: 'student' },
            { user_id: 'jane_002', name: 'Jane Smith', time: '09:25:30', type: 'teacher' },
          ],
        },
      },
    }
  },

  getAnalytics: async () => {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    return {
      data: {
        basic_stats: {
          total_users: 156,
          today_attendance: 142,
          students_today: 128,
          employees_today: 14,
          total_notices: 8,
        },
        weekly_trends: [
          { date: '01_13_25', total: 145, students: 130, employees: 15 },
          { date: '01_14_25', total: 138, students: 125, employees: 13 },
          { date: '01_15_25', total: 152, students: 135, employees: 17 },
          { date: '01_16_25', total: 149, students: 132, employees: 17 },
          { date: '01_17_25', total: 142, students: 128, employees: 14 },
          { date: '01_18_25', total: 156, students: 140, employees: 16 },
          { date: '01_19_25', total: 134, students: 120, employees: 14 },
        ],
        monthly_trend: [
          { month: 'Aug 2024', attendance: 85, students: 78, employees: 7 },
          { month: 'Sep 2024', attendance: 92, students: 84, employees: 8 },
          { month: 'Oct 2024', attendance: 88, students: 81, employees: 7 },
          { month: 'Nov 2024', attendance: 94, students: 86, employees: 8 },
          { month: 'Dec 2024', attendance: 76, students: 69, employees: 7 },
          { month: 'Jan 2025', attendance: 98, students: 89, employees: 9 },
        ],
        weekly_pattern: [
          { day: 'Monday', average: 22, students: 20, employees: 2 },
          { day: 'Tuesday', average: 24, students: 22, employees: 2 },
          { day: 'Wednesday', average: 21, students: 19, employees: 2 },
          { day: 'Thursday', average: 23, students: 21, employees: 2 },
          { day: 'Friday', average: 20, students: 18, employees: 2 },
          { day: 'Saturday', average: 8, students: 7, employees: 1 },
          { day: 'Sunday', average: 3, students: 3, employees: 0 },
        ],
        class_wise_stats: [
          { class: 'CS 4th Year', total_students: 45, present_today: 42, attendance_rate: 93.3 },
          { class: 'EE 3rd Year', total_students: 38, present_today: 35, attendance_rate: 92.1 },
          { class: 'ME 2nd Year', total_students: 41, present_today: 36, attendance_rate: 87.8 },
          { class: 'IT 4th Year', total_students: 32, present_today: 29, attendance_rate: 90.6 },
          { class: 'Faculty', total_members: 18, present_today: 16, attendance_rate: 88.9 },
        ],
        attendance_by_time: [
          { time_slot: '08:00-09:00', count: 45, percentage: 31.7 },
          { time_slot: '09:00-10:00', count: 67, percentage: 47.2 },
          { time_slot: '10:00-11:00', count: 23, percentage: 16.2 },
          { time_slot: '11:00-12:00', count: 7, percentage: 4.9 },
        ],
        top_attendees: [
          { user_id: 'CS001', name: 'Alice Johnson', attendance_count: 28 },
          { user_id: 'CS002', name: 'Bob Smith', attendance_count: 27 },
          { user_id: 'CS003', name: 'Carol Davis', attendance_count: 26 },
          { user_id: 'EE001', name: 'David Wilson', attendance_count: 25 },
          { user_id: 'ME001', name: 'Emma Brown', attendance_count: 25 },
        ],
        recent_system_activity: [
          {
            date: '2025-01-18',
            time: '09:15:30',
            status: 'present',
            user_id: 'CS001',
            user_name: 'Alice Johnson',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:18:45',
            status: 'present',
            user_id: 'CS002',
            user_name: 'Bob Smith',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:22:10',
            status: 'present',
            user_id: 'EE001',
            user_name: 'David Wilson',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:25:33',
            status: 'present',
            user_id: 'ME001',
            user_name: 'Emma Brown',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:28:15',
            status: 'present',
            user_id: 'IT001',
            user_name: 'Grace Lee',
            user_type: 'student',
          },
          {
            date: '2025-01-17',
            time: '09:10:22',
            status: 'present',
            user_id: 'CS001',
            user_name: 'Alice Johnson',
            user_type: 'student',
          },
          {
            date: '2025-01-17',
            time: '09:05:18',
            status: 'present',
            user_id: 'CS002',
            user_name: 'Bob Smith',
            user_type: 'student',
          },
          {
            date: '2025-01-17',
            time: '09:15:45',
            status: 'present',
            user_id: 'EE001',
            user_name: 'David Wilson',
            user_type: 'student',
          },
        ],
        performance_insights: {
          goal: 'Maintain 90%+ attendance rate across all classes',
          trend: 'Overall attendance is improving by 5% this month',
          achievement: 'CS department has highest attendance rate',
        },
      },
    }
  },

  getRecentActivity: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    return {
      data: {
        activities: [
          {
            date: '2025-01-18',
            time: '09:15:30',
            status: 'present',
            user_id: 'demo_user',
            user_name: 'Demo User',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:20:15',
            status: 'present',
            user_id: 'john_001',
            user_name: 'John Doe',
            user_type: 'student',
          },
          {
            date: '2025-01-18',
            time: '09:25:45',
            status: 'present',
            user_id: 'jane_002',
            user_name: 'Jane Smith',
            user_type: 'teacher',
          },
          {
            date: '2025-01-17',
            time: '09:10:45',
            status: 'present',
            user_id: 'demo_user',
            user_name: 'Demo User',
            user_type: 'student',
          },
          {
            date: '2025-01-17',
            time: '09:25:30',
            status: 'present',
            user_id: 'jane_002',
            user_name: 'Jane Smith',
            user_type: 'teacher',
          },
        ],
      },
    }
  },

  // Add missing methods that admin dashboard expects
  getActiveClasses: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    return {
      data: {
        classes: [
          { id: 1, name: 'CS 4th Year A', students: 25, present_today: 22, attendance_rate: 88.0 },
          { id: 2, name: 'CS 4th Year B', students: 23, present_today: 20, attendance_rate: 87.0 },
          { id: 3, name: 'EE 3rd Year A', students: 28, present_today: 25, attendance_rate: 89.3 },
          { id: 4, name: 'ME 2nd Year A', students: 30, present_today: 26, attendance_rate: 86.7 },
        ],
      },
    }
  },

  updateUserPassword: async (userId: string, password: string) => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        success: true,
        message: 'Password updated successfully',
      },
    }
  },

  deleteUser: async (userId: string) => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        success: true,
        message: 'User deleted successfully',
      },
    }
  },

  deleteNotice: async (noticeId: string) => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    return {
      data: {
        success: true,
        message: 'Notice deleted successfully',
      },
    }
  },

  saveClassConfig: async (config: any) => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        success: true,
        message: 'Class configuration saved successfully',
      },
    }
  },

  saveTimeSettings: async (settings: any) => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    return {
      data: {
        success: true,
        message: 'Time settings saved successfully',
      },
    }
  },
}

// Get current user from localStorage for personalized demo data
const getCurrentDemoUser = () => {
  const token = localStorage.getItem('token')
  if (token === 'mock-user-token') {
    const userStr = localStorage.getItem('currentUser')
    if (userStr) {
      try {
        return JSON.parse(userStr)
      } catch (e) {
        return null
      }
    }
  }
  return null
}

// Generate user-specific demo data based on user type
const generateUserSpecificData = (userType: string, userName: string) => {
  const baseData = {
    student: {
      attendance_rate: 85.2,
      monthly_attendance: [18, 20, 19, 21, 16, 23],
      weekly_pattern: [4, 5, 4, 5],
      notices_count: 6,
      recent_days: 23,
    },
    teacher: {
      attendance_rate: 92.5,
      monthly_attendance: [22, 23, 21, 24, 19, 26],
      weekly_pattern: [5, 5, 5, 4],
      notices_count: 8,
      recent_days: 26,
    },
    staff: {
      attendance_rate: 88.7,
      monthly_attendance: [20, 21, 20, 22, 18, 24],
      weekly_pattern: [5, 5, 4, 5],
      notices_count: 5,
      recent_days: 24,
    },
  }

  return baseData[userType as keyof typeof baseData] || baseData.student
}

// Mock user analytics data with dynamic user-specific content
export const mockUserAPI = {
  getMyAttendance: async () => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    const currentUser = getCurrentDemoUser()
    const userType = currentUser?.type || 'student'
    const userData = generateUserSpecificData(userType, currentUser?.name || 'Demo User')

    return {
      data: {
        total_days: 30,
        attended_days: userData.recent_days,
        attendance_rate: userData.attendance_rate,
        this_month: userData.monthly_attendance[5],
        attendance: Array.from({ length: userData.recent_days }, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - i)
          const hour =
            userType === 'student'
              ? 8 + Math.floor(Math.random() * 2)
              : 7 + Math.floor(Math.random() * 3)
          const minute = Math.floor(Math.random() * 60)

          return {
            date: date.toISOString().split('T')[0],
            time: `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}:00`,
            type: userType,
          }
        }),
      },
    }
  },

  // Add the method that dashboard actually calls
  getMyAnalytics: async () => {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const currentUser = getCurrentDemoUser()
    const userType = currentUser?.type || 'student'
    const userData = generateUserSpecificData(userType, currentUser?.name || 'Demo User')

    return {
      data: {
        basic_stats: {
          total_attendance_days: userData.recent_days,
          present_today: Math.random() > 0.2,
          last_attendance: '2025-01-18',
        },
        // Add fields that loadDashboardStats expects for users
        total_classmates: 25,
        present_today: userData.recent_days > 20 ? 1 : 0,
        absent_today: userData.recent_days > 20 ? 0 : 1,
        attendance_rate: userData.attendance_rate,
        recent_activity: Array.from({ length: 8 }, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - i)
          const hour =
            userType === 'student'
              ? 8 + Math.floor(Math.random() * 2)
              : 7 + Math.floor(Math.random() * 3)
          const minute = Math.floor(Math.random() * 60)

          return {
            date: date.toISOString().split('T')[0],
            time: `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}:00`,
            status: 'present',
            user_name: currentUser?.name || 'Demo User',
          }
        }),
        monthly_trend: [
          { month: 'Aug', attendance: userData.monthly_attendance[0] },
          { month: 'Sep', attendance: userData.monthly_attendance[1] },
          { month: 'Oct', attendance: userData.monthly_attendance[2] },
          { month: 'Nov', attendance: userData.monthly_attendance[3] },
          { month: 'Dec', attendance: userData.monthly_attendance[4] },
          { month: 'Jan', attendance: userData.monthly_attendance[5] },
        ],
        weekly_pattern: [
          { name: 'Monday', percentage: (userData.weekly_pattern[0] / 5) * 100 },
          { name: 'Tuesday', percentage: (userData.weekly_pattern[1] / 5) * 100 },
          { name: 'Wednesday', percentage: (userData.weekly_pattern[2] / 5) * 100 },
          { name: 'Thursday', percentage: (userData.weekly_pattern[3] / 5) * 100 },
          { name: 'Friday', percentage: (userData.weekly_pattern[1] / 5) * 100 },
          { name: 'Saturday', percentage: userType === 'student' ? 0 : 20 },
          { name: 'Sunday', percentage: 0 },
        ],
      },
    }
  },

  getUserAnalytics: async () => {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const currentUser = getCurrentDemoUser()
    const userType = currentUser?.type || 'student'
    const userData = generateUserSpecificData(userType, currentUser?.name || 'Demo User')

    return {
      data: {
        basic_stats: {
          total_attendance_days: userData.recent_days,
          present_today: Math.random() > 0.2, // 80% chance of being present today
          last_attendance: '2025-01-18',
        },
        recent_attendance: Array.from({ length: 10 }, (_, i) => {
          const date = new Date()
          date.setDate(date.getDate() - i)
          const hour =
            userType === 'student'
              ? 8 + Math.floor(Math.random() * 2)
              : 7 + Math.floor(Math.random() * 3)
          const minute = Math.floor(Math.random() * 60)

          return {
            date: date.toISOString().split('T')[0],
            time: `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}:00`,
            status: 'present',
          }
        }),
        day_frequency: [
          {
            name: 'Monday',
            count: userData.weekly_pattern[0],
            percentage: (userData.weekly_pattern[0] / 5) * 100,
          },
          {
            name: 'Tuesday',
            count: userData.weekly_pattern[1],
            percentage: (userData.weekly_pattern[1] / 5) * 100,
          },
          {
            name: 'Wednesday',
            count: userData.weekly_pattern[2],
            percentage: (userData.weekly_pattern[2] / 5) * 100,
          },
          {
            name: 'Thursday',
            count: userData.weekly_pattern[3],
            percentage: (userData.weekly_pattern[3] / 5) * 100,
          },
          {
            name: 'Friday',
            count: userData.weekly_pattern[1],
            percentage: (userData.weekly_pattern[1] / 5) * 100,
          },
          {
            name: 'Saturday',
            count: userType === 'student' ? 0 : 1,
            percentage: userType === 'student' ? 0 : 20,
          },
          { name: 'Sunday', count: 0, percentage: 0 },
        ],
        attendance_rate: userData.attendance_rate,
        monthly_trend: [
          { month: 'Aug', attendance: userData.monthly_attendance[0] },
          { month: 'Sep', attendance: userData.monthly_attendance[1] },
          { month: 'Oct', attendance: userData.monthly_attendance[2] },
          { month: 'Nov', attendance: userData.monthly_attendance[3] },
          { month: 'Dec', attendance: userData.monthly_attendance[4] },
          { month: 'Jan', attendance: userData.monthly_attendance[5] },
        ],
        weekly_pattern: [
          { week: 'Week 1', days: userData.weekly_pattern[0] },
          { week: 'Week 2', days: userData.weekly_pattern[1] },
          { week: 'Week 3', days: userData.weekly_pattern[2] },
          { week: 'Week 4', days: userData.weekly_pattern[3] },
        ],
        // Performance insights for dashboard display
        performance_insights:
          userType === 'student'
            ? {
                goal: 'Maintain 85%+ attendance rate',
                trend: 'Your attendance has improved by 7% this month',
                achievement: 'Perfect attendance this week!',
              }
            : userType === 'teacher'
              ? {
                  goal: 'Maintain 90%+ attendance rate',
                  trend: 'Your class attendance is above average',
                  achievement: 'Most consistent faculty member',
                }
              : {
                  goal: 'Maintain regular attendance',
                  trend: 'Your attendance is consistent',
                  achievement: 'Perfect punctuality record',
                },
      },
    }
  },

  getUserNotices: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    const currentUser = getCurrentDemoUser()
    const userType = currentUser?.type || 'student'

    // User-type specific notices
    const noticesByType = {
      student: [
        {
          id: 1,
          title: 'Welcome to Your Student Dashboard',
          content:
            'Track your attendance, view analytics, and stay updated with class announcements.',
          priority: 'normal',
          created_date: '2025-01-18',
          created_by: 'admin',
        },
        {
          id: 2,
          title: 'Attendance Requirement Reminder',
          content: 'Maintain 75% attendance to be eligible for final examinations.',
          priority: 'high',
          created_date: '2025-01-17',
          created_by: 'admin',
        },
        {
          id: 3,
          title: 'New Study Resources Available',
          content: 'Check out the latest study materials uploaded to the learning portal.',
          priority: 'normal',
          created_date: '2025-01-16',
          created_by: 'admin',
        },
        {
          id: 4,
          title: 'Upcoming Assignment Deadline',
          content: "Don't forget to submit your project assignments by January 25th.",
          priority: 'high',
          created_date: '2025-01-15',
          created_by: 'admin',
        },
      ],
      teacher: [
        {
          id: 1,
          title: 'Faculty Dashboard Welcome',
          content:
            'Access student analytics, manage class attendance, and view department insights.',
          priority: 'normal',
          created_date: '2025-01-18',
          created_by: 'admin',
        },
        {
          id: 2,
          title: 'Grade Submission Deadline',
          content: 'Please submit mid-semester grades by January 22nd through the faculty portal.',
          priority: 'high',
          created_date: '2025-01-17',
          created_by: 'admin',
        },
        {
          id: 3,
          title: 'Faculty Meeting Scheduled',
          content: 'Department meeting on January 20th at 2:00 PM in Conference Room A.',
          priority: 'normal',
          created_date: '2025-01-16',
          created_by: 'admin',
        },
        {
          id: 4,
          title: 'New Teaching Resources',
          content: 'Updated curriculum guidelines and teaching materials are now available.',
          priority: 'normal',
          created_date: '2025-01-15',
          created_by: 'admin',
        },
      ],
      staff: [
        {
          id: 1,
          title: 'Staff Portal Access',
          content: 'Your administrative dashboard provides access to system management tools.',
          priority: 'normal',
          created_date: '2025-01-18',
          created_by: 'admin',
        },
        {
          id: 2,
          title: 'System Maintenance Window',
          content: 'Scheduled maintenance on January 21st from 2:00 AM to 4:00 AM.',
          priority: 'high',
          created_date: '2025-01-17',
          created_by: 'admin',
        },
        {
          id: 3,
          title: 'Security Protocol Update',
          content: 'New security measures implemented. Please review the updated guidelines.',
          priority: 'high',
          created_date: '2025-01-16',
          created_by: 'admin',
        },
        {
          id: 4,
          title: 'Staff Training Session',
          content: 'Mandatory training on new attendance system features on January 23rd.',
          priority: 'normal',
          created_date: '2025-01-15',
          created_by: 'admin',
        },
      ],
    }

    return {
      data: {
        notices: noticesByType[userType as keyof typeof noticesByType] || noticesByType.student,
      },
    }
  },

  // Additional methods for comprehensive demo experience
  markAttendance: async () => {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const currentUser = getCurrentDemoUser()

    return {
      data: {
        success: true,
        message: `Attendance marked successfully for ${currentUser?.name || 'Demo User'}`,
        timestamp: new Date().toISOString(),
        location: 'Main Campus',
      },
    }
  },

  getAttendanceStats: async () => {
    await new Promise((resolve) => setTimeout(resolve, 800))
    const currentUser = getCurrentDemoUser()
    const userType = currentUser?.type || 'student'
    const userData = generateUserSpecificData(userType, currentUser?.name || 'Demo User')

    return {
      data: {
        current_month: {
          total_days: 30,
          attended_days: userData.monthly_attendance[5],
          attendance_rate: userData.attendance_rate,
          streak: Math.floor(Math.random() * 10) + 5,
        },
        comparison: {
          last_month: userData.monthly_attendance[4],
          improvement: userData.monthly_attendance[5] - userData.monthly_attendance[4],
          class_average: userType === 'student' ? 82.5 : userType === 'teacher' ? 89.2 : 85.8,
        },
        achievements: [
          userType === 'student' ? 'Perfect Week Streak' : 'Consistent Professional',
          'Early Bird Award',
          'Monthly Goal Achieved',
        ],
      },
    }
  },

  // Add missing methods that dashboard expects
  getNotices: async () => {
    return mockUserAPI.getUserNotices()
  },

  getMyProfile: async () => {
    await new Promise((resolve) => setTimeout(resolve, 600))
    const currentUser = getCurrentDemoUser()
    const userData = generateUserSpecificData(
      currentUser?.type || 'student',
      currentUser?.name || 'Demo User',
    )

    return {
      data: {
        profile: {
          id: currentUser?.id || 'demo_user',
          name: currentUser?.name || 'Demo User',
          username: currentUser?.id || 'demo_user',
          type: currentUser?.type || 'student',
          class_section: currentUser?.class_section || 'Demo Class',
          registered_date: '2024-01-15',
        },
        total_logins: Math.floor(Math.random() * 50) + 20,
        consecutive_days: Math.floor(Math.random() * 15) + 5,
        best_month: 'January 2025',
        avg_daily_time: '2h 15m',
        achievements: [
          currentUser?.type === 'student' ? 'Perfect Week Streak' : 'Consistent Professional',
          'Early Bird Award',
          'Monthly Goal Achieved',
        ],
      },
    }
  },
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
