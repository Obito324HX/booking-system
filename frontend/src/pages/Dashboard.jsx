import { useState, useEffect } from 'react';
import { api } from '../api';
import './Dashboard.css';

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export default function Dashboard({ navigate }) {
  const [tab, setTab] = useState('bookings');
  const business = JSON.parse(localStorage.getItem('business') || 'null');

  if (!business) {
    navigate('/login');
    return null;
  }

  function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('business');
    navigate('/login');
  }

  const bookingUrl = `${window.location.origin}/book/${business.slug}`;

  return (
    <div className="dash">
      <header className="dash-header">
        <div>
          <p className="dash-eyebrow">Dashboard</p>
          <h1>{business.name}</h1>
        </div>
        <button className="btn-ghost" onClick={logout}>Log out</button>
      </header>

      <div className="dash-link-bar">
        <span className="dash-link-label">Your booking page</span>
        <a href={bookingUrl} target="_blank" rel="noreferrer" className="dash-link">{bookingUrl}</a>
        <button className="copy-btn" onClick={() => navigator.clipboard.writeText(bookingUrl)}>Copy</button>
      </div>

      <nav className="dash-tabs">
        {['bookings', 'services', 'availability'].map((t) => (
          <button key={t} className={`dash-tab ${tab === t ? 'active' : ''}`} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </nav>

      {tab === 'bookings' && <BookingsTab />}
      {tab === 'services' && <ServicesTab />}
      {tab === 'availability' && <AvailabilityTab />}
    </div>
  );
}

function BookingsTab() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);

  function load() {
    api.listBookings().then(setBookings).finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function setStatus(id, status) {
    await api.updateBooking(id, { status });
    load();
  }

  if (loading) return <p className="dash-empty">Loading…</p>;
  if (!bookings.length) return <p className="dash-empty">No bookings yet. Share your booking link to get your first one.</p>;

  return (
    <div className="booking-list">
      {bookings.map((b) => (
        <div key={b.id} className={`booking-row status-${b.status}`}>
          <div className="booking-row-main">
            <span className="booking-client">{b.clientName}</span>
            <span className="booking-service">{b.service.name}</span>
            <span className="booking-time">{new Date(b.bookingTime).toLocaleString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}</span>
          </div>
          <div className="booking-row-actions">
            <span className={`status-badge status-${b.status}`}>{b.status.replace('_', ' ')}</span>
            {b.status === 'confirmed' && (
              <>
                <button onClick={() => setStatus(b.id, 'completed')}>Mark done</button>
                <button onClick={() => setStatus(b.id, 'no_show')}>No-show</button>
                <button className="danger" onClick={() => setStatus(b.id, 'cancelled')}>Cancel</button>
              </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

function ServicesTab() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ name: '', durationMinutes: 30, price: '' });
  const [error, setError] = useState(null);

  function load() {
    api.myServices().then(setServices).finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function addService(e) {
    e.preventDefault();
    setError(null);
    try {
      await api.createService({ ...form, price: Number(form.price), durationMinutes: Number(form.durationMinutes) });
      setForm({ name: '', durationMinutes: 30, price: '' });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeService(id) {
    await api.deleteService(id);
    load();
  }

  return (
    <div>
      <form className="inline-form" onSubmit={addService}>
        <input placeholder="Service name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input type="number" placeholder="Minutes" value={form.durationMinutes} onChange={(e) => setForm({ ...form, durationMinutes: e.target.value })} required />
        <input type="number" placeholder="Price (K)" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required />
        <button className="btn-primary" type="submit">Add service</button>
      </form>
      {error && <p className="form-error">{error}</p>}

      {loading ? (
        <p className="dash-empty">Loading…</p>
      ) : !services.length ? (
        <p className="dash-empty">No services yet — add your first one above.</p>
      ) : (
        <div className="service-manage-list">
          {services.map((s) => (
            <div key={s.id} className="service-manage-row">
              <span>{s.name}</span>
              <span className="muted">{s.durationMinutes} min</span>
              <span className="muted">K{s.price}</span>
              <button className="danger" onClick={() => removeService(s.id)}>Remove</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function AvailabilityTab() {
  const [windows, setWindows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ dayOfWeek: 0, startTime: '09:00', endTime: '17:00' });
  const [error, setError] = useState(null);

  function load() {
    api.listAvailability().then(setWindows).finally(() => setLoading(false));
  }

  useEffect(load, []);

  async function addWindow(e) {
    e.preventDefault();
    setError(null);
    try {
      await api.setAvailability({ ...form, dayOfWeek: Number(form.dayOfWeek) });
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <form className="inline-form" onSubmit={addWindow}>
        <select value={form.dayOfWeek} onChange={(e) => setForm({ ...form, dayOfWeek: e.target.value })}>
          {DAYS.map((d, i) => <option key={d} value={i}>{d}</option>)}
        </select>
        <input type="time" value={form.startTime} onChange={(e) => setForm({ ...form, startTime: e.target.value })} />
        <input type="time" value={form.endTime} onChange={(e) => setForm({ ...form, endTime: e.target.value })} />
        <button className="btn-primary" type="submit">Add hours</button>
      </form>
      {error && <p className="form-error">{error}</p>}

      {loading ? (
        <p className="dash-empty">Loading…</p>
      ) : !windows.length ? (
        <p className="dash-empty">No working hours set yet — clients can't book until you add some.</p>
      ) : (
        <div className="service-manage-list">
          {windows.map((w) => (
            <div key={w.id} className="service-manage-row">
              <span>{DAYS[w.dayOfWeek]}</span>
              <span className="muted">{w.startTime} – {w.endTime}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
