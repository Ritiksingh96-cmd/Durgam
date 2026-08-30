import { Link } from 'react-router-dom';
import Navbar from '../../components/Navbar';

export default function About() {
  return (
    <div className="durgam-landing">
      <Navbar />

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px 80px 24px', width: '100%' }}>
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <div className="hero-pill-badge" style={{ marginBottom: 16 }}>
            <span className="hero-pill-dot" />
            <span>INDIAN CYBER CRIME COORDINATION CENTRE (I4C)</span>
          </div>
          <h1 className="hero-headline" style={{ fontSize: 44, marginBottom: 16 }}>
            About the <span className="gradient-text">Durgam Framework</span>
          </h1>
          <p className="hero-description" style={{ maxWidth: 720, margin: '0 auto' }}>
            A proactive national initiative under the Ministry of Home Affairs (MHA) designed to predict cash withdrawal locations, trace recursive mule account networks, and enable rapid fund blocking.
          </p>
        </div>

        {/* Feature Cards Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 24, marginBottom: 60 }}>
          <div className="portal-card" style={{ '--portal-accent': '#6366f1' }}>
            <div className="portal-icon" style={{ background: 'rgba(99,102,241,0.1)' }}>⚡</div>
            <h3 className="portal-title">&lt; 72-Hour Rapid Response</h3>
            <p className="portal-desc">
              Focuses on the critical initial window post-fraud where money is transferred between mule accounts prior to ATM/branch cash withdrawals.
            </p>
          </div>

          <div className="portal-card" style={{ '--portal-accent': '#10b981' }}>
            <div className="portal-icon" style={{ background: 'rgba(16,185,129,0.1)' }}>🔗</div>
            <h3 className="portal-title">Recursive Chain Detection</h3>
            <p className="portal-desc">
              When Account A transfers to B, Bank B is alerted. Once Bank B submits statement data showing transfers to C, Bank C is automatically notified recursively.
            </p>
          </div>

          <div className="portal-card" style={{ '--portal-accent': '#f59e0b' }}>
            <div className="portal-icon" style={{ background: 'rgba(245,158,11,0.1)' }}>🗺️</div>
            <h3 className="portal-title">Predictive Hotspot Mapping</h3>
            <p className="portal-desc">
              Generates intelligence on likely cash withdrawal ATMs and branches for state/local Law Enforcement Agencies (LEAs) to deploy proactive interventions.
            </p>
          </div>
        </div>

        {/* How It Works Flow */}
        <div className="map-glass-card" style={{ maxWidth: '100%', padding: 36, marginBottom: 60 }}>
          <h2 style={{ fontSize: 24, fontWeight: 800, color: '#fff', marginBottom: 24, textAlign: 'center' }}>
            🔄 End-to-End Execution Workflow
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 20 }}>
            <div style={{ background: 'rgba(255,255,255,0.05)', padding: 20, borderRadius: 16, border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>1️⃣</div>
              <div style={{ fontWeight: 700, color: '#fff', fontSize: 15, marginBottom: 6 }}>Complaint Filing</div>
              <div style={{ fontSize: 13, color: '#94a3b8' }}>Victim files complaint with transaction details &amp; suspect account.</div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.05)', padding: 20, borderRadius: 16, border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>2️⃣</div>
              <div style={{ fontWeight: 700, color: '#fff', fontSize: 15, marginBottom: 6 }}>Bank Alerted</div>
              <div style={{ fontSize: 13, color: '#94a3b8' }}>Target Bank receives immediate automated notification via IFSC code matching.</div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.05)', padding: 20, borderRadius: 16, border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>3️⃣</div>
              <div style={{ fontWeight: 700, color: '#fff', fontSize: 15, marginBottom: 6 }}>Data Upload</div>
              <div style={{ fontSize: 13, color: '#94a3b8' }}>Bank uploads account holder info and outgoing transactions.</div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.05)', padding: 20, borderRadius: 16, border: '1px solid rgba(255,255,255,0.1)' }}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>4️⃣</div>
              <div style={{ fontWeight: 700, color: '#fff', fontSize: 15, marginBottom: 6 }}>Chain Expansion</div>
              <div style={{ fontSize: 13, color: '#94a3b8' }}>Durgam algorithm recursively alerts downstream banks (B → C → D).</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div style={{ textAlign: 'center' }}>
          <Link to="/user/login" className="btn-glow" style={{ fontSize: 16, padding: '14px 32px' }}>
            File a Cyber Complaint Now ✨
          </Link>
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
