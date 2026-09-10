import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { i4cLogin } from '../../api';
import Navbar from '../../components/Navbar';

export default function I4CLogin() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await i4cLogin(form);
      login(data);
      toast.success('Welcome, I4C Officer!');
      navigate('/i4c/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Invalid credentials');
    } finally { setLoading(false); }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <Navbar />

      <div className="auth-page" style={{ flex: 1 }}>
        <div className="auth-left" style={{ background: '#1e1b4b' }}>
          <div className="auth-left-content">
            <div className="auth-left-logo">
              <div className="logo-icon" style={{ background: 'linear-gradient(135deg, #3b82f6, #6366f1)' }}>🛡️</div>
              <h1>Durgam</h1>
            </div>
            <h2>
              I4C Command<br />
              <span className="gradient-text" style={{ background: 'linear-gradient(135deg, #60a5fa, #c084fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                Intelligence Hub
              </span>
            </h2>
            <p>
              Centralised intelligence dashboard for I4C officers. Monitor all complaints,
              coordinate bank responses, and analyse transfer chains across India.
            </p>
            <ul className="auth-feature-list">
              <li><span className="feat-icon">📊</span> Real-time fraud analytics</li>
              <li><span className="feat-icon">🗺️</span> Transfer chain visualization</li>
              <li><span className="feat-icon">🏦</span> All-bank coordination</li>
              <li><span className="feat-icon">⚡</span> Predictive intelligence</li>
            </ul>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrap">
            <div className="auth-form-title">I4C Officer Login</div>
            <div className="auth-form-subtitle">Secure access — authorised personnel only</div>

            <div className="alert alert-info" style={{ marginBottom: 20 }}>
              🔐 Default credentials: <strong>i4c@gov.in</strong> / <strong>i4c@2024</strong>
            </div>

            <form onSubmit={handle}>
              <div className="form-group">
                <label className="form-label">Officer Email</label>
                <input className="form-input" type="email" placeholder="officer@i4c.gov.in"
                  value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
              </div>
              <div className="form-group" style={{ marginBottom: 20 }}>
                <label className="form-label">Password</label>
                <input className="form-input" type="password" placeholder="••••••••"
                  value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
              </div>
              <button className="btn-glow" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #3b82f6, #6366f1)' }} type="submit" disabled={loading}>
                {loading ? 'Authenticating...' : '🛡️ Secure Officer Login ✨'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
