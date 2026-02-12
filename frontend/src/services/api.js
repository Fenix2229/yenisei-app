import axios from 'axios';

const API_BASE_URL = 'https://yenisei-backend.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Эпохи
export const getEpochs = () => api.get('/epochs/');
export const getEpochWithEvents = (epochId) => api.get(`/epochs/${epochId}`);

// События
export const getAllEvents = (params = {}) => api.get('/events/', { params });
export const getEvent = (eventId) => api.get(`/events/${eventId}`);
export const getImportantEvents = (limit = 10) => 
  api.get('/events/important/top', { params: { limit } });

// География
export const getGeographicPoints = (type = null) => 
  api.get('/geography/', { params: type ? { type } : {} });
export const getGeographicPoint = (pointId) => api.get(`/geography/${pointId}`);
export const getMajorCities = () => api.get('/geography/cities/major');

// Галерея
export const getGalleryImages = (params = {}) => 
  api.get('/gallery/', { params });
export const getGalleryImage = (imageId) => api.get(`/gallery/${imageId}`);

// Викторина
export const getRandomQuestions = (params = {}) => 
  api.get('/quiz/questions/random', { params });
export const checkAnswer = (data) => api.post('/quiz/check-answer', data);
export const getQuizCategories = () => api.get('/quiz/categories');

// Факты
export const getFacts = (category = null) => 
  api.get('/facts/', { params: category ? { category } : {} });
export const getRandomFact = () => api.get('/facts/random');

export default api;