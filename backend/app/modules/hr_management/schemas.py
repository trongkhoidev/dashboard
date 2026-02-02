"""
Pydantic Schemas for HR Management Module
Data validation và serialization cho API responses
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, Literal, List
from decimal import Decimal


# ============================================================================
# Employee Schemas
# ============================================================================

class EmployeeBase(BaseModel):
    """Base employee schema với common fields"""
    EmployeeID: int
    FullName: str
    DepartmentID: Optional[int] = None
    PositionID: Optional[int] = None
    Status: Optional[str] = "Đang làm việc"


class EmployeeDetail(EmployeeBase):
    """Unified employee profile - JOIN data từ cả HR và Payroll"""
    DateOfBirth: Optional[date] = None
    Gender: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Email: Optional[EmailStr] = None
    HireDate: Optional[date] = None
    DepartmentName: Optional[str] = None
    PositionName: Optional[str] = None
    SyncStatus: Literal["synced", "needs_sync", "syncing", "error"] = "needs_sync"
    CreatedAt: Optional[datetime] = None
    UpdatedAt: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EmployeeListItem(BaseModel):
    """Simplified schema cho employee list view"""
    EmployeeID: int
    FullName: str
    DepartmentName: Optional[str] = "Chưa phân công"
    PositionName: Optional[str] = "Chưa xác định"
    Status: str
    SyncStatus: Literal["synced", "needs_sync", "syncing", "error"]
    HireDate: Optional[date] = None


# ============================================================================
# Department & Position Schemas
# ============================================================================

class DepartmentSchema(BaseModel):
    """Department schema"""
    DepartmentID: int
    DepartmentName: str
    EmployeeCount: Optional[int] = 0
    
    class Config:
        from_attributes = True


class PositionSchema(BaseModel):
    """Position schema"""
    PositionID: int
    PositionName: str
    
    class Config:
        from_attributes = True


# ============================================================================
# Dividend Schemas
# ============================================================================

class DividendSchema(BaseModel):
    """Dividend schema"""
    DividendID: int
    EmployeeID: int
    EmployeeName: Optional[str] = None
    DividendAmount: Decimal
    DividendDate: date
    CreatedAt: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============================================================================
# Sync Schemas
# ============================================================================

class SyncNeed(BaseModel):
    """Thông tin về một employee cần sync"""
    EmployeeID: int
    FullName: str
    Action: Literal["INSERT", "UPDATE", "NONE"]
    Reason: str
    HRData: Optional[dict] = None
    PayrollData: Optional[dict] = None


class SyncCheckResponse(BaseModel):
    """Response cho sync check request"""
    TotalEmployees: int
    NeedSync: int
    AlreadySynced: int
    SyncNeeds: List[SyncNeed]
    CheckedAt: datetime = Field(default_factory=datetime.utcnow)


class SyncExecuteRequest(BaseModel):
    """Request để execute sync"""
    EmployeeIDs: List[int] = Field(..., description="Danh sách EmployeeID cần sync")


class SyncExecuteResponse(BaseModel):
    """Response sau khi execute sync"""
    Success: bool
    Message: str
    SyncedCount: int
    FailedCount: int
    Details: List[dict]
    SyncedAt: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Organization Structure Schema
# ============================================================================

class OrgStructureNode(BaseModel):
    """Node trong organization tree"""
    DepartmentID: int
    DepartmentName: str
    Employees: List[EmployeeListItem]
    EmployeeCount: int


class OrgStructureResponse(BaseModel):
    """Organization structure response"""
    Departments: List[OrgStructureNode]
    TotalDepartments: int
    TotalEmployees: int
