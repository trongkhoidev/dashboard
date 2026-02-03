/**
 * Enhanced Sync Status Badge với modern design
 */
import React from 'react';

const SyncStatusBadge = ({ status }) => {
    const statusConfig = {
        synced: {
            label: 'Đã đồng bộ',
            gradient: 'from-green-400 to-emerald-500',
            icon: '✓',
            glow: 'shadow-[0_0_15px_rgba(52,211,153,0.4)]',
        },
        needs_sync: {
            label: 'Cần đồng bộ',
            gradient: 'from-rose-400 to-red-500',
            icon: '⚠',
            glow: 'shadow-[0_0_15px_rgba(244,63,94,0.4)]',
        },
        syncing: {
            label: 'Đang đồng bộ',
            gradient: 'from-amber-400 to-yellow-500',
            icon: '⟳',
            glow: 'shadow-[0_0_15px_rgba(251,191,36,0.4)]',
        },
        error: {
            label: 'Lỗi',
            gradient: 'from-gray-400 to-slate-500',
            icon: '✕',
            glow: 'shadow-[0_0_15px_rgba(100,116,139,0.4)]',
        },
    };

    const config = statusConfig[status] || statusConfig.error;

    return (
        <span
            className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${config.gradient} ${config.glow} transition-all duration-300 hover:scale-105`}
        >
            <span className={status === 'syncing' ? 'animate-spin' : ''}>
                {config.icon}
            </span>
            {config.label}
        </span>
    );
};

export default SyncStatusBadge;
