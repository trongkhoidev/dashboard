/**
 * Zustand Store for Sync Management
 */
import { create } from 'zustand';
import { hrAPI } from '../services/api';

const useSyncStore = create((set) => ({
  syncNeeds: [],
  syncStatus: null,
  syncing: false,
  error: null,
  
  checkSync: async () => {
    set({ syncing: true, error: null });
    try {
      const response = await hrAPI.checkSync();
      set({ 
        syncStatus: response.data,
        syncNeeds: response.data.SyncNeeds,
        syncing: false 
      });
    } catch (error) {
      set({ error: error.message, syncing: false });
    }
  },
  
  executeSync: async ( employeeIds) => {
    set({ syncing: true, error: null });
    try {
      const response = await hrAPI.executeSync(employeeIds);
      set({ syncing: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, syncing: false });
      throw error;
    }
  },
}));

export default useSyncStore;
