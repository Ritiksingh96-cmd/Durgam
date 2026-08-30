import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  const path = location.pathname;

  return (
    <nav className="durgam-nav">
      <Link to="/" className="durgam-logo">
        <div className="durgam-logo-icon">🛡️</div>
        <span className="durgam-logo-text">DURGAM</span>
        <span className="durgam-logo-tag">I4C MHA</span>
      </Link>

      <ul className="durgam-nav-links">
        <li>
          <Link to="/about" className={path === '/about' ? 'active-link' : ''}>
            About Framework
          </Link>
        </li>
        <li>
          <Link to="/live-map" className={path === '/live-map' ? 'active-link' : ''}>
            Live Map
          </Link>
        </li>
        <li>
          <Link to="/portals" className={path === '/portals' ? 'active-link' : ''}>
            Portals
          </Link>
        </li>
        <li>
          <Link to="/resources" className={path === '/resources' ? 'active-link' : ''}>
            Resources
          </Link>
        </li>
        <li>
          <Link to="/contact" className={path === '/contact' ? 'active-link' : ''}>
            Contact Desk
          </Link>
        </li>
      </ul>

      <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
        <Link to="/user/login" className="btn-glow">
          File a Complaint ✨
        </Link>
      </div>
    </nav>
  );
}
