# Integrated HR & Payroll Dashboard

Enterprise-grade HR & Payroll management system với dual database integration.

## 🎯 Project Summary

**Mục tiêu**: Xây dựng lớp ứng dụng quản trị trung tâm hợp nhất dữ liệu giữa:
- **SQL Server (HUMAN_2025)**: Hệ thống quản lý nhân sự
- **MySQL (payroll_2026)**: Hệ thống quản lý lương

**Stack**: Python (FastAPI) + ReactJS + SQL Server + MySQL

**Status**: ✅ Module A (HR Management) - COMPLETED

---

## 📦 Module A: HR Management

### Features
✅ Employee management với unified profiles  
✅ Real-time sync detection giữa HR và Payroll  
✅ Bulk sync execution  
✅ Organization structure management  
✅ Dividends tracking  
✅ Responsive UI với Tailwind CSS  

### Quick Start

📖 **New Developer?** → Xem [SETUP.md](SETUP.md) để setup trong 5 phút!

**Backend**:
```bash
# 1. Copy .env template
cp .env.example .env
# 2. Sửa database credentials trong .env
# 3. Test connections
cd backend
../venv/bin/python test_connections.py
# 4. Start server
../venv/bin/uvicorn app.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

**Frontend**:
```bash
cd frontend
npm run dev
# App: http://localhost:5173 hoặc 5174
```

**Database Setup Guide**: Xem [backend/app/database/README.md](backend/app/database/README.md)

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   React UI      │ ◄─────► │  FastAPI Backend │
│  (Port 5173)    │         │   (Port 8000)    │
└─────────────────┘         └──────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
            ┌───────────────┐               ┌────────────────┐
            │  SQL Server   │               │     MySQL      │
            │  (HUMAN_2025) │               │ (payroll_2026) │
            │   Master Data │               │   Synced Data  │
            └───────────────┘               └────────────────┘
```

---

## 📁 Project Structure

```
Dashboard/
├── backend/            # Python FastAPI backend
│   ├── app/
│   │   ├── database/  # DB connections & models
│   │   ├── modules/   # Business logic modules
│   │   │   └── hr_management/  # Module A
│   │   └── main.py    # FastAPI app
│   └── README.md
│
├── frontend/           # React + Vite frontend
│   ├── src/
│   │   ├── pages/     # UI pages
│   │   ├── components/ # Reusable components
│   │   ├── store/     # Zustand state management
│   │   └── services/  # API client
│   └── README.md
│
├── Documentation/      # DB backups & specs
├── .env               # Environment config
└── README.md          # This file
```

---

## 🚀 Features Showcase

### 1. Master HR View
- 📊 Employee list với filters và search
- 🎨 Color-coded sync status badges
- 🔍 Real-time department filtering
- 📈 Live statistics

### 2. Sync Center
- 🔄 Automatic sync detection
- ✅ Bulk sync operations
- 📝 Detailed change tracking
- ⚡ Transaction rollback support

### 3. API Documentation
- 📚 Interactive Swagger UI
- 🔗 8 RESTful endpoints
- 📊 Pydantic schema validation
- 🛡️ JWT authentication ready

---

## 📘 Documentation

- **Walkthrough**: [walkthrough.md](file:///Users/admin/.gemini/antigravity/brain/b9ac7ca5-b1ef-4ed3-b7d6-af3c36bdc8ea/walkthrough.md) - Detailed implementation guide
- **Implementation Plan**: [implementation_plan.md](file:///Users/admin/.gemini/antigravity/brain/b9ac7ca5-b1ef-4ed3-b7d6-af3c36bdc8ea/implementation_plan.md) - Technical architecture
- **Backend**: [backend/README.md](file:///Users/admin/Development/Dashboard/backend/README.md) - API setup guide
- **Frontend**: [frontend/README.md](file:///Users/admin/Development/Dashboard/frontend/README.md) - UI development guide

---

## 🔧 Configuration

### Database Setup

✅ **CẢ 2 DATABASES ĐÃ KẾT NỐI THÀNH CÔNG!**

**SQL Server (HUMAN_2025)**:
- Host: `127.0.0.1:1433` (Docker container)
- User: `sa`
- Database: `HUMAN_2025`
- Status: ✅ Connected

**MySQL (payroll)**:
- Host: `localhost:3306`
- User: `root`
- Database: `payroll`
- Status: ✅ Connected

📖 **Xem hướng dẫn chi tiết**: [backend/app/database/README.md](backend/app/database/README.md)

### Environment Variables

File `.env` đã được cấu hình:
```env
# SQL Server
SQL_SERVER_HOST=127.0.0.1
SQL_SERVER_PORT=1433
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=Ntkkidz2k50@
SQL_SERVER_DATABASE=HUMAN_2025

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=payroll
```

---

## 🧪 Testing

### Backend
```bash
cd backend
# Test DB connections
../venv/bin/python test_connections.py

# Run API server
../venv/bin/uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm run dev
```

### Integration Test
1. Open http://localhost:5173
2. Navigate to "Trung tâm đồng bộ"
3. Click "Kiểm tra lại"
4. Select employees và "Đồng bộ"
5. Verify in Master HR View

---

## 👥 Team Expansion

Module A đã tạo foundation cho team. Next modules:

**Module B - Payroll Calculation** (Assigned to: _)
- Tính lương dựa trên attendance và base salary
- Tích hợp với synced employee data

**Module C - Attendance Management** (Assigned to: _)
- Time tracking
- Leave management

**Module D - Reporting & Analytics** (Assigned to: _)
- Dashboards
- Export functionality

### Extension Points
- `/backend/app/modules/` - Add new modules
- `/frontend/src/pages/` - Add new UI pages
- APIs follow same pattern as Module A

---

## 📊 Stats

- **Backend**: 8 API endpoints | 6 DB models | 2 service classes
- **Frontend**: 2 main pages | 1 reusable component | 2 Zustand stores
- **Lines of Code**: ~2000+ (backend) | ~800+ (frontend)
- **Development Time**: 1 session (with Antigravity 🚀)

---

## 🎓 Tech Stack

**Backend**:
- FastAPI 0.128.0
- SQLAlchemy 2.0.46
- Pydantic 2.12.5
- PyODBC 5.3.0 (SQL Server)
- PyMySQL 1.1.2 (MySQL)

**Frontend**:
- React 18
- Vite 7.3.1
- Tailwind CSS
- Zustand (state management)
- Axios (HTTP client)
- React Router

---

## 📄 License

Internal enterprise project - All rights reserved

---

## 👨‍💻 Created By

Core Developer - Module A: HR Management  
Using **Antigravity** AI Coding Assistant  
Date: February 2, 2026

---

✅ **Ready for team collaboration and production deployment!**
