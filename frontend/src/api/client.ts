import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const coreApiUrl = process.env.REACT_APP_CORE_API_URL || 'http://localhost:8000';
const gisApiUrl = process.env.REACT_APP_GIS_API_URL || 'http://localhost:8001';
const crisisApiUrl = process.env.REACT_APP_CRISIS_API_URL || 'http://localhost:8002';
const analyticsApiUrl = process.env.REACT_APP_ANALYTICS_API_URL || 'http://localhost:8003';

export const coreApi = axios.create({ baseURL: coreApiUrl });
export const gisApi = axios.create({ baseURL: gisApiUrl });
export const crisisApi = axios.create({ baseURL: crisisApiUrl });
export const analyticsApi = axios.create({ baseURL: analyticsApiUrl });

[coreApi, gisApi, crisisApi, analyticsApi].forEach((api) => {
  api.interceptors.request.use((config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
});

export const authApi = {
  login: (username: string, password: string) =>
    coreApi.post('/api/v1/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  me: (token?: string) =>
    coreApi.get('/api/v1/auth/me', token ? { headers: { Authorization: `Bearer ${token}` } } : undefined),
};

export const churchesApi = {
  list: () => coreApi.get('/api/v1/churches/'),
  create: (payload: Record<string, unknown>) => coreApi.post('/api/v1/churches/', payload),
};

export const denominationsApi = {
  list: () => coreApi.get('/api/v1/denominations/'),
};

export const ministriesApi = {
  list: () => coreApi.get('/api/v1/ministries/'),
};

export const leadersApi = {
  list: () => coreApi.get('/api/v1/leaders/'),
};

export const hierarchyApi = {
  summary: () => coreApi.get('/api/v1/hierarchy/summary'),
  regions: () => coreApi.get('/api/v1/hierarchy/regions'),
  zones: () => coreApi.get('/api/v1/hierarchy/zones'),
  woredas: () => coreApi.get('/api/v1/hierarchy/woredas'),
  kebeles: () => coreApi.get('/api/v1/hierarchy/kebeles'),
};

export const diasporaApi = {
  communities: () => coreApi.get('/api/v1/diaspora/communities'),
  partnerships: () => coreApi.get('/api/v1/diaspora/partnerships'),
};

export const registrationsApi = {
  summary: () => gisApi.get('/api/v1/summary'),
  list: () => gisApi.get('/api/v1/registrations'),
};

export const crisisPortalApi = {
  summary: () => crisisApi.get('/api/v1/summary'),
  incidents: () => crisisApi.get('/api/v1/incidents'),
  volunteers: () => crisisApi.get('/api/v1/volunteers'),
  distributions: () => crisisApi.get('/api/v1/distributions'),
};

export const analyticsPortalApi = {
  dashboard: () => analyticsApi.get('/api/v1/analytics/dashboard'),
};
