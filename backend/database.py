import sqlite3
import os
import json
import base64
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self, db_path='attendance.db'):
        self.db_path = db_path
        self.init_database()
    
    def _parse_date(self, date_str):
        """Helper function to parse dates in different formats"""
        try:
            # Try parsing standard YYYY-MM-DD format first
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            try:
                # Try parsing MM_DD_YY format
                return datetime.strptime(date_str, '%m_%d_%y')
            except ValueError:
                # If both fail, return None
                return None

    def _normalize_date(self, date_str):
        """Convert any date format to YYYY-MM-DD"""
        parsed_date = self._parse_date(date_str)
        if parsed_date:
            return parsed_date.strftime('%Y-%m-%d')
        return date_str  # Return original if parsing fails
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                username TEXT UNIQUE,
                password_hash TEXT,
                type TEXT DEFAULT 'student',
                class_section TEXT,
                registered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Face data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                face_encoding BLOB,
                image_path TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                type TEXT DEFAULT 'student',
                created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Notices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                priority TEXT DEFAULT 'normal',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT DEFAULT 'admin',
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # System settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Add migration for username and password fields if they don't exist
        self.migrate_user_auth_fields()
        
        conn.close()
    
    def migrate_user_auth_fields(self):
        """Add username and password fields to existing users table if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if username column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'username' not in columns:
                cursor.execute('ALTER TABLE users ADD COLUMN username TEXT UNIQUE')
            
            if 'password_hash' not in columns:
                cursor.execute('ALTER TABLE users ADD COLUMN password_hash TEXT')
                
            conn.commit()
        except Exception as e:
            print(f"Migration error: {e}")
        finally:
            conn.close()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # User management methods
    def add_user(self, user_id, name, username, password_hash, user_type='student', class_section=''):
        """Add a new user to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, name, username, password_hash, type, class_section)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, name, username, password_hash, user_type, class_section))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # User already exists
        finally:
            conn.close()
    
    def get_user(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'user_id': result[1],
                'name': result[2],
                'username': result[3],
                'password_hash': result[4],
                'type': result[5],
                'class_section': result[6],
                'registered_date': result[7],
                'is_active': result[8]
            }
        return None
    
    def get_user_by_username(self, username):
        """Get user by username for authentication"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND is_active = 1', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'user_id': result[1],
                'name': result[2],
                'username': result[3],
                'password_hash': result[4],
                'type': result[5],
                'class_section': result[6],
                'registered_date': result[7],
                'is_active': result[8]
            }
        return None
    
    def update_user_password(self, user_id, password_hash):
        """Update user password (admin only)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users SET password_hash = ? WHERE user_id = ?
            ''', (password_hash, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            return False
        finally:
            conn.close()
        return None
    
    def get_all_users(self):
        """Get all active users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE is_active = 1 ORDER BY name')
        results = cursor.fetchall()
        conn.close()
        
        users = []
        for result in results:
            users.append({
                'id': result[0],
                'user_id': result[1],
                'name': result[2],
                'username': result[3],
                'password_hash': result[4],
                'type': result[5],
                'class_section': result[6],
                'registered_date': result[7],
                'is_active': result[8]
            })
        
        return users
    
    def delete_user(self, user_id):
        """Soft delete a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_active = 0 WHERE user_id = ?', (user_id,))
        # Also delete associated face data
        cursor.execute('DELETE FROM face_data WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build the update query dynamically based on provided data
        update_fields = []
        update_values = []
        
        for field in ['name', 'user_id', 'username', 'type', 'class_section']:
            if field in user_data:
                update_fields.append(f"{field} = ?")
                update_values.append(user_data[field])
        
        if not update_fields:
            conn.close()
            return False
        
        # Add the user_id for the WHERE clause
        update_values.append(user_id)
        
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
        
        try:
            cursor.execute(query, update_values)
            conn.commit()
            success = cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            # Handle unique constraint violations
            conn.close()
            raise ValueError(f"Update failed: {str(e)}")
        
        conn.close()
        return success
    
    # Face data management
    def add_face_data(self, user_id, face_encoding, image_path=None):
        """Add face encoding data for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Convert numpy array to blob
        face_blob = face_encoding.tobytes() if face_encoding is not None else None
        
        cursor.execute('''
            INSERT INTO face_data (user_id, face_encoding, image_path)
            VALUES (?, ?, ?)
        ''', (user_id, face_blob, image_path))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def get_face_data(self, user_id=None):
        """Get face data for a user or all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('SELECT * FROM face_data WHERE user_id = ?', (user_id,))
        else:
            cursor.execute('SELECT * FROM face_data')
        
        results = cursor.fetchall()
        conn.close()
        
        face_data = []
        for result in results:
            face_data.append({
                'id': result[0],
                'user_id': result[1],
                'face_encoding': result[2],
                'image_path': result[3],
                'created_date': result[4]
            })
        
        return face_data
    
    def delete_face_data(self, user_id):
        """Delete face data for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM face_data WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    # Attendance management
    def add_attendance(self, user_id, name, date_str, time_str, user_type='student'):
        """Add attendance record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if attendance already exists for this user today
        cursor.execute('''
            SELECT id FROM attendance WHERE user_id = ? AND date = ?
        ''', (user_id, date_str))
        
        if cursor.fetchone():
            conn.close()
            return False  # Already marked attendance
        
        cursor.execute('''
            INSERT INTO attendance (user_id, name, date, time, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, date_str, time_str, user_type))
        
        conn.commit()
        attendance_id = cursor.lastrowid
        conn.close()
        return attendance_id

    def mark_attendance(self, user_id, name, roll, type='student'):
        """Mark attendance for a user (wrapper around add_attendance for compatibility)"""
        from datetime import datetime
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M:%S')
        
        return self.add_attendance(user_id, name, current_date, current_time, type)
    
    def get_attendance(self, date_str=None):
        """Get attendance records for a specific date or all"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if date_str:
            cursor.execute('SELECT * FROM attendance WHERE date = ? ORDER BY time', (date_str,))
        else:
            cursor.execute('SELECT * FROM attendance ORDER BY date DESC, time')
        
        results = cursor.fetchall()
        conn.close()
        
        attendance = []
        for result in results:
            attendance.append({
                'id': result[0],
                'user_id': result[1],
                'name': result[2],
                'date': result[3],
                'time': result[4],
                'type': result[5],
                'created_timestamp': result[6]
            })
        
        return attendance
    
    def get_user_attendance_history(self, user_id):
        """Get attendance history for a specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM attendance WHERE user_id = ? ORDER BY date DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        attendance = []
        for result in results:
            # Normalize date format to YYYY-MM-DD
            normalized_date = self._normalize_date(result[3])
            attendance.append({
                'date': normalized_date,
                'time': result[4],
                'type': result[5]
            })
        
        return attendance
    
    def get_user_attendance_stats(self, user_id):
        """Get attendance statistics for a specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get total attendance count
            cursor.execute('''
                SELECT COUNT(*) as total_days,
                       COUNT(CASE WHEN date = date('now') THEN 1 END) as today_present,
                       MAX(created_timestamp) as last_attendance
                FROM attendance 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            
            return {
                'total_attendance_days': result[0] if result else 0,
                'present_today': bool(result[1]) if result else False,
                'last_attendance': result[2] if result else None
            }
        finally:
            conn.close()
    
    def get_user_attendance_for_date(self, user_id, date):
        """Check if user has attendance for specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM attendance 
                WHERE user_id = ? AND date = ?
            ''', (user_id, date))
            
            result = cursor.fetchone()
            return result is not None
        finally:
            conn.close()
    
    def get_attendance_data(self):
        """Get all attendance records in CSV format for compatibility"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, user_id, date, time, type 
            FROM attendance 
            ORDER BY date DESC, time DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        attendance_data = []
        for result in results:
            attendance_data.append({
                'Name': result[0],
                'Roll': result[1],
                'Date': result[2], 
                'Time': result[3],
                'Type': result[4] or 'student'
            })
        
        return attendance_data
    
    # Notice management
    def add_notice(self, title, content, priority='normal', created_by='admin'):
        """Add a new notice"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notices (title, content, priority, created_by)
            VALUES (?, ?, ?, ?)
        ''', (title, content, priority, created_by))
        
        conn.commit()
        notice_id = cursor.lastrowid
        conn.close()
        return notice_id
    
    def get_notices(self, active_only=True):
        """Get all notices"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if active_only:
            cursor.execute('SELECT * FROM notices WHERE is_active = 1 ORDER BY created_date DESC')
        else:
            cursor.execute('SELECT * FROM notices ORDER BY created_date DESC')
        
        results = cursor.fetchall()
        conn.close()
        
        notices = []
        for result in results:
            notices.append({
                'id': result[0],
                'title': result[1],
                'content': result[2],
                'priority': result[3],
                'created_date': result[4],
                'created_by': result[5],
                'is_active': result[6]
            })
        
        return notices
    
    def get_active_notices(self):
        """Get all active notices"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, content, priority, created_date, created_by
                FROM notices 
                WHERE is_active = 1 
                ORDER BY created_date DESC
            ''')
            
            results = cursor.fetchall()
            
            notices = []
            for result in results:
                notices.append({
                    'id': result[0],
                    'title': result[1],
                    'content': result[2],
                    'priority': result[3],
                    'created_date': result[4],
                    'created_by': result[5]
                })
            
            return notices
        finally:
            conn.close()
    
    def delete_notice(self, notice_id):
        """Delete a notice"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE notices SET is_active = 0 WHERE id = ?', (notice_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    # Backup and restore methods
    def backup_database(self, backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_{timestamp}.db"
        
        try:
            # Create backup directory if it doesn't exist
            backup_dir = os.path.dirname(backup_path) if os.path.dirname(backup_path) else 'backups'
            if not os.path.exists(backup_dir) and backup_dir:
                os.makedirs(backup_dir)
            
            # Copy database file
            import shutil
            shutil.copy2(self.db_path, backup_path)
            
            return backup_path
        except Exception as e:
            raise Exception(f"Backup failed: {str(e)}")
    
    def export_to_json(self, export_path=None):
        """Export database to JSON format"""
        if export_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"export_{timestamp}.json"
        
        try:
            data = {
                'users': self.get_all_users(),
                'attendance': self.get_attendance(),
                'notices': self.get_notices(active_only=False),
                'export_date': datetime.now().isoformat()
            }
            
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return export_path
        except Exception as e:
            raise Exception(f"Export failed: {str(e)}")
    
    def export_attendance_csv(self, date_str=None, export_path=None):
        """Export attendance to CSV"""
        if export_path is None:
            if date_str:
                export_path = f"attendance_{date_str}.csv"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                export_path = f"attendance_all_{timestamp}.csv"
        
        try:
            attendance_data = self.get_attendance(date_str)
            
            if attendance_data:
                df = pd.DataFrame(attendance_data)
                df.to_csv(export_path, index=False)
            else:
                # Create empty CSV with headers
                df = pd.DataFrame(columns=['user_id', 'name', 'date', 'time', 'type'])
                df.to_csv(export_path, index=False)
            
            return export_path
        except Exception as e:
            raise Exception(f"CSV export failed: {str(e)}")
    
    # Statistics methods
    def get_attendance_stats(self):
        """Get attendance statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total registered users
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
        total_users = cursor.fetchone()[0]
        
        # Today's attendance
        today = datetime.now().strftime("%m_%d_%y")
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ?', (today,))
        today_attendance = cursor.fetchone()[0]
        
        # Students vs employees today
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND type = "student"', (today,))
        students_today = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND type = "employee"', (today,))
        employees_today = cursor.fetchone()[0]
        
        # Total notices
        cursor.execute('SELECT COUNT(*) FROM notices WHERE is_active = 1')
        total_notices = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'today_attendance': today_attendance,
            'students_today': students_today,
            'employees_today': employees_today,
            'total_notices': total_notices
        }
    
    def get_attendance_trends(self, days=7):
        """Get attendance trends for the last N days"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        trends = []
        for i in range(days):
            date_obj = datetime.now() - pd.Timedelta(days=i)
            date_str = date_obj.strftime("%m_%d_%y")
            
            cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ?', (date_str,))
            total = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND type = "student"', (date_str,))
            students = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM attendance WHERE date = ? AND type = "employee"', (date_str,))
            employees = cursor.fetchone()[0]
            
            trends.append({
                'date': date_str,
                'total': total,
                'students': students,
                'employees': employees
            })
        
        conn.close()
        trends.reverse()  # Show oldest to newest
        return trends

    # Missing methods needed by app.py
    def init_db(self):
        """Initialize database - alias for backward compatibility"""
        self.init_database()
    
    def get_all_notices(self):
        """Get all notices - alias for compatibility"""
        return self.get_notices(active_only=False)
    
    def get_attendance_history(self):
        """Get attendance history grouped by date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT date, user_id, name, time, type
                FROM attendance 
                ORDER BY date DESC, time DESC
            ''')
            
            results = cursor.fetchall()
            
            # Group by date
            history = {}
            for result in results:
                date_str = result[0]
                if date_str not in history:
                    history[date_str] = []
                
                history[date_str].append({
                    'user_id': result[1],
                    'name': result[2],
                    'date': result[0],
                    'time': result[3],
                    'type': result[4]
                })
            
            return history
        finally:
            conn.close()
    
    def get_analytics_data(self):
        """Get comprehensive analytics data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Basic stats
            stats = self.get_attendance_stats()
            
            # Weekly trends
            weekly_trends = self.get_attendance_trends(7)
            
            # Monthly summary
            cursor.execute('''
                SELECT 
                    COUNT(DISTINCT user_id) as unique_attendees,
                    COUNT(*) as total_records,
                    AVG(CASE WHEN type = 'student' THEN 1.0 ELSE 0.0 END) * 100 as student_percentage
                FROM attendance 
                WHERE date >= date('now', '-30 days')
            ''')
            monthly_data = cursor.fetchone()
            
            # Top attendance users
            cursor.execute('''
                SELECT user_id, name, COUNT(*) as attendance_count
                FROM attendance 
                WHERE date >= date('now', '-30 days')
                GROUP BY user_id, name
                ORDER BY attendance_count DESC
                LIMIT 10
            ''')
            top_attendees = cursor.fetchall()
            
            # If no real data, return mock data for demo
            if not top_attendees:
                return self.get_mock_admin_analytics()
            
            return {
                'basic_stats': stats,
                'weekly_trends': weekly_trends,
                'monthly_summary': {
                    'unique_attendees': monthly_data[0] if monthly_data else 0,
                    'total_records': monthly_data[1] if monthly_data else 0,
                    'student_percentage': round(monthly_data[2] if monthly_data else 0, 1)
                },
                'top_attendees': [
                    {
                        'user_id': row[0],
                        'name': row[1],
                        'attendance_count': row[2]
                    } for row in top_attendees
                ],
                'monthly_trend': self.get_mock_monthly_trend(),
                'weekly_pattern': self.get_mock_weekly_pattern(),
                'recent_system_activity': self.get_mock_recent_activity(),
                'class_wise_stats': self.get_mock_class_stats(),
                'attendance_by_time': self.get_mock_time_distribution()
            }
        finally:
            conn.close()

    def get_mock_admin_analytics(self):
        """Generate comprehensive mock analytics for admin dashboard"""
        import random
        
        return {
            'basic_stats': {
                'total_users': 156,
                'today_attendance': 142,
                'students_today': 128,
                'employees_today': 14,
                'total_notices': 8
            },
            'weekly_trends': [
                {'date': '01_13_25', 'total': 145, 'students': 130, 'employees': 15},
                {'date': '01_14_25', 'total': 138, 'students': 125, 'employees': 13},
                {'date': '01_15_25', 'total': 152, 'students': 135, 'employees': 17},
                {'date': '01_16_25', 'total': 149, 'students': 132, 'employees': 17},
                {'date': '01_17_25', 'total': 142, 'students': 128, 'employees': 14},
                {'date': '01_18_25', 'total': 156, 'students': 140, 'employees': 16},
                {'date': '01_19_25', 'total': 134, 'students': 120, 'employees': 14}
            ],
            'monthly_summary': {
                'unique_attendees': 156,
                'total_records': 2847,
                'student_percentage': 89.2
            },
            'top_attendees': [
                {'user_id': 'CS001', 'name': 'Alice Johnson', 'attendance_count': 28},
                {'user_id': 'CS002', 'name': 'Bob Smith', 'attendance_count': 27},
                {'user_id': 'CS003', 'name': 'Carol Davis', 'attendance_count': 26},
                {'user_id': 'EE001', 'name': 'David Wilson', 'attendance_count': 25},
                {'user_id': 'ME001', 'name': 'Emma Brown', 'attendance_count': 25},
                {'user_id': 'CS004', 'name': 'Frank Miller', 'attendance_count': 24},
                {'user_id': 'IT001', 'name': 'Grace Lee', 'attendance_count': 24},
                {'user_id': 'CS005', 'name': 'Henry Taylor', 'attendance_count': 23},
                {'user_id': 'EE002', 'name': 'Ivy Chen', 'attendance_count': 23},
                {'user_id': 'ME002', 'name': 'Jack Anderson', 'attendance_count': 22}
            ],
            'monthly_trend': self.get_mock_monthly_trend(),
            'weekly_pattern': self.get_mock_weekly_pattern(),
            'recent_system_activity': self.get_mock_recent_activity(),
            'class_wise_stats': self.get_mock_class_stats(),
            'attendance_by_time': self.get_mock_time_distribution()
        }

    def get_mock_monthly_trend(self):
        """Generate mock monthly attendance trend"""
        return [
            {'month': 'Aug 2024', 'attendance': 2156, 'students': 1924, 'employees': 232},
            {'month': 'Sep 2024', 'attendance': 2298, 'students': 2045, 'employees': 253},
            {'month': 'Oct 2024', 'attendance': 2187, 'students': 1956, 'employees': 231},
            {'month': 'Nov 2024', 'attendance': 2345, 'students': 2089, 'employees': 256},
            {'month': 'Dec 2024', 'attendance': 1876, 'students': 1678, 'employees': 198},
            {'month': 'Jan 2025', 'attendance': 2847, 'students': 2541, 'employees': 306}
        ]

    def get_mock_weekly_pattern(self):
        """Generate mock weekly attendance pattern"""
        return [
            {'day': 'Monday', 'average': 148, 'students': 132, 'employees': 16},
            {'day': 'Tuesday', 'average': 152, 'students': 135, 'employees': 17},
            {'day': 'Wednesday', 'average': 145, 'students': 129, 'employees': 16},
            {'day': 'Thursday', 'average': 149, 'students': 133, 'employees': 16},
            {'day': 'Friday', 'average': 142, 'students': 127, 'employees': 15},
            {'day': 'Saturday', 'average': 89, 'students': 78, 'employees': 11},
            {'day': 'Sunday', 'average': 34, 'students': 28, 'employees': 6}
        ]

    def get_mock_recent_activity(self):
        """Generate mock recent system activity"""
        import random
        from datetime import datetime, timedelta
        
        activities = []
        names = ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown', 
                'Frank Miller', 'Grace Lee', 'Henry Taylor', 'Ivy Chen', 'Jack Anderson']
        user_ids = ['CS001', 'CS002', 'CS003', 'EE001', 'ME001', 'CS004', 'IT001', 'CS005', 'EE002', 'ME002']
        
        for i in range(20):
            time_ago = datetime.now() - timedelta(hours=random.randint(1, 48))
            activities.append({
                'type': 'attendance',
                'user_id': random.choice(user_ids),
                'user_name': random.choice(names),
                'timestamp': time_ago.strftime('%Y-%m-%d %H:%M:%S'),
                'action': 'Marked attendance'
            })
        
        return activities

    def get_mock_class_stats(self):
        """Generate mock class-wise statistics"""
        return [
            {'class': 'CS 4th Year', 'total_students': 45, 'present_today': 42, 'attendance_rate': 93.3},
            {'class': 'EE 3rd Year', 'total_students': 38, 'present_today': 35, 'attendance_rate': 92.1},
            {'class': 'ME 2nd Year', 'total_students': 41, 'present_today': 36, 'attendance_rate': 87.8},
            {'class': 'IT 4th Year', 'total_students': 32, 'present_students': 29, 'attendance_rate': 90.6},
            {'class': 'Faculty', 'total_members': 18, 'present_today': 16, 'attendance_rate': 88.9}
        ]

    def get_mock_time_distribution(self):
        """Generate mock attendance time distribution"""
        return [
            {'time_slot': '08:00-09:00', 'count': 45, 'percentage': 31.7},
            {'time_slot': '09:00-10:00', 'count': 67, 'percentage': 47.2},
            {'time_slot': '10:00-11:00', 'count': 23, 'percentage': 16.2},
            {'time_slot': '11:00-12:00', 'count': 7, 'percentage': 4.9}
        ]
    
    def get_recent_activity(self, limit=20):
        """Get recent activity for admin dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    'attendance' as type,
                    user_id,
                    name,
                    date || ' ' || time as timestamp,
                    'Marked attendance' as action
                FROM attendance
                ORDER BY created_timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            
            activities = []
            for result in results:
                activities.append({
                    'type': result[0],
                    'user_id': result[1],
                    'user_name': result[2],
                    'timestamp': result[3],
                    'action': result[4]
                })
            
            return activities
        finally:
            conn.close()
    
    def get_user_attendance(self, user_id):
        """Get attendance records for a specific user"""
        return self.get_user_attendance_history(user_id)
    
    def get_user_analytics(self, user_id):
        """Get analytics data for a specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # User's attendance stats
            stats = self.get_user_attendance_stats(user_id)
            
            # User's attendance history (last 30 days)
            cursor.execute('''
                SELECT date, time
                FROM attendance 
                WHERE user_id = ? AND date >= date('now', '-30 days')
                ORDER BY date DESC
            ''', (user_id,))
            
            recent_attendance = cursor.fetchall()
            
            # Attendance frequency by day of week
            cursor.execute('''
                SELECT 
                    CASE strftime('%w', date)
                        WHEN '0' THEN 'Sunday'
                        WHEN '1' THEN 'Monday'
                        WHEN '2' THEN 'Tuesday'
                        WHEN '3' THEN 'Wednesday'
                        WHEN '4' THEN 'Thursday'
                        WHEN '5' THEN 'Friday'
                        WHEN '6' THEN 'Saturday'
                    END as day_name,
                    COUNT(*) as count
                FROM attendance 
                WHERE user_id = ?
                GROUP BY strftime('%w', date)
                ORDER BY strftime('%w', date)
            ''', (user_id,))
            
            day_frequency = cursor.fetchall()
            
            # If no real data, return mock data for demo
            if not recent_attendance:
                return self.get_mock_user_analytics(user_id)
            
            return {
                'basic_stats': stats,
                'recent_attendance': [
                    {'date': row[0], 'time': row[1]} 
                    for row in recent_attendance
                ],
                'day_frequency': [
                    {'day': row[0], 'count': row[1]} 
                    for row in day_frequency
                ],
                'attendance_rate': round(len(recent_attendance) / 30 * 100, 1) if recent_attendance else 0
            }
        finally:
            conn.close()

    def get_mock_user_analytics(self, user_id):
        """Generate mock analytics data for demo purposes"""
        import random
        from datetime import datetime, timedelta
        
        # Generate mock attendance for last 30 days
        mock_attendance = []
        base_date = datetime.now()
        
        for i in range(30):
            date = base_date - timedelta(days=i)
            # 85% chance of attendance on weekdays, 20% on weekends
            attendance_chance = 0.85 if date.weekday() < 5 else 0.20
            
            if random.random() < attendance_chance:
                # Random time between 8:00 and 10:00 AM
                hour = random.randint(8, 9)
                minute = random.randint(0, 59)
                time_str = f"{hour:02d}:{minute:02d}:00"
                
                mock_attendance.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'time': time_str
                })
        
        # Day frequency mock data
        day_frequency = [
            {'day': 'Monday', 'count': random.randint(8, 12)},
            {'day': 'Tuesday', 'count': random.randint(7, 11)},
            {'day': 'Wednesday', 'count': random.randint(8, 12)},
            {'day': 'Thursday', 'count': random.randint(6, 10)},
            {'day': 'Friday', 'count': random.randint(7, 11)},
            {'day': 'Saturday', 'count': random.randint(1, 3)},
            {'day': 'Sunday', 'count': random.randint(0, 2)}
        ]
        
        return {
            'basic_stats': {
                'total_attendance_days': len(mock_attendance),
                'present_today': random.choice([True, False]),
                'last_attendance': mock_attendance[0]['date'] if mock_attendance else None
            },
            'recent_attendance': mock_attendance,
            'day_frequency': day_frequency,
            'attendance_rate': round(len(mock_attendance) / 30 * 100, 1),
            'monthly_trend': [
                {'month': 'Jan', 'attendance': random.randint(18, 22)},
                {'month': 'Feb', 'attendance': random.randint(16, 20)},
                {'month': 'Mar', 'attendance': random.randint(19, 23)},
                {'month': 'Apr', 'attendance': random.randint(17, 21)},
                {'month': 'May', 'attendance': random.randint(18, 22)},
                {'month': 'Jun', 'attendance': random.randint(15, 19)}
            ],
            'weekly_pattern': [
                {'week': 'Week 1', 'days': random.randint(4, 5)},
                {'week': 'Week 2', 'days': random.randint(3, 5)},
                {'week': 'Week 3', 'days': random.randint(4, 5)},
                {'week': 'Week 4', 'days': random.randint(3, 5)}
            ]
        }
