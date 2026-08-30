import Navbar from '../../components/Navbar';

export default function Resources() {
  const resources = [
    { icon: '📞', title: 'National Cyber Helpline 1930', desc: 'Direct toll-free helpline operating 24x7 for immediate financial cyber fraud reporting.' },
    { icon: '📄', title: 'Citizen Financial Fraud SOP', desc: 'Standard Operating Procedures for victims to freeze funds within the golden hour.' },
    { icon: '🏛️', title: 'RBI & FI Regulatory Directives', desc: 'Mandatory guidelines for banks regarding mule account monitoring and fast fund blocking.' },
    { icon: '🛡️', title: 'I4C Prevention Playbook', desc: 'Best practices for state LEAs to deploy proactive teams at high-risk ATM hotspots.' },
  ];

  return (
    <div className="durgam-landing">
      <Navbar />

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '60px 24px 80px 24px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 50 }}>
          <div className="hero-pill-badge" style={{ marginBottom: 12 }}>
            <span className="hero-pill-dot" />
            <span>KNOWLEDGE &amp; GUIDELINES HUB</span>
          </div>
          <h1 className="hero-headline" style={{ fontSize: 38, marginBottom: 12 }}>
            Resources &amp; <span className="gradient-text">Cyber Awareness</span>
          </h1>
          <p className="hero-description" style={{ maxWidth: 650, margin: '0 auto' }}>
            Official documentation, regulatory guidelines, and standard operating procedures for citizens, banks, and law enforcement agencies.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 24 }}>
          {resources.map((res, i) => (
            <div key={i} className="portal-card" style={{ '--portal-accent': '#6366f1' }}>
              <div className="portal-icon" style={{ background: 'rgba(99,102,241,0.1)' }}>{res.icon}</div>
              <h3 className="portal-title">{res.title}</h3>
              <p className="portal-desc">{res.desc}</p>
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
