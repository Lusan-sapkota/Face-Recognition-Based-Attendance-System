# 🎯 RecognizeMe Demo Data Guide

This guide explains how to set up and use the comprehensive demo data system for RecognizeMe, providing realistic data for testing and demonstration purposes.

## 🚀 Quick Demo Setup

### Option 1: Automatic Setup (Recommended)

```bash
# Navigate to backend directory
cd backend

# Run the demo setup script
python run_demo_setup.py
```

### Option 2: Manual Setup via API

1. Start the backend server:
```bash
cd backend
python app.py
```

2. Login as admin and use the demo data manager in the admin dashboard
3. Click "Populate Demo Data" button

### Option 3: Frontend-Only Demo Mode

Set the environment variable in `frontend/.env`:
```
VITE_DEMO_MODE=true
```

This enables frontend-only demo mode with mock data (no backend required).

## 📊 What's Included in Demo Data

### 👥 Sample Users (21 total)

#### Students (14 users)
- **Computer Science**: Alice Johnson, Bob Smith, Carol Davis, Frank Miller, Henry Taylor
- **Electrical Engineering**: David Wilson, Ivy Chen, Kevin Park  
- **Mechanical Engineering**: Emma Brown, Jack Anderson, Lisa Wang
- **Information Technology**: Grace Lee, Mike Rodriguez, Nina Patel

#### Faculty (4 users)
- Dr. Sarah Mitchell (Computer Science Dept)
- Prof. John Williams (Electrical Engineering Dept)
- Dr. Maria Garcia (Mechanical Engineering Dept)
- Prof. Robert Kim (Information Technology Dept)

#### Staff (3 users)
- Jennifer Adams (Administration)
- Thomas Clark (IT Support)
- Amanda White (Library)

### 📈 Attendance Data
- **30 days** of realistic attendance records
- **Weekday patterns**: 85% attendance rate
- **Weekend patterns**: 30% attendance rate
- **Time variations**: Realistic arrival times (8:00-10:00 AM)
- **User type patterns**: Different attendance behaviors for students/faculty/staff

### 📢 System Notices (6 notices)
- Welcome messages
- System updates
- Holiday announcements
- Security protocols
- Maintenance notices
- Report availability

### 📊 Analytics & Reports
- **Monthly trends**: 6 months of historical data
- **Weekly patterns**: Day-wise attendance analysis
- **Class-wise statistics**: Department and year-wise breakdown
- **Time distribution**: Peak attendance hours
- **Top performers**: Most regular attendees
- **Recent activity**: System-wide activity logs

## 🔐 Demo Login Credentials

### Admin Access
```
Username: admin
Password: admin123
```

### User Access (All demo users)
```
Username: [any demo username]
Password: demo123
```

### Example User Logins
```
alice.johnson / demo123    (CS Student)
sarah.mitchell / demo123   (CS Professor)
jennifer.adams / demo123   (Admin Staff)
```

## 🎨 Demo Features by User Type

### 👨‍💼 Admin Dashboard Features
- **User Management**: View all 21 demo users with realistic data
- **Attendance Analytics**: Comprehensive charts and statistics
- **System Monitoring**: Real-time attendance tracking
- **Notice Management**: Create and manage announcements
- **Reports & Export**: Download attendance data in various formats
- **Demo Data Manager**: Populate and manage demo data

### 👤 Student Dashboard Features
- **Personal Analytics**: Individual attendance patterns and trends
- **Attendance History**: 30 days of personal attendance records
- **Performance Insights**: Weekly and monthly attendance analysis
- **Notices**: Personalized announcements and updates
- **Profile Management**: View and update personal information

### 👨‍🏫 Teacher Dashboard Features
- **Class Analytics**: Department-wise attendance insights
- **Student Monitoring**: Track class attendance patterns
- **Professional Profile**: Faculty-specific dashboard features
- **Academic Notices**: Education-focused announcements

## 📱 Demo Data API Endpoints

### Admin Endpoints
```
POST /api/admin/populate-demo-data    # Populate comprehensive demo data
GET  /api/admin/demo-summary          # Get demo data summary
GET  /api/admin/analytics             # Enhanced analytics with demo data
```

### User Endpoints
```
GET /api/user/my-attendance           # Personal attendance with demo data
GET /api/user/analytics               # Personal analytics with demo patterns
GET /api/user/notices                 # User-specific notices
```

## 🔧 Customizing Demo Data

### Adding More Users
Edit `backend/mock_data.py` and modify the `generate_sample_users()` method:

```python
def generate_sample_users(self):
    sample_users = [
        # Add your custom users here
        {'user_id': 'CUSTOM001', 'name': 'Your Name', 'username': 'your.username', 'type': 'student', 'class_section': 'Your Class'},
    ]
    return sample_users
```

### Modifying Attendance Patterns
Adjust attendance rates in `generate_sample_attendance()`:

```python
# Different attendance patterns for different user types
if user['type'] == 'student':
    base_rate = 0.82  # 82% attendance rate for students
elif user['type'] == 'teacher':
    base_rate = 0.90  # 90% attendance rate for teachers
```

### Custom Analytics Data
Modify the mock analytics methods in `database.py`:
- `get_mock_admin_analytics()`
- `get_mock_user_analytics()`
- `get_mock_monthly_trend()`

## 🎯 Demo Scenarios

### Scenario 1: School Administrator
1. Login as admin (admin/admin123)
2. Explore user management with 21 diverse users
3. View comprehensive attendance analytics
4. Generate and download reports
5. Manage system notices and announcements

### Scenario 2: Computer Science Student
1. Login as alice.johnson (alice.johnson/demo123)
2. View personal attendance dashboard
3. Analyze individual performance trends
4. Check class-specific notices
5. Track monthly attendance goals

### Scenario 3: Faculty Member
1. Login as sarah.mitchell (sarah.mitchell/demo123)
2. Monitor department-wise attendance
3. View faculty-specific analytics
4. Access professional dashboard features
5. Review academic announcements

## 🔍 Troubleshooting Demo Data

### Common Issues

**Demo data not appearing?**
- Ensure you've run the demo setup script
- Check database connection
- Verify API endpoints are working

**Login not working?**
- Use exact credentials: demo123 (case-sensitive)
- Clear browser cache and localStorage
- Check network connectivity

**Analytics not loading?**
- Refresh the page
- Check browser console for errors
- Verify demo data was populated successfully

### Reset Demo Data
```bash
# Delete database and regenerate
cd backend
rm attendance.db
python run_demo_setup.py
```

## 🌟 Demo Data Benefits

### For Development
- **Realistic Testing**: Test with diverse user types and patterns
- **Performance Testing**: Large dataset for optimization
- **UI/UX Testing**: Rich data for interface validation

### For Demonstrations
- **Client Presentations**: Professional, realistic data
- **Feature Showcasing**: Comprehensive functionality display
- **Training Sessions**: Realistic scenarios for user training

### For Analytics
- **Pattern Recognition**: Diverse attendance patterns
- **Reporting Validation**: Rich data for report testing
- **Dashboard Testing**: Complex analytics visualization

## 📞 Support

If you encounter issues with demo data:

1. **Check the logs**: Look for error messages in console
2. **Verify setup**: Ensure all steps were completed
3. **Reset data**: Use the reset procedure above
4. **Contact support**: Create an issue on GitHub

---

🎉 **Enjoy exploring RecognizeMe with comprehensive, realistic demo data!**

The demo data system provides a complete, professional experience that showcases all features of the RecognizeMe attendance system with realistic scenarios and diverse user types.