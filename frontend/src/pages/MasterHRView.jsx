/**
 * Master HR View - Main Employee List Dashboard
 * Features: Employee list với sync status, filters, search
 */
import React, { useEffect, useState } from 'react';
import useEmployeeStore from '../store/useEmployeeStore';
import SyncStatusBadge from '../components/SyncStatusBadge';

const MasterHRView = () => {
    const {
        employees,
        departments,
        loading,
        error,
        filters,
        fetchEmployees,
        fetchDepartments,
        setFilters,
        clearFilters
    } = useEmployeeStore();

    const [searchInput, setSearchInput] = useState('');

    useEffect(() => {
        fetchEmployees();
        fetchDepartments();
    }, []);

    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchInput(value);
        // Debounce search
        const timer = setTimeout(() => {
            setFilters({ search: value });
        }, 500);
        return () => clearTimeout(timer);
    };

    const handleDepartmentFilter = (departmentId) => {
        setFilters({ departmentId: departmentId || null });
    };

    const handleClearFilters = () => {
        setSearchInput('');
        clearFilters();
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Master HR View
                    </h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Quản lý nhân sự và kiểm tra trạng thái đồng bộ
                    </p>
                </div>
            </div>

            {/* Filters */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="bg-white rounded-lg shadow p-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Search */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Tìm kiếm nhân viên
                            </label>
                            <input
                                type="text"
                                value={searchInput}
                                onChange={handleSearchChange}
                                placeholder="Nhập tên nhân viên..."
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            />
                        </div>

                        {/* Department Filter */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Phòng ban
                            </label>
                            <select
                                value={filters.departmentId || ''}
                                onChange={(e) => handleDepartmentFilter(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            >
                                <option value="">Tất cả phòng ban</option>
                                {departments.map((dept) => (
                                    <option key={dept.DepartmentID} value={dept.DepartmentID}>
                                        {dept.DepartmentName} ({dept.EmployeeCount})
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Actions */}
                        <div className="flex items-end gap-2">
                            <button
                                onClick={handleClearFilters}
                                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition"
                            >
                                Xóa bộ lọc
                            </button>
                            <button
                                onClick={() => fetchEmployees(filters)}
                                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition"
                            >
                                Làm mới
                            </button>
                        </div>
                    </div>
                </div>

                {/* Employee Table */}
                <div className="mt-6 bg-white rounded-lg shadow overflow-hidden">
                    {loading ? (
                        <div className="p-8 text-center">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                            <p className="mt-2 text-gray-600">Đang tải dữ liệu...</p>
                        </div>
                    ) : error ? (
                        <div className="p-8 text-center text-red-600">
                            <p>Lỗi: {error}</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Mã NV
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Họ và Tên
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Phòng ban
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Chức vụ
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Trạng thái
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Sync Status
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Ngày vào
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {employees.length === 0 ? (
                                        <tr>
                                            <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                                                Không tìm thấy nhân viên nào
                                            </td>
                                        </tr>
                                    ) : (
                                        employees.map((employee) => (
                                            <tr key={employee.EmployeeID} className="hover:bg-gray-50">
                                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                    {employee.EmployeeID}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                    {employee.FullName}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {employee.DepartmentName}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {employee.PositionName}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {employee.Status}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                    <SyncStatusBadge status={employee.SyncStatus} />
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {employee.HireDate ? new Date(employee.HireDate).toLocaleDateString('vi-VN') : 'N/A'}
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                {/* Stats */}
                {!loading && employees.length > 0 && (
                    <div className="mt-4 flex justify-between items-center text-sm text-gray-600">
                        <div>
                            Tổng số: <span className="font-semibold">{employees.length}</span> nhân viên
                        </div>
                        <div className="flex gap-4">
                            <span>
                                🟢 Đã đồng bộ: {employees.filter(e => e.SyncStatus === 'synced').length}
                            </span>
                            <span>
                                🔴 Cần đồng bộ: {employees.filter(e => e.SyncStatus === 'needs_sync').length}
                            </span>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default MasterHRView;
