import { useState, useEffect } from 'react';
import { api } from '../api';
import './BookingPage.css';

function nextDays(n) {
  const days = [];
  const today = new Date();
  for (let i = 0; i < n; i++) {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    days.push(d);
  }
  return days;
}

function fmtDate(d) {
  return d.toISOString().split('T')[0];
}

export default function BookingPage({ slug }) {
  const [business, setBusiness] = useState(null);
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [selectedDate, setSelectedDate] = useState(fmtDate(new Date()));
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [clientName, setClientName] = useState('');
  const [clientPhone, setClientPhone] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [confirmedBooking, setConfirmedBooking] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const days = nextDays(14);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [biz, svc] = await Promise.all([api.getBusiness(slug), api.getServices(slug)]);
        if (cancelled) return;
        setBusiness(biz);
        setServices(svc);
        if (svc.length) setSelectedService(svc[0]);
      } catch (e) {
        if (!cancelled) setError('This booking page could not be found.');
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
  }, [slug]);

  useEffect(() => {
    if (!selectedService) return;
    setSelectedSlot(null);
    api.getAvailability(slug, selectedService.id, selectedDate)
      .then((res) => setSlots(res.slots))
      .catch(() => setSlots([]));
  }, [slug, selectedService, selectedDate]);

  async function handleConfirm(e) {
    e.preventDefault();
    if (!selectedSlot || !clientName || !clientPhone) return;
    setSubmitting(true);
    setError(null);
    try {
      const bookingTime = `${selectedDate}T${selectedSlot}:00`;
      const booking = await api.createBooking(slug, {
        serviceId: selectedService.id,
        clientName,
        clientPhone,
        bookingTime,
      });
      setConfirmedBooking(booking);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <div className="booking-status">Loading…</div>;
  if (error && !business) return <div className="booking-status">{error}</div>;

  if (confirmedBooking) {
    return (
      <div className="booking-page">
        <Ticket business={business} booking={confirmedBooking} />
      </div>
    );
  }

  return (
    <div className="booking-page">
      <header className="booking-header">
        <p className="booking-eyebrow">Book a slot at</p>
        <h1>{business.name}</h1>
      </header>

      <section className="booking-section">
        <h2 className="section-label">01 — Choose a service</h2>
        <div className="service-list">
          {services.map((s) => (
            <button
              key={s.id}
              className={`service-card ${selectedService?.id === s.id ? 'selected' : ''}`}
              onClick={() => setSelectedService(s)}
            >
              <span className="service-name">{s.name}</span>
              <span className="service-meta">{s.durationMinutes} min · K{s.price}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="booking-section">
        <h2 className="section-label">02 — Choose a day</h2>
        <div className="day-strip">
          {days.map((d) => {
            const key = fmtDate(d);
            const isSelected = key === selectedDate;
            return (
              <button
                key={key}
                className={`day-chip ${isSelected ? 'selected' : ''}`}
                onClick={() => setSelectedDate(key)}
              >
                <span className="day-dow">{d.toLocaleDateString('en-GB', { weekday: 'short' })}</span>
                <span className="day-num">{d.getDate()}</span>
              </button>
            );
          })}
        </div>
      </section>

      <section className="booking-section">
        <h2 className="section-label">03 — Choose a time</h2>
        {slots.length === 0 ? (
          <p className="no-slots">No open slots this day — try another date.</p>
        ) : (
          <div className="slot-grid">
            {slots.map((slot) => (
              <button
                key={slot}
                className={`slot-chip ${selectedSlot === slot ? 'selected' : ''}`}
                onClick={() => setSelectedSlot(slot)}
              >
                {slot}
              </button>
            ))}
          </div>
        )}
      </section>

      {selectedSlot && (
        <section className="booking-section">
          <h2 className="section-label">04 — Your details</h2>
          <form className="detail-form" onSubmit={handleConfirm}>
            <label>
              Full name
              <input
                type="text"
                required
                value={clientName}
                onChange={(e) => setClientName(e.target.value)}
                placeholder="e.g. Grace Luwi"
              />
            </label>
            <label>
              WhatsApp number
              <input
                type="tel"
                required
                value={clientPhone}
                onChange={(e) => setClientPhone(e.target.value)}
                placeholder="e.g. 0977000000"
              />
            </label>
            {error && <p className="form-error">{error}</p>}
            <button className="btn-primary" type="submit" disabled={submitting}>
              {submitting ? 'Confirming…' : 'Confirm booking'}
            </button>
          </form>
        </section>
      )}
    </div>
  );
}

function Ticket({ business, booking }) {
  const dt = new Date(booking.bookingTime);
  return (
    <div className="ticket">
      <div className="ticket-top">
        <p className="ticket-eyebrow">Booking confirmed</p>
        <h1 className="ticket-name">{booking.clientName}</h1>
      </div>
      <div className="ticket-perf" aria-hidden="true">
        {Array.from({ length: 24 }).map((_, i) => <span key={i} />)}
      </div>
      <div className="ticket-bottom">
        <div className="ticket-row">
          <span className="ticket-label">Business</span>
          <span className="ticket-value">{business.name}</span>
        </div>
        <div className="ticket-row">
          <span className="ticket-label">Service</span>
          <span className="ticket-value">{booking.service.name}</span>
        </div>
        <div className="ticket-row">
          <span className="ticket-label">Date</span>
          <span className="ticket-value">{dt.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' })}</span>
        </div>
        <div className="ticket-row">
          <span className="ticket-label">Time</span>
          <span className="ticket-value">{dt.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}</span>
        </div>
        <div className="ticket-row">
          <span className="ticket-label">Price</span>
          <span className="ticket-value">K{booking.service.price}</span>
        </div>
      </div>
      <p className="ticket-footer">A confirmation will be sent to your WhatsApp.</p>
    </div>
  );
}
