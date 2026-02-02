# HR & Payroll Dashboard - Frontend

React + Vite frontend cho Integrated HR & Payroll Management System

## 🚀 Quick Start

```bash
cd frontend
npm install  # Already done during setup
npm run dev  # Start development server
```

Server will start at: `http://localhost:5173`

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable components
│   │   └── SyncStatusBadge.jsx
│   ├── pages/           # Page components
│   │   ├── MasterHRView.jsx   # Main employee list
│   │   └── SyncCenter.jsx     # Sync management
│   ├── services/        # API clients
│   │   └── api.js       # Axios HTTP client
│   ├── store/           # Zustand state management
│   │   ├── useEmployeeStore.js
│   │   └── useSyncStore.js
│   ├── App.jsx          # Main app with routing
│   └── index.css        # Tailwind CSS
├── .env                 # Environment variables
├── tailwind.config.js   # Tailwind configuration
└── package.json
```

## 🎨 Pages

### 1. Master HR View (`/`)
- Employee list table với sync status
- Filter by department
- Search by name (debounced)
- Sync status badges (🟢 🔴 🟡)

### 2. Sync Center (`/sync`)
- Sync needs detection
- Bulk employee selection
- Execute sync
- Real-time sync status

## 🔧 Configuration

### Environment Variables (`.env`)
```
VITE_API_URL=http://localhost:8000/api
```

### Tailwind Colors
Primary color palette đã được config trong `tailwind.config.js`

## 📡 API Integration

API client đã tích hợp JWT auth interceptor. Tất cả requests tự động gắn Bearer token nếu có trong localStorage.

```javascript
import { hrAPI } from './services/api';

// Usage
const employees = await hrAPI.getEmployees();
const syncStatus = await hrAPI.checkSync();
await hrAPI.executeSync([1, 2, 3]);
```

## 🧪 Testing with Backend

**Prerequisites**: Backend API must be running on `http://localhost:8000`

1. Start backend:
```bash
cd ../backend
../venv/bin/uvicorn app.main:app --reload
```

2. Start frontend:
```bash
npm run dev
```

3. Open browser: `http://localhost:5173`

## 🎯 Features

✅ **Implemented**:
- Employee list với filters
- Department dropdown
- Search functionality (debounced)
- Sync status badges
- Sync Center dashboard
- Bulk sync operations
- Loading states
- Error handling

🚧 **Future** (for other modules):
- Employee detail modal
- Organization tree view
- Dividends management
- Payroll calculation UI

## 🐛 Troubleshooting

### API Connection Failed
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS in backend .env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Tailwind not working
```bash
# Rebuild
npm run build
```
