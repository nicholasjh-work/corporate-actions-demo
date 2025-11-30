import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const eventAPI = {
  createEvent: (eventData) => api.post('/api/v1/events', eventData),
  
  listEvents: (params = {}) => api.get('/api/v1/events', { params }),
  
  getEvent: (eventId) => api.get(`/api/v1/events/${eventId}`),
  
  cancelEvent: (eventId) => api.post(`/api/v1/events/${eventId}/cancel`),
  
  getMetrics: () => api.get('/api/v1/metrics'),
  
  healthCheck: () => api.get('/api/v1/health'),
};

export default api;
