import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { userRegister } from '../../api';
import Navbar from '../../components/Navbar';

export default function UserRegister() {
  const [form, setForm] = useState({ name: '', email: '', mobile: '', address: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await userRegister(form);
      login(data);
      toast.success('Account created! Welcome to Durgam.');
      navigate('/user/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    } finally { setLoading(false); }
  };

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <Navbar />

      <div className="auth-page" style={{ flex: 1 }}>
        <div className="auth-left">
          <div className="auth-left-content">
            <div className="auth-left-logo">
              <div className="logo-icon">🛡️</div>
              <h1>Durgam</h1>
            </div>
            <h2>
              Join the<br />
              <span className="gradient-text">fight against fraud.</span>
            </h2>
            <p>
              Register as a citizen on the Durgam platform. Your complaints help law enforcement
              detect mule accounts and stop the flow of fraudulent money.
            </p>
            <ul className="auth-feature-list">
              <li><span className="feat-icon">🔒</span> Secure &amp; private by design</li>
              <li><span className="feat-icon">⚡</span> Instant complaint filing</li>
              <li><span className="feat-icon">📡</span> Real-time I4C coordination</li>
              <li><span className="feat-icon">🏦</span> Direct bank notification</li>
            </ul>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrap" style={{ maxWidth: 440 }}>
            <div className="auth-form-title">Create Citizen Account</div>
            <div className="auth-form-subtitle">Register to file and track cybercrime complaints</div>

            <form onSubmit={handle}>
              <div className="form-grid-2">
                <div className="form-group">
                  <label className="form-label">Full Name *</label>
                  <input className="form-input" placeholder="Rahul Sharma" value={form.name} onChange={set('name')} required />
                </div>
                <div className="form-group">
                  <label className="form-label">Mobile Number *</label>
                  <input className="form-input" placeholder="98XXXXXXXX" value={form.mobile} onChange={set('mobile')} required />
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Email Address *</label>
                <input className="form-input" type="email" placeholder="you@example.com" value={form.email} onChange={set('email')} required />
              </div>
              <div className="form-group">
                <label className="form-label">Address *</label>
                <input className="form-input" placeholder="123 Street, City, State" value={form.address} onChange={set('address')} required />
              </div>
              <div className="form-group" style={{ marginBottom: 20 }}>
                <label className="form-label">Password *</label>
                <input className="form-input" type="password" placeholder="Min. 6 characters" value={form.password} onChange={set('password')} required minLength={6} />
              </div>
              <button className="btn-glow" style={{ width: '100%', justifyContent: 'center' }} type="submit" disabled={loading}>
                {loading ? 'Creating account...' : 'Create Account ✨'}
              </button>
            </form>

            <div className="auth-switch">
              Already have an account? <Link to="/user/login" style={{ color: 'var(--primary)', fontWeight: 700 }}>Sign in</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
