import { useEffect, useState } from 'react';
import './IndiaMap.css';

// Key Cyber Crime Hotspots Overlaid on Map Image
const HOTSPOTS = [
  { id: 'delhi', name: 'Delhi NCR', top: '28%', left: '44%', hub: true },
  { id: 'jamtara', name: 'Jamtara (JH)', top: '42%', left: '68%', hub: true },
  { id: 'mewat', name: 'Mewat (RJ)', top: '34%', left: '38%', hub: true },
  { id: 'mumbai', name: 'Mumbai (MH)', top: '56%', left: '30%', hub: false },
  { id: 'bengaluru', name: 'Bengaluru (KA)', top: '76%', left: '42%', hub: false },
];

const CHAINS = [
  { from: 'Jamtara', to: 'Delhi NCR', amount: '₹42.5L' },
  { from: 'Mewat', to: 'Mumbai', amount: '₹88.2L' },
  { from: 'Delhi NCR', to: 'Bengaluru', amount: '₹34.0L' },
];

export default function IndiaMapWidget() {
  const [activeChain, setActiveChain] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveChain((prev) => (prev + 1) % CHAINS.length);
    }, 2500);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="india-pure-map-container">
      {/* Pure India Map Image (100% Transparent background PNG, no card box, no dark borders) */}
      <div className="map-pure-wrapper">
        <img
          src="/india_transparent_map.png"
          alt="Bharat India State Map"
          className="pure-india-img"
        />

        {/* Hotspot Markers */}
        {HOTSPOTS.map((city) => (
          <div
            key={city.id}
            className={`map-pure-hotspot ${city.hub ? 'hub' : ''}`}
            style={{ top: city.top, left: city.left }}
          >
            <div className="hotspot-dot" />
            {city.hub && <div className="hotspot-pulse" />}
            <span className="hotspot-tag">{city.name}</span>
          </div>
        ))}
      </div>

      {/* Floating Transfer Ticker Pill */}
      <div className="pure-map-ticker">
        <span className="ticker-pulse-dot" />
        <span className="ticker-text">
          ⚡ <strong>{CHAINS[activeChain].from}</strong> → <strong>{CHAINS[activeChain].to}</strong>
        </span>
        <span className="ticker-amount">{CHAINS[activeChain].amount}</span>
      </div>
    </div>
  );
}
