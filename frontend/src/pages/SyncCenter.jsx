/**
 * Sync Center - Premium Modern Design
 * Features: Real-time sync management với glassmorphism UI
 */
import React, { useEffect, useState } from 'react';
import useSyncStore from '../store/useSyncStore';

const SyncCenter = () => {
    const { syncNeeds, syncStatus, syncing, error, checkSync, executeSync } = useSyncStore();
    const [selectedIds, setSelectedIds] = useState([]);
    const [syncResult, setSyncResult] = useState(null);

    useEffect(() => {
        checkSync();
    }, []);

    const handleSelectAll = (e) => {
        if (e.target.checked) {
            setSelectedIds(syncNeeds.map(need => need.EmployeeID));
        } else {
            setSelectedIds([]);
        }
    };

    const handleSelectOne = (employeeId) => {
        setSelectedIds(prev =>
            prev.includes(employeeId)
                ? prev.filter(id => id !== employeeId)
                : [...prev, employeeId]
        );
    };

    const handleExecuteSync = async () => {
        if (selectedIds.length === 0) return;

        try {
            const result = await executeSync(selectedIds);
            setSyncResult(result);
            setTimeout(() => {
                checkSync();
                setSelectedIds([]);
            }, 1000);
        } catch (err) {
            console.error('Sync failed:', err);
        }
    };

    return (
        <div className="animate-fade-in">
            {/* Header */}
            <div className="glass-card p-8 mb-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-4xl font-bold bg-gradient-primary bg-clip-text text-transparent mb-2">
                            🔄 Trung tâm đồng bộ
                        </h1>
                        <p className="text-gray-600">Quản lý và thực hiện đồng bộ dữ liệu giữa HR và Payroll</p>
                    </div>
                    <button
                        onClick={() => checkSync()}
                        disabled={syncing}
                        className="btn-gradient text-white px-6 py-3 rounded-xl font-medium disabled:opacity-50"
                    >
                        ↻ Kiểm tra lại
                    </button>
                </div>
            </div>

            {/* Sync Status Summary */}
            {syncStatus && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div className="glass-card p-6 hover:scale-105 transition-transform duration-300">
                        <div className="flex items-center justify-between">
                            <div>
                                <div className="text-sm font-semibold text-gray-600 mb-1">Tổng số nhân viên</div>
                                <div className="text-4xl font-bold text-primary-600">{syncStatus.TotalEmployees}</div>
                            </div>
                            <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl flex items-center justify-center">
                                <span className="text-3xl">👥</span>
                            </div>
                        </div>
                        <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div className="h-full bg-gradient-primary w-full"></div>
                        </div>
                    </div>

                    <div className="glass-card p-6 hover:scale-105 transition-transform duration-300">
                        <div className="flex items-center justify-between">
                            <div>
                                <div className="text-sm font-semibold text-gray-600 mb-1">Cần đồng bộ</div>
                                <div className="text-4xl font-bold text-red-600">{syncStatus.NeedSync}</div>
                            </div>
                            <div className="w-16 h-16 bg-gradient-to-br from-red-100 to-rose-200 rounded-2xl flex items-center justify-center">
                                <span className="text-3xl">⚠️</span>
                            </div>
                        </div>
                        <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-red-500 to-rose-500"
                                style={{ width: `${(syncStatus.NeedSync / syncStatus.TotalEmployees) * 100}%` }}
                            ></div>
                        </div>
                    </div>

                    <div className="glass-card p-6 hover:scale-105 transition-transform duration-300">
                        <div className="flex items-center justify-between">
                            <div>
                                <div className="text-sm font-semibold text-gray-600 mb-1">Đã đồng bộ</div>
                                <div className="text-4xl font-bold text-green-600">{syncStatus.AlreadySynced}</div>
                            </div>
                            <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-emerald-200 rounded-2xl flex items-center justify-center">
                                <span className="text-3xl">✓</span>
                            </div>
                        </div>
                        <div className="mt-4 h-2 bg-gray-200 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                                style={{ width: `${(syncStatus.AlreadySynced / syncStatus.TotalEmployees) * 100}%` }}
                            ></div>
                        </div>
                    </div>
                </div>
            )}

            {/* Sync Actions */}
            <div className="glass-card p-6 mb-6">
                <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center text-white font-bold text-lg">
                            {selectedIds.length}
                        </div>
                        <div>
                            <div className="font-semibold text-gray-900">
                                {selectedIds.length} nhân viên được chọn
                            </div>
                            <div className="text-sm text-gray-600">
                                {selectedIds.length > 0 ? 'Sẵn sàng để đồng bộ' : 'Chọn nhân viên để bắt đầu'}
                            </div>
                        </div>
                    </div>
                    <button
                        onClick={handleExecuteSync}
                        disabled={syncing || selectedIds.length === 0}
                        className="btn-gradient text-white px-8 py-3 rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {syncing ? (
                            <span className="flex items-center gap-2">
                                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                Đang đồng bộ...
                            </span>
                        ) : (
                            `🚀 Đồng bộ (${selectedIds.length})`
                        )}
                    </button>
                </div>
            </div>

            {/* Sync Result */}
            {syncResult && (
                <div className={`glass-card p-6 mb-6 border-2 ${syncResult.Success ? 'border-green-300 bg-gradient-to-r from-green-50 to-emerald-50' : 'border-red-300 bg-gradient-to-r from-red-50 to-rose-50'}`}>
                    <div className="flex items-center gap-4">
                        <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-3xl ${syncResult.Success ? 'bg-green-100' : 'bg-red-100'}`}>
                            {syncResult.Success ? '✅' : '❌'}
                        </div>
                        <div className="flex-1">
                            <div className="font-bold text-lg text-gray-900">
                                {syncResult.Message}
                            </div>
                            <div className="flex gap-6 mt-2 text-sm">
                                <span className="text-green-600 font-semibold">
                                    ✓ Thành công: {syncResult.SyncedCount}
                                </span>
                                <span className="text-red-600 font-semibold">
                                    ✕ Thất bại: {syncResult.FailedCount}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Sync Needs Table */}
            <div className="glass-card overflow-hidden">
                {syncing && !syncNeeds.length ? (
                    <div className="p-16 text-center">
                        <div className="inline-block animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600 mb-4"></div>
                        <p className="text-gray-600 font-medium">Đang kiểm tra dữ liệu...</p>
                    </div>
                ) : syncNeeds.length === 0 ? (
                    <div className="p-16 text-center">
                        <div className="text-8xl mb-6">✅</div>
                        <p className="text-2xl font-bold text-green-600 mb-2">Hoàn hảo!</p>
                        <p className="text-gray-600">Tất cả dữ liệu đã được đồng bộ thành công</p>
                    </div>
                ) : (
                    <>
                        <div className="overflow-x-auto">
                            <table className="min-w-full">
                                <thead>
                                    <tr className="bg-gradient-to-r from-primary-50 to-secondary-50 border-b-2 border-primary-100">
                                        <th className="px-6 py-4 text-left w-12">
                                            <input
                                                type="checkbox"
                                                checked={selectedIds.length === syncNeeds.length && syncNeeds.length > 0}
                                                onChange={handleSelectAll}
                                                className="w-5 h-5 rounded border-2 border-primary-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                                            />
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase">
                                            Mã NV
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase">
                                            Họ và Tên
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase">
                                            Action
                                        </th>
                                        <th className="px-6 py-4 text-left text-xs font-bold text-primary-900 uppercase">
                                            Lý do
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-100">
                                    {syncNeeds.map((need, index) => (
                                        <tr
                                            key={need.EmployeeID}
                                            className={`hover:bg-gradient-to-r hover:from-primary-50 hover:to-transparent transition-all duration-200 animate-slide-up ${selectedIds.includes(need.EmployeeID) ? 'bg-primary-50' : ''}`}
                                            style={{ animationDelay: `${index * 0.05}s` }}
                                        >
                                            <td className="px-6 py-4">
                                                <input
                                                    type="checkbox"
                                                    checked={selectedIds.includes(need.EmployeeID)}
                                                    onChange={() => handleSelectOne(need.EmployeeID)}
                                                    className="w-5 h-5 rounded border-2 border-primary-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                                                />
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className="text-sm font-bold text-primary-600">
                                                    #{need.EmployeeID}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center">
                                                    <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold mr-3">
                                                        {need.FullName.charAt(0)}
                                                    </div>
                                                    <span className="text-sm font-semibold text-gray-900">
                                                        {need.FullName}
                                                    </span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`px-4 py-2 rounded-full text-xs font-bold ${need.Action === 'INSERT'
                                                        ? 'bg-gradient-to-r from-blue-400 to-cyan-400 text-white shadow-glow'
                                                        : 'bg-gradient-to-r from-orange-400 to-amber-400 text-white shadow-glow'
                                                    }`}>
                                                    {need.Action === 'INSERT' ? '+ INSERT' : '⟳ UPDATE'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-700">
                                                {need.Reason}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        <div className="bg-gradient-to-r from-gray-50 to-primary-50 px-6 py-4 border-t border-gray-200">
                            <div className="text-sm font-semibold text-gray-700">
                                Tổng số: <span className="text-primary-600">{syncNeeds.length}</span> nhân viên cần đồng bộ
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SyncCenter;
