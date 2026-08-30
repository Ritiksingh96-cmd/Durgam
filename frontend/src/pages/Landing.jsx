import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import IndiaMapWidget from '../components/IndiaMapWidget';

export default function Landing() {
  const roles = [
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
      {/* ── STICKY GLASS NAVBAR ── */}
      <Navbar />

      {/* ── HERO SECTION ── */}
      <section className="hero-section-wrapper">
        <div className="durgam-hero-container">
          {/* Left Column: Headlines & CTA */}
          <div className="hero-left-content">
            <div className="hero-pill-badge">
              <span className="hero-pill-dot" />
              <span>OFFICIAL I4C CYBER CRIME MITIGATION FRAMEWORK</span>
            </div>

            <h1 className="hero-headline">
              Proactive Cyber Crime Mitigation &amp;{' '}
              <span className="gradient-text">Mule Account Tracking.</span>
            </h1>

            <p className="hero-description">
              Durgam enables real-time intelligence sharing between Law Enforcement Agencies (LEAs),
              Banks, and Financial Institutions to predict cash withdrawal locations, trace recursive
              money transfer chains, and execute rapid fund blocking across India.
            </p>

            <div className="hero-actions-row">
              <Link to="/user/login" className="btn-glow">
                File a Complaint ✨
              </Link>
              <Link to="/i4c/login" className="btn-secondary-glass">
                Explore I4C Dashboard →
              </Link>
            </div>

            {/* Key Metrics Row */}
            <div className="hero-key-metrics">
              <div className="metric-item">
                <span className="metric-number">&lt; 72 hrs</span>
                <span className="metric-label">Fast Scam Window</span>
              </div>
              <div className="metric-item">
                <span className="metric-number">Automated</span>
                <span className="metric-label">Bank Alerts</span>
              </div>
              <div className="metric-item">
                <span className="metric-number">Recursive</span>
                <span className="metric-label">Chain Detection</span>
              </div>
            </div>
          </div>

          {/* Right Column: 3D Master India Map Glass Card */}
          <div className="hero-map-wrapper" id="grid">
            <IndiaMapWidget />
          </div>
        </div>
      </section>

      {/* ── LIVE STATS TICKER STRIP ── */}
      <section className="stats-ticker-strip">
        <div className="ticker-grid">
          <div className="ticker-box">
            <span className="ticker-val" style={{ color: '#6366f1' }}>12,480+</span>
            <span className="ticker-lbl">Complaints Managed</span>
          </div>
          <div className="ticker-box">
            <span className="ticker-val" style={{ color: '#10b981' }}>₹48.2 Cr</span>
            <span className="ticker-lbl">Fraudulent Funds Blocked</span>
          </div>
          <div className="ticker-box">
            <span className="ticker-val" style={{ color: '#f59e0b' }}>1,840+</span>
            <span className="ticker-lbl">Mule Chains Identified</span>
          </div>
          <div className="ticker-box">
            <span className="ticker-val" style={{ color: '#3b82f6' }}>140+</span>
            <span className="ticker-lbl">Banks &amp; FIs Onboarded</span>
          </div>
        </div>
      </section>

      {/* ── PORTALS SELECTION ── */}
      <section className="portals-section" id="portals">
        <div className="section-header">
          <h2>Choose Your Access Portal</h2>
          <p>Unified ecosystem connecting citizens, banking institutions, and law enforcement agencies.</p>
        </div>

        <div className="portals-grid">
          {roles.map((r) => (
            <div
              key={r.title}
              className="portal-card"
              style={{ '--portal-accent': r.color }}
            >
              <div className="portal-icon" style={{ background: r.bgColor }}>
                {r.emoji}
              </div>
              <h3 className="portal-title">{r.title}</h3>
              <p className="portal-desc">{r.desc}</p>
              <div className="portal-actions">
                <Link
                  to={r.loginPath}
                  className="btn-glow"
                  style={{ background: r.color, fontSize: '13.5px', padding: '9px 20px' }}
                >
                  Login
                </Link>
                {r.registerPath && (
                  <Link to={r.registerPath} className="btn-secondary-glass" style={{ fontSize: '13.5px', padding: '9px 18px' }}>
                    Register
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="durgam-footer">
        <div className="footer-content">
          <span>© 2024 Durgam Framework · Ministry of Home Affairs, Govt. of India</span>
          <span>Indian Cyber Crime Coordination Centre (I4C)</span>
        </div>
      </footer>
    </div>
  );
}
