/**
 * Sync Status Badge Component
 * Hiển thị trực quan sync status với màu sắc tương ứng
 */
import React from 'react';

const SyncStatusBadge = ({ status }) => {
    const statusConfig = {
        synced: {
            label: 'Đã đồng bộ',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800',
            dotColor: 'bg-green-500',
        },
        needs_sync: {
            label: 'Cần đồng bộ',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800',
            dotColor: 'bg-red-500',
        },
        syncing: {
            label: 'Đang đồng bộ',
            bgColor: 'bg-yellow-100',
            textColor: 'text-yellow-800',
            dotColor: 'bg-yellow-500',
        },
        error: {
            label: 'Lỗi',
            bgColor: 'bg-gray-100',
            textColor: 'text-gray-800',
            dotColor: 'bg-gray-500',
        },
    };

    const config = statusConfig[status] || statusConfig.error;

    return (
        <span
            className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${config.bgColor} ${config.textColor}`}
        >
            <span className={`w-2 h-2 rounded-full ${config.dotColor}`}></span>
            {config.label}
        </span>
    );
};

export default SyncStatusBadge;
