import type { AuthResponse, Booking, EventItem, User } from './types';

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`/api${path}`, {
    ...init,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...init.headers },
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || `Request failed (${response.status})`);
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

export const api = {
  me: () => request<User>('/auth/me'),
  signup: (name: string, email: string, password: string) => request<AuthResponse>('/auth/signup', { method: 'POST', body: JSON.stringify({ name, email, password }) }),
  login: (email: string, password: string) => request<AuthResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  logout: () => request<void>('/auth/logout', { method: 'POST' }),
  events: () => request<EventItem[]>('/events'),
  wishlist: () => request<EventItem[]>('/me/wishlist'),
  addWishlist: (event_id: number) => request<EventItem>('/me/wishlist', { method: 'POST', body: JSON.stringify({ event_id }) }),
  removeWishlist: (eventId: number) => request<void>(`/me/wishlist/${eventId}`, { method: 'DELETE' }),
  bookings: () => request<Booking[]>('/me/bookings'),
  addBooking: (event_id: number, quantity: number, note: string) => request<Booking>('/me/bookings', { method: 'POST', body: JSON.stringify({ event_id, quantity, note }) }),
};
