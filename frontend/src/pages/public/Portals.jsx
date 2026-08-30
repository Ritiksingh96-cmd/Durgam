import { Link } from 'react-router-dom';
import Navbar from '../../components/Navbar';

export default function Portals() {
  const portals = [
    {
      emoji: '👤',
      title: 'Citizen Portal',
      desc: 'Report cyber financial fraud instantly. Track your complaint status and transfer chain investigation in real-time.',
      color: '#6366f1',
      bgColor: 'rgba(99, 102, 241, 0.1)',
      loginPath: '/user/login',
      registerPath: '/user/register',
    },
    {
      emoji: '🏦',
      title: 'Bank Portal',
      desc: 'Receive immediate mule account alerts, upload account holder statements, and initiate emergency fund freezes.',
      color: '#10b981',
      bgColor: 'rgba(16, 185, 129, 0.1)',
      loginPath: '/bank/login',
      registerPath: '/bank/register',
    },
    {
      emoji: '🛡️',
      title: 'I4C Command Center',
      desc: 'National cybercrime intelligence dashboard for monitoring multi-hop transfer chains and coordinating law enforcement.',
      color: '#3b82f6',
      bgColor: 'rgba(59, 130, 246, 0.1)',
      loginPath: '/i4c/login',
      registerPath: null,
    },
  ];

  return (
    <div className="durgam-landing">
      <Navbar />

      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '60px 24px 80px 24px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <div className="hero-pill-badge" style={{ marginBottom: 12 }}>
            <span className="hero-pill-dot" />
            <span>AUTHENTICATION DIRECTORY</span>
          </div>
          <h1 className="hero-headline" style={{ fontSize: 38, marginBottom: 12 }}>
            Access <span className="gradient-text">Durgam Ecosystem Portals</span>
          </h1>
          <p className="hero-description" style={{ maxWidth: 650, margin: '0 auto' }}>
            Select your institution or user role to sign in or register on the Durgam platform.
          </p>
        </div>

        <div className="portals-grid">
          {portals.map((r) => (
            <div key={r.title} className="portal-card" style={{ '--portal-accent': r.color }}>
              <div className="portal-icon" style={{ background: r.bgColor }}>
                {r.emoji}
              </div>
              <h3 className="portal-title">{r.title}</h3>
              <p className="portal-desc">{r.desc}</p>
              <div className="portal-actions">
                <Link to={r.loginPath} className="btn-glow" style={{ background: r.color, fontSize: '14px', padding: '10px 22px' }}>
                  Login
                </Link>
                {r.registerPath && (
                  <Link to={r.registerPath} className="btn-secondary-glass" style={{ fontSize: '14px', padding: '10px 20px' }}>
                    Register
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <footer className="durgam-footer">
        <div className="footer-content">
          <span>© 2024 Durgam Framework · Ministry of Home Affairs, Govt. of India</span>
          <span>Indian Cyber Crime Coordination Centre (I4C)</span>
        </div>
      </footer>
    </div>
  );
}
