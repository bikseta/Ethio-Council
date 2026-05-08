import axios from 'axios';

export const coreApi = axios.create({ baseURL: process.env.REACT_APP_CORE_API_URL || 'http://localhost:8011' });
export const gisApi = axios.create({ baseURL: process.env.REACT_APP_GIS_API_URL || 'http://localhost:8012' });
export const analyticsApi = axios.create({ baseURL: process.env.REACT_APP_ANALYTICS_API_URL || 'http://localhost:8013' });
export const crisisApi = axios.create({ baseURL: process.env.REACT_APP_CRISIS_API_URL || 'http://localhost:8014' });
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
