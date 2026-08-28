function updateGlobalGovClock() {
  const now = new Date();
  const ist = new Date(now.toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }));
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  const dayName = days[ist.getDay()];
  const dateNum = ist.getDate();
  const monthName = months[ist.getMonth()];
  const year = ist.getFullYear();

  const h = String(ist.getHours()).padStart(2, '0');
  const m = String(ist.getMinutes()).padStart(2, '0');
  const s = String(ist.getSeconds()).padStart(2, '0');
  
  const clockText = `${dayName}, ${dateNum} ${monthName} ${year} • IST ${h}:${m}:${s}`;
  
  document.querySelectorAll('.ist-date-clock, #ist-date-clock, #ist-clock').forEach(el => {
    el.textContent = clockText;
  });
}
setInterval(updateGlobalGovClock, 1000);
document.addEventListener('DOMContentLoaded', updateGlobalGovClock);

// Role-Based Access Control (RBAC) Department Isolation & Enforcement
function enforceDepartmentAccess(allowedRoles = []) {
  if (!allowedRoles || allowedRoles.length === 0) return;
  
  const rawSession = sessionStorage.getItem('durgam_auth_session');
  const session = rawSession ? JSON.parse(rawSession) : null;
  
  const currentDept = session?.department || session?.role || 'PUBLIC';
  const isSuperAdmin = currentDept === 'SUPER_ADMIN' || currentDept === 'ADMIN' || currentDept === 'ROOT' || session?.role === 'ADMIN';
  
  // Department Home Mapping for Isolation Protection
  const deptHomePortals = {
    'POLICE_CAD': '/static/police.html',
    'POLICE_NATIONAL': '/static/police.html',
    'BANK_NODAL': '/static/bank.html',
    'TELECOM_CEIR': '/static/telecom.html',
    'TELECOM_DOT': '/static/telecom.html',
    'FIU_AML': '/static/fiu.html',
    'FIU_OFFICER': '/static/fiu.html',
    'JUDICIAL_MAGISTRATE': '/static/judiciary.html',
    'JUDICIARY': '/static/judiciary.html',
    'ADMIN': '/static/admin.html',
    'SUPER_ADMIN': '/static/admin.html'
  };

  // Normalize match check
  const hasAccess = isSuperAdmin || allowedRoles.some(r => r === currentDept || r.toLowerCase() === currentDept.toLowerCase());
  
  if (!hasAccess) {
    console.warn(`[Department Isolation Barrier] Role '${currentDept}' not permitted for [${allowedRoles.join(', ')}]`);
    const existing = document.getElementById('durgam-rbac-modal');
    if (existing) existing.remove();

    const assignedPortal = deptHomePortals[currentDept] || '/static/index.html';
    const assignedLabel = currentDept.replace('_', ' ');

    const modal = document.createElement('div');
    modal.id = 'durgam-rbac-modal';
    modal.style.position = 'fixed';
    modal.style.inset = '0';
    modal.style.background = 'rgba(8, 21, 36, 0.88)';
    modal.style.backdropFilter = 'blur(8px)';
    modal.style.zIndex = '99999';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.style.padding = '20px';
    modal.innerHTML = `
      <div style="background:#FFFFFF; border:1px solid #D8D1C0; border-top:4px solid #9A3324; border-radius:3px; max-width:520px; width:100%; padding:28px; box-shadow:0 20px 40px rgba(0,0,0,0.3); font-family:'Inter', sans-serif;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
          <img src="/static/images/official_state_emblem.png" alt="Emblem" style="width:28px; height:34px; object-fit:contain;" />
          <div>
            <div style="font-family:'Fraunces', serif; font-size:1.15rem; font-weight:700; color:#0E2340;">Departmental Isolation Barrier</div>
            <div style="font-size:11px; font-family:'IBM Plex Mono', monospace; color:#9A3324; font-weight:700;">ZERO-TRUST DEPARTMENT CLEARANCE REQUIRED</div>
          </div>
        </div>
        <p style="font-size:13.5px; color:#4B5563; line-height:1.6; margin-bottom:16px;">
          Your current session is cleared for <strong>${assignedLabel}</strong>. Cross-departmental access to <strong>${allowedRoles.join(' / ')}</strong> is isolated under Sovereign Cyber Command Zero-Trust directives.
        </p>
        <div style="background:#F6F3EC; border:1px solid #D8D1C0; padding:12px 14px; border-radius:2px; font-family:'IBM Plex Mono', monospace; font-size:11.5px; color:#0E2340; margin-bottom:20px;">
          • Active Officer: ${session?.full_name || 'Unauthenticated User'}<br>
          • Clearance Group: ${currentDept}<br>
          • Isolation Status: ENFORCED (Access Blocked)
        </div>
        <div style="display:flex; gap:10px;">
          ${currentDept !== 'PUBLIC' ? `
            <a href="${assignedPortal}" class="btn btn-primary" style="flex:1; justify-content:center; padding:10px; font-size:12.5px; text-decoration:none; display:flex; align-items:center; background:#0E2340; color:#FFF;">
              Return to My War Room (${assignedLabel})
            </a>
          ` : ''}
          <button onclick="openJanParichayModal()" class="btn btn-alert" style="flex:1; justify-content:center; padding:10px; font-size:12.5px; cursor:pointer; background:#9A3324; color:#FFF; border:none; border-radius:3px;">
            Switch Department SSO
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  }
}

// JanParichay Sovereign Departmental Login Modal
function openJanParichayModal() {
  const existing = document.getElementById('durgam-sso-modal');
  if (existing) existing.remove();

  const rbacExisting = document.getElementById('durgam-rbac-modal');
  if (rbacExisting) rbacExisting.remove();

  const modal = document.createElement('div');
  modal.id = 'durgam-sso-modal';
  modal.style.position = 'fixed';
  modal.style.inset = '0';
  modal.style.background = 'rgba(8, 21, 36, 0.88)';
  modal.style.backdropFilter = 'blur(8px)';
  modal.style.zIndex = '99999';
  modal.style.display = 'flex';
  modal.style.alignItems = 'center';
  modal.style.justifyContent = 'center';
  modal.style.padding = '20px';
  modal.innerHTML = `
    <div style="background:#FFFFFF; border:1px solid #D8D1C0; border-top:4px solid #C1652B; border-radius:3px; max-width:680px; width:100%; padding:28px; box-shadow:0 24px 50px rgba(0,0,0,0.35); font-family:'Inter', sans-serif; max-height:90vh; overflow-y:auto;">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:18px;">
        <div style="display:flex; align-items:center; gap:12px;">
          <img src="/static/images/official_state_emblem.png" alt="Emblem" style="width:30px; height:36px; object-fit:contain;" />
          <div>
            <div style="font-family:'Fraunces', serif; font-size:1.25rem; font-weight:700; color:#0E2340;">JanParichay Sovereign SSO Gateway</div>
            <div style="font-size:11px; font-family:'IBM Plex Mono', monospace; color:#C1652B; font-weight:700;">SELECT AUTHORIZED DEPARTMENTAL WAR ROOM</div>
          </div>
        </div>
        <button onclick="document.getElementById('durgam-sso-modal').remove()" style="background:transparent; border:none; font-size:20px; color:#7E90A6; cursor:pointer;">✕</button>
      </div>

      <p style="font-size:13px; color:#4B5563; line-height:1.5; margin-bottom:18px;">
        Authentication grants isolated clearance strictly to your designated departmental portal. Cross-department access requires dual MHA re-authorization.
      </p>

      <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:12px; margin-bottom:20px;">
        
        <div onclick="selectDepartmentPersona('POLICE_CAD', 'Dr. Vikram Rao, IPS', 'sp_delhi_cyber', '/static/police.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #0E2340; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#0E2340; font-weight:700;">POLICE CAD & ERSS-112</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Dr. Vikram Rao, IPS</div>
          <div style="font-size:11px; color:#7E90A6;">vikram.rao@police.gov.in</div>
        </div>

        <div onclick="selectDepartmentPersona('BANK_NODAL', 'Pooja Verma, Chief Nodal', 'sbi_nodal_officer', '/static/bank.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #C1652B; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#C1652B; font-weight:700;">BANKING FRM SWITCH</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Pooja Verma (SBI FRM)</div>
          <div style="font-size:11px; color:#7E90A6;">pooja.verma@sbi.co.in</div>
        </div>

        <div onclick="selectDepartmentPersona('TELECOM_CEIR', 'Suresh Kumar, Director DoT', 'dot_ceir_officer', '/static/telecom.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #1A5B8C; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#1A5B8C; font-weight:700;">TELECOM CEIR & IMEI</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Suresh Kumar (DoT CEIR)</div>
          <div style="font-size:11px; color:#7E90A6;">suresh.kumar@dot.gov.in</div>
        </div>

        <div onclick="selectDepartmentPersona('FIU_AML', 'Anandita Sen, FIU-IND', 'fiu_officer', '/static/fiu.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #9A3324; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#9A3324; font-weight:700;">FIU-IND FINNET 2.0</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Anandita Sen (FIU-IND)</div>
          <div style="font-size:11px; color:#7E90A6;">anandita.sen@fiuindia.gov.in</div>
        </div>

        <div onclick="selectDepartmentPersona('JUDICIAL_MAGISTRATE', 'Hon. Justice S.K. Mahajan', 'cjm_delhi_cyber', '/static/judiciary.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #2F6B4F; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#2F6B4F; font-weight:700;">SPECIAL CYBER COURT</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Hon. Justice S.K. Mahajan</div>
          <div style="font-size:11px; color:#7E90A6;">justice.mahajan@delhicourts.nic.in</div>
        </div>

        <div onclick="selectDepartmentPersona('ADMIN', 'Director General (I4C / MHA)', 'i4c_master_admin', '/static/admin.html')" style="background:#F6F3EC; border:1px solid #D8D1C0; border-left:4px solid #081524; padding:12px 14px; border-radius:2px; cursor:pointer; transition:all 0.15s ease;" onmouseover="this.style.background='#EEEAE0'" onmouseout="this.style.background='#F6F3EC'">
          <div style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#081524; font-weight:700;">SOVEREIGN CENTRAL ADMIN</div>
          <div style="font-size:12.5px; font-weight:600; color:#1B2430; margin-top:2px;">Director Central (I4C)</div>
          <div style="font-size:11px; color:#7E90A6;">admin.i4c@mha.gov.in</div>
        </div>

      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #D8D1C0; padding-top:14px;">
        <span style="font-family:'IBM Plex Mono', monospace; font-size:11px; color:#7E90A6;">DPDP 2023 ZERO-KNOWLEDGE CERTIFIED</span>
        <a href="/static/login.html" class="btn btn-outline" style="font-size:12px; padding:6px 14px; text-decoration:none;">Full Login Page →</a>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

function selectDepartmentPersona(dept, name, user, portal, bankCode = 'SBIN', badge = '') {
  const session = {
    authenticated: true,
    token: 'jwt_sovereign_' + Date.now(),
    department: dept,
    role: dept,
    full_name: name,
    username: user,
    bank_code: bankCode || (dept === 'BANK_NODAL' ? 'SBIN' : 'GENERIC'),
    badge: badge || (dept === 'BANK_NODAL' ? `${bankCode}-FRM-8291` : (dept === 'POLICE_CAD' ? 'IPS-DL-1094' : 'GOV-SOV-01')),
    jurisdiction: dept === 'BANK_NODAL' ? `${bankCode} Central Gateway` : 'National Command War Room',
    timestamp: new Date().toISOString()
  };
  sessionStorage.setItem('durgam_auth_session', JSON.stringify(session));
  alert(`🔐 JANPARICHAY SSO AUTHENTICATED:\n\n• Officer: ${name}\n• Role: ${dept}\n• Bank / Agency: ${session.bank_code}\n• Routing to isolated war room...`);
  window.location.href = portal;
}

function getCurrentAuthSession() {
  const raw = sessionStorage.getItem('durgam_auth_session');
  return raw ? JSON.parse(raw) : null;
}

function logoutUser() {
  sessionStorage.removeItem('durgam_auth_session');
  alert('You have safely signed out of your operational session.');
  window.location.href = '/static/login.html';
}
  alert('You have safely signed out of your operational session.');
  window.location.href = '/static/login.html';
}

// Pan-India Real-Time Dynamic Hotspots
const PAN_INDIA_HOTSPOTS = [
  { name: "Delhi NCR (Connaught Place)", lat: 28.6315, lng: 77.2167, risk: "CRITICAL", amount: "₹2.50L", bank: "SBI CP" },
  { name: "Mewat (Nuh Cluster)", lat: 28.1065, lng: 76.9984, risk: "CRITICAL", amount: "₹1.80L", bank: "PNB Mewat" },
  { name: "Mumbai (Nariman Point)", lat: 18.9256, lng: 72.8242, risk: "HIGH", amount: "₹5.40L", bank: "ICICI Hub" },
  { name: "Bengaluru (Koramangala)", lat: 12.9352, lng: 77.6245, risk: "HIGH", amount: "₹3.10L", bank: "HDFC Koramangala" },
  { name: "Hyderabad (HITEC City)", lat: 17.4435, lng: 78.3772, risk: "HIGH", amount: "₹2.20L", bank: "Axis HITEC" },
  { name: "Kolkata (Salt Lake Sector V)", lat: 22.5804, lng: 88.4378, risk: "MEDIUM", amount: "₹1.50L", bank: "Canara Salt Lake" },
  { name: "Jamtara (Mihijam Sector)", lat: 23.9576, lng: 86.8042, risk: "CRITICAL", amount: "₹4.20L", bank: "BOB Jamtara" },
  { name: "Ahmedabad (SG Highway)", lat: 23.0338, lng: 72.5089, risk: "MEDIUM", amount: "₹1.90L", bank: "SBI SG Highway" }
];

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initDynamicLeafletMap();
  initTelemetryCharts();
  initMultiversalTimelineCanvas();
  initFraudAutoSlider();
  initParticleMeshCanvas();
  initGlobalQuickActionDrawer();
  init3DCardTiltPhysics();
  initTacticalWebAudio();
  init3DHolographicGlobe();
  initLiveNetworkTelemetryStream();
});

// Hero Interactive Live Bank Simulation Cascade Trigger
function triggerHeroBankCascade() {
  const amt = document.getElementById('hero-amt-slider')?.value || 500000;
  const hops = document.getElementById('hero-hops-slider')?.value || 4;
  const timerEl = document.getElementById('hero-sim-timer');

  if (timerEl) {
    timerEl.innerText = "BROADCASTING ISO 20022 CAMT.056...";
    timerEl.style.color = "#FF681A";
  }

  playFreezeChime();

  setTimeout(() => {
    if (timerEl) {
      timerEl.innerText = `✓ ₹${Number(amt).toLocaleString('en-IN')} QUARANTINED ACROSS ${hops} HOPS (118.4ms)`;
      timerEl.style.color = "#00F0FF";
    }
    alert(`[DURGAM ISO 20022 camt.056 DIRECTIVE ISSUED]\n\n• Quarantined Volume: ₹${Number(amt).toLocaleString('en-IN')}\n• Beneficiary Depth: ${hops} Multi-Hop Accounts\n• Hold Latency: 118.4 ms\n• Core Banking Status: LIEN_PRE_SETTLEMENT_LOCKED\n• Court Restitution: Section 106 BNSS 2023 Order Generated.`);
  }, 350);
}

  async function fetchTelemetry() {
    try {
      const res = await fetch('/api/v1/bank/network-telemetry');
      if (res.ok) {
        const data = await res.json();
        const fundsEl = document.getElementById('live-funds-quarantined');
        if (fundsEl && data.total_quarantined_volume_inr) {
          fundsEl.innerText = '₹' + (data.total_quarantined_volume_inr / 10000000).toFixed(2) + ' Cr';
        }
      }
    } catch (e) {
      // Graceful offline fallback
    }
  }
  fetchTelemetry();
  setInterval(fetchTelemetry, 3500);
}


// Section 63 BSA 2023 Explainable AI (XAI) Modal
function openXAIExplanationModal(caseId = "DURGAM-DE-8309") {
  let modal = document.getElementById('xai-modal-backdrop');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'xai-modal-backdrop';
    modal.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(3,8,16,0.85); backdrop-filter:blur(10px); z-index:9999999; display:flex; align-items:center; justify-content:center; padding:20px;';
    modal.innerHTML = `
      <div class="glass-card" style="width:100%; max-width:680px; background:#07152B; border:1px solid #00F0FF; border-radius:12px; padding:24px; color:#F8FAFC; box-shadow:0 20px 50px rgba(0,0,0,0.8);">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:12px; margin-bottom:16px;">
          <div>
            <h3 style="margin:0; font-family:var(--font-heading); color:#00F0FF; font-size:1.15rem; display:flex; align-items:center; gap:8px;">
              ⚖️ SECTION 63 BSA 2023 — EXPLAINABLE AI EVIDENCE CERTIFICATE
            </h3>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">Statutory Feature Attribution & Integrated Gradients for Special Cyber Courts</div>
          </div>
          <button onclick="document.getElementById('xai-modal-backdrop').style.display='none'" style="background:none; border:none; color:#94A3B8; font-size:1.4rem; cursor:pointer;">&times;</button>
        </div>

        <div style="display:flex; flex-direction:column; gap:12px; font-size:0.85rem;">
          <div style="display:flex; justify-content:space-between; background:rgba(0,240,255,0.05); padding:10px; border-radius:6px; border:1px solid rgba(0,240,255,0.2);">
            <div><strong>Case Identifier:</strong> <span style="font-family:var(--font-mono); color:#00F0FF;">${caseId}</span></div>
            <div><strong>Attribution Model:</strong> <span style="color:#007A5E; font-weight:700;">PyTorch GATv2 + LightGBM</span></div>
          </div>

          <div><strong>Key Decision Factors (Integrated Gradients Feature Weights):</strong></div>
          <div style="display:flex; flex-direction:column; gap:8px;">
            <div>
              <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:2px;">
                <span>1. Net Layering Velocity (> ₹850/sec)</span>
                <span style="color:#DC2626; font-weight:700;">+44.2% Risk Weight</span>
              </div>
              <div style="height:6px; background:#1E293B; border-radius:3px; overflow:hidden;"><div style="width:44.2%; height:100%; background:#DC2626;"></div></div>
            </div>
            <div>
              <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:2px;">
                <span>2. Out-Degree Fan-Out Rapid Splitting (4 Hops)</span>
                <span style="color:#FF681A; font-weight:700;">+28.5% Risk Weight</span>
              </div>
              <div style="height:6px; background:#1E293B; border-radius:3px; overflow:hidden;"><div style="width:28.5%; height:100%; background:#FF681A;"></div></div>
            </div>
            <div>
              <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:2px;">
                <span>3. Jan Dhan Zero-Balance Dormancy Shift</span>
                <span style="color:#F59E0B; font-weight:700;">+16.3% Risk Weight</span>
              </div>
              <div style="height:6px; background:#1E293B; border-radius:3px; overflow:hidden;"><div style="width:16.3%; height:100%; background:#F59E0B;"></div></div>
            </div>
          </div>

          <div style="margin-top:8px; padding:10px; background:rgba(0,122,94,0.1); border:1px solid #007A5E; border-radius:6px; font-size:0.75rem; color:#A7F3D0;">
            ✓ <strong>Section 63 BSA Legal Hash:</strong> <span style="font-family:var(--font-mono);">0x8f29c4b10e9721ad...</span> (Anchored on Polygon Amoy EVM Ledger)
          </div>
        </div>

        <div style="display:flex; justify-content:flex-end; gap:10px; margin-top:16px;">
          <button onclick="window.print()" style="background:#007A5E; color:#fff; border:none; padding:8px 16px; border-radius:6px; font-weight:600; cursor:pointer;">🖨️ Export Section 63 BSA PDF</button>
          <button onclick="document.getElementById('xai-modal-backdrop').style.display='none'" style="background:#334155; color:#fff; border:none; padding:8px 16px; border-radius:6px; cursor:pointer;">Close</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  } else {
    modal.style.display = 'flex';
  }
}

// 3D Holographic Globe with Live Threat Arcs
function init3DHolographicGlobe() {
  const canvas = document.getElementById('hero-3d-globe-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = canvas.width = canvas.offsetWidth || 440;
  let height = canvas.height = canvas.offsetHeight || 320;
  let angle = 0;

  const hubs = [
    { name: "Delhi", x: 0.5, y: 0.35, color: "#00F0FF" },
    { name: "Mumbai", x: 0.35, y: 0.55, color: "#0284C7" },
    { name: "Jamtara", x: 0.65, y: 0.45, color: "#DC2626" },
    { name: "Mewat", x: 0.48, y: 0.40, color: "#FF681A" },
    { name: "Bengaluru", x: 0.45, y: 0.75, color: "#007A5E" }
  ];

  function drawGlobe() {
    ctx.clearRect(0, 0, width, height);
    angle += 0.015;

    // Glowing Hologram Globe Wireframe
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.15)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, 110, 0, Math.PI * 2);
    ctx.stroke();

    // Rotating Longitude Ellipses
    for (let i = 0; i < 4; i++) {
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, Math.abs(Math.cos(angle + i * 0.8)) * 110, 110, 0, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Draw Threat Arcs
    ctx.strokeStyle = 'rgba(220, 38, 38, 0.7)';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(width * 0.65, height * 0.45); // Jamtara
    ctx.quadraticCurveTo(width * 0.55, height * 0.25, width * 0.50, height * 0.35); // Delhi
    ctx.stroke();

    ctx.strokeStyle = 'rgba(255, 104, 26, 0.7)';
    ctx.beginPath();
    ctx.moveTo(width * 0.48, height * 0.40); // Mewat
    ctx.quadraticCurveTo(width * 0.38, height * 0.45, width * 0.35, height * 0.55); // Mumbai
    ctx.stroke();

    // Draw Command Hub Nodes
    hubs.forEach(h => {
      ctx.fillStyle = h.color;
      ctx.beginPath();
      ctx.arc(width * h.x, height * h.y, 4.5, 0, Math.PI * 2);
      ctx.fill();
    });

    requestAnimationFrame(drawGlobe);
  }
  drawGlobe();
}


// Synthesized Web Audio API Tactical Sound Engine (Zero external audio assets)
let audioCtx = null;
function getAudioContext() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioCtx;
}

function playTacticalClick() {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(1200, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.05);
    gain.gain.setValueAtTime(0.12, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.05);
  } catch (e) {}
}

function playFreezeChime() {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(520, ctx.currentTime);
    osc.frequency.setValueAtTime(880, ctx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.18, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.35);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.35);
  } catch (e) {}
}

function initTacticalWebAudio() {
  document.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON' || e.target.closest('button') || e.target.tagName === 'A') {
      playTacticalClick();
    }
  });
}

// 3D Perspective Card Tilt Physics
function init3DCardTiltPhysics() {
  document.querySelectorAll('.glass-card, .gov-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -6;
      const rotateY = ((x - centerX) / centerX) * 6;
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-2px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)';
    });
  });
}


// Global Quick Action Drawer (Ctrl+Shift+E)
function initGlobalQuickActionDrawer() {
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 'E' || e.key === 'e')) {
      e.preventDefault();
      toggleQuickActionDrawer();
    }
  });
}

function toggleQuickActionDrawer() {
  let drawer = document.getElementById('global-quick-drawer');
  if (!drawer) {
    drawer = document.createElement('div');
    drawer.id = 'global-quick-drawer';
    drawer.innerHTML = `
      <div style="position:fixed; top:0; right:0; width:380px; height:100vh; background:#07152B; border-left:2px solid #00F0FF; z-index:999999; box-shadow:-10px 0 30px rgba(0,0,0,0.8); padding:24px; color:#F1F5F9; font-family:var(--font-sans); display:flex; flex-direction:column; gap:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:12px;">
          <h3 style="margin:0; font-family:var(--font-heading); color:#00F0FF; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
            <svg style="width:18px; height:18px; color:#00F0FF;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            EMERGENCY QUICK-ACTION
          </h3>
          <button onclick="document.getElementById('global-quick-drawer').style.display='none'" style="background:none; border:none; color:#94A3B8; font-size:1.4rem; cursor:pointer;">&times;</button>
        </div>
        <div style="font-size:0.85rem; color:#94A3B8;">Shortcut: <kbd style="background:#1E293B; padding:2px 6px; border-radius:4px; color:#00F0FF;">Ctrl+Shift+E</kbd></div>
        <button onclick="alert('Section 106 BNSS 2023 Restitution Warrant Generated & Dispatched to Special Cyber Court!')" style="background:#007A5E; color:#fff; border:none; padding:12px; border-radius:6px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:10px;">
          <svg style="width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/></svg>
          Generate Section 106 BNSS Decree
        </button>
        <button onclick="alert('ISO 20022 camt.056 Cascade Micro-Hold Broadcast Dispatched to all 48 Banks!')" style="background:#0284C7; color:#fff; border:none; padding:12px; border-radius:6px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:10px;">
          <svg style="width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          Broadcast ISO 20022 Micro-Hold
        </button>
        <button onclick="alert('Remote ATM Dispenser Killswitch Dispatched to Target Hotspot Kiosks!')" style="background:#DC2626; color:#fff; border:none; padding:12px; border-radius:6px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:10px;">
          <svg style="width:18px; height:18px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
          Remote ATM Shutter Lock
        </button>
      </div>

    document.body.appendChild(drawer);
  } else {
    drawer.style.display = drawer.style.display === 'none' ? 'block' : 'none';
  }
}

// Interactive 3D Canvas Particle Mesh
function initParticleMeshCanvas() {
  const canvas = document.getElementById('particle-mesh-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let width = canvas.width = canvas.offsetWidth || window.innerWidth;
  let height = canvas.height = canvas.offsetHeight || 300;

  const particles = [];
  for (let i = 0; i < 45; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      radius: Math.random() * 2 + 1
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(0, 240, 255, 0.6)';
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.12)';

    for (let i = 0; i < particles.length; i++) {
      let p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();

      for (let j = i + 1; j < particles.length; j++) {
        let p2 = particles[j];
        let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
        if (dist < 110) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
}


// 1. Clock Display
function initClock() {
  const clock = document.getElementById('ist-clock-display');
  if (!clock) return;
  setInterval(() => {
    const now = new Date();
    clock.innerText = 'IST ' + now.toLocaleTimeString('en-IN', { hour12: false }) + ' • SECURE GATEWAY';
  }, 1000);
}

// 2. Real-Time Dynamic Pan-India Hotspot Heatmap
function initDynamicLeafletMap() {
  const container = document.getElementById('atm-map-canvas');
  if (!container) return;

  map = L.map('atm-map-canvas', {
    center: [22.5937, 78.9629], // Center of India
    zoom: 4.5,
    zoomControl: false
  });

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors • DURGAM Tactical Radar',
    maxZoom: 18
  }).addTo(map);

  markerLayer = L.layerGroup().addTo(map);
  renderHotspotMarkers();

  setInterval(() => {
    renderHotspotMarkers();
  }, 3000);
}

function renderHotspotMarkers() {
  if (!markerLayer) return;
  markerLayer.clearLayers();

  const activeSet = PAN_INDIA_HOTSPOTS.sort(() => 0.5 - Math.random()).slice(0, 5);

  activeSet.forEach((spot, index) => {
    const isPrimary = index === 0;
    const color = spot.risk === 'CRITICAL' ? '#DC2626' : spot.risk === 'HIGH' ? '#FF681A' : '#007A5E';
    const radius = isPrimary ? 18 : 12;

    const circle = L.circleMarker([spot.lat, spot.lng], {
      radius: radius,
      fillColor: color,
      color: '#FFFFFF',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    });

    circle.bindPopup(`
      <div style="font-family:'Inter',sans-serif; font-size:12px; line-height:1.5;">
        <strong style="color:${color}; font-size:13px;">🚨 ${spot.name}</strong><br>
        <strong>Risk Status:</strong> ${spot.risk}<br>
        <strong>Disputed Flow:</strong> ${spot.amount}<br>
        <strong>Target CBS Node:</strong> ${spot.bank}<br>
        <button onclick="handleCADDispatch()" style="margin-top:6px; background:#007A5E; color:#FFF; border:none; padding:5px 8px; border-radius:4px; font-size:11px; font-weight:700; cursor:pointer; width:100%;">🚨 Dispatch Nearest Patrol</button>
      </div>
    `);

    circle.addTo(markerLayer);
  });
}

// 3. Auto-Sliding Fraud Carousel
function initFraudAutoSlider() {
  const track = document.getElementById('fraud-slider-track');
  if (!track) return;

  const slides = document.querySelectorAll('.fraud-slide');
  if (slides.length === 0) return;

  slideInterval = setInterval(() => {
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    updateFraudSlidePosition();
  }, 4500);
}

function jumpToFraudSlide(index) {
  if (slideInterval) clearInterval(slideInterval);
  currentSlideIndex = index;
  updateFraudSlidePosition();
  
  const slideshow = document.getElementById('fraud-slideshow');
  if (slideshow) {
    slideshow.scrollIntoView({ behavior: 'smooth' });
  }

  slideInterval = setInterval(() => {
    const slides = document.querySelectorAll('.fraud-slide');
    currentSlideIndex = (currentSlideIndex + 1) % slides.length;
    updateFraudSlidePosition();
  }, 4500);
}

function updateFraudSlidePosition() {
  const track = document.getElementById('fraud-slider-track');
  const dots = document.querySelectorAll('.slider-dot');
  if (!track) return;

  track.style.transform = `translateX(-${currentSlideIndex * 100}%)`;

  dots.forEach((dot, idx) => {
    if (idx === currentSlideIndex) {
      dot.classList.add('active');
    } else {
      dot.classList.remove('active');
    }
  });
}

// 4. Telemetry Charts
function initTelemetryCharts() {
  const ctxVel = document.getElementById('chart-fraud-velocity')?.getContext('2d');
  if (ctxVel) {
    chartVelocity = new Chart(ctxVel, {
      type: 'line',
      data: {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', 'Now'],
        datasets: [
          { label: 'Fraud Inflow (₹ Cr)', data: [1.2, 0.8, 3.4, 6.2, 8.9, 11.4, 14.8], borderColor: '#DC2626', backgroundColor: 'rgba(220,38,38,0.1)', fill: true, tension: 0.4 },
          { label: 'Quarantined (₹ Cr)', data: [1.1, 0.7, 3.1, 5.8, 8.4, 10.9, 14.2], borderColor: '#007A5E', backgroundColor: 'rgba(0,122,94,0.1)', fill: true, tension: 0.4 }
        ]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
    });
  }

  const ctxDepth = document.getElementById('chart-mule-depth')?.getContext('2d');
  if (ctxDepth) {
    chartDepth = new Chart(ctxDepth, {
      type: 'bar',
      data: {
        labels: ['L1 Direct', 'L2 Split', 'L3 Aggregator', 'L4 Cashout / Crypto'],
        datasets: [{ label: 'Mule Accounts Traversed', data: [820, 640, 310, 145], backgroundColor: ['#007A5E', '#0284C7', '#FF681A', '#7C3AED'] }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });
  }

  const ctxBanks = document.getElementById('chart-bank-ratios')?.getContext('2d');
  if (ctxBanks) {
    chartBanks = new Chart(ctxBanks, {
      type: 'doughnut',
      data: {
        labels: ['SBI', 'HDFC', 'ICICI', 'PNB', 'Canara', 'Others'],
        datasets: [{ data: [34, 22, 18, 12, 8, 6], backgroundColor: ['#007A5E', '#0284C7', '#FF681A', '#DC2626', '#7C3AED', '#64748B'] }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
    });
  }

  const ctxDecay = document.getElementById('chart-atm-decay')?.getContext('2d');
  if (ctxDecay) {
    chartDecay = new Chart(ctxDecay, {
      type: 'line',
      data: {
        labels: ['0m', '5m', '10m', '15m', '20m', '25m', '30m', '45m', '60m'],
        datasets: [{ label: 'Recovery Probability (%)', data: [98, 91, 82, 71, 58, 44, 28, 14, 4], borderColor: '#007A5E', borderWidth: 2.5, tension: 0.3 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
    });
  }
}

// 5. Multiversal Quantum Timeline & GNN Neural Branching Engine
function initMultiversalTimelineCanvas() {
  const canvas = document.getElementById('gnn-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  // Define Multi-Branching Timeline Nodes (Origin ➔ Nexus Branches ➔ Divergent Leaf Realities)
  const timelineNodes = [
    // Origin / Nexus Core
    { id: 0, x: 0.08, y: 0.50, label: 'Origin Remitter', sub: 'SBI ₹2.5L', color: '#60A5FA', radius: 8, isOrigin: true },

    // Branch Layer 1 (Nexus Divergence)
    { id: 1, x: 0.28, y: 0.22, label: 'Timeline α [Mewat]', sub: 'PNB Splitting', color: '#FBBF24', radius: 6 },
    { id: 2, x: 0.28, y: 0.50, label: 'Timeline β [Cyber]', sub: 'UPI Fast Rail', color: '#38BDF8', radius: 6 },
    { id: 3, x: 0.28, y: 0.78, label: 'Timeline γ [Jamtara]', sub: 'Canara Smurfing', color: '#FBBF24', radius: 6 },

    // Branch Layer 2 (Aggregator Quantum Clusters)
    { id: 4, x: 0.54, y: 0.16, label: 'Aggregator Node A', sub: 'ICICI Nariman Pt', color: '#F87171', radius: 6.5 },
    { id: 5, x: 0.54, y: 0.38, label: 'Merchant Gateway', sub: 'Razorpay Proxy', color: '#A78BFA', radius: 6 },
    { id: 6, x: 0.54, y: 0.62, label: 'FinNet STR Escrow', sub: 'TRC-20 USDT', color: '#FB923C', radius: 6.5 },
    { id: 7, x: 0.54, y: 0.84, label: 'Aggregator Node B', sub: 'HDFC Salt Lake', color: '#F87171', radius: 6.5 },

    // Branch Layer 3 (Terminal Endpoints / Interception Targets)
    { id: 8, x: 0.82, y: 0.18, label: 'ATM Cashout CP', sub: '🚨 CAD Intercept (94%)', color: '#34D399', radius: 7.5, isTarget: true },
    { id: 9, x: 0.82, y: 0.40, label: 'CEIR Telecom Bar', sub: 'IMEI Barred (114ms)', color: '#C084FC', radius: 7, isTarget: true },
    { id: 10, x: 0.82, y: 0.62, label: 'VASP Cold Wallet', sub: 'PMLA Sec 17 Lock', color: '#F43F5E', radius: 7, isTarget: true },
    { id: 11, x: 0.82, y: 0.82, label: 'Judicial Vault', sub: 'Sec 63 BSA Restitution', color: '#10B981', radius: 7.5, isTarget: true }
  ];

  // Multiversal Branching Connections (Bifurcations & Quantum Links)
  const timelineBranches = [
    [0, 1], [0, 2], [0, 3],
    [1, 4], [1, 5],
    [2, 5], [2, 6],
    [3, 6], [3, 7],
    [4, 8], [5, 9], [6, 10], [7, 11]
  ];

  // Particle Streams for Timeline Energy Flux
  const energyParticles = [];
  for (let i = 0; i < 36; i++) {
    energyParticles.push({
      branchIdx: Math.floor(Math.random() * timelineBranches.length),
      progress: Math.random(),
      speed: 0.005 + Math.random() * 0.008,
      color: ['#00F0FF', '#34D399', '#FBBF24', '#C084FC'][Math.floor(Math.random() * 4)],
      size: 2 + Math.random() * 2
    });
  }

  let time = 0;
  function animateMultiverse() {
    time += 0.02;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const h = canvas.height;

    // Draw Subtle Multiverse Temporal Background Waves
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.04)';
    ctx.lineWidth = 1;
    for (let j = 0; j < 3; j++) {
      ctx.beginPath();
      for (let x = 0; x < w; x += 10) {
        const y = h * 0.5 + Math.sin(x * 0.01 + time + j) * 40 * (j + 1);
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }

    // Draw Curved Multiversal Timeline Branches
    timelineBranches.forEach(([fromId, toId], idx) => {
      const fromNode = timelineNodes[fromId];
      const toNode = timelineNodes[toId];

      const x1 = fromNode.x * w;
      const y1 = fromNode.y * h;
      const x2 = toNode.x * w;
      const y2 = toNode.y * h;

      // Smooth Bezier Curve between Timeline Nodes
      const cpX1 = x1 + (x2 - x1) * 0.5;
      const cpY1 = y1;
      const cpX2 = x1 + (x2 - x1) * 0.5;
      const cpY2 = y2;

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.bezierCurveTo(cpX1, cpY1, cpX2, cpY2, x2, y2);

      // Glowing branch styling
      const grad = ctx.createLinearGradient(x1, y1, x2, y2);
      grad.addColorStop(0, 'rgba(96, 165, 250, 0.35)');
      grad.addColorStop(0.5, 'rgba(0, 240, 255, 0.45)');
      grad.addColorStop(1, 'rgba(52, 211, 153, 0.35)');

      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.8;
      ctx.stroke();
    });

    // Animate Quantum Particles along Bezier Branches
    energyParticles.forEach(p => {
      p.progress += p.speed;
      if (p.progress > 1) {
        p.progress = 0;
        p.branchIdx = Math.floor(Math.random() * timelineBranches.length);
      }

      const [fromId, toId] = timelineBranches[p.branchIdx];
      const n1 = timelineNodes[fromId];
      const n2 = timelineNodes[toId];

      const x1 = n1.x * w;
      const y1 = n1.y * h;
      const x2 = n2.x * w;
      const y2 = n2.y * h;
      const cpX1 = x1 + (x2 - x1) * 0.5;
      const cpY1 = y1;
      const cpX2 = x1 + (x2 - x1) * 0.5;
      const cpY2 = y2;

      // Cubic Bezier interpolation
      const t = p.progress;
      const cx = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * cpX1 + 3 * (1 - t) * t ** 2 * cpX2 + t ** 3 * x2;
      const cy = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * cpY1 + 3 * (1 - t) * t ** 2 * cpY2 + t ** 3 * y2;

      ctx.fillStyle = p.color;
      ctx.shadowColor = p.color;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(cx, cy, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0; // reset
    });

    // Draw Nodes with Temporal Halo Rings & Cyber Labels
    timelineNodes.forEach(node => {
      const nx = node.x * w;
      const ny = node.y * h;

      // Halo ring
      ctx.strokeStyle = node.color;
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.arc(nx, ny, node.radius + 4 + Math.sin(time * 3 + node.id) * 2, 0, Math.PI * 2);
      ctx.stroke();

      // Node core
      ctx.fillStyle = node.color;
      ctx.shadowColor = node.color;
      ctx.shadowBlur = 10;
      ctx.beginPath();
      ctx.arc(nx, ny, node.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Multiversal Badge Labels
      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 10.5px "Space Grotesk", sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(node.label, nx, ny - node.radius - 8);

      ctx.fillStyle = '#94A3B8';
      ctx.font = '9.5px "JetBrains Mono", monospace';
      ctx.fillText(node.sub, nx, ny + node.radius + 14);
    });

    requestAnimationFrame(animateMultiverse);
  }
  animateMultiverse();
}

// 6. Auth Gateway Modal & Action Execution Routing
function openAuthModal(preferredRole) {
  const modal = document.getElementById('auth-modal');
  if (modal) {
    modal.classList.add('active');
  } else {
    window.location.href = '/static/login.html';
  }
}

function handleCADDispatch() {
  const session = JSON.parse(sessionStorage.getItem('durgam_auth_session') || '{}');
  if (!session.token || !['POLICE_NATIONAL', 'SUPER_ADMIN'].includes(session.role)) {
    openAuthModal('POLICE');
    return;
  }

  const modal = document.getElementById('dispatch-modal');
  const consoleEl = document.getElementById('dispatch-console');
  const spinner = document.getElementById('dispatch-spinner');
  if (!modal || !consoleEl) return;

  modal.classList.add('active');
  consoleEl.innerHTML = '';
  if (spinner) spinner.style.display = 'block';

  const logs = [
    '[00.012s] ST-KDE Interception Engine initialized for Case DURGAM-DL-001.',
    '[00.045s] Calculating nearest physical cashout ATMs across Connaught Place cluster...',
    '[00.089s] Highest Probability Target: SBI ATM Inner Circle (Lat: 28.6315, Lng: 77.2167).',
    '[00.124s] ERSS-112 CAD Integration: Transmitting GPS waypoints to PCR Falcon 1.',
    '[00.180s] ✓ DISPATCH CONFIRMED: Unit DL-PCR-01 en route. ETA: 3.8 minutes.'
  ];

  logs.forEach((log, index) => {
    setTimeout(() => {
      const line = document.createElement('div');
      line.className = 'terminal-line';
      line.style.color = index === logs.length - 1 ? '#34D399' : '#E2E8F0';
      line.innerText = log;
      consoleEl.appendChild(line);
      consoleEl.scrollTop = consoleEl.scrollHeight;

      if (index === logs.length - 1 && spinner) {
        spinner.style.display = 'none';
      }
    }, index * 350);
  });
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.classList.remove('active');
}

// 7. Quick SSO Demo Login Helper

function quickDemoLogin(role) {
  const roles = {
    'POLICE': { role: 'POLICE_NATIONAL', name: 'Dr. Vikram Rao, IPS', portal: '/static/police.html' },
    'BANK': { role: 'BANK_NODAL', name: 'Pooja Verma, SBI FRM', portal: '/static/bank.html' },
    'CITIZEN': { role: 'CITIZEN', name: 'Dr. Rajiv Malhotra', portal: '/static/citizen.html' },
    'TELECOM': { role: 'TELECOM_DOT', name: 'Suresh Kumar, DoT CEIR', portal: '/static/telecom.html' },
    'FIU': { role: 'FIU_OFFICER', name: 'Anandita Sen, FIU-IND', portal: '/static/fiu.html' },
    'JUDICIARY': { role: 'JUDGE_MAGISTRATE', name: 'Hon. Justice Rajesh Sharma', portal: '/static/judiciary.html' }
  };

  const target = roles[role] || roles['POLICE'];
  sessionStorage.setItem('durgam_auth_session', JSON.stringify({
    token: 'jwt_mock_' + Date.now(),
    role: target.role,
    full_name: target.name
  }));
  window.location.href = target.portal;
}

function logoutUser() {
  sessionStorage.removeItem('durgam_auth_session');
  window.location.href = '/static/login.html';
}

function handleHeroQuickReport() {
  alert('⚡ EMERGENCY 1930 SOS DOCKET INGESTED:\n\n• Case ID: DURGAM-DL-001\n• Sub-180ms camt.056 Lien Applied\n• Funds Quarantined: INR 2,50,000.00\n• Police CAD Notified: ERSS Unit Falcon 1');
}

// 8. Live Interactive Landing Page AI Risk & Time-to-Cashout Estimator
async function executeLandingAIEstimate() {
  const amount = parseFloat(document.getElementById('estimator-amount')?.value || 250000);
  const elapsed = parseFloat(document.getElementById('estimator-elapsed')?.value || 5);
  const channel = document.getElementById('estimator-channel')?.value || 'UPI';

  const elapsedLabel = document.getElementById('estimator-elapsed-val');
  if (elapsedLabel) elapsedLabel.innerText = `${elapsed} Mins`;

  try {
    const res = await fetch('/api/v1/ai/predict-time-to-cashout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hop_level: amount > 500000 ? 3 : (amount > 100000 ? 2 : 1),
        total_amount: amount,
        avg_hop_velocity: amount / (elapsed * 60 || 120),
        time_elapsed_mins: elapsed,
        channel_type: channel
      })
    });

    const data = await res.json();
    const pred = data.time_prediction;

    const winEl = document.getElementById('est-res-window');
    const probEl = document.getElementById('est-res-prob');
    const urgEl = document.getElementById('est-res-urgency');
    const hopsEl = document.getElementById('est-res-hops');

    if (winEl) winEl.innerText = `${pred.estimated_minutes_remaining} Mins`;
    if (probEl) probEl.innerText = `${data.golden_hour_recovery_probability}%`;
    if (urgEl) {
      urgEl.innerText = pred.golden_hour_urgency;
      urgEl.style.color = pred.golden_hour_urgency === 'CRITICAL' ? '#DC2626' : (pred.golden_hour_urgency === 'HIGH' ? '#FF681A' : '#007A5E');
    }
    if (hopsEl) hopsEl.innerText = `${pred.hop_level} Multi-Hop Traversal`;
  } catch (err) {
    console.error('Estimator error:', err);
  }
}

// 9. Live 1930 Case & UTR Quick Tracker
async function executeLandingCaseTrack() {
  const inputEl = document.getElementById('landing-track-input');
  const identifier = inputEl ? inputEl.value.trim() : '';

  if (!identifier) {
    alert('Please enter a 12-digit Bank UTR or NCRP Case Number.');
    return;
  }

  const resultBox = document.getElementById('landing-track-result');
  if (resultBox) {
    resultBox.style.display = 'block';
    resultBox.innerHTML = `
      <div style="font-family:var(--font-mono); font-size:12px; line-height:1.7;">
        <div style="color:var(--gov-green); font-weight:800; margin-bottom:6px;">✓ ACTIVE INCIDENT RETRIEVED: Case ${identifier}</div>
        <div>Originating UTR: <strong>482910482910</strong></div>
        <div>Beneficiary CBS Account: <strong>SBI Mewat (XXXX-XXXX-9182)</strong></div>
        <div>Quarantined Amount: <strong style="color:var(--gov-green);">INR 2,50,000.00</strong></div>
        <div>Statutory Defense Status: <strong style="color:var(--gov-blue);">ISO 20022 camt.056 Lien Active (Section 106 BNSS)</strong></div>
        <div>Blockchain Anchor: <strong style="color:var(--text-muted); font-size:10.5px;">Polygon Amoy (0x4a1879cd...291b)</strong></div>
      </div>
    `;
    resultBox.scrollIntoView({ behavior: 'smooth' });
  }
}

// 10. Multi-Lingual Regional Language Dictionary & Switcher
const REGIONAL_TRANSLATIONS = {
  'en': {
    headline: 'Building a Secure and Resilient Digital India',
    desc: 'DURGAM protects India\'s digital infrastructure, empowers citizens, and intercepts financial cybercrime across 48 commercial banks with sub-180ms automated inter-bank defense.',
    reportBtn: 'Report a Cybercrime',
    exploreBtn: 'Explore Fraud Vectors',
    matrixTitle: 'National Core Banking camt.056 Health & Hold SLA Matrix (48 Nodes)',
    feedTitle: '🚨 Real-Time Sovereign Cyber Defense Interception Stream (I4C Live Feed)'
  },
  'hi': {
    headline: 'सुरक्षित और सशक्त डिजिटल भारत का निर्माण',
    desc: 'दूर्गम (DURGAM) भारत के डिजिटल बुनियादी ढांचे की सुरक्षा करता है, नागरिकों को सशक्त बनाता है, और 48 वाणिज्यिक बैंकों में 180 मिलीसेकंड से कम समय में वित्तीय साइबर अपराध को रोकता है।',
    reportBtn: 'साइबर अपराध की शिकायत करें',
    exploreBtn: 'धोखाधड़ी के तरीकों को समझें',
    matrixTitle: 'राष्ट्रीय कोर बैंकिंग camt.056 स्वास्थ्य और होल्ड एसएलए मैट्रिक्स (48 नोड्स)',
    feedTitle: '🚨 वास्तविक समय संप्रभु साइबर रक्षा अवरोधन धारा (I4C लाइव फीड)'
  },
  'ta': {
    headline: 'பாதுகாப்பான மற்றும் நெகிழ்வான டிஜிட்டல் இந்தியாவை உருவாக்குதல்',
    desc: 'துர்கம் (DURGAM) இந்தியாவின் டிஜிட்டல் கட்டமைப்பைப் பாதுகாக்கிறது, குடிமக்களுக்கு அதிகாரம் அளிக்கிறது, மற்றும் 48 வணிக வங்கிகளில் நிதி இணைய குற்றங்களைத் தடுக்கிறது.',
    reportBtn: 'சைபர் குற்றத்தைப் புகாரளிக்கவும்',
    exploreBtn: 'மோசடி முறைகளை ஆராயுங்கள்',
    matrixTitle: 'தேசிய வங்கி camt.056 ஹோல்ட் எஸ்எல்ஏ மேட்ரிக்ஸ் (48 முனையங்கள்)',
    feedTitle: '🚨 நிகழ்நேர தேசிய இணைய பாதுகாப்பு இடைமறிப்பு ஸ்ட்ரீம்'
  },
  'te': {
    headline: 'సురక్షితమైన మరియు బలమైన డిజిటల్ భారతదేశ నిర్మాణం',
    desc: 'దుర్గం (DURGAM) భారతదేశ డిజిటల్ మౌలిక సదుపాయాలను రక్షిస్తుంది, పౌరులను శక్తివంతం చేస్తుంది మరియు 48 వాణిజ్య బ్యాంకులలో ఆర్థిక సైబర్ నేరాలను అడ్డుకుంటుంది.',
    reportBtn: 'సైబర్ క్రైమ్ ఫిర్యాదు చేయండి',
    exploreBtn: 'మోసాల పద్ధతులను తెలుసుకోండి',
    matrixTitle: 'జాతీయ కోర్ బ్యాంకింగ్ camt.056 హెల్త్ మరియు హోల్డ్ SLA మ్యాట్రిక్స్',
    feedTitle: '🚨 రియల్-టైమ్ సార్వభౌమ సైబర్ డిఫెన్స్ ఇంటర్‌సెప్షన్ స్ట్రీమ్'
  },
  'mr': {
    headline: 'सुरक्षित आणि सक्षम डिजिटल भारताची निर्मिती',
    desc: 'दुर्गम (DURGAM) भारताच्या डिजिटल पायाभूत सुविधांचे रक्षण करते, नागरिकांना सक्षम करते आणि 48 बँकांमध्ये आर्थिक सायबर गुन्हे त्वरित रोखते.',
    reportBtn: 'सायबर गुन्ह्याची तक्रार करा',
    exploreBtn: 'फसवणुकीचे प्रकार पहा',
    matrixTitle: 'राष्ट्रीय कोर बँकिंग camt.056 आरोग्य आणि होल्ड SLA मॅट्रिक्स',
    feedTitle: '🚨 रिअल-टाइम राष्ट्रीय सायबर सुरक्षा थेट प्रवाह'
  },
  'bn': {
    headline: 'একটি নিরাপদ ও স্থিতিস্থাপক ডিজিটাল ভারত গঠন',
    desc: 'দুর্গম (DURGAM) ভারতের ডিজিটাল পরিকাঠামো রক্ষা করে, নাগরিকদের ক্ষমতায়ন করে এবং ৪৮টি বাণিজ্যিক ব্যাংকে আর্থিক সাইবার অপরাধ প্রতিহত করে।',
    reportBtn: 'সাইবার অপরাধ রিপোর্ট করুন',
    exploreBtn: 'জালিয়াতির ধরন অন্বেষণ করুন',
    matrixTitle: 'জাতীয় কোর ব্যাংকিং camt.056 হেলথ ও হোল্ড SLA ম্যাট্রিক্স',
    feedTitle: '🚨 রিয়েল-টাইম জাতীয় সাইবার প্রতিরক্ষা ইন্টারসেপশন স্ট্রিম'
  }
};

function switchPlatformLanguage(lang) {
  const t = REGIONAL_TRANSLATIONS[lang] || REGIONAL_TRANSLATIONS['en'];

  const headlineEl = document.querySelector('.hero-head, .icsc-hero-headline');
  const descEl = document.querySelector('.hero-desc, .icsc-hero-desc');
  const matrixTitleEl = document.getElementById('bank-matrix-title');
  const feedTitleEl = document.getElementById('threat-feed-title');

  if (headlineEl) headlineEl.innerHTML = t.headline;
  if (descEl) descEl.innerHTML = t.desc;
  if (matrixTitleEl) matrixTitleEl.innerText = t.matrixTitle;
  if (feedTitleEl) feedTitleEl.innerText = t.feedTitle;
}

function switchLanguage(lang) {
  switchPlatformLanguage(lang);
}

// 11. Live Threat Ticker Dynamic Stream Simulation
function initLiveThreatFeedSimulation() {
  const container = document.getElementById('live-threat-feed-container');
  if (!container) return;

  const mockThreatEvents = [
    { text: '[03:21:02 IST] 🚨 PHISHING APK BARRED: "Bijli_Bill_Update.apk" hash sealed across Google Play Protect / DoT', color: '#F87171' },
    { text: '[03:20:55 IST] 🏦 ISO 20022 camt.056 HOLD APPLIED: ₹1,80,000.00 locked in Canara Salt Lake (119ms)', color: '#34D399' },
    { text: '[03:20:48 IST] 📱 DoT CEIR HARDWARE BLACKLIST: IMEI 864910281920194 barred across Pan-India TSPs', color: '#38BDF8' },
    { text: '[03:20:39 IST] ⚖️ SEC 63 BSA RESTITUTION DECREE: e-Courts fast-track refund confirmed for Case DURGAM-JK-002', color: '#A78BFA' }
  ];

  setInterval(() => {
    const item = mockThreatEvents[Math.floor(Math.random() * mockThreatEvents.length)];
    const div = document.createElement('div');
    div.className = 'terminal-line';
    div.style.color = item.color;
    div.innerText = item.text;
    container.insertBefore(div, container.firstChild);

    if (container.children.length > 6) {
      container.removeChild(container.lastChild);
    }
  }, 4000);
}

// 12. 3D Sovereign Cyber Globe & Constellation Particle Engine
function init3DCyberGlobe() {
  const canvas = document.getElementById('hero-3d-globe-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const hubs = [
    { name: 'Delhi', lat: 28.61, lon: 77.20, color: '#007A5E' },
    { name: 'Mumbai', lat: 19.07, lon: 72.87, color: '#0284C7' },
    { name: 'Bengaluru', lat: 12.97, lon: 77.59, color: '#007A5E' },
    { name: 'Hyderabad', lat: 17.38, lon: 78.48, color: '#7C3AED' },
    { name: 'Kolkata', lat: 22.57, lon: 88.36, color: '#FF681A' },
    { name: 'Chennai', lat: 13.08, lon: 80.27, color: '#0284C7' },
    { name: 'Jammu', lat: 32.72, lon: 74.85, color: '#DC2626' }
  ];

  let rotation = 0;

  function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const radius = Math.min(cx, cy) * 0.72;

    // Glowing Sphere Background
    const grad = ctx.createRadialGradient(cx, cy, radius * 0.2, cx, cy, radius);
    grad.addColorStop(0, 'rgba(0, 122, 94, 0.08)');
    grad.addColorStop(0.8, 'rgba(15, 37, 55, 0.05)');
    grad.addColorStop(1, 'rgba(0, 122, 94, 0.15)');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'rgba(0, 122, 94, 0.35)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Orbital latitude rings
    for (let i = -2; i <= 2; i++) {
      const yOffset = (i / 3) * (radius * 0.85);
      const rRing = Math.sqrt(Math.max(0, radius * radius - yOffset * yOffset));
      ctx.beginPath();
      ctx.ellipse(cx, cy + yOffset, rRing, rRing * 0.28, 0, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(15, 37, 55, 0.12)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    rotation += 0.008;

    // Project and render command hub nodes
    const projected = hubs.map(h => {
      const lonRad = (h.lon * Math.PI) / 180 + rotation;
      const latRad = (h.lat * Math.PI) / 180;
      const x = cx + radius * Math.cos(latRad) * Math.sin(lonRad);
      const y = cy - radius * Math.sin(latRad);
      const z = Math.cos(latRad) * Math.cos(lonRad);
      return { ...h, x, y, z };
    });

    // Draw inter-hub defense vectors (Arcs)
    ctx.lineWidth = 1.2;
    for (let i = 0; i < projected.length; i++) {
      for (let j = i + 1; j < projected.length; j++) {
        const p1 = projected[i];
        const p2 = projected[j];
        if (p1.z > -0.2 && p2.z > -0.2) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          const midX = (p1.x + p2.x) / 2;
          const midY = (p1.y + p2.y) / 2 - 18;
          ctx.quadraticCurveTo(midX, midY, p2.x, p2.y);
          ctx.strokeStyle = 'rgba(0, 122, 94, 0.25)';
          ctx.stroke();
        }
      }
    }

    // Draw hub points
    projected.forEach(p => {
      if (p.z > -0.3) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4.5, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.font = '10px Space Grotesk, sans-serif';
        ctx.fillStyle = 'var(--gov-navy)';
        ctx.fillText(p.name, p.x + 7, p.y + 3);
      }
    });

    requestAnimationFrame(render);
  }
  render();
}

// 13. Interactive 3D Dynamic Force-Directed GNN Mule Network Engine
let gnnNodes = [
  { id: '1', name: 'Victim (Remitter)', x: 80, y: 130, vx: 0, vy: 0, isMule: false, hold: 'CLEAN', score: 0.02, color: '#007A5E' },
  { id: '2', name: 'Mule Layer 1 (SBI)', x: 220, y: 80, vx: 0, vy: 0, isMule: true, hold: 'camt.056 ACTIVE', score: 0.94, color: '#DC2626' },
  { id: '3', name: 'Mule Layer 1 (PNB)', x: 220, y: 180, vx: 0, vy: 0, isMule: true, hold: 'camt.056 ACTIVE', score: 0.88, color: '#DC2626' },
  { id: '4', name: 'Crypto OTC Gateway', x: 380, y: 70, vx: 0, vy: 0, isMule: true, hold: 'FIU SEC 17', score: 0.96, color: '#7C3AED' },
  { id: '5', name: 'ATM Kiosk Cashout', x: 390, y: 190, vx: 0, vy: 0, isMule: true, hold: 'CAD PATROL DISPATCH', score: 0.99, color: '#FF681A' }
];

let gnnLinks = [
  { source: '1', target: '2', value: 150000 },
  { source: '1', target: '3', value: 100000 },
  { source: '2', target: '4', value: 150000 },
  { source: '3', target: '5', value: 100000 }
];

let draggedNode = null;

function init3DForceDirectedGNN() {
  const canvas = document.getElementById('gnn-force-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  canvas.addEventListener('mousedown', e => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    gnnNodes.forEach(n => {
      const dist = Math.hypot(n.x - mx, n.y - my);
      if (dist < 18) {
        draggedNode = n;
        updateGNNInspector(n);
      }
    });
  });

  window.addEventListener('mousemove', e => {
    if (draggedNode) {
      const rect = canvas.getBoundingClientRect();
      draggedNode.x = e.clientX - rect.left;
      draggedNode.y = e.clientY - rect.top;
    }
  });

  window.addEventListener('mouseup', () => {
    draggedNode = null;
  });

  let packetT = 0;

  function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Force simulation physics step
    gnnNodes.forEach(n => {
      if (n !== draggedNode) {
        // Return to center gravity
        n.x += (canvas.width / 2 - n.x) * 0.002;
        n.y += (canvas.height / 2 - n.y) * 0.002;
      }
    });

    packetT += 0.015;

    // Draw links
    gnnLinks.forEach(link => {
      const s = gnnNodes.find(n => n.id === link.source);
      const t = gnnNodes.find(n => n.id === link.target);
      if (s && t) {
        ctx.beginPath();
        ctx.moveTo(s.x, s.y);
        ctx.lineTo(t.x, t.y);
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.35)';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Pulsating transfer packet
        const progress = (packetT % 1);
        const px = s.x + (t.x - s.x) * progress;
        const py = s.y + (t.y - s.y) * progress;
        ctx.beginPath();
        ctx.arc(px, py, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#00F0FF';
        ctx.fill();
      }
    });

    // Draw nodes
    gnnNodes.forEach(n => {
      ctx.beginPath();
      ctx.arc(n.x, n.y, 14, 0, Math.PI * 2);
      ctx.fillStyle = n.color;
      ctx.fill();
      ctx.strokeStyle = '#FFFFFF';
      ctx.lineWidth = 2;
      ctx.stroke();

      ctx.font = '11px JetBrains Mono, monospace';
      ctx.fillStyle = '#E2E8F0';
      ctx.fillText(n.name, n.x + 18, n.y + 4);
    });

    requestAnimationFrame(loop);
  }
  loop();
}

function updateGNNInspector(n) {
  document.getElementById('insp-name').innerText = n.name;
  document.getElementById('insp-score').innerText = `${n.score} [${n.score > 0.8 ? 'CRITICAL' : 'CLEAN'}]`;
  document.getElementById('insp-hold').innerText = n.hold;
}

function injectSimulatedMuleNode() {
  const newId = String(gnnNodes.length + 1);
  const newNode = {
    id: newId,
    name: `Mule Layer 2 (Hop ${newId})`,
    x: Math.random() * 300 + 100,
    y: Math.random() * 150 + 50,
    vx: 0,
    vy: 0,
    isMule: true,
    hold: 'camt.056 INJECTED',
    score: 0.95,
    color: '#DC2626'
  };
  gnnNodes.push(newNode);
  gnnLinks.push({ source: '2', target: newId, value: 50000 });
}

function resetGNNPhysics() {
  gnnNodes[0].x = 80; gnnNodes[0].y = 130;
  gnnNodes[1].x = 220; gnnNodes[1].y = 80;
  gnnNodes[2].x = 220; gnnNodes[2].y = 180;
  gnnNodes[3].x = 380; gnnNodes[3].y = 70;
  gnnNodes[4].x = 390; gnnNodes[4].y = 190;
}

document.addEventListener('DOMContentLoaded', () => {
  init3DCyberGlobe();
  init3DForceDirectedGNN();
  initCursorParticleFollower();
  initSavedTheme();
});

// 14. Sovereign Cyber Dark/Light Theme Engine
function initSavedTheme() {
  const saved = localStorage.getItem('durgam_theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeButtonUI(saved);
}

function toggleSovereignTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('durgam_theme', next);
  updateThemeButtonUI(next);
  playCyberAudioAlert('click');
}

function updateThemeButtonUI(theme) {
  const btn = document.getElementById('theme-toggle-btn');
  if (btn) {
    btn.innerHTML = theme === 'dark' ? '☀️ <span>Light Mode</span>' : '🌙 <span>Dark Mode</span>';
  }
}

// 15. Real-Time Web Audio API Synthesizer (No external audio files required)
let audioFXEnabled = true;

function toggleCyberAudio() {
  audioFXEnabled = !audioFXEnabled;
  const btn = document.getElementById('audio-toggle-btn');
  if (btn) {
    btn.innerHTML = audioFXEnabled ? '🔊 <span>Audio FX: ON</span>' : '🔇 <span>Audio FX: OFF</span>';
  }
  if (audioFXEnabled) playCyberAudioAlert('beep');
}

function playCyberAudioAlert(type = 'beep') {
  if (!audioFXEnabled) return;
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    if (type === 'beep') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, ctx.currentTime); // A5
      osc.frequency.exponentialRampToValueAtTime(1760, ctx.currentTime + 0.08);
      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
      osc.start();
      osc.stop(ctx.currentTime + 0.12);
    } else if (type === 'alert') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      osc.frequency.linearRampToValueAtTime(220, ctx.currentTime + 0.25);
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
      osc.start();
      osc.stop(ctx.currentTime + 0.25);
    } else {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(1200, ctx.currentTime);
      gain.gain.setValueAtTime(0.06, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.04);
      osc.start();
      osc.stop(ctx.currentTime + 0.04);
    }
  } catch (e) {
    // AudioContext permission guard
  }
}

// 16. Custom Cyber Cursor Particle Follower
function initCursorParticleFollower() {
  const canvas = document.getElementById('cursor-particle-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  const particles = [];

  window.addEventListener('mousemove', e => {
    for (let i = 0; i < 2; i++) {
      particles.push({
        x: e.clientX,
        y: e.clientY,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        size: Math.random() * 3 + 1.5,
        alpha: 0.8,
        color: '#00F0FF'
      });
    }
  });

  window.addEventListener('click', e => {
    playCyberAudioAlert('click');
    for (let i = 0; i < 12; i++) {
      const angle = (i / 12) * Math.PI * 2;
      particles.push({
        x: e.clientX,
        y: e.clientY,
        vx: Math.cos(angle) * 3,
        vy: Math.sin(angle) * 3,
        size: 3.5,
        alpha: 1,
        color: '#34D399'
      });
    }
  });

  function loop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.alpha -= 0.025;

      if (p.alpha <= 0) {
        particles.splice(i, 1);
        continue;
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.alpha;
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    requestAnimationFrame(loop);
  }
  loop();
}

// 17. Citizen APK Malware Sandbox Scanner Simulation
function simulateAPKScan() {
  const resultBox = document.getElementById('apk-scan-result');
  if (!resultBox) return;

  resultBox.innerHTML = `
    <div style="color:#FBBF24; font-weight:800; margin-bottom:4px;">⏳ DECOMPILING "Bijli_Bill_Update.apk"...</div>
    <div>Extracting AndroidManifest.xml & DEX bytecode...</div>
  `;

  setTimeout(() => {
    resultBox.innerHTML = `
      <div style="color:#F87171; font-weight:800; margin-bottom:4px;">🚨 CRITICAL MALWARE SIGNATURE DETECTED</div>
      <div>Package: <strong>com.sec.bijli.stealer</strong></div>
      <div>C2 Server: <strong>https://cyber-command-bot.ru/gate.php</strong></div>
      <div>Permissions Hijacked: <span style="color:#F87171;">BIND_ACCESSIBILITY_SERVICE, RECEIVE_SMS, READ_CONTACTS</span></div>
      <div>Action: <strong style="color:#34D399;">SHA-256 Hash Added to DoT/I4C Pan-India Barred Registry</strong></div>
    `;
    playCyberAudioAlert('alert');
  }, 1200);
}

// 18. Live Multi-Agency End-to-End Incident Simulation Engine
function triggerMultiAgencyEndToEndSimulation() {
  playCyberAudioAlert('alert');
  speakTacticalVoiceAlert("Emergency alert. Multi-agency 360-degree cyber defense protocol activated across all 6 departments.");
  alert(`🚨 MULTI-AGENCY 360° DEFENSE SIMULATION TRIGGERED (Case DURGAM-SIM-99):

[1] 🛡️ CITIZEN 1930: SOS docket ingested (₹2,50,000 loss).
[2] 🏦 BANK FRM: ISO 20022 camt.056 hold applied on SBI Mewat (118.2ms).
[3] 🚔 POLICE CAD: ST-KDE PCR Eagle 4 dispatched to Connaught Place ATM.
[4] 📱 DoT CEIR: Handset IMEI 864910281920194 barred pan-India.
[5] 💼 FIU-IND: 30,000 USDT escrow frozen under PMLA Section 17.
[6] ⚖️ JUDICIARY: Section 106 BNSS / Section 63 BSA restitution decree sealed on Polygon Amoy!

100% Inter-Agency Orchestration Succeeded.`);
}

// 19. Active User JWT Claims Inspector
function openJWTClaimsModal() {
  const session = JSON.parse(sessionStorage.getItem('durgam_auth_session') || '{}');
  const details = `
🔐 DECODED ACTIVE JWT ACCESS TOKEN CLAIMS:

• Subject (User): ${session.username || 'sp_delhi_cyber'}
• Full Name: ${session.full_name || 'Dr. Vikram Rao, IPS'}
• Role: ${session.role || 'POLICE_NATIONAL'}
• Badge: ${session.badge_number || 'IPS-DL-48219'}
• Jurisdiction: ${session.jurisdiction || 'Delhi NCR Command'}
• Token Standard: ECDSA HS256 Signed
• Compliance: DPDP Act 2023 / Section 63 BSA 2023
  `;
  alert(details);
}

// 20. Tactical Voice Assistant Synthesizer (Web Speech API)
function speakTacticalVoiceAlert(text) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.95;
    window.speechSynthesis.speak(utterance);
  }
}

// 21. Live Multimodal Sandbox Execution
async function runLiveMultimodalSandbox() {
  const narrative = document.getElementById('sandbox-narrative')?.value || "";
  const voiceStress = parseFloat(document.getElementById('sandbox-voice-stress')?.value || 0.88);
  const perms = parseInt(document.getElementById('sandbox-apk-perms')?.value || 5);
  const resBox = document.getElementById('sandbox-result-box');

  if (resBox) {
    resBox.innerHTML = '<div style="color:var(--gov-blue); font-weight:800;">🧠 RUNNING MULTIMODAL DEEP LEARNING INFERENCE...</div>';
  }

  try {
    const res = await fetch('/api/v1/ai/analyze-multivector-threat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        narrative: narrative,
        voice_stress_score: voiceStress,
        apk_suspicious_permissions_count: perms,
        c2_ip_flagged: true
      })
    });
    const data = await res.json();

    if (resBox) {
      const isCrit = data.threat_tier === 'CRITICAL_COMPOUND_THREAT';
      resBox.innerHTML = `
        <div style="color:${isCrit ? 'var(--gov-red)' : 'var(--gov-green)'}; font-weight:800; font-size:13px; margin-bottom:8px;">
          ${isCrit ? '🚨 CRITICAL COMPOUND CYBER THREAT DETECTED' : '✅ LOW RISK PATTERN'}
        </div>
        <div>Composite Probability: <strong style="color:var(--gov-navy); font-size:14px;">${(data.composite_threat_probability*100).toFixed(1)}%</strong></div>
        <div style="margin-top:6px; color:var(--text-secondary);">
          • NLP Semantic Score: <strong>${(data.sub_modality_scores.nlp_semantic_intent*100).toFixed(1)}%</strong><br>
          • Voice Synthetic Score: <strong>${(data.sub_modality_scores.voice_deepfake_synthetic_probability*100).toFixed(1)}%</strong><br>
          • APK Opcode Risk Density: <strong>${(data.sub_modality_scores.apk_malicious_opcode_density*100).toFixed(1)}%</strong>
        </div>
        <div style="margin-top:8px; font-size:11px; background:#FEF2F2; color:#991B1B; padding:6px 10px; border-radius:4px; font-weight:700;">
          MANDATE: ${data.interception_mandate}
        </div>
      `;
      playCyberAudioAlert('alert');
      speakTacticalVoiceAlert(`Critical multimodal threat detected. Threat score ${Math.round(data.composite_threat_probability*100)} percent.`);
    }
  } catch (e) {
    if (resBox) resBox.innerText = "Inference completed.";
  }
}

// 22. Live Crypto Mixer Tracer Test
async function runLiveCryptoMixerTest() {
  const resBox = document.getElementById('sandbox-result-box');
  if (resBox) {
    resBox.innerHTML = '<div style="color:var(--gov-blue); font-weight:800;">⛓️ TRACING TRC-20 USDT TRANSACTIONS THROUGH MIXERS...</div>';
  }

  try {
    const res = await fetch('/api/v1/ai/trace-crypto-mixer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tx_hash: "0x8f2a10b492019482910482910482910482910482910482910482910482910",
        token: "USDT (TRC-20)",
        amount: 30000.0,
        hops_count: 3
      })
    });
    const data = await res.json();
    if (resBox) {
      resBox.innerHTML = `
        <div style="color:var(--gov-red); font-weight:800; font-size:13px; margin-bottom:8px;">
          🚨 PEEL CHAIN & MIXER OBFUSCATION DETECTED
        </div>
        <div>Flow: <strong>${data.total_flow_usdt} USDT</strong> across <strong>${data.peel_chain_depth} Layering Hops</strong></div>
        <div style="margin-top:6px; color:var(--text-secondary);">
          • Target Domestic Exchange: <strong>${data.fiu_injunction_target_vasp}</strong><br>
          • Mixer Fingerprint: <strong>SunSwap V2 Liquidity Pool</strong><br>
          • Statutory Directive: <strong style="color:var(--gov-red);">${data.statutory_action}</strong>
        </div>
      `;
      playCyberAudioAlert('alert');
      speakTacticalVoiceAlert("PMLA Section 17 crypto asset freeze directive issued.");
    }
  } catch (e) {
    if (resBox) resBox.innerText = "Mixer trace completed.";
  }
}

// 23. Real-World 100k Dataset Explorer Simulation Data
const DATASET_100K_SAMPLES = [
  { id: "DURGAM-REC-100001", cat: "DIGITAL_ARREST", amount: "₹18,50,000", bank: "State Bank of India (SBIN004821)", loc: "Delhi NCR", eta: "18.5 mins", status: "HOLD_APPLIED" },
  { id: "DURGAM-REC-100002", cat: "PART_TIME_JOB", amount: "₹4,20,000", bank: "Punjab National Bank (PUNB001920)", loc: "Jammu", eta: "24.2 mins", status: "HOLD_APPLIED" },
  { id: "DURGAM-REC-100003", cat: "APK_MALWARE", amount: "₹1,85,000", bank: "HDFC Bank (HDFC000192)", loc: "Bengaluru", eta: "12.1 mins", status: "HOLD_APPLIED" },
  { id: "DURGAM-REC-100004", cat: "CRYPTO_MIXER_WASH", amount: "₹28,00,000", bank: "ICICI Bank (ICIC000849)", loc: "Mumbai", eta: "8.4 mins", status: "PMLA_FROZEN" },
  { id: "DURGAM-REC-100005", cat: "DIGITAL_ARREST", amount: "₹52,00,000", bank: "Canara Bank (CNRB002910)", loc: "Jaipur", eta: "31.0 mins", status: "HOLD_APPLIED" },
  { id: "DURGAM-REC-100006", cat: "PART_TIME_JOB", amount: "₹6,40,000", bank: "Axis Bank (UTIB000192)", loc: "Chandigarh", eta: "21.5 mins", status: "HOLD_APPLIED" }
];

function filterDatasetCategory(cat) {
  const tbody = document.getElementById('dataset-explorer-tbody');
  if (!tbody) return;

  const filtered = cat === 'ALL' ? DATASET_100K_SAMPLES : DATASET_100K_SAMPLES.filter(r => r.cat === cat);
  tbody.innerHTML = '';

  filtered.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td style="font-family:var(--font-mono); font-weight:800; color:var(--gov-navy);">${r.id}</td>
      <td><span class="badge-live-dot" style="font-size:10.5px;">${r.cat}</span></td>
      <td style="font-weight:800; color:var(--gov-red); font-family:var(--font-mono);">${r.amount}</td>
      <td><strong>${r.bank}</strong></td>
      <td>${r.loc}</td>
      <td style="font-family:var(--font-mono); color:var(--gov-blue);">${r.eta}</td>
      <td><span class="badge-live-dot" style="background:var(--gov-green-light); color:var(--gov-green-dark);">${r.status}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

// 24. 1930 Call Center IVR Audio Stream & Speech-to-Text Simulator
let ivrAnimId = null;
function start1930IVRSimulation() {
  const ivrBox = document.getElementById('ivr-audio-box');
  if (!ivrBox) return;

  ivrBox.style.display = 'block';
  playCyberAudioAlert('alert');
  speakTacticalVoiceAlert("1930 emergency financial fraud helpline call incoming. Live audio waveform active.");

  const canvas = document.getElementById('ivr-waveform-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let phase = 0;

    if (ivrAnimId) cancelAnimationFrame(ivrAnimId);

    function drawWave() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.beginPath();
      ctx.lineWidth = 2;
      ctx.strokeStyle = '#38BDF8';

      for (let x = 0; x < canvas.width; x++) {
        const y = (canvas.height / 2) + Math.sin((x * 0.05) + phase) * 12 * Math.sin(x * 0.01);
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
      phase += 0.15;
      ivrAnimId = requestAnimationFrame(drawWave);
    }
    drawWave();
  }

  // Auto-fill complaint form fields
  setTimeout(() => {
    const nameInput = document.getElementById('cit-name');
    const amountInput = document.getElementById('cit-amount');
    const utrInput = document.getElementById('cit-utr');
    if (nameInput) nameInput.value = "Dr. Rajiv Malhotra";
    if (amountInput) amountInput.value = "250000.00";
    if (utrInput) utrInput.value = "482910482910";
  }, 1000);
}

// 26. Command-K (Spotlight HUD) Quick Search Engine
function toggleCommandK(forceOpen) {
  const overlay = document.getElementById('cmd-k-overlay');
  const input = document.getElementById('cmd-k-input');
  if (!overlay) return;

  const shouldOpen = forceOpen !== undefined ? forceOpen : !overlay.classList.contains('active');
  if (shouldOpen) {
    overlay.classList.add('active');
    if (input) {
      input.value = '';
      setTimeout(() => input.focus(), 50);
    }
  } else {
    overlay.classList.remove('active');
  }
}

function filterCommandKItems(query) {
  const items = document.querySelectorAll('.cmd-k-item');
  const q = query.toLowerCase();
  items.forEach(item => {
    const text = item.innerText.toLowerCase();
    item.style.display = text.includes(q) ? 'flex' : 'none';
  });
}

// Global Keyboard Listener for Cmd+K / Ctrl+K & Escape
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    toggleCommandK();
  } else if (e.key === 'Escape') {
    toggleCommandK(false);
  }
});

// 27. 3D Card Tilt & Specular Physics
document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.gov-card, .chart-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -4.0;
      const rotateY = ((x - centerX) / centerX) * 4.0;
      card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-2px)`;
    });

// 28. Floating Tactical Alert Toast Engine
function showTacticalToast(title, message, type = 'success') {
  let container = document.getElementById('tactical-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'tactical-toast-container';
    container.className = 'tactical-toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `tactical-toast ${type}`;
  const icon = type === 'alert' ? '🚨' : (type === 'warning' ? '⚠️' : '✅');

  toast.innerHTML = `
    <div style="font-size:18px;">${icon}</div>
    <div>
      <div class="tactical-toast-title">${title}</div>
      <div class="tactical-toast-desc">${message}</div>
    </div>
  `;

  container.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 50);

// 29. Citizen Section 106 BNSS Restitution Calculator Logic
function calculateRestitutionPayout() {
  const amtInput = document.getElementById('calc-loss-amt');
  const timeInput = document.getElementById('calc-time-mins');
  if (!amtInput || !timeInput) return;

  const amt = parseFloat(amtInput.value);
  const mins = parseFloat(timeInput.value);

  document.getElementById('calc-amt-val').innerText = '₹' + amt.toLocaleString('en-IN');
  document.getElementById('calc-mins-val').innerText = mins + ' Mins';

  // Golden Hour Recovery Decay Formula: R(t) = max(15%, 98% * exp(-t / 35))
  const decay = Math.max(0.15, 0.98 * Math.exp(-mins / 35.0));
  const recoverySum = amt * decay;

  document.getElementById('calc-recovery-pct').innerText = (decay * 100).toFixed(1) + '%';
  document.getElementById('calc-recovery-sum').innerText = '₹' + Math.round(recoverySum).toLocaleString('en-IN') + ' Expected Restitution';
}

// 30. Live Audio Spectrogram FFT Renderer
function renderLiveAudioSpectrogram() {
  const canvas = document.getElementById('spectrogram-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  playCyberAudioAlert('alert');

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const numBars = 36;
  const barWidth = canvas.width / numBars;

  for (let i = 0; i < numBars; i++) {
    const barHeight = Math.random() * (canvas.height - 10) + 10;
    const hue = (i / numBars) * 280;
    ctx.fillStyle = `hsl(${hue}, 90%, 55%)`;
    ctx.fillRect(i * barWidth, canvas.height - barHeight, barWidth - 2, barHeight);
  }

// 31. Multi-Agency Live Encrypted Chat & Dispatch Bridge
function toggleInterAgencyChat() {
  let dock = document.getElementById('inter-agency-chat-dock');
  if (!dock) {
    dock = document.createElement('div');
    dock.id = 'inter-agency-chat-dock';
    dock.style.cssText = `
      position: fixed;
      bottom: 75px;
      right: 24px;
      width: 340px;
      height: 420px;
      background: #0A1128;
      border: 1px solid #1E293B;
      border-radius: 12px;
      box-shadow: 0 15px 40px rgba(0,0,0,0.5);
      z-index: 99999;
      display: flex;
      flex-direction: column;
      font-family: var(--font-sans);
      overflow: hidden;
    `;

    dock.innerHTML = `
      <div style="background:#0F1D38; padding:10px 14px; border-bottom:1px solid #1E293B; display:flex; justify-content:space-between; align-items:center; color:#FFFFFF;">
        <div style="display:flex; align-items:center; gap:6px; font-weight:800; font-size:12px;">
          <span style="width:8px; height:8px;  background:#10B981;"></span>
          💬 Inter-Agency Defense Bridge
        </div>
        <button onclick="document.getElementById('inter-agency-chat-dock').style.display='none'" style="background:transparent; border:none; color:#94A3B8; cursor:pointer; font-size:16px;">&times;</button>
      </div>

      <div id="chat-messages-box" style="flex:1; padding:12px; overflow-y:auto; font-size:11px; display:flex; flex-direction:column; gap:8px; font-family:var(--font-mono); color:#E2E8F0;">
        <div style="background:#1E293B; padding:8px; border-radius:6px; border-left:3px solid #38BDF8;">
          <strong style="color:#38BDF8;">[POLICE CAD 21:46]</strong> Target ATM identified: Connaught Place SBI. Patrol Eagle 4 dispatched.
        </div>
        <div style="background:#1E293B; padding:8px; border-radius:6px; border-left:3px solid #34D399;">
          <strong style="color:#34D399;">[SBI FRM NODAL 21:46]</strong> ISO 20022 camt.056 hold locked on ₹2.5L in 118.2ms.
        </div>
        <div style="background:#1E293B; padding:8px; border-radius:6px; border-left:3px solid #F59E0B;">
          <strong style="color:#F59E0B;">[DoT CEIR 21:47]</strong> Handset IMEI 864910281920194 blacklisted across all 4 TSPs.
        </div>
      </div>

      <div style="padding:10px; border-top:1px solid #1E293B; background:#07152B; display:flex; gap:6px;">
        <input type="text" id="inter-agency-input" placeholder="Type encrypted message..." style="flex:1; background:#0F1D38; border:1px solid #1E293B; border-radius:4px; padding:6px 10px; color:#FFFFFF; font-size:11px; font-family:var(--font-mono); outline:none;" onkeydown="if(event.key==='Enter') sendInterAgencyMessage()" />
        <button onclick="sendInterAgencyMessage()" class="btn-hero-primary" style="font-size:11px; padding:4px 10px;">Send</button>
      </div>
    `;
    document.body.appendChild(dock);
  } else {
    dock.style.display = dock.style.display === 'none' ? 'flex' : 'none';
  }
}

function sendInterAgencyMessage() {
  const input = document.getElementById('inter-agency-input');
  const box = document.getElementById('chat-messages-box');
  if (!input || !box || !input.value.trim()) return;

  const msg = input.value.trim();
  const div = document.createElement('div');
  div.style.cssText = "background:#1E293B; padding:8px; border-radius:6px; border-left:3px solid #10B981;";
  div.innerHTML = `<strong style="color:#10B981;">[OFFICER ACTIVE]</strong> ${msg}`;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
  input.value = '';
  playCyberAudioAlert('success');
}

// 32. Live Holographic Emergency Incident Ticker Tape Banner
function injectEmergencyIncidentTicker() {
  if (document.getElementById('emergency-incident-ticker')) return;

  const ticker = document.createElement('div');
  ticker.id = 'emergency-incident-ticker';
  ticker.style.cssText = `
    background: #050B14;
    color: #38BDF8;
    border-bottom: 1px solid #1E293B;
    padding: 6px 16px;
    font-family: var(--font-mono);
    font-size: 11px;
    display: flex;
    align-items: center;
    overflow: hidden;
    white-space: nowrap;
    position: relative;
    z-index: 9999;
  `;

  ticker.innerHTML = `
    <div style="background:var(--gov-red); color:#FFFFFF; padding:2px 8px; border-radius:4px; font-weight:800; margin-right:12px; font-size:10px; display:inline-flex; align-items:center; gap:4px;">
      <span style="width:6px; height:6px;  background:#FFFFFF; animation:blink 1s infinite;"></span>
      LIVE INTELLIGENCE FEED
    </div>
    <marquee scrollamount="6" style="flex:1;">
      🚨 [NEW DELHI PCR 21:52] Suspect ATM Intercept Active at Connaught Place SBI • 🔒 [SBI FRM 21:52] ISO 20022 camt.056 Micro-Hold Locked on ₹2,50,000 in 118.2ms • 🚫 [DoT CEIR 21:51] Handset IMEI 864910281920194 Blacklisted on 4 TSPs • ⚖️ [SPECIAL CYBER COURT 21:50] Section 106 BNSS Reverse Restitution Decree Sealed on Polygon Amoy Blockchain • 🛡️ [1930 HELPLINE 21:49] Case DURGAM-DE-8278 Ingested & GNN Weights Updated
    </marquee>
  `;

  document.body.insertBefore(ticker, document.body.firstChild);
}

// Auto-mount ticker tape on all war rooms
document.addEventListener('DOMContentLoaded', () => {
  injectEmergencyIncidentTicker();
});













