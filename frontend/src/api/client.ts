/**
 * API Configuration and HTTP Client
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://api.dailybread.com';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// API methods
export const authAPI = {
  register: (data: any) => api.post('/auth/register', data),
  login: (email: string, password: string) => api.post('/auth/login', { email, password }),
  getCurrentUser: () => api.get('/auth/me'),
  refreshToken: (refreshToken: string) => api.post('/auth/refresh', { refresh_token: refreshToken }),
};

export const profileAPI = {
  getProfile: (userId: string) => api.get(`/profiles/${userId}`),
  updateProfile: (userId: string, data: any) => api.put(`/profiles/${userId}`, data),
};

export const recipesAPI = {
  getRecipes: (params?: any) => api.get('/recipes', { params }),
  getRecipe: (id: string) => api.get(`/recipes/${id}`),
  searchRecipes: (query: string) => api.get(`/recipes/search?q=${query}`),
};

export const tipsAPI = {
  getDailyTips: () => api.get('/tips/daily'),
  getTips: (params?: any) => api.get('/tips', { params }),
};

export const favoritesAPI = {
  getFavorites: () => api.get('/favorites'),
  addFavorite: (itemId: string, itemType: string) => api.post('/favorites', { item_id: itemId, item_type: itemType }),
  removeFavorite: (itemId: string) => api.delete(`/favorites/${itemId}`),
};

export const mealsAPI = {
  getRecommendations: (mealType: string) => api.post('/meals/recommendations', { meal_type: mealType }),
  createMealPlan: (data: any) => api.post('/meals/plans', data),
  getMealPlans: () => api.get('/meals/plans'),
};

export const ordersAPI = {
  createOrder: (data: any) => api.post('/orders', data),
  getOrders: () => api.get('/orders'),
  getOrder: (id: string) => api.get(`/orders/${id}`),
  updateOrderStatus: (id: string, status: string) => api.patch(`/orders/${id}`, { status }),
};

export default api;
