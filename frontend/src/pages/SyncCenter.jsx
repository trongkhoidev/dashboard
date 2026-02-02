/**
 * Sync Center Page
 * Dashboard quản lý đồng bộ giữa HR và Payroll databases
 */
import React, { useEffect, useState } from 'react';
import useSyncStore from '../store/useSyncStore';
import SyncStatusBadge from '../components/SyncStatusBadge';

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
            // Refresh sync status
            setTimeout(() => {
                checkSync();
                setSelectedIds([]);
            }, 1000);
        } catch (err) {
            console.error('Sync failed:', err);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Trung tâm đồng bộ
                    </h1>
                    <p className="mt-1 text-sm text-gray-500">
                        Kiểm tra và thực hiện đồng bộ dữ liệu giữa HR và Payroll
                    </p>
                </div>
            </div>

            {/* Sync Status Summary */}
            {syncStatus && (
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-sm font-medium text-gray-600">Tổng số nhân viên</div>
                            <div className="mt-2 text-3xl font-bold text-gray-900">
                                {syncStatus.TotalEmployees}
                            </div>
                        </div>
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-sm font-medium text-gray-600">Cần đồng bộ</div>
                            <div className="mt-2 text-3xl font-bold text-red-600">
                                {syncStatus.NeedSync}
                            </div>
                        </div>
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-sm font-medium text-gray-600">Đã đồng bộ</div>
                            <div className="mt-2 text-3xl font-bold text-green-600">
                                {syncStatus.AlreadySynced}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Sync Actions */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
                    <div>
                        <span className="text-sm text-gray-600">
                            {selectedIds.length} nhân viên được chọn
                        </span>
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={() => checkSync()}
                            disabled={syncing}
                            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition disabled:opacity-50"
                        >
                            Kiểm tra lại
                        </button>
                        <button
                            onClick={handleExecuteSync}
                            disabled={syncing || selectedIds.length === 0}
                            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition disabled:opacity-50"
                        >
                            {syncing ? 'Đang đồng bộ...' : `Đồng bộ (${selectedIds.length})`}
                        </button>
                    </div>
                </div>

                {/* Sync Result */}
                {syncResult && (
                    <div className={`mt-4 rounded-lg p-4 ${syncResult.Success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                        <div className="flex items-center gap-2">
                            <span className="text-lg">{syncResult.Success ? '✅' : '❌'}</span>
                            <div>
                                <div className="font-medium">
                                    {syncResult.Message}
                                </div>
                                <div className="text-sm text-gray-600 mt-1">
                                    Thành công: {syncResult.SyncedCount} | Thất bại: {syncResult.FailedCount}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Sync Needs Table */}
                <div className="mt-6 bg-white rounded-lg shadow overflow-hidden">
                    {syncing && !syncNeeds.length ? (
                        <div className="p-8 text-center">
                            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                            <p className="mt-2 text-gray-600">Đang kiểm tra...</p>
                        </div>
                    ) : syncNeeds.length === 0 ? (
                        <div className="p-8 text-center text-green-600">
                            <div className="text-5xl mb-4">✅</div>
                            <p className="text-lg font-medium">Tất cả dữ liệu đã được đồng bộ!</p>
                            <p className="text-sm text-gray-600 mt-2">Không có nhân viên nào cần đồng bộ</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left">
                                            <input
                                                type="checkbox"
                                                checked={selectedIds.length === syncNeeds.length}
                                                onChange={handleSelectAll}
                                                className="rounded border-gray-300"
                                            />
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Mã NV
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Họ và Tên
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Action
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Lý do
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {syncNeeds.map((need) => (
                                        <tr key={need.EmployeeID} className="hover:bg-gray-50">
                                            <td className="px-6 py-4">
                                                <input
                                                    type="checkbox"
                                                    checked={selectedIds.includes(need.EmployeeID)}
                                                    onChange={() => handleSelectOne(need.EmployeeID)}
                                                    className="rounded border-gray-300"
                                                />
                                            </td>
                                            <td className="px-6 py-4 text-sm font-medium text-gray-900">
                                                {need.EmployeeID}
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-900">
                                                {need.FullName}
                                            </td>
                                            <td className="px-6 py-4 text-sm">
                                                <span className={`px-2 py-1 rounded text-xs font-medium ${need.Action === 'INSERT'
                                                    ? 'bg-blue-100 text-blue-800'
                                                    : 'bg-orange-100 text-orange-800'
                                                    }`}>
                                                    {need.Action}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-sm text-gray-600">
                                                {need.Reason}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SyncCenter;
