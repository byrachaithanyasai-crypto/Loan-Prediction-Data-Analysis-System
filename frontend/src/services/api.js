import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const getHealth = async () => (await api.get('/api/health')).data;
export const getDashboardStats = async () => (await api.get('/api/dashboard/stats')).data;
export const predictRisk = async (data) => (await api.post('/api/predict', data)).data;
export const getModelPerformance = async () => (await api.get('/api/models/performance')).data;
export const getModels = async () => (await api.get('/api/models')).data;
export const getAnalysisSummary = async () => (await api.get('/api/analysis/summary')).data;
