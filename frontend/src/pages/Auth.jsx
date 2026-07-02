import { useState } from 'react';
import { api } from '../api';
import './Auth.css';

export default function Auth({ navigate }) {
  const [mode, setMode] = useState('login'); // login | signup
  const [form, setForm] = useState({ name: '', email: '', password: '', phone: '', serviceType: 'salon' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = mode === 'login'
        ? await api.login({ email: form.email, password: form.password })
        : await api.signup(form);
      localStorage.setItem('token', res.token);
      localStorage.setItem('business', JSON.stringify(res.business));
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <p className="auth-eyebrow">{mode === 'login' ? 'Welcome back' : 'Get set up'}</p>
        <h1>{mode === 'login' ? 'Log in' : 'Create your account'}</h1>

        <form onSubmit={handleSubmit} className="auth-form">
          {mode === 'signup' && (
            <label>
              Business name
              <input required value={form.name} onChange={(e) => update('name', e.target.value)} placeholder="e.g. Beauty Empire Salon" />
            </label>
          )}
          <label>
            Email
            <input type="email" required value={form.email} onChange={(e) => update('email', e.target.value)} />
          </label>
          <label>
            Password
            <input type="password" required value={form.password} onChange={(e) => update('password', e.target.value)} />
          </label>
          {mode === 'signup' && (
            <>
              <label>
                Phone / WhatsApp
                <input value={form.phone} onChange={(e) => update('phone', e.target.value)} placeholder="0977000000" />
              </label>
              <label>
                Business type
                <select value={form.serviceType} onChange={(e) => update('serviceType', e.target.value)}>
                  <option value="salon">Salon</option>
                  <option value="barbershop">Barbershop</option>
                  <option value="spa">Spa</option>
                  <option value="clinic">Clinic</option>
                </select>
              </label>
            </>
          )}
          {error && <p className="form-error">{error}</p>}
          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? 'Please wait…' : mode === 'login' ? 'Log in' : 'Create account'}
          </button>
        </form>

        <button className="auth-switch" onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}>
          {mode === 'login' ? "Don't have an account? Sign up" : 'Already have an account? Log in'}
        </button>
      </div>
    </div>
  );
}
