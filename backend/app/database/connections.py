"""
Database Connection Manager
Manages dual database connections to SQL Server (HUMAN_2025) and MySQL (PAYROLL_2026)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# Base classes for ORM models
Base_HR = declarative_base()
Base_Payroll = declarative_base()


class DatabaseManager:
    """Manages connections to both HR and Payroll databases"""
    
    def __init__(self):
        self.sql_server_engine = None
        self.mysql_engine = None
        self.SessionLocal_HR = None
        self.SessionLocal_Payroll = None
        
    def init_databases(self):
        """Initialize both database connections"""
        # SQL Server Connection (HUMAN_2025)
        sql_server_conn_str = (
            f"mssql+pyodbc://{os.getenv('SQL_SERVER_USER')}:{os.getenv('SQL_SERVER_PASSWORD')}"
            f"@{os.getenv('SQL_SERVER_HOST')},{os.getenv('SQL_SERVER_PORT')}"
            f"/{os.getenv('SQL_SERVER_DATABASE')}"
            f"?driver=ODBC+Driver+18+for+SQL+Server"
            f"&TrustServerCertificate=yes"
        )
        
        self.sql_server_engine = create_engine(
            sql_server_conn_str,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=os.getenv('DEBUG', 'False') == 'True'
        )
        
        # MySQL Connection (PAYROLL_2026)
        mysql_password = os.getenv('MYSQL_PASSWORD', '')
        if mysql_password:
            mysql_conn_str = (
                f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{mysql_password}"
                f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}"
                f"/{os.getenv('MYSQL_DATABASE')}"
            )
        else:
            mysql_conn_str = (
                f"mysql+pymysql://{os.getenv('MYSQL_USER')}"
                f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}"
                f"/{os.getenv('MYSQL_DATABASE')}"
            )
        
        self.mysql_engine = create_engine(
            mysql_conn_str,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=os.getenv('DEBUG', 'False') == 'True'
        )
        
        # Create session factories
        self.SessionLocal_HR = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.sql_server_engine
        )
        
        self.SessionLocal_Payroll = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.mysql_engine
        )
        
        print("✅ Database connections initialized successfully")
        
    @contextmanager
    def get_hr_db(self):
        """Get SQL Server (HR) database session"""
        db = self.SessionLocal_HR()
        try:
            yield db
        finally:
            db.close()
            
    @contextmanager
    def get_payroll_db(self):
        """Get MySQL (Payroll) database session"""
        db = self.SessionLocal_Payroll()
        try:
            yield db
        finally:
            db.close()
    
    def test_connections(self):
        """Test both database connections"""
        try:
            # Test SQL Server
            with self.get_hr_db() as db:
                result = db.execute("SELECT @@VERSION").fetchone()
                print(f"✅ SQL Server connected: {result[0][:50]}...")
                
            # Test MySQL
            with self.get_payroll_db() as db:
                result = db.execute("SELECT VERSION()").fetchone()
                print(f"✅ MySQL connected: Version {result[0]}")
                
            return True
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()
