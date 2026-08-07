import axios from 'axios';

const api = axios.create({
  baseURL: '/dashboard',
});

export const getSummary = () => api.get('/summary/');
export const getSlowAPIs = () => api.get('/slow-apis/');
export const getPerformanceIssues = () => api.get('/issues/');
export const getTopProblematicAPIs = () => api.get('/top-apis/');
export const getSlowQueries = () => api.get('/slow-queries/');
export const getRecommendations = () => api.get('/recommendations/');

export default api;
