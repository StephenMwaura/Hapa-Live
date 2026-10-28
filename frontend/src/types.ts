export interface User { id: number; name: string; email: string }
export interface EventItem {
  id: number; slug: string; title: string; artist: string; city: string; venue: string;
  starts_at: string; price_from_kes: number | null; genre: string; source_url: string;
  source_label: string; art: string; featured: boolean;
}
export interface Booking { id: number; event: EventItem; quantity: number; note: string | null; created_at: string }
export interface AuthResponse { user: User }
