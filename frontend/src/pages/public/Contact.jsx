import Navbar from '../../components/Navbar';

export default function Contact() {
  return (
    <div className="durgam-landing">
      <Navbar />

      <div style={{ maxWidth: 1000, margin: '0 auto', padding: '60px 24px 80px 24px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <div className="hero-pill-badge" style={{ marginBottom: 12 }}>
            <span className="hero-pill-dot" />
            <span>OFFICIAL CONTACT DESK</span>
          </div>
          <h1 className="hero-headline" style={{ fontSize: 38, marginBottom: 12 }}>
            Contact <span className="gradient-text">I4C Support &amp; Escalation</span>
          </h1>
          <p className="hero-description" style={{ maxWidth: 600, margin: '0 auto' }}>
            Reach out to the Indian Cyber Crime Coordination Centre (I4C), Ministry of Home Affairs, for assistance or escalation.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
          <div className="portal-card" style={{ '--portal-accent': '#6366f1' }}>
            <h3 className="portal-title">🏛️ Headquarters</h3>
            <p style={{ fontSize: 14, color: '#475569', lineHeight: 1.7, marginBottom: 16 }}>
              Indian Cyber Crime Coordination Centre (I4C)<br />
              Cyber &amp; Information Security (CIS) Division<br />
              Ministry of Home Affairs, Government of India<br />
              New Delhi – 110001
            </p>
            <div style={{ fontSize: 14, color: '#0f172a', fontWeight: 600 }}>
              📞 Helpline: 1930 (Toll-Free)<br />
              ✉️ Email: support@i4c.gov.in
            </div>
          </div>

          <div className="portal-card" style={{ '--portal-accent': '#10b981' }}>
            <h3 className="portal-title">⚡ Bank &amp; FI Nodal Desk</h3>
            <p style={{ fontSize: 14, color: '#475569', lineHeight: 1.7, marginBottom: 16 }}>
              Dedicated technical integration and escalation desk for banks, payment gateways, and financial institutions onboarded to Durgam.
            </p>
            <div style={{ fontSize: 14, color: '#0f172a', fontWeight: 600 }}>
              🌐 Portal Support: bank-desk@i4c.gov.in<br />
              ⏰ Hours: 24 x 7 Operations
            </div>
          </div>
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
