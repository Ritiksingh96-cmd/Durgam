import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { bankRegister } from '../../api';
import Navbar from '../../components/Navbar';

export default function BankRegister() {
  const [form, setForm] = useState({ bank_name: '', ifsc_prefix: '', email: '', password: '', contact_number: '' });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handle = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await bankRegister(form);
      login(data);
      toast.success('Bank registered successfully!');
      navigate('/bank/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed');
    } finally { setLoading(false); }
  };

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

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
              Register your<br />
              <span className="gradient-text" style={{ background: 'linear-gradient(135deg, #34d399, #60a5fa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                institution.
              </span>
            </h2>
            <p>
              Connect your bank to the Durgam platform to receive mule account alerts
              and participate in the national cyber fraud coordination network.
            </p>
            <ul className="auth-feature-list">
              <li><span className="feat-icon">🏛️</span> Official bank onboarding</li>
              <li><span className="feat-icon">🔐</span> IFSC-based account matching</li>
              <li><span className="feat-icon">📊</span> Real-time alert dashboard</li>
            </ul>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrap" style={{ maxWidth: 440 }}>
            <div className="auth-form-title">Register Institution</div>
            <div className="auth-form-subtitle">Onboard your bank or financial institution</div>

            <form onSubmit={handle}>
              <div className="form-group">
                <label className="form-label">Bank Name *</label>
                <input className="form-input" placeholder="e.g. State Bank of India" value={form.bank_name} onChange={set('bank_name')} required />
              </div>
              <div className="form-grid-2">
                <div className="form-group">
                  <label className="form-label">IFSC Prefix (4 chars) *</label>
                  <input className="form-input" placeholder="e.g. SBIN" maxLength={4}
                    value={form.ifsc_prefix} onChange={set('ifsc_prefix')} required
                    style={{ textTransform: 'uppercase', fontFamily: 'monospace' }} />
                </div>
                <div className="form-group">
                  <label className="form-label">Contact Number *</label>
                  <input className="form-input" placeholder="1800XXXXXX" value={form.contact_number} onChange={set('contact_number')} required />
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Official Email *</label>
                <input className="form-input" type="email" placeholder="fraud@bank.in" value={form.email} onChange={set('email')} required />
              </div>
              <div className="form-group" style={{ marginBottom: 12 }}>
                <label className="form-label">Password *</label>
                <input className="form-input" type="password" placeholder="Min. 6 characters" value={form.password} onChange={set('password')} required minLength={6} />
              </div>
              <div className="alert alert-info" style={{ marginBottom: 16, fontSize: 12 }}>
                ℹ️ IFSC prefix = first 4 chars of your IFSC code (e.g. SBI → SBIN, HDFC → HDFC)
              </div>
              <button className="btn-glow" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, #059669, #10b981)' }} type="submit" disabled={loading}>
                {loading ? 'Registering...' : 'Register Institution ✨'}
              </button>
            </form>

            <div className="auth-switch">
              Already registered? <Link to="/bank/login" style={{ color: '#059669', fontWeight: 700 }}>Login here</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
