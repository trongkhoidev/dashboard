"""
Sync Service - Handles synchronization between HR and Payroll databases
BR-01: SQL Server is single source of truth
BR-03: Auto-create employee in MySQL if not exists (salary = 0)
BR-04: Update department/position if changed
BR-05: Soft delete only (Status = 'Inactive')
"""
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...database.models_hr import Employee, Department, Position
from ...database.models_payroll import (
    EmployeePayroll, DepartmentPayroll, PositionPayroll
)
from .schemas import SyncNeed, SyncCheckResponse, SyncExecuteResponse


class SyncService:
    """Service for database synchronization operations"""
    
    @staticmethod
    def check_sync_needs(
        hr_db: Session,
        payroll_db: Session
    ) -> SyncCheckResponse:
        """
        Detect employees needing sync by comparing HR and Payroll databases
        Returns detailed list của employees cần INSERT hoặc UPDATE
        """
        # Get all employees từ SQL Server (source of truth)
        hr_employees = hr_db.query(Employee).all()
        
        # Get all employees từ MySQL payroll
        payroll_employees = {
            emp.EmployeeID: emp
            for emp in payroll_db.query(EmployeePayroll).all()
        }
        
        sync_needs = []
        need_sync_count = 0
        already_synced_count = 0
        
        for hr_emp in hr_employees:
            payroll_emp = payroll_employees.get(hr_emp.EmployeeID)
            
            if not payroll_emp:
                # Employee không tồn tại trong payroll -> cần INSERT
                sync_needs.append(SyncNeed(
                    EmployeeID=hr_emp.EmployeeID,
                    FullName=hr_emp.FullName,
                    Action="INSERT",
                    Reason=f"Employee chưa tồn tại trong payroll system",
                    HRData={
                        "DepartmentID": hr_emp.DepartmentID,
                        "PositionID": hr_emp.PositionID,
                        "Status": hr_emp.Status
                    },
                    PayrollData=None
                ))
                need_sync_count += 1
                
            elif (payroll_emp.DepartmentID != hr_emp.DepartmentID or
                  payroll_emp.PositionID != hr_emp.PositionID or
                  payroll_emp.Status != hr_emp.Status or
                  payroll_emp.FullName != hr_emp.FullName):
                # Data không khớp -> cần UPDATE
                changes = []
                if payroll_emp.FullName != hr_emp.FullName:
                    changes.append(f"FullName: {payroll_emp.FullName} -> {hr_emp.FullName}")
                if payroll_emp.DepartmentID != hr_emp.DepartmentID:
                    changes.append(f"DepartmentID: {payroll_emp.DepartmentID} -> {hr_emp.DepartmentID}")
                if payroll_emp.PositionID != hr_emp.PositionID:
                    changes.append(f"PositionID: {payroll_emp.PositionID} -> {hr_emp.PositionID}")
                if payroll_emp.Status != hr_emp.Status:
                    changes.append(f"Status: {payroll_emp.Status} -> {hr_emp.Status}")
                
                sync_needs.append(SyncNeed(
                    EmployeeID=hr_emp.EmployeeID,
                    FullName=hr_emp.FullName,
                    Action="UPDATE",
                    Reason=f"Thay đổi: {', '.join(changes)}",
                    HRData={
                        "DepartmentID": hr_emp.DepartmentID,
                        "PositionID": hr_emp.PositionID,
                        "Status": hr_emp.Status,
                        "FullName": hr_emp.FullName
                    },
                    PayrollData={
                        "DepartmentID": payroll_emp.DepartmentID,
                        "PositionID": payroll_emp.PositionID,
                        "Status": payroll_emp.Status,
                        "FullName": payroll_emp.FullName
                    }
                ))
                need_sync_count += 1
            else:
                # Đã sync, không cần action
                already_synced_count += 1
        
        return SyncCheckResponse(
            TotalEmployees=len(hr_employees),
            NeedSync=need_sync_count,
            AlreadySynced=already_synced_count,
            SyncNeeds=sync_needs
        )
    
    @staticmethod
    def execute_sync(
        hr_db: Session,
        payroll_db: Session,
        employee_ids: List[int]
    ) -> SyncExecuteResponse:
        """
        Execute sync for specified employees
        BR-03: Auto-create với salary = 0 nếu chưa tồn tại
        BR-04: Update nếu đã tồn tại
        """
        synced_count = 0
        failed_count = 0
        details = []
        
        try:
            for emp_id in employee_ids:
                try:
                    # Get employee từ HR database
                    hr_emp = hr_db.query(Employee).filter(
                        Employee.EmployeeID == emp_id
                    ).first()
                    
                    if not hr_emp:
                        details.append({
                            "EmployeeID": emp_id,
                            "Status": "failed",
                            "Message": f"Employee {emp_id} không tồn tại trong HR database"
                        })
                        failed_count += 1
                        continue
                    
                    # Check nếu employee đã tồn tại trong payroll
                    payroll_emp = payroll_db.query(EmployeePayroll).filter(
                        EmployeePayroll.EmployeeID == emp_id
                    ).first()
                    
                    if not payroll_emp:
                        # INSERT new employee (BR-03)
                        new_payroll_emp = EmployeePayroll(
                            EmployeeID=hr_emp.EmployeeID,
                            FullName=hr_emp.FullName,
                            DepartmentID=hr_emp.DepartmentID,
                            PositionID=hr_emp.PositionID,
                            Status=hr_emp.Status,
                            SyncedAt=datetime.utcnow()
                        )
                        payroll_db.add(new_payroll_emp)
                        
                        # Sync department nếu chưa tồn tại
                        if hr_emp.DepartmentID:
                            SyncService._sync_department(hr_db, payroll_db, hr_emp.DepartmentID)
                        
                        # Sync position nếu chưa tồn tại
                        if hr_emp.PositionID:
                            SyncService._sync_position(hr_db, payroll_db, hr_emp.PositionID)
                        
                        details.append({
                            "EmployeeID": emp_id,
                            "Action": "INSERT",
                            "Status": "success",
                            "Message": f"Đã thêm {hr_emp.FullName} vào payroll system"
                        })
                        synced_count += 1
                        
                    else:
                        # UPDATE existing employee (BR-04)
                        payroll_emp.FullName = hr_emp.FullName
                        payroll_emp.DepartmentID = hr_emp.DepartmentID
                        payroll_emp.PositionID = hr_emp.PositionID
                        payroll_emp.Status = hr_emp.Status
                        payroll_emp.SyncedAt = datetime.utcnow()
                        
                        # Sync department và position nếu cần
                        if hr_emp.DepartmentID:
                            SyncService._sync_department(hr_db, payroll_db, hr_emp.DepartmentID)
                        if hr_emp.PositionID:
                            SyncService._sync_position(hr_db, payroll_db, hr_emp.PositionID)
                        
                        details.append({
                            "EmployeeID": emp_id,
                            "Action": "UPDATE",
                            "Status": "success",
                            "Message": f"Đã cập nhật thông tin {hr_emp.FullName}"
                        })
                        synced_count += 1
                    
                except Exception as e:
                    details.append({
                        "EmployeeID": emp_id,
                        "Status": "failed",
                        "Message": f"Lỗi: {str(e)}"
                    })
                    failed_count += 1
            
            # Commit all changes
            payroll_db.commit()
            
            return SyncExecuteResponse(
                Success=failed_count == 0,
                Message=f"Đã sync {synced_count}/{len(employee_ids)} employees",
                SyncedCount=synced_count,
                FailedCount=failed_count,
                Details=details
            )
            
        except Exception as e:
            payroll_db.rollback()
            return SyncExecuteResponse(
                Success=False,
                Message=f"Sync failed: {str(e)}",
                SyncedCount=0,
                FailedCount=len(employee_ids),
                Details=[{
                    "Status": "failed",
                    "Message": str(e)
                }]
            )
    
    @staticmethod
    def _sync_department(hr_db: Session, payroll_db: Session, dept_id: int):
        """Sync department nếu chưa tồn tại trong payroll"""
        existing = payroll_db.query(DepartmentPayroll).filter(
            DepartmentPayroll.DepartmentID == dept_id
        ).first()
        
        if not existing:
            hr_dept = hr_db.query(Department).filter(
                Department.DepartmentID == dept_id
            ).first()
            
            if hr_dept:
                new_dept = DepartmentPayroll(
                    DepartmentID=hr_dept.DepartmentID,
                    DepartmentName=hr_dept.DepartmentName,
                    SyncedAt=datetime.utcnow()
                )
                payroll_db.add(new_dept)
    
    @staticmethod
    def _sync_position(hr_db: Session, payroll_db: Session, pos_id: int):
        """Sync position nếu chưa tồn tại trong payroll"""
        existing = payroll_db.query(PositionPayroll).filter(
            PositionPayroll.PositionID == pos_id
        ).first()
        
        if not existing:
            hr_pos = hr_db.query(Position).filter(
                Position.PositionID == pos_id
            ).first()
            
            if hr_pos:
                new_pos = PositionPayroll(
                    PositionID=hr_pos.PositionID,
                    PositionName=hr_pos.PositionName,
                    SyncedAt=datetime.utcnow()
                )
                payroll_db.add(new_pos)
