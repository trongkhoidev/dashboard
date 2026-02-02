/**
 * Zustand Store for Employee Management
 * Global state management cho employee data và sync status
 */
import { create } from 'zustand';
import { hrAPI } from '../services/api';

const useEmployeeStore = create((set, get) => ({
  // State
  employees: [],
  selectedEmployee: null,
  departments: [],
  loading: false,
  error: null,
  filters: {
    departmentId: null,
    search: '',
  },
  
  // Actions
  fetchEmployees: async (filters = {}) => {
    set({ loading: true, error: null });
    try {
      const response = await hrAPI.getEmployees(filters);
      set({ employees: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  
  fetchEmployee: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await hrAPI.getEmployee(id);
      set({ selectedEmployee: response.data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
  
  fetchDepartments: async () => {
    try {
      const response = await hrAPI.getDepartments();
      set({ departments: response.data });
    } catch (error) {
      console.error('Failed to fetch departments:', error);
    }
  },
  
  setFilters: (newFilters) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters }
    }));
    // Auto-fetch with new filters
    get().fetchEmployees(get().filters);
  },
  
  clearFilters: () => {
    set({ filters: { departmentId: null, search: '' } });
    get().fetchEmployees();
  },
}));

export default useEmployeeStore;
