import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { userLogin } from '../../api';
import Navbar from '../../components/Navbar';

export default function UserLogin() {
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await userLogin(form);
      login(data);
      toast.success(`Welcome back, ${data.name}!`);
      navigate('/user/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Login failed');
    } finally { setLoading(false); }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: '#f8fafc' }}>
      <Navbar />

      <div className="auth-page" style={{ flex: 1 }}>
        {/* Left Panel */}
        <div className="auth-left">
          <div className="auth-left-content">
            <div className="auth-left-logo">
              <div className="logo-icon">🛡️</div>
              <h1>Durgam</h1>
            </div>
            <h2>
              Report fraud.<br />
              <span className="gradient-text">Track justice.</span>
            </h2>
            <p>
              File a cyber fraud complaint in minutes and track its progress in real-time.
              Every complaint triggers automated mule account detection.
            </p>
            <ul className="auth-feature-list">
              <li><span className="feat-icon">📋</span> File a complaint instantly</li>
              <li><span className="feat-icon">🔢</span> Get a unique complaint number</li>
              <li><span className="feat-icon">🔍</span> Track investigation status</li>
              <li><span className="feat-icon">🔗</span> See transfer chain detection</li>
            </ul>
          </div>
        </div>

        {/* Right Panel */}
        <div className="auth-right">
          <div className="auth-form-wrap">
            <div className="auth-form-title">Citizen Sign In</div>
            <div className="auth-form-subtitle">Enter your details to access your account</div>

            <form onSubmit={handle}>
              <div className="form-group">
                <label className="form-label">Email Address</label>
                <input className="form-input" type="email" placeholder="you@example.com"
                  value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
              </div>
              <div className="form-group" style={{ marginBottom: 20 }}>
                <label className="form-label">Password</label>
                <input className="form-input" type="password" placeholder="••••••••"
                  value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
              </div>
              <button className="btn-glow" style={{ width: '100%', justifyContent: 'center' }} type="submit" disabled={loading}>
                {loading ? 'Signing in...' : 'Sign In to Citizen Portal ✨'}
              </button>
            </form>

            <div className="auth-switch">
              Don't have an account? <Link to="/user/register" style={{ color: 'var(--primary)', fontWeight: 700 }}>Register here</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
