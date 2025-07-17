"""
Mock data generator for RecognizeMe system
Provides realistic demo data for both admin and student dashboards
"""

import random
import json
from datetime import datetime, timedelta
from database import Database

class MockDataGenerator:
    def __init__(self, db_instance=None):
        self.db = db_instance or Database()
        
    def generate_sample_users(self):
        """Generate sample users for demo"""
        sample_users = [
            # Students
            {'user_id': 'CS001', 'name': 'Alice Johnson', 'username': 'alice.johnson', 'type': 'student', 'class_section': 'CS 4th Year A'},
            {'user_id': 'CS002', 'name': 'Bob Smith', 'username': 'bob.smith', 'type': 'student', 'class_section': 'CS 4th Year A'},
            {'user_id': 'CS003', 'name': 'Carol Davis', 'username': 'carol.davis', 'type': 'student', 'class_section': 'CS 4th Year B'},
            {'user_id': 'CS004', 'name': 'Frank Miller', 'username': 'frank.miller', 'type': 'student', 'class_section': 'CS 4th Year B'},
            {'user_id': 'CS005', 'name': 'Henry Taylor', 'username': 'henry.taylor', 'type': 'student', 'class_section': 'CS 3rd Year A'},
            
            {'user_id': 'EE001', 'name': 'David Wilson', 'username': 'david.wilson', 'type': 'student', 'class_section': 'EE 3rd Year A'},
            {'user_id': 'EE002', 'name': 'Ivy Chen', 'username': 'ivy.chen', 'type': 'student', 'class_section': 'EE 3rd Year B'},
            {'user_id': 'EE003', 'name': 'Kevin Park', 'username': 'kevin.park', 'type': 'student', 'class_section': 'EE 2nd Year A'},
            
            {'user_id': 'ME001', 'name': 'Emma Brown', 'username': 'emma.brown', 'type': 'student', 'class_section': 'ME 2nd Year A'},
            {'user_id': 'ME002', 'name': 'Jack Anderson', 'username': 'jack.anderson', 'type': 'student', 'class_section': 'ME 2nd Year B'},
            {'user_id': 'ME003', 'name': 'Lisa Wang', 'username': 'lisa.wang', 'type': 'student', 'class_section': 'ME 1st Year A'},
            
            {'user_id': 'IT001', 'name': 'Grace Lee', 'username': 'grace.lee', 'type': 'student', 'class_section': 'IT 4th Year A'},
            {'user_id': 'IT002', 'name': 'Mike Rodriguez', 'username': 'mike.rodriguez', 'type': 'student', 'class_section': 'IT 3rd Year A'},
            {'user_id': 'IT003', 'name': 'Nina Patel', 'username': 'nina.patel', 'type': 'student', 'class_section': 'IT 2nd Year A'},
            
            # Faculty/Staff
            {'user_id': 'FAC001', 'name': 'Dr. Sarah Mitchell', 'username': 'sarah.mitchell', 'type': 'teacher', 'class_section': 'Computer Science Dept'},
            {'user_id': 'FAC002', 'name': 'Prof. John Williams', 'username': 'john.williams', 'type': 'teacher', 'class_section': 'Electrical Engineering Dept'},
            {'user_id': 'FAC003', 'name': 'Dr. Maria Garcia', 'username': 'maria.garcia', 'type': 'teacher', 'class_section': 'Mechanical Engineering Dept'},
            {'user_id': 'FAC004', 'name': 'Prof. Robert Kim', 'username': 'robert.kim', 'type': 'teacher', 'class_section': 'Information Technology Dept'},
            
            {'user_id': 'STF001', 'name': 'Jennifer Adams', 'username': 'jennifer.adams', 'type': 'staff', 'class_section': 'Administration'},
            {'user_id': 'STF002', 'name': 'Thomas Clark', 'username': 'thomas.clark', 'type': 'staff', 'class_section': 'IT Support'},
            {'user_id': 'STF003', 'name': 'Amanda White', 'username': 'amanda.white', 'type': 'staff', 'class_section': 'Library'},
        ]
        
        return sample_users
    
    def generate_sample_attendance(self, days_back=30):
        """Generate realistic attendance data for the past N days"""
        users = self.generate_sample_users()
        attendance_records = []
        
        base_date = datetime.now()
        
        for i in range(days_back):
            current_date = base_date - timedelta(days=i)
            date_str = current_date.strftime("%m_%d_%y")
            
            # Weekend attendance is lower
            is_weekend = current_date.weekday() >= 5
            attendance_rate = 0.3 if is_weekend else 0.85
            
            for user in users:
                # Different attendance patterns for different user types
                if user['type'] == 'student':
                    base_rate = 0.82
                elif user['type'] == 'teacher':
                    base_rate = 0.90
                else:  # staff
                    base_rate = 0.88
                
                # Adjust for weekends
                final_rate = base_rate * attendance_rate
                
                if random.random() < final_rate:
                    # Generate realistic arrival times
                    if user['type'] == 'student':
                        # Students arrive between 8:00-10:00 AM
                        hour = random.randint(8, 9)
                        minute = random.randint(0, 59)
                    else:
                        # Faculty/staff arrive between 7:30-9:30 AM
                        hour = random.randint(7, 9)
                        minute = random.randint(0 if hour > 7 else 30, 59)
                    
                    time_str = f"{hour:02d}:{minute:02d}:{random.randint(0, 59):02d}"
                    
                    attendance_records.append({
                        'user_id': user['user_id'],
                        'name': user['name'],
                        'date': date_str,
                        'time': time_str,
                        'type': user['type']
                    })
        
        return attendance_records
    
    def generate_sample_notices(self):
        """Generate sample notices for demo"""
        notices = [
            {
                'title': 'Welcome to New Academic Year 2025',
                'content': 'We are excited to welcome all students and faculty to the new academic year. Please ensure you have registered for face recognition attendance system.',
                'priority': 'high',
                'created_by': 'admin'
            },
            {
                'title': 'Face Recognition System Update',
                'content': 'The attendance system has been updated with improved accuracy. If you experience any issues, please contact the IT support team.',
                'priority': 'normal',
                'created_by': 'admin'
            },
            {
                'title': 'Holiday Schedule Announcement',
                'content': 'Please note the upcoming holiday schedule. Classes will be suspended from January 26-28, 2025 for Republic Day celebrations.',
                'priority': 'normal',
                'created_by': 'admin'
            },
            {
                'title': 'New Security Protocols',
                'content': 'Enhanced security measures have been implemented. All users must mark attendance using the face recognition system. Manual attendance will not be accepted.',
                'priority': 'high',
                'created_by': 'admin'
            },
            {
                'title': 'System Maintenance Notice',
                'content': 'Scheduled maintenance will be performed on the attendance system this Sunday from 2:00 AM to 4:00 AM. The system may be temporarily unavailable.',
                'priority': 'normal',
                'created_by': 'admin'
            },
            {
                'title': 'Attendance Report Available',
                'content': 'Monthly attendance reports are now available for download. Faculty can access detailed analytics from the admin dashboard.',
                'priority': 'low',
                'created_by': 'admin'
            }
        ]
        
        return notices
    
    def populate_demo_data(self):
        """Populate database with comprehensive demo data"""
        import bcrypt
        
        print("🚀 Generating comprehensive demo data...")
        
        # Generate users with hashed passwords
        users = self.generate_sample_users()
        for user in users:
            # Default password for all demo users
            password_hash = bcrypt.hashpw('demo123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            success = self.db.add_user(
                user['user_id'],
                user['name'],
                user['username'],
                password_hash,
                user['type'],
                user['class_section']
            )
            
            if success:
                print(f"✅ Added user: {user['name']} ({user['user_id']})")
            else:
                print(f"⚠️  User already exists: {user['name']} ({user['user_id']})")
        
        # Generate attendance records
        attendance_records = self.generate_sample_attendance(30)
        for record in attendance_records:
            self.db.add_attendance(
                record['user_id'],
                record['name'],
                record['date'],
                record['time'],
                record['type']
            )
        
        print(f"✅ Generated {len(attendance_records)} attendance records")
        
        # Generate notices
        notices = self.generate_sample_notices()
        for notice in notices:
            self.db.add_notice(
                notice['title'],
                notice['content'],
                notice['priority'],
                notice['created_by']
            )
        
        print(f"✅ Generated {len(notices)} notices")
        print("🎉 Demo data population completed!")
        
        return {
            'users_created': len(users),
            'attendance_records': len(attendance_records),
            'notices_created': len(notices)
        }
    
    def get_demo_analytics_summary(self):
        """Get a summary of demo data for verification"""
        stats = self.db.get_attendance_stats()
        users = self.db.get_all_users()
        notices = self.db.get_all_notices()
        
        return {
            'total_users': len(users),
            'students': len([u for u in users if u['type'] == 'student']),
            'teachers': len([u for u in users if u['type'] == 'teacher']),
            'staff': len([u for u in users if u['type'] == 'staff']),
            'total_notices': len(notices),
            'attendance_stats': stats
        }

def main():
    """Run demo data generation"""
    print("🎯 RecognizeMe Demo Data Generator")
    print("=" * 50)
    
    # Initialize database and mock data generator
    db = Database()
    mock_gen = MockDataGenerator(db)
    
    # Populate demo data
    result = mock_gen.populate_demo_data()
    
    print("\n📊 Demo Data Summary:")
    print("=" * 30)
    summary = mock_gen.get_demo_analytics_summary()
    
    print(f"👥 Total Users: {summary['total_users']}")
    print(f"   📚 Students: {summary['students']}")
    print(f"   👨‍🏫 Teachers: {summary['teachers']}")
    print(f"   👨‍💼 Staff: {summary['staff']}")
    print(f"📢 Notices: {summary['total_notices']}")
    print(f"📈 Today's Attendance: {summary['attendance_stats']['today_attendance']}")
    
    print("\n🔐 Demo Login Credentials:")
    print("=" * 30)
    print("Admin: admin / admin123")
    print("Users: [username] / demo123")
    print("Example: alice.johnson / demo123")

if __name__ == "__main__":
    main()