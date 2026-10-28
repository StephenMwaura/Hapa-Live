import { ArrowUpRight, CalendarDays, Check, Heart, MapPin } from 'lucide-react';
import type { EventItem } from '../types';

export default function EventCard({ event, saved, onWishlist, onBooked, compact = false }: { event: EventItem; saved: boolean; onWishlist: () => void; onBooked?: () => void; compact?: boolean }) {
  const date = new Date(event.starts_at); const month = date.toLocaleString('en', { month: 'short' }).toUpperCase(); const day = date.toLocaleString('en', { day: '2-digit' });
  return <article className={`event-card ${compact ? 'event-card-compact' : ''}`}>
    <div className={`event-art art-${event.art}`}><div className="date-tile"><b>{day}</b><span>{month}</span></div><span className="art-type">{event.genre}</span>{!compact && <button className={`heart-button ${saved ? 'is-saved' : ''}`} onClick={onWishlist} aria-label={saved ? 'Remove from wishlist' : 'Add to wishlist'} title={saved ? 'Remove from wishlist' : 'Add to wishlist'}><Heart size={18} fill={saved ? 'currentColor' : 'none'} /></button>}</div>
    <div className="event-content"><div className="event-city"><MapPin size={13}/>{event.city}</div><h3>{event.title}</h3><p className="event-artist">{event.artist}</p><div className="event-venue"><CalendarDays size={14}/><span>{date.toLocaleString('en-KE', { weekday: 'short', day: 'numeric', month: 'short' })}</span><i>·</i><MapPin size={14}/><span>{event.venue}</span></div>
      <div className="event-bottom"><div className="event-price">{event.price_from_kes ? `KSh ${event.price_from_kes.toLocaleString()}+` : 'Check listing'}<small>per ticket · see organiser for latest</small></div><a className="ticket-link" href={event.source_url} target="_blank" rel="noreferrer">Get tickets <ArrowUpRight size={15}/></a></div>
      {onBooked && <button className="record-link" onClick={onBooked}><Check size={14}/> I’ve booked this</button>}
      <div className="source-label">Listed by <a href={event.source_url} target="_blank" rel="noreferrer">{event.source_label} ↗</a></div>
    </div>
  </article>;
}