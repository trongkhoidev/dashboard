"""
SQLAlchemy Models for MySQL (PAYROLL_2026) Database
Tables: employees_payroll, departments_payroll, positions_payroll
"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database.connections import Base_Payroll


class EmployeePayroll(Base_Payroll):
    """Employee model mapping to MySQL employees_payroll table"""
    __tablename__ = 'employees_payroll'
    
    EmployeeID = Column(Integer, primary_key=True)
    FullName = Column(String(100), nullable=False)
    DepartmentID = Column(Integer, nullable=True)
    PositionID = Column(Integer, nullable=True)
    Status = Column(String(50), nullable=True)
    SyncedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DepartmentPayroll(Base_Payroll):
    """Department model mapping to MySQL departments_payroll table"""
    __tablename__ = 'departments_payroll'
    
    DepartmentID = Column(Integer, primary_key=True)
    DepartmentName = Column(String(100), nullable=False)
    SyncedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PositionPayroll(Base_Payroll):
    """Position model mapping to MySQL positions_payroll table"""
    __tablename__ = 'positions_payroll'
    
    PositionID = Column(Integer, primary_key=True)
    PositionName = Column(String(100), nullable=False)
    SyncedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
