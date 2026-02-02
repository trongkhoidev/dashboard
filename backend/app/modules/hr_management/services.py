"""
HR Management Business Logic Services
Core services: Unified Profile, Sync Detection, Sync Execution
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Optional
from datetime import datetime

from ...database.models_hr import Employee, Department, Position, Dividend
from ...database.models_payroll import EmployeePayroll, DepartmentPayroll, PositionPayroll
from .schemas import (
    EmployeeDetail, EmployeeListItem, SyncNeed, SyncCheckResponse,
    SyncExecuteResponse, OrgStructureNode, OrgStructureResponse,
    DepartmentSchema, DividendSchema
)


class HRService:
    """Service for HR Management operations"""
    
    @staticmethod
    def get_unified_employee_profile(
        hr_db: Session,
        payroll_db: Session,
        employee_id: int
    ) -> Optional[EmployeeDetail]:
        """
        Get unified employee profile by joining HR and Payroll data
        BR-01: SQL Server is single source of truth
        """
        # Query từ SQL Server
        employee = hr_db.query(Employee).options(
            joinedload(Employee.department),
            joinedload(Employee.position)
        ).filter(Employee.EmployeeID == employee_id).first()
        
        if not employee:
            return None
        
        # Check sync status với MySQL
        payroll_employee = payroll_db.query(EmployeePayroll).filter(
            EmployeePayroll.EmployeeID == employee_id
        ).first()
        
        # Determine sync status
        sync_status = "synced"
        if not payroll_employee:
            sync_status = "needs_sync"
        elif (payroll_employee.DepartmentID != employee.DepartmentID or
              payroll_employee.PositionID != employee.PositionID or
              payroll_employee.Status != employee.Status):
            sync_status = "needs_sync"
        
        # Build unified profile
        return EmployeeDetail(
            EmployeeID=employee.EmployeeID,
            FullName=employee.FullName,
            DateOfBirth=employee.DateOfBirth,
            Gender=employee.Gender,
            PhoneNumber=employee.PhoneNumber,
            Email=employee.Email,
            HireDate=employee.HireDate,
            DepartmentID=employee.DepartmentID,
            PositionID=employee.PositionID,
            DepartmentName=employee.department.DepartmentName if employee.department else None,
            PositionName=employee.position.PositionName if employee.position else None,
            Status=employee.Status,
            SyncStatus=sync_status,
            CreatedAt=employee.CreatedAt,
            UpdatedAt=employee.UpdatedAt
        )
    
    @staticmethod
    def list_employees_with_sync_status(
        hr_db: Session,
        payroll_db: Session,
        department_id: Optional[int] = None,
        search_name: Optional[str] = None
    ) -> List[EmployeeListItem]:
        """
        List all employees với sync status
        Support filter by department và search by name
        """
        # Query từ SQL Server
        query = hr_db.query(Employee).options(
            joinedload(Employee.department),
            joinedload(Employee.position)
        )
        
        if department_id:
            query = query.filter(Employee.DepartmentID == department_id)
        
        if search_name:
            query = query.filter(Employee.FullName.like(f'%{search_name}%'))
        
        employees = query.all()
        
        # Get all payroll employees để compare
        payroll_employees = {
            emp.EmployeeID: emp
            for emp in payroll_db.query(EmployeePayroll).all()
        }
        
        result = []
        for employee in employees:
            payroll_emp = payroll_employees.get(employee.EmployeeID)
            
            # Determine sync status
            if not payroll_emp:
                sync_status = "needs_sync"
            elif (payroll_emp.DepartmentID != employee.DepartmentID or
                  payroll_emp.PositionID != employee.PositionID or
                  payroll_emp.Status != employee.Status):
                sync_status = "needs_sync"
            else:
                sync_status = "synced"
            
            result.append(EmployeeListItem(
                EmployeeID=employee.EmployeeID,
                FullName=employee.FullName,
                DepartmentName=employee.department.DepartmentName if employee.department else "Chưa phân công",
                PositionName=employee.position.PositionName if employee.position else "Chưa xác định",
                Status=employee.Status or "Đang làm việc",
                SyncStatus=sync_status,
                HireDate=employee.HireDate
            ))
        
        return result
    
    @staticmethod
    def get_organization_structure(
        hr_db: Session,
        payroll_db: Session
    ) -> OrgStructureResponse:
        """Get organization structure với employees grouped by department"""
        departments = hr_db.query(Department).all()
        
        org_nodes = []
        total_employees = 0
        
        for dept in departments:
            # Get employees trong department này
            employees = HRService.list_employees_with_sync_status(
                hr_db, payroll_db, department_id=dept.DepartmentID
            )
            
            total_employees += len(employees)
            
            org_nodes.append(OrgStructureNode(
                DepartmentID=dept.DepartmentID,
                DepartmentName=dept.DepartmentName,
                Employees=employees,
                EmployeeCount=len(employees)
            ))
        
        return OrgStructureResponse(
            Departments=org_nodes,
            TotalDepartments=len(departments),
            TotalEmployees=total_employees
        )
    
    @staticmethod
    def get_departments(hr_db: Session) -> List[DepartmentSchema]:
        """Get all departments"""
        departments = hr_db.query(Department).all()
        return [
            DepartmentSchema(
                DepartmentID=dept.DepartmentID,
                DepartmentName=dept.DepartmentName,
                EmployeeCount=len(dept.employees)
            )
            for dept in departments
        ]
    
    @staticmethod
    def get_employee_dividends(
        hr_db: Session,
        employee_id: Optional[int] = None
    ) -> List[DividendSchema]:
        """
        Get dividends from SQL Server
        Filter by employee_id nếu provided
        """
        query = hr_db.query(Dividend).options(joinedload(Dividend.employee))
        
        if employee_id:
            query = query.filter(Dividend.EmployeeID == employee_id)
        
        dividends = query.all()
        
        return [
            DividendSchema(
                DividendID=div.DividendID,
                EmployeeID=div.EmployeeID,
                EmployeeName=div.employee.FullName if div.employee else None,
                DividendAmount=div.DividendAmount,
                DividendDate=div.DividendDate,
                CreatedAt=div.CreatedAt
            )
            for div in dividends
        ]
