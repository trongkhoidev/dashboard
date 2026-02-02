"""
API Routes for HR Management Module
Endpoints: /employees, /org-structure, /sync, /dividends
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ...database.connections import db_manager
from .services import HRService
from .sync_service import SyncService
from .schemas import (
    EmployeeDetail, EmployeeListItem, DepartmentSchema, DividendSchema,
    SyncCheckResponse, SyncExecuteRequest, SyncExecuteResponse,
    OrgStructureResponse
)

router = APIRouter(prefix="/hr", tags=["HR Management"])


# ============================================================================
# Employee Endpoints
# ============================================================================

@router.get("/employees", response_model=List[EmployeeListItem])
def list_employees(
    department_id: Optional[int] = Query(None, description="Filter by DepartmentID"),
    search: Optional[str] = Query(None, description="Search by employee name")
):
    """
    List all employees với sync status
    Supports filtering by department và search by name
    """
    with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
        employees = HRService.list_employees_with_sync_status(
            hr_db, payroll_db,
            department_id=department_id,
            search_name=search
        )
        return employees


@router.get("/employees/{employee_id}", response_model=EmployeeDetail)
def get_employee_detail(employee_id: int):
    """Get detailed employee profile với unified data từ HR và Payroll"""
    with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
        employee = HRService.get_unified_employee_profile(
            hr_db, payroll_db, employee_id
        )
        
        if not employee:
            raise HTTPException(
                status_code=404,
                detail=f"Employee with ID {employee_id} not found"
            )
        
        return employee


# ============================================================================
# Organization Structure Endpoints
# ============================================================================

@router.get("/org-structure", response_model=OrgStructureResponse)
def get_organization_structure():
    """Get organization structure với employees grouped by department"""
    with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
        org_structure = HRService.get_organization_structure(hr_db, payroll_db)
        return org_structure


@router.get("/departments", response_model=List[DepartmentSchema])
def list_departments():
    """Get all departments với employee count"""
    with db_manager.get_hr_db() as hr_db:
        departments = HRService.get_departments(hr_db)
        return departments


# ============================================================================
# Sync Endpoints
# ============================================================================

@router.post("/sync/check", response_model=SyncCheckResponse)
def check_sync_status():
    """
    Check sync status giữa HR và Payroll databases
    Trả về danh sách employees cần sync
    """
    with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
        sync_check = SyncService.check_sync_needs(hr_db, payroll_db)
        return sync_check


@router.post("/sync/execute", response_model=SyncExecuteResponse)
def execute_sync(request: SyncExecuteRequest):
    """
    Execute sync for selected employees
    BR-03: Auto-create employee trong MySQL nếu chưa tồn tại (salary = 0)
    BR-04: Update nếu đã tồn tại
    """
    if not request.EmployeeIDs:
        raise HTTPException(
            status_code=400,
            detail="EmployeeIDs list cannot be empty"
        )
    
    with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
        sync_result = SyncService.execute_sync(
            hr_db, payroll_db, request.EmployeeIDs
        )
        return sync_result


# ============================================================================
# Dividends Endpoints
# ============================================================================

@router.get("/dividends", response_model=List[DividendSchema])
def list_dividends(
    employee_id: Optional[int] = Query(None, description="Filter by EmployeeID")
):
    """Get dividends từ HR database, optionally filter by employee"""
    with db_manager.get_hr_db() as hr_db:
        dividends = HRService.get_employee_dividends(hr_db, employee_id)
        return dividends
