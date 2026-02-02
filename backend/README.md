# HR & Payroll Dashboard - Module A

Integrated HR & Payroll Management System - Backend API

## 📋 Project Structure

```
backend/
├── app/
│   ├── core/              # Core utilities (JWT, config)
│   ├── database/          # Database connections & models
│   │   ├── connections.py # Dual DB manager
│   │   ├── models_hr.py   # SQL Server models
│   │   └── models_payroll.py # MySQL models
│   ├── modules/
│   │   └── hr_management/ # Module A: HR Management
│   │       ├── routes.py  # API endpoints
│   │       ├── services.py# Business logic
│   │       ├── sync_service.py # Sync logic
│   │       └── schemas.py # Pydantic models
│   └── main.py            # FastAPI app
├── requirements.txt
└── test_connections.py    # DB connection test
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.14+ (with venv already created)
- SQL Server (running in Azure Data Studio)
- MySQL (running locally)
- Databases:
  - `HUMAN_2025` (SQL Server)
  - `payroll_2026` (MySQL)

### 2. Configuration

Edit `.env` file and update MySQL password:

```env
MYSQL_PASSWORD=your_actual_mysql_password
```

💡 **How to find MySQL password:**
```bash
# If you don't remember, reset it:
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Test Database Connections

```bash
cd backend
../venv/bin/python test_connections.py
```

Expected output:
```
✅ SQL Server connected: Microsoft SQL Server...
✅ MySQL connected: Version 8.0.41
✅ ALL TESTS PASSED - Database connections successful!
```

### 4. Start API Server

```bash
cd backend
../venv/bin/uvicorn app.main:app --reload --port 8000
```

Server will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/docs`

## 📡 API Endpoints

### Employees
- `GET /api/hr/employees` - List employees with sync status
  - Query params: `department_id`, `search`
- `GET /api/hr/employees/{id}` - Get employee detail

### Organization
- `GET /api/hr/org-structure` - Get org structure
- `GET /api/hr/departments` - List departments

### Sync
- `POST /api/hr/sync/check` - Check sync needs
- `POST /api/hr/sync/execute` - Execute sync
  - Body: `{"EmployeeIDs": [1, 2, 3]}`

### Dividends
- `GET /api/hr/dividends` - List dividends
  - Query param: `employee_id`

## 🔧 Troubleshooting

### SQL Server Connection Failed
```bash
# Check if SQL Server is running in Azure Data Studio
# Verify connection credentials in .env
# Test port 1433 is accessible
```

### MySQL Connection Failed
```bash
# Check MySQL service
brew services list | grep mysql

# Start if not running
brew services start mysql

# Verify database exists
mysql -u root -p
SHOW DATABASES;
# Should see 'payroll_2026'
```

## 📚 Next Steps

After backend is running:
1. Frontend development (React + Vite)
2. Integration testing
3. Deploy to local environment
