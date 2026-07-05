import { useState, useEffect } from 'react';
import { api } from '../api';
import { Ticket } from './BookingPage';
import './BookingPage.css';

const METHODS = [
  { id: 'card', label: 'Visa / Mastercard' },
  { id: 'airtel', label: 'Airtel Money' },
  { id: 'mtn', label: 'MTN Mobile Money' },
  { id: 'zamtel', label: 'Zamtel Kwacha' },
];

export default function BookingDemoPay() {
  const [business, setBusiness] = useState(null);
  const [booking, setBooking] = useState(null);
  const [method, setMethod] = useState('card');
  const [loading, setLoading] = useState(true);
  const [paying, setPaying] = useState(false);
  const [error, setError] = useState(null);
  const [paid, setPaid] = useState(false);

  // path shape: /book/:slug/pay/:bookingId
  const parts = window.location.pathname.split('/');
  const slug = parts[2];
  const bookingId = parts[4];

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const [biz, bk] = await Promise.all([
          api.getBusiness(slug),
          api.getBookingPublic(bookingId),
        ]);
        if (cancelled) return;
        setBusiness(biz);
        setBooking(bk);
        if (bk.paymentStatus === 'paid') setPaid(true);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    load();
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handlePay() {
    setPaying(true);
    setError(null);
    try {
      const result = await api.demoPay(bookingId);
      setBooking(result);
      setPaid(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setPaying(false);
    }
  }

  if (loading) return <div className="booking-status">Loading…</div>;
  if (error && !booking) return <div className="booking-status">{error}</div>;

  if (paid) {
    return (
      <div className="booking-page">
        <Ticket business={business} booking={booking} />
      </div>
    );
  }

  return (
    <div className="booking-page">
      <div className="demo-payment-card">
        <p className="demo-banner">
          Demo payment — no real charge. Real card / mobile money processing activates
          once the business's payment provider account is fully registered.
        </p>
        <h2>Pay K{booking.depositAmount} deposit</h2>
        <p className="demo-summary">
          {booking.service?.name} · {new Date(booking.bookingTime).toLocaleString()}
        </p>

        <div className="payment-methods">
          {METHODS.map((m) => (
            <label key={m.id} className={`payment-method ${method === m.id ? 'selected' : ''}`}>
              <input
                type="radio"
                name="method"
                value={m.id}
                checked={method === m.id}
                onChange={() => setMethod(m.id)}
              />
              {m.label}
            </label>
          ))}
        </div>

        {error && <p className="form-error">{error}</p>}
        <button className="btn-primary" onClick={handlePay} disabled={paying}>
          {paying ? 'Processing…' : `Pay K${booking.depositAmount} now`}
        </button>
      </div>
    </div>
  );
}
