import axios from 'axios';

const tokenHeader = () => {
  const token = localStorage.getItem('ecfe_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const coreApi = axios.create({ baseURL: process.env.REACT_APP_CORE_API_URL || 'http://localhost:8001' });
export const gisApi = axios.create({ baseURL: process.env.REACT_APP_GIS_API_URL || 'http://localhost:8002' });
export const analyticsApi = axios.create({ baseURL: process.env.REACT_APP_ANALYTICS_API_URL || 'http://localhost:8003' });
export const crisisApi = axios.create({ baseURL: process.env.REACT_APP_CRISIS_API_URL || 'http://localhost:8004' });
export const mapboxToken = process.env.REACT_APP_MAPBOX_TOKEN || '';

[coreApi, gisApi, analyticsApi, crisisApi].forEach((client) => {
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem('ecfe_token');

    if (token) {
      (config.headers as any).Authorization = `Bearer ${token}`;
    }

    return config;
  });
});
