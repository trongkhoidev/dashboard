"""
Database Connection Manager với Improved Error Handling
Manages dual database connections to SQL Server (HUMAN_2025) and MySQL (PAYROLL_2026)
"""
from sqlalchemy import create_engine, text
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
        self.sql_server_available = False
        self.mysql_available = False
        
    def init_databases(self):
        """Initialize both database connections with graceful error handling"""
        # Try SQL Server Connection
        try:
            print("🔵 Attempting SQL Server connection...")
            from urllib.parse import quote_plus
            
            sql_server_host = os.getenv('SQL_SERVER_HOST', '127.0.0.1')
            sql_server_port = os.getenv('SQL_SERVER_PORT', '1433')
            sql_server_user = os.getenv('SQL_SERVER_USER')
            sql_server_password = os.getenv('SQL_SERVER_PASSWORD')
            sql_server_db = os.getenv('SQL_SERVER_DATABASE')
            
            # Build ODBC connection string
            odbc_conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={sql_server_host},{sql_server_port};"
                f"DATABASE={sql_server_db};"
                f"UID={sql_server_user};"
                f"PWD={sql_server_password};"
                f"TrustServerCertificate=yes;"
                f"Encrypt=no;"
                f"LoginTimeout=30"
            )
            
            # SQLAlchemy connection string with URL encoded ODBC string
            sql_server_conn_str = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_conn_str)}"
            
            self.sql_server_engine = create_engine(
                sql_server_conn_str,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30
            )
            
            # Test connection
            with self.sql_server_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.SessionLocal_HR = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.sql_server_engine
            )
            
            self.sql_server_available = True
            print("✅ SQL Server connected successfully")
            
        except Exception as e:
            print(f"⚠️  SQL Server unavailable: {str(e)[:100]}")
            print("   API will run with limited functionality")
            self.sql_server_engine = None
            self.SessionLocal_HR = None
        
        # Try MySQL Connection
        try:
            print("🟢 Attempting MySQL connection...")
            mysql_host = os.getenv('MYSQL_HOST', 'localhost')
            mysql_port = os.getenv('MYSQL_PORT', '3306')
            mysql_user = os.getenv('MYSQL_USER')
            mysql_password = os.getenv('MYSQL_PASSWORD', '')
            mysql_db = os.getenv('MYSQL_DATABASE')
            
            if mysql_password:
                mysql_conn_str = (
                    f"mysql+pymysql://{mysql_user}:{mysql_password}"
                    f"@{mysql_host}:{mysql_port}/{mysql_db}"
                )
            else:
                mysql_conn_str = (
                    f"mysql+pymysql://{mysql_user}"
                    f"@{mysql_host}:{mysql_port}/{mysql_db}"
                )
            
            self.mysql_engine = create_engine(
                mysql_conn_str,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                pool_timeout=3
            )
            
            # Test connection
            with self.mysql_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.SessionLocal_Payroll = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.mysql_engine
            )
            
            self.mysql_available = True
            print("✅ MySQL connected successfully")
            
        except Exception as e:
            print(f"⚠️  MySQL unavailable: {str(e)[:100]}")
            print("   API will run with limited functionality")
            self.mysql_engine = None
            self.SessionLocal_Payroll = None
        
    @contextmanager
    def get_hr_db(self):
        """Get SQL Server (HR) database session"""
        if not self.SessionLocal_HR:
            raise RuntimeError("SQL Server not available. Please check database configuration.")
        db = self.SessionLocal_HR()
        try:
            yield db
        finally:
            db.close()
            
    @contextmanager
    def get_payroll_db(self):
        """Get MySQL (Payroll) database session"""
        if not self.SessionLocal_Payroll:
            raise RuntimeError("MySQL not available. Please check database configuration.")
        db = self.SessionLocal_Payroll()
        try:
            yield db
        finally:
            db.close()
    
    def test_connections(self):
        """Test both database connections"""
        all_ok = True
        
        # Test SQL Server
        if self.sql_server_engine:
            try:
                with self.get_hr_db() as db:
                    result = db.execute(text("SELECT @@VERSION")).fetchone()
                    print(f"✅ SQL Server OK: {result[0][:50]}...")
            except Exception as e:
                print(f"❌ SQL Server test failed: {e}")
                all_ok = False
        else:
            print("⚠️  SQL Server not initialized")
            all_ok = False
                
        # Test MySQL
        if self.mysql_engine:
            try:
                with self.get_payroll_db() as db:
                    result = db.execute(text("SELECT VERSION()")).fetchone()
                    print(f"✅ MySQL OK: Version {result[0]}")
            except Exception as e:
                print(f"❌ MySQL test failed: {e}")
                all_ok = False
        else:
            print("⚠️  MySQL not initialized")
            all_ok = False
                
        return all_ok


# Global database manager instance
db_manager = DatabaseManager()
