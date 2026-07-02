const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

function getToken() {
  return localStorage.getItem('token');
}

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(data?.error || 'Something went wrong');
  }
  return data;
}

export const api = {
  signup: (payload) => request('/auth/signup', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),

  getBusiness: (slug) => request(`/businesses/${slug}`),
  getServices: (slug) => request(`/businesses/${slug}/services`),
  getAvailability: (slug, serviceId, date) =>
    request(`/businesses/${slug}/availability?service_id=${serviceId}&date=${date}`),
  createBooking: (slug, payload) =>
    request(`/businesses/${slug}/bookings`, { method: 'POST', body: JSON.stringify(payload) }),

  myServices: () => request('/services'), // not implemented server-side yet, placeholder
  createService: (payload) => request('/services', { method: 'POST', body: JSON.stringify(payload) }),
  updateService: (id, payload) => request(`/services/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteService: (id) => request(`/services/${id}`, { method: 'DELETE' }),

  setAvailability: (payload) => request('/availability', { method: 'POST', body: JSON.stringify(payload) }),
  listAvailability: () => request('/availability'),

  listBookings: (status) => request(`/bookings${status ? `?status=${status}` : ''}`),
  updateBooking: (id, payload) => request(`/bookings/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
};

export { getToken };
