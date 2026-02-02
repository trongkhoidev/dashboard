/**
 * Axios API Client for HR & Payroll Dashboard
 * Handles all HTTP requests to backend API with JWT auth
 */
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor - Add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor - Handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('access_token');
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// HR Management API Methods
// ============================================================================

export const hrAPI = {
  // Employees
  getEmployees: (params = {}) => api.get('/hr/employees', { params }),
  getEmployee: (id) => api.get(`/hr/employees/${id}`),
  
  // Organization
  getOrgStructure: () => api.get('/hr/org-structure'),
  getDepartments: () => api.get('/hr/departments'),
  
  // Sync
  checkSync: () => api.post('/hr/sync/check'),
  executeSync: (employeeIds) => api.post('/hr/sync/execute', { EmployeeIDs: employeeIds }),
  
  // Dividends
  getDividends: (employeeId) => 
    api.get('/hr/dividends', { params: employeeId ? { employee_id: employeeId } : {} }),
};

export default api;
