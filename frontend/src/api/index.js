import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Attach JWT token to every request
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── AUTH ───
export const userRegister = (data) => API.post('/auth/user/register', data);
export const userLogin = (data) => API.post('/auth/user/login', data);
export const bankRegister = (data) => API.post('/auth/bank/register', data);
export const bankLogin = (data) => API.post('/auth/bank/login', data);
export const i4cLogin = (data) => API.post('/auth/i4c/login', data);

// ─── USER ───
export const getMyProfile = () => API.get('/user/me');
export const fileComplaint = (data) => API.post('/user/complaint', data);
export const trackComplaint = (no) => API.get(`/user/complaint/track/${no}`);
export const listMyComplaints = () => API.get('/user/complaints');

// ─── BANK ───
export const getBankProfile = () => API.get('/bank/me');
export const getBankNotifications = () => API.get('/bank/notifications');
export const uploadBankStatement = (data) => API.post('/bank/statement/upload', data);
export const getBankChains = () => API.get('/bank/chains');
export const getBankAccounts = () => API.get('/bank/accounts');
export const updateNotificationStatus = (id, status) =>
  API.put(`/bank/notification/${id}/status`, { status });

// ─── I4C ───
export const getI4CDashboard = () => API.get('/i4c/dashboard');
export const getAllComplaints = (params) => API.get('/i4c/complaints', { params });
export const getAllChains = () => API.get('/i4c/chains');
export const getChainDetail = (no) => API.get(`/i4c/chain/${no}`);
export const getAllBankData = () => API.get('/i4c/bank-data');
export const getAllUsers = () => API.get('/i4c/users');
export const getAllBanks = () => API.get('/i4c/banks');
export const getAllNotifications = () => API.get('/i4c/notifications');
export const updateComplaintStatus = (no, status) =>
  API.put(`/i4c/complaint/${no}/status`, { status });
export const getMoneyFlowAnalytics = () => API.get('/i4c/analytics/money-flow');

export default API;
