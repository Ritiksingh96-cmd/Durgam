import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { bankLogin } from '../../api';
import Navbar from '../../components/Navbar';

export default function BankLogin() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await bankLogin(form);
      login(data);
      toast.success(`Welcome, ${data.bank_name}!`);
      navigate('/bank/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Login failed');
    } finally { setLoading(false); }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <Navbar />

      <div className="auth-page" style={{ flex: 1 }}>
        <div className="auth-left" style={{ background: '#064e3b' }}>
          <div className="auth-left-content">
            <div className="auth-left-logo">
              <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #059669, #10b981)' }}>🏦</div>
              <h1>Durgam</h1>
            </div>
            <h2>
              Bank Intelligence<br />
              <span className="gradient-text" style={{ background: 'linear-gradient(135deg, #34d399, #60a5fa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                Command Center
              </span>
            </h2>
            <p>
              Receive real-time mule account alerts, submit account holder data,
              and track transfer chains to help stop financial cybercrime.
            </p>
            <ul className="auth-feature-list">
              <li><span className="feat-icon">🔔</span> Mule account notifications</li>
              <li><span className="feat-icon">📤</span> Upload bank statements</li>
              <li><span className="feat-icon">🔗</span> Transfer chain tracking</li>
              <li><span className="feat-icon">🤝</span> I4C data sharing</li>
            </ul>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrap">
            <div className="auth-form-title">Bank Portal Sign In</div>
            <div className="auth-form-subtitle">Secure access for banks &amp; financial institutions</div>

            <form onSubmit={handle}>
              <div className="form-group">
                <label className="form-label">Bank Official Email</label>
                <input className="form-input" type="email" placeholder="fraud@yourbank.in"
                  value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
              </div>
              <div className="form-group" style={{ marginBottom: 20 }}>
                <label className="form-label">Password</label>
                <input className="form-input" type="password" placeholder="••••••••"
                  value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
              </div>
              <button className="btn-glow" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #059669, #10b981)' }} type="submit" disabled={loading}>
                {loading ? 'Authenticating...' : 'Sign In as Bank ✨'}
              </button>
            </form>

            <div className="auth-switch">
              New bank? <Link to="/bank/register" style={{ color: '#059669', fontWeight: 700 }}>Register your institution</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
