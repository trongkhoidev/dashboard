# 🗄️ Database Connection Guide

## 📋 Tổng quan

Hệ thống sử dụng **2 databases**:
- **SQL Server** (HUMAN_2025): Quản lý HR data
- **MySQL** (payroll): Quản lý Payroll data

File này hướng dẫn cách **setup database connection cho môi trường DEV của bạn**.

---

## 🚀 Quick Start (3 bước)

### Bước 1: Copy file `.env`

Từ thư mục root của project:

```bash
# Tạo file .env từ template
cp .env.example .env
```

### Bước 2: Điền Database Credentials

Mở file `.env` và **chỉnh sửa các giá trị sau** theo môi trường của bạn:

#### **SQL Server:**
```env
SQL_SERVER_HOST=127.0.0.1          # 👈 IP/hostname của SQL Server
SQL_SERVER_PORT=1433                # 👈 Port (mặc định 1433)
SQL_SERVER_USER=sa                  # 👈 Username
SQL_SERVER_PASSWORD=YourPassword    # 👈 ĐỔI PASSWORD NÀY!
SQL_SERVER_DATABASE=HUMAN_2025      # ⚠️ KHÔNG ĐỔI - Tên database phải giống nhau
```

#### **MySQL:**
```env
MYSQL_HOST=localhost                # 👈 IP/hostname của MySQL
MYSQL_PORT=3306                     # 👈 Port (mặc định 3306)
MYSQL_USER=root                     # 👈 Username
MYSQL_PASSWORD=YourMySQLPassword    # 👈 ĐỔI PASSWORD NÀY!
MYSQL_DATABASE=payroll              # ⚠️ KHÔNG ĐỔI - Tên database phải giống nhau
```

> **⚠️ QUAN TRỌNG:** 
> - Chỉ đổi: `HOST`, `PORT`, `USER`, `PASSWORD`
> - **KHÔNG đổi**: `DATABASE` name (phải giống team để đồng bộ schema)

### Bước 3: Setup Databases

#### **Option A: Dùng Docker (Recommended cho SQL Server trên macOS/Linux)**

**SQL Server:**
```bash
# Pull và chạy SQL Server container
docker run -d \
  --name sql \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=YourPassword123@' \
  -p 1433:1433 \
  mcr.microsoft.com/azure-sql-edge

# Tạo database
docker exec -it sql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P 'YourPassword123@' -C \
  -Q "CREATE DATABASE HUMAN_2025"

# Import schema (nếu có file backup)
# docker cp schema.sql sql:/tmp/
# docker exec sql /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P 'YourPassword' -d HUMAN_2025 -i /tmp/schema.sql
```

**MySQL:**
```bash
# Nếu chưa cài MySQL
brew install mysql
brew services start mysql

# Tạo database
mysql -u root -p -e "CREATE DATABASE payroll;"

# Import schema (nếu có file backup)
# mysql -u root -p payroll < schema.sql
```

#### **Option B: Dùng native SQL Server (Windows)**

1. Cài SQL Server Express
2. Mở SQL Server Management Studio (SSMS)
3. Tạo database `HUMAN_2025`
4. Update `.env` với credentials của bạn

---

## ✅ Verify Connection

Sau khi setup xong, kiểm tra kết nối:

```bash
cd backend
../venv/bin/python test_connections.py
```

**Kết quả mong đợi:**
```
================================================================================
TESTING DATABASE CONNECTIONS
================================================================================

📡 Initializing database connections...
🔵 Attempting SQL Server connection...
✅ SQL Server connected successfully
🟢 Attempting MySQL connection...
✅ MySQL connected successfully

🔍 Testing connections...
✅ SQL Server OK: Microsoft Azure SQL Edge Developer (RTM) - 15.0.20...
✅ MySQL OK: Version 9.5.0

================================================================================
✅ ALL TESTS PASSED - Database connections successful!
================================================================================
```

**Nếu có lỗi:**
- ✅ Kiểm tra database service đã chạy chưa
- ✅ Kiểm tra credentials trong `.env`
- ✅ Kiểm tra firewall/port có bị block không
- ✅ Xem phần **Troubleshooting** bên dưới

---

## 🔧 Chi tiết các biến môi trường

| Biến | Mô tả | Giá trị mẫu | Có thể đổi? |
|------|-------|-------------|-------------|
| `SQL_SERVER_HOST` | IP/hostname SQL Server | `127.0.0.1` | ✅ Có |
| `SQL_SERVER_PORT` | Port SQL Server | `1433` | ✅ Có |
| `SQL_SERVER_USER` | Username SQL Server | `sa` | ✅ Có |
| `SQL_SERVER_PASSWORD` | Password SQL Server | `YourPass123@` | ✅ Có |
| `SQL_SERVER_DATABASE` | Tên database | `HUMAN_2025` | ❌ **KHÔNG** |
| `MYSQL_HOST` | IP/hostname MySQL | `localhost` | ✅ Có |
| `MYSQL_PORT` | Port MySQL | `3306` | ✅ Có |
| `MYSQL_USER` | Username MySQL | `root` | ✅ Có |
| `MYSQL_PASSWORD` | Password MySQL | `yourpass` | ✅ Có |
| `MYSQL_DATABASE` | Tên database | `payroll` | ❌ **KHÔNG** |

---

## 🏗️ Kiến trúc Database Connection

```
┌─────────────────────────────────────┐
│     connections.py                  │  ← File này quản lý tất cả connections
│  (Singleton DatabaseManager)        │
└─────────────┬───────────────────────┘
              │
    ┌─────────┴─────────┐
    ▼                   ▼
┌─────────┐        ┌──────────┐
│SQL      │        │MySQL     │
│Server   │        │          │
│Engine   │        │Engine    │
└─────────┘        └──────────┘
    │                   │
    ▼                   ▼
SessionLocal_HR    SessionLocal_Payroll
```

**Các phương thức sử dụng:**
- `db_manager.get_hr_db()` - Lấy SQL Server session
- `db_manager.get_payroll_db()` - Lấy MySQL session

---

## 💻 Sử dụng trong Code

### Import
```python
from app.database.connections import db_manager
```

### Trong Route Handler
```python
from fastapi import APIRouter
from app.database.connections import db_manager

router = APIRouter()

@router.get("/employees")
def get_employees():
    # Sử dụng context manager
    with db_manager.get_hr_db() as db:
        employees = db.query(Employee).all()
        return employees
```

### Với Dependency Injection
```python
from fastapi import Depends
from app.modules.hr_management.dependencies import get_hr_db, get_payroll_db

@router.get("/sync-status")
def check_sync(
    hr_db = Depends(get_hr_db),
    payroll_db = Depends(get_payroll_db)
):
    # Đã có db sessions sẵn sàng
    employees = hr_db.query(Employee).all()
    return {"count": len(employees)}
```

---

## 🐛 Troubleshooting

### ❌ Lỗi: "Login timeout expired"

**Nguyên nhân:** SQL Server không chạy hoặc không accessible

**Giải pháp:**
```bash
# Kiểm tra Docker container
docker ps | grep sql

# Nếu stopped, start lại
docker start sql

# Kiểm tra logs
docker logs sql

# Test connection thủ công
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -C -Q "SELECT @@VERSION"
```

### ❌ Lỗi: "Access denied for user 'root'@'localhost'"

**Nguyên nhân:** MySQL password sai

**Giải pháp:**
```bash
# Test password
mysql -u root -p

# Reset password nếu cần
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### ❌ Lỗi: "Can't connect to MySQL server"

**Nguyên nhân:** MySQL service chưa chạy

**Giải pháp:**
```bash
# macOS
brew services start mysql

# Linux
sudo systemctl start mysql

# Kiểm tra port
lsof -i :3306
```

### ❌ Lỗi: "Database 'HUMAN_2025' does not exist"

**Nguyên nhân:** Database chưa được tạo

**Giải pháp:**
```bash
# SQL Server
sqlcmd -S 127.0.0.1,1433 -U sa -P 'YourPassword' -C \
  -Q "CREATE DATABASE HUMAN_2025"

# MySQL
mysql -u root -p -e "CREATE DATABASE payroll"
```

---

## 📊 Database Schema

### SQL Server (HUMAN_2025)

**Bảng chính:**
- `Employees` - Thông tin nhân viên
- `Departments` - Phòng ban
- `Positions` - Chức vụ
- `Attendance` - Chấm công

### MySQL (payroll)

**Bảng chính:**
- `EmployeePayroll` - Bảng lương
- `Payslips` - Phiếu lương
- `SalaryComponents` - Các khoản lương

> **📁 Backup files:** Tìm trong thư mục `Documentation/` để import schema

---

## 🔒 Security Best Practices

1. ✅ **KHÔNG commit file `.env`** vào Git
2. ✅ Sử dụng `.env.example` làm template
3. ✅ Đổi password mặc định trong production
4. ✅ Sử dụng environment variables trong CI/CD
5. ✅ Giữ database credentials riêng tư

---

## 📞 Cần giúp đỡ?

**Liên hệ:**
- Team Lead: [Your Name]
- Quick Setup: `SETUP.md` (root folder)
- Issues: GitHub Issues

**Trước khi hỏi, hãy:**
1. ✅ Đọc file này kỹ
2. ✅ Chạy `test_connections.py`
3. ✅ Kiểm tra logs của database service
4. ✅ Đảm bảo `.env` đã được tạo và điền đúng

---

## 📝 Checklist Setup

- [ ] Copy `.env.example` thành `.env`
- [ ] Điền SQL Server credentials
- [ ] Điền MySQL credentials
- [ ] Start SQL Server (Docker hoặc native)
- [ ] Start MySQL service
- [ ] Tạo database `HUMAN_2025` trong SQL Server
- [ ] Tạo database `payroll` trong MySQL
- [ ] Import schema (nếu có backup files)
- [ ] Chạy `test_connections.py`
- [ ] Thấy ✅ ALL TESTS PASSED
- [ ] Start backend: `../venv/bin/uvicorn app.main:app --reload`
- [ ] Verify API health: `curl http://localhost:8000/health`

---

**✨ Sau khi hoàn thành checklist, bạn đã sẵn sàng develop!**

Last Updated: 2026-02-03
