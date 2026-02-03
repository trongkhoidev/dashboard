/**
 * Master HR View - Premium Modern Design
 * Features: Glassmorphism, Gradients, Animations
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

    const syncedCount = employees.filter(e => e.SyncStatus === 'synced').length;
    const needsSyncCount = employees.filter(e => e.SyncStatus === 'needs_sync').length;

    return (
        <div className="animate-fade-in">
            {/* Header with Stats */}
            <div className="glass-card p-8 mb-6">
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
                            Master HR View
                        </h1>
                        <p className="text-gray-600">Quản lý toàn diện nhân sự và trạng thái đồng bộ</p>
                    </div>

                    {/* Quick Stats */}
                    <div className="flex gap-4">
                        <div className="text-center px-6 py-4 bg-gradient-to-br from-teal-50 to-cyan-50 rounded-xl border border-primary-200">
                            <div className="text-3xl font-bold text-primary-600">{employees.length}</div>
                            <div className="text-xs text-gray-600 font-medium mt-1">Tổng NV</div>
                        </div>
                        <div className="text-center px-6 py-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200">
                            <div className="text-3xl font-bold text-green-600">{syncedCount}</div>
                            <div className="text-xs text-gray-600 font-medium mt-1">Đã sync</div>
                        </div>
                        <div className="text-center px-6 py-4 bg-gradient-to-br from-rose-50 to-red-50 rounded-xl border border-red-200">
                            <div className="text-3xl font-bold text-red-600">{needsSyncCount}</div>
                            <div className="text-xs text-gray-600 font-medium mt-1">Cần sync</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters Card */}
            <div className="glass-card p-6 mb-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Search */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            🔍 Tìm kiếm nhân viên
                        </label>
                        <input
                            type="text"
                            value={searchInput}
                            onChange={handleSearchChange}
                            placeholder="Nhập tên nhân viên..."
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all duration-200"
                        />
                    </div>

                    {/* Department Filter */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            🏢 Phòng ban
                        </label>
                        <select
                            value={filters.departmentId || ''}
                            onChange={(e) => handleDepartmentFilter(e.target.value)}
                            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-primary-500 focus:ring-4 focus:ring-primary-100 transition-all duration-200 bg-white"
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
                            className="flex-1 px-4 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 font-medium transition-all duration-200 hover:shadow-md"
                        >
                            ✕ Xóa bộ lọc
                        </button>
                        <button
                            onClick={() => fetchEmployees(filters)}
                            className="flex-1 btn-gradient text-white rounded-xl px-4 py-3 font-medium"
                        >
                            ↻ Làm mới
                        </button>
                    </div>
                </div>
            </div>

            {/* Employee Table */}
            <div className="glass-card overflow-hidden">
                {loading ? (
                    <div className="p-16 text-center">
                        <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600 mb-4"></div>
                        <p className="text-gray-600 font-medium">Đang tải dữ liệu...</p>
                    </div>
                ) : error ? (
                    <div className="p-16 text-center">
                        <div className="text-6xl mb-4">⚠️</div>
                        <p className="text-red-600 font-semibold text-lg">Lỗi: {error}</p>
                    </div>
                ) : (
                    <>
                        <div className="overflow-x-auto">
                            <table className="min-w-full">
                                <thead>
                                    <tr className="bg-gradient-to-r from-primary-50 to-secondary-50 border-b-2 border-primary-100">
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Mã NV
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Họ và Tên
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Phòng ban
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Chức vụ
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Trạng thái
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Sync Status
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase tracking-wider">
                                            Ngày vào
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {employees.length === 0 ? (
                                        <tr>
                                            <td colSpan="7" className="px-6 py-12 text-center">
                                                <div className="text-6xl mb-4">📭</div>
                                                <p className="text-gray-500 font-medium">Không tìm thấy nhân viên nào</p>
                                            </td>
                                        </tr>
                                    ) : (
                                        employees.map((employee, index) => (
                                            <tr
                                                key={employee.EmployeeID}
                                                className="hover:bg-gradient-to-r hover:from-primary-50 hover:to-transparent transition-all duration-200 animate-slide-up"
                                                style={{ animationDelay: `${index * 0.05}s` }}
                                            >
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className="text-sm font-bold text-primary-600">
                                                        #{employee.EmployeeID}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <div className="flex items-center">
                                                        <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold mr-3">
                                                            {employee.FullName.charAt(0)}
                                                        </div>
                                                        <span className="text-sm font-semibold text-gray-900">
                                                            {employee.FullName}
                                                        </span>
                                                    </div>
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-medium">
                                                    {employee.DepartmentName}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                                                    {employee.PositionName}
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${employee.Status === 'Active'
                                                        ? 'bg-green-100 text-green-700'
                                                        : 'bg-gray-100 text-gray-700'
                                                        }`}>
                                                        {employee.Status}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <SyncStatusBadge status={employee.SyncStatus} />
                                                </td>
                                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 font-medium">
                                                    {employee.HireDate ? new Date(employee.HireDate).toLocaleDateString('vi-VN') : 'N/A'}
                                                </td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </table>
                        </div>

                        {/* Footer Stats */}
                        {!loading && employees.length > 0 && (
                            <div className="bg-gradient-to-r from-gray-50 to-primary-50 px-6 py-4 border-t border-gray-200">
                                <div className="flex justify-between items-center text-sm">
                                    <div className="font-semibold text-gray-700">
                                        Hiển thị <span className="text-primary-600">{employees.length}</span> nhân viên
                                    </div>
                                    <div className="flex gap-6">
                                        <span className="flex items-center gap-2">
                                            <span className="w-3 h-3 rounded-full bg-green-500"></span>
                                            <span className="font-medium text-gray-700">
                                                Đã đồng bộ: <span className="text-green-600 font-bold">{syncedCount}</span>
                                            </span>
                                        </span>
                                        <span className="flex items-center gap-2">
                                            <span className="w-3 h-3 rounded-full bg-red-500"></span>
                                            <span className="font-medium text-gray-700">
                                                Cần đồng bộ: <span className="text-red-600 font-bold">{needsSyncCount}</span>
                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default MasterHRView;
