"""
SQLAlchemy Models for SQL Server (HUMAN_2025) Database
Tables: Employees, Departments, Positions, Dividends
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connections import Base_HR


class Employee(Base_HR):
    """Employee model mapping to SQL Server Employees table"""
    __tablename__ = 'Employees'
    
    EmployeeID = Column(Integer, primary_key=True, autoincrement=True)
    FullName = Column(String(100), nullable=False)
    DateOfBirth = Column(Date, nullable=False)
    Gender = Column(String(10), nullable=True)
    PhoneNumber = Column(String(15), nullable=True)
    Email = Column(String(100), nullable=True)
    HireDate = Column(Date, nullable=False)
    DepartmentID = Column(Integer, ForeignKey('Departments.DepartmentID'), nullable=True)
    PositionID = Column(Integer, ForeignKey('Positions.PositionID'), nullable=True)
    Status = Column(String(50), nullable=True, default='Đang làm việc')
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")
    dividends = relationship("Dividend", back_populates="employee")


class Department(Base_HR):
    """Department model mapping to SQL Server Departments table"""
    __tablename__ = 'Departments'
    
    DepartmentID = Column(Integer, primary_key=True, autoincrement=True)
    DepartmentName = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employees = relationship("Employee", back_populates="department")


class Position(Base_HR):
    """Position model mapping to SQL Server Positions table"""
    __tablename__ = 'Positions'
    
    PositionID = Column(Integer, primary_key=True, autoincrement=True)
    PositionName = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employees = relationship("Employee", back_populates="position")


class Dividend(Base_HR):
    """Dividend model mapping to SQL Server Dividends table"""
    __tablename__ = 'Dividends'
    
    DividendID = Column(Integer, primary_key=True, autoincrement=True)
    EmployeeID = Column(Integer, ForeignKey('Employees.EmployeeID'), nullable=True)
    DividendAmount = Column(Numeric(12, 2), nullable=False)
    DividendDate = Column(Date, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="dividends")
