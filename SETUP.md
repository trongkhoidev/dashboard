# 🚀 Quick Setup Guide for New Developers

## Setup trong 5 phút

### 1️⃣ Clone Project
```bash
git clone <repository-url>
cd Dashboard
```

### 2️⃣ Setup Backend
```bash
# Copy environment template
cp .env.example .env

# Sửa .env với database credentials của bạn
# CHỈ đổi: HOST, PORT, USER, PASSWORD
# KHÔNG đổi: DATABASE names (HUMAN_2025, payroll)
nano .env  # hoặc code .env

# Cài dependencies
cd backend
pip install -r requirements.txt

# Test database connections
../venv/bin/python test_connections.py
# Kỳ vọng: ✅ ALL TESTS PASSED

# Start backend server
../venv/bin/uvicorn app.main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

### 3️⃣ Setup Frontend
```bash
cd frontend
npm install
npm run dev
# App: http://localhost:5173 hoặc http://localhost:5174
```

### 4️⃣ Setup Databases

**SQL Server (Docker - Recommended):**
```bash
docker run -d --name sql \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=YourPassword123@' \
  -p 1433:1433 \
  mcr.microsoft.com/azure-sql-edge

# Tạo database
docker exec -it sql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P 'YourPassword123@' -C \
  -Q "CREATE DATABASE HUMAN_2025"
```

**MySQL:**
```bash
# macOS
brew install mysql
brew services start mysql

# Tạo database
mysql -u root -p -e "CREATE DATABASE payroll"
```

---

## 📁 Quan trọng nhất

### File cần đọc:
1. **`backend/app/database/README.md`** ← Hướng dẫn database connection chi tiết
2. **`.env.example`** ← Template environment variables

### Commands hay dùng:

```bash
# Test database connections
cd backend
../venv/bin/python test_connections.py

# Start backend
../venv/bin/uvicorn app.main:app --reload

# Start frontend
cd frontend
npm run dev

# Check API health
curl http://localhost:8000/health
```

---

## ⚠️ Lưu ý

- ✅ **KHÔNG commit file `.env`** (đã có trong .gitignore)
- ✅ Chỉ đổi credentials trong `.env`, không sửa code
- ✅ Database names phải giống team: `HUMAN_2025` và `payroll`
- ✅ Nếu lỗi connection, xem `backend/app/database/README.md`

---

## 🔗 Links

- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Frontend: http://localhost:5173
- Health Check: http://localhost:8000/health

---

✨ **Happy Coding!**
