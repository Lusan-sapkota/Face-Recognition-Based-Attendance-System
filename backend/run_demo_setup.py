#!/usr/bin/env python3
"""
RecognizeMe Demo Data Setup Script
Quickly populate the system with comprehensive demo data
"""

import os
import sys
from mock_data import MockDataGenerator
from database import Database

def main():
    print("🎯 RecognizeMe Demo Data Setup")
    print("=" * 50)
    
    try:
        # Initialize database and mock data generator
        print("📊 Initializing database...")
        db = Database()
        mock_gen = MockDataGenerator(db)
        
        # Check if data already exists
        existing_users = db.get_all_users()
        if len(existing_users) > 0:
            print(f"⚠️  Found {len(existing_users)} existing users in database")
            response = input("Do you want to add demo data anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("❌ Demo data setup cancelled")
                return
        
        # Populate demo data
        print("\n🚀 Populating demo data...")
        result = mock_gen.populate_demo_data()
        
        # Get summary
        print("\n📈 Getting demo summary...")
        summary = mock_gen.get_demo_analytics_summary()
        
        print("\n✅ Demo Data Setup Complete!")
        print("=" * 50)
        print(f"👥 Total Users: {summary['total_users']}")
        print(f"   📚 Students: {summary['students']}")
        print(f"   👨‍🏫 Teachers: {summary['teachers']}")
        print(f"   👨‍💼 Staff: {summary['staff']}")
        print(f"📢 Notices: {summary['total_notices']}")
        print(f"📈 Today's Attendance: {summary['attendance_stats']['today_attendance']}")
        
        print("\n🔐 Demo Login Credentials:")
        print("=" * 30)
        print("🔑 Admin Access:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👤 User Access:")
        print("   Username: [any demo username]")
        print("   Password: demo123")
        print("\n💡 Example Users:")
        print("   alice.johnson / demo123")
        print("   bob.smith / demo123")
        print("   sarah.mitchell / demo123")
        
        print("\n🌐 Next Steps:")
        print("1. Start the backend server: python app.py")
        print("2. Start the frontend: npm run dev")
        print("3. Visit http://localhost:5173")
        print("4. Login with admin credentials to explore admin features")
        print("5. Login with user credentials to explore student/teacher features")
        
        print("\n🎉 Enjoy exploring RecognizeMe with realistic demo data!")
        
    except Exception as e:
        print(f"❌ Error during demo setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()