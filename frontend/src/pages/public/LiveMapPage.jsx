import Navbar from '../../components/Navbar';
import IndiaMapWidget from '../../components/IndiaMapWidget';

export default function LiveMapPage() {
  return (
    <div className="durgam-landing">
      <Navbar />

      <div style={{ maxWidth: 1280, margin: '0 auto', padding: '40px 24px 80px 24px', width: '100%' }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <div className="hero-pill-badge" style={{ marginBottom: 12 }}>
            <span className="hero-pill-dot" />
            <span>REAL-TIME NATIONAL CYBER GRID</span>
          </div>
          <h1 className="hero-headline" style={{ fontSize: 38, marginBottom: 12 }}>
            Bharat Cyber Crime <span className="gradient-text">Live Intelligence Map</span>
          </h1>
          <p className="hero-description" style={{ maxWidth: 650, margin: '0 auto' }}>
            Interactive state-wise risk heatmaps, city hotspots (Jamtara, Mewat, Delhi NCR, Mumbai), and live inter-state mule transfer chain tracking.
          </p>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div style={{ width: '100%', maxWidth: 780 }}>
            <IndiaMapWidget />
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
