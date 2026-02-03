"""
API Routes for HR Management Module
Endpoints: /employees, /org-structure, /sync, /dividends
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from ...database.connections import db_manager
from ...core.mock_data import mock_service
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
    # Fallback to mock data if databases unavailable
    if not db_manager.sql_server_available or not db_manager.mysql_available:
        print("⚠️  Using mock data for employees (databases unavailable)")
        return mock_service.get_mock_employees()
    
    try:
        with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
            employees = HRService.list_employees_with_sync_status(
                hr_db, payroll_db,
                department_id=department_id,
                search_name=search
            )
            return employees
    except Exception as e:
        print(f"⚠️  Database error, falling back to mock data: {e}")
        return mock_service.get_mock_employees()


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
    # Fallback to mock data if database unavailable
    if not db_manager.sql_server_available:
        print("⚠️  Using mock data for departments (SQL Server unavailable)")
        return mock_service.get_mock_departments()
    
    try:
        with db_manager.get_hr_db() as hr_db:
            departments = HRService.get_departments(hr_db)
            return departments
    except Exception as e:
        print(f"⚠️  Database error, falling back to mock data: {e}")
        return mock_service.get_mock_departments()


# ============================================================================
# Sync Endpoints
# ============================================================================

@router.post("/sync/check", response_model=SyncCheckResponse)
def check_sync_status():
    """
    Check sync status giữa HR và Payroll databases
    Trả về danh sách employees cần sync
    """
    # Fallback to mock data if databases unavailable
    if not db_manager.sql_server_available or not db_manager.mysql_available:
        print("⚠️  Using mock data for sync check (databases unavailable)")
        return mock_service.get_mock_sync_status()
    
    try:
        with db_manager.get_hr_db() as hr_db, db_manager.get_payroll_db() as payroll_db:
            sync_check = SyncService.check_sync_needs(hr_db, payroll_db)
            return sync_check
    except Exception as e:
        print(f"⚠️  Database error, falling back to mock data: {e}")
        return mock_service.get_mock_sync_status()


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
