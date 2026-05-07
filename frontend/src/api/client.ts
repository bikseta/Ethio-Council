import axios, { AxiosInstance } from 'axios';

const CORE_API_URL = process.env.REACT_APP_CORE_API_URL || 'http://localhost:8001';
const GIS_API_URL = process.env.REACT_APP_GIS_API_URL || 'http://localhost:8002';
const ANALYTICS_API_URL = process.env.REACT_APP_ANALYTICS_API_URL || 'http://localhost:8003';
const CRISIS_API_URL = process.env.REACT_APP_CRISIS_API_URL || 'http://localhost:8004';

function createClient(baseURL: string): AxiosInstance {
  const client = axios.create({ baseURL });
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
  client.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }
      return Promise.reject(error);
    }
  );
  return client;
}

export const coreClient = createClient(CORE_API_URL);
export const gisClient = createClient(GIS_API_URL);
export const analyticsClient = createClient(ANALYTICS_API_URL);
export const crisisClient = createClient(CRISIS_API_URL);

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    coreClient.post('/api/v1/auth/login', { email, password }),
  me: () => coreClient.get('/api/v1/auth/me'),
};

// Members API
export const membersApi = {
  list: (params?: Record<string, unknown>) => coreClient.get('/api/v1/members/', { params }),
  get: (id: string) => coreClient.get(`/api/v1/members/${id}`),
  create: (data: Record<string, unknown>) => coreClient.post('/api/v1/members/', data),
  delete: (id: string) => coreClient.delete(`/api/v1/members/${id}`),
};

// Churches API
export const churchesApi = {
  list: (params?: Record<string, unknown>) => coreClient.get('/api/v1/churches/', { params }),
  get: (id: string) => coreClient.get(`/api/v1/churches/${id}`),
  create: (data: Record<string, unknown>) => coreClient.post('/api/v1/churches/', data),
  denominations: () => coreClient.get('/api/v1/churches/denominations'),
};

// Analytics API
export const analyticsApi = {
  summary: () => analyticsClient.get('/api/v1/analytics/summary'),
  growth: (period?: string) => analyticsClient.get('/api/v1/analytics/growth', { params: { period } }),
};

// Crisis API
export const crisisApi = {
  list: (params?: Record<string, unknown>) => crisisClient.get('/api/v1/crisis/alerts', { params }),
  create: (data: Record<string, unknown>) => crisisClient.post('/api/v1/crisis/alerts', data),
  acknowledge: (id: string) => crisisClient.patch(`/api/v1/crisis/alerts/${id}/acknowledge`),
  dashboard: () => crisisClient.get('/api/v1/crisis/dashboard'),
};

// GIS API
export const gisApi = {
  churches: (params?: Record<string, unknown>) => gisClient.get('/api/v1/gis/churches/geojson', { params }),
  crisis: (params?: Record<string, unknown>) => gisClient.get('/api/v1/gis/crisis/geojson', { params }),
  regions: () => gisClient.get('/api/v1/gis/regions/geojson'),
};
