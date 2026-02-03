"""
Mock Data Service - For testing when databases are unavailable
"""
from datetime import datetime
from typing import List
from ..modules.hr_management.schemas import (
    EmployeeListItem, DepartmentSchema, SyncCheckResponse, SyncNeed
)


class MockDataService:
    """Provides mock data when real databases are unavailable"""
    
    @staticmethod
    def get_mock_employees() -> List[EmployeeListItem]:
        """Return mock employee data"""
        return [
            EmployeeListItem(
                EmployeeID=1,
                FullName="Nguyễn Văn An",
                DepartmentName="IT Department",
                PositionName="Senior Developer",
                Status="Active",
                SyncStatus="synced",
                HireDate=datetime(2023, 1, 15)
            ),
            EmployeeListItem(
                EmployeeID=2,
                FullName="Trần Thị Bình",
                DepartmentName="HR Department",
                PositionName="HR Manager",
                Status="Active",
                SyncStatus="synced",
                HireDate=datetime(2023, 3, 10)
            ),
            EmployeeListItem(
                EmployeeID=3,
                FullName="Lê Văn Cường",
                DepartmentName="IT Department",
                PositionName="Junior Developer",
                Status="Active",
                SyncStatus="needs_sync",
                HireDate=datetime(2024, 1, 5)
            ),
            EmployeeListItem(
                EmployeeID=4,
                FullName="Phạm Thị Dung",
                DepartmentName="Accounting",
                PositionName="Accountant",
                Status="Active",
                SyncStatus="synced",
                HireDate=datetime(2023, 6, 20)
            ),
            EmployeeListItem(
                EmployeeID=5,
                FullName="Hoàng Văn Em",
                DepartmentName="IT Department",
                PositionName="DevOps Engineer",
                Status="Active",
                SyncStatus="needs_sync",
                HireDate=datetime(2024, 2, 1)
            ),
        ]
    
    @staticmethod
    def get_mock_departments() -> List[DepartmentSchema]:
        """Return mock department data"""
        return [
            DepartmentSchema(
                DepartmentID=1,
                DepartmentName="IT Department",
                EmployeeCount=3
            ),
            DepartmentSchema(
                DepartmentID=2,
                DepartmentName="HR Department",
                EmployeeCount=1
            ),
            DepartmentSchema(
                DepartmentID=3,
                DepartmentName="Accounting",
                EmployeeCount=1
            ),
        ]
    
    @staticmethod
    def get_mock_sync_status() -> SyncCheckResponse:
        """Return mock sync status"""
        return SyncCheckResponse(
            TotalEmployees=5,
            NeedSync=2,
            AlreadySynced=3,
            SyncNeeds=[
                SyncNeed(
                    EmployeeID=3,
                    FullName="Lê Văn Cường",
                    Action="INSERT",
                    Reason="Employee chưa tồn tại trong payroll system"
                ),
                SyncNeed(
                    EmployeeID=5,
                    FullName="Hoàng Văn Em",
                    Action="UPDATE",
                    Reason="Thay đổi: DepartmentID"
                ),
            ],
            CheckedAt=datetime.utcnow()
        )


mock_service = MockDataService()
