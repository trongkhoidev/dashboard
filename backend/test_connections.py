"""
Test Database Connections
Run this script to verify SQL Server and MySQL connections
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connections import db_manager

def main():
    print("=" * 80)
    print("TESTING DATABASE CONNECTIONS")
    print("=" * 80)
    
    try:
        # Initialize databases
        print("\n📡 Initializing database connections...")
        db_manager.init_databases()
        
        # Test connections
        print("\n🔍 Testing connections...")
        success = db_manager.test_connections()
        
        if success:
            print("\n" + "=" * 80)
            print("✅ ALL TESTS PASSED - Database connections successful!")
            print("=" * 80)
            return 0
        else:
            print("\n" + "=" * 80)
            print("❌ TESTS FAILED - Check connection details in .env")
            print("=" * 80)
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check .env file exists và filled correctly")
        print("  2. Verify SQL Server is running (Azure Data Studio)")
        print("  3. Verify MySQL is running: brew services list")
        print("  4. Check database names: HUMAN_2025 and payroll_2026")
        return 1

if __name__ == "__main__":
    exit(main())
