// DURGAM Sovereign Script Engine & Cross-Portal Reactive Sync Bus

const API_BASE_URL = window.location.origin;

// ROLE-BASED NAVIGATION SCHEMA
const ROLE_NAV_SCHEMA = {
    citizen: {
        portalUrl: "citizen.html",
        features: [
            { label: "Express Report", targetTab: "report" },
            { label: "Live Tracker", targetTab: "tracker" },
            { label: "My Complaints", targetTab: "mycomplaints" },
            { label: "1-Tap Unblock Desk", targetTab: "unblock" }
        ]
    },
    user: {
        portalUrl: "citizen.html",
        features: [
            { label: "Express Report", targetTab: "report" },
            { label: "Live Tracker", targetTab: "tracker" },
            { label: "My Complaints", targetTab: "mycomplaints" },
            { label: "1-Tap Unblock Desk", targetTab: "unblock" }
        ]
    },
    bank: {
        portalUrl: "bank.html",
        features: [
            { label: "ZK Mule Registry", targetTab: "zk" },
            { label: "ISO 20022 Holds", targetTab: "holds" },
            { label: "Statement Upload", targetTab: "upload" },
            { label: "Submitted Data", targetTab: "accounts" },
            { label: "Transfer Chains", targetTab: "chains" }
        ]
    },
    command: {
        portalUrl: "command.html",
        features: [
            { label: "Dashboard", targetTab: "dashboard" },
            { label: "ATM Cashout Radar", targetTab: "radar" },
            { label: "All Complaints", targetTab: "complaints" },
            { label: "Transfer Chains", targetTab: "chains" },
            { label: "Bank Records", targetTab: "bankdata" },
            { label: "Analytics", targetTab: "analytics" }
        ]
    },
    i4c: {
        portalUrl: "command.html",
        features: [
            { label: "Dashboard", targetTab: "dashboard" },
            { label: "ATM Cashout Radar", targetTab: "radar" },
            { label: "All Complaints", targetTab: "complaints" },
            { label: "Transfer Chains", targetTab: "chains" },
            { label: "Bank Records", targetTab: "bankdata" },
            { label: "Analytics", targetTab: "analytics" }
        ]
    },
    police: {
        portalUrl: "police.html",
        features: [
            { label: "Hotspot Radar", action: "window.scrollTo({top: 0, behavior: 'smooth'})" },
            { label: "CAD Dispatch", action: "if(typeof triggerPatrolDispatch==='function') triggerPatrolDispatch('ATM_SBI_101')" }
        ]
    },
    judiciary: {
        portalUrl: "judiciary.html",
        features: [
            { label: "Section 63 BSA Vault", action: "window.scrollTo({top: 0, behavior: 'smooth'})" },
            { label: "Issue Restitution Decree", action: "if(typeof issueRestitutionOrder==='function') issueRestitutionOrder('NCRP-1930-48291048')" }
        ]
    },
    court: {
        portalUrl: "judiciary.html",
        features: [
            { label: "Section 63 BSA Vault", action: "window.scrollTo({top: 0, behavior: 'smooth'})" },
            { label: "Issue Restitution Decree", action: "if(typeof issueRestitutionOrder==='function') issueRestitutionOrder('NCRP-1930-48291048')" }
        ]
    }
};

function getLoggedInUser() {
    try {
        const u = localStorage.getItem("durgam_user");
        return u ? JSON.parse(u) : null;
    } catch(e) {
        return null;
    }
}

function getAuthToken() {
    return localStorage.getItem("durgam_token") || "";
}

function getAuthHeaders() {
    const headers = { "Content-Type": "application/json" };
    const token = getAuthToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

// ALL OPERATIONAL & INFORMATIONAL PORTAL PAGES FOR TOP NAVIGATION
const TOP_PORTAL_LINKS = [
    { name: "Home", href: "index.html", match: ["index.html", ""] },
    { name: "Citizen", href: "citizen.html", match: ["citizen.html"] },
    { name: "Bank", href: "bank.html", match: ["bank.html"] },
    { name: "Police", href: "police.html", match: ["police.html"] },
    { name: "Court", href: "judiciary.html", match: ["judiciary.html"] },
    { name: "Official Portal", href: "command.html", match: ["command.html"] },
    { name: "Evidence Vault", href: "verify.html", match: ["verify.html"] },
    { name: "About", href: "about.html", match: ["about.html"] }
];

// RENDER UNIFIED CONTEXTUAL NAVBAR FOR LOGGED-IN OFFICER & PORTAL
function renderGlobalNavbar() {
    const navLinks = document.querySelector(".nav-links");
    const navRight = document.querySelector(".nav-right");
    if (!navLinks || !navRight) return;

    const user = getLoggedInUser();
    const currentPath = window.location.pathname.split("/").pop() || "index.html";

    // 1. AUTHENTICATION PAGES (login.html, register.html)
    if (currentPath === "login.html" || currentPath === "register.html") {
        navLinks.innerHTML = `
            <span style="font-size:11px; color:#5c8000; font-weight:700; display:flex; align-items:center; gap:6px; letter-spacing:0.5px;">
                <i data-lucide="lock" style="width:13px; height:13px;"></i> SECURE 256-BIT ENCRYPTED GATEWAY
            </span>
        `;
        navRight.innerHTML = `
            <a href="index.html" class="outline-btn" style="height:36px; padding:0 14px; font-size:12px; display:inline-flex; align-items:center; gap:6px;">
                <i data-lucide="arrow-left"></i> Return to Home
            </a>
        `;
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
        }
        return;
    }

    // 2. OFFICER PORTAL NAVBAR SPECIFICATION (Clean, official government titles)
    const portalTitles = {
        "bank.html": { name: "Bank Nodal Desk", role: "Account Freeze & Lien Management (Sec 106 BNSS)" },
        "citizen.html": { name: "Citizen Reporting Desk", role: "CFCFRMS / 1930 Helpline Desk" },
        "command.html": { name: "I4C National Command", role: "National Cybercrime Operations Center" },
        "police.html": { name: "State Police Cyber Command", role: "ERSS 112 / PCR Field Intercept Desk" },
        "judiciary.html": { name: "Judicial Magistrate Bench", role: "Section 106 BNSS Restitution Desk" },
        "verify.html": { name: "Digital Evidence Vault", role: "Section 63 BSA 2023 Certificate Verification" }
    };

    if (portalTitles[currentPath]) {
        // Render high-level portal switcher and operational status badge (no duplicate internal tabs)
        navLinks.innerHTML = `
            <div style="display:flex; align-items:center; gap:16px; font-size:12.5px; font-weight:600; color:#626b70;">
                <span style="color:#111820; font-weight:700; display:flex; align-items:center; gap:8px;">
                    <span class="pulse-dot-lime" style="width:8px; height:8px; border-radius:50%; background:#0b6b32; box-shadow:0 0 0 2px rgba(11,107,50,0.2);"></span>
                    ${portalTitles[currentPath].name}
                </span>
                <span style="color:#deddd7;">|</span>
                <span style="font-size:11px; color:#0b6b32; font-family:'DM Sans',sans-serif; font-weight:700; letter-spacing:0.4px; background:rgba(11,107,50,0.08); border:1px solid rgba(11,107,50,0.2); padding:3px 10px; border-radius:20px;">
                    <i data-lucide="shield-check" style="width:12px; height:12px; display:inline-block; vertical-align:middle; margin-right:4px;"></i>SOVEREIGN GRID ACTIVE • 89ms
                </span>
            </div>
        `;

        navRight.innerHTML = `
            <a href="index.html" class="outline-btn" style="height:34px; padding:0 12px; font-size:12px; display:inline-flex; align-items:center; gap:6px; color:#111820; border:1.5px solid #deddd7; background:#ffffff;">
                <i data-lucide="home"></i> Home
            </a>
            ${user ? `
                <span class="portal-btn" style="cursor: default; border: 1.5px solid #deddd7; height: 34px; padding: 0 12px; font-size:12px; white-space: nowrap; background:#f7f6f1; color:#111820;">
                    <i data-lucide="shield-check" style="color:#0b6b32;"></i>
                    <span>${user.name || user.email || user.id} <small style="color:#0b6b32; text-transform:uppercase; font-weight:700;">(${user.role || 'Officer'})</small></span>
                </span>
                <button onclick="handleUserLogout()" class="outline-btn" style="height: 34px; padding: 0 12px; font-size: 12px; color: #dc2626; border: 1.5px solid rgba(220,38,38,0.3); background:#ffffff; display:inline-flex; align-items:center; gap:6px;" title="Logout and Switch Portal">
                    <i data-lucide="log-out"></i> Logout
                </button>
            ` : `
                <a href="login.html" class="primary-btn" style="height:34px; padding:0 14px; font-size:12px;">
                    <i data-lucide="shield"></i> Sign In
                </a>
            `}
        `;
        if (typeof lucide !== 'undefined' && lucide.createIcons) {
            lucide.createIcons();
        }
        return;
    }

    // 3. PUBLIC LANDING & INFORMATIONAL PAGES (index.html, about.html, resources.html, contact.html)
    if (currentPath === "index.html" || currentPath === "") {
        navLinks.innerHTML = `
            <a href="index.html" class="active">Home</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#estimator">Recovery Calculator</a>
            <a href="#portals">Access Portals</a>
            <a href="about.html">About</a>
        `;
    } else {
        navLinks.innerHTML = `
            <a href="index.html">Home</a>
            <a href="index.html#portals">Portals</a>
            <a href="resources.html" class="${currentPath === 'resources.html' ? 'active' : ''}">Resources</a>
            <a href="contact.html" class="${currentPath === 'contact.html' ? 'active' : ''}">Contact</a>
            <a href="about.html" class="${currentPath === 'about.html' ? 'active' : ''}">About</a>
        `;
    }

    navRight.innerHTML = `
        ${user ? `
            <span class="portal-btn" style="cursor: default; border: 1.5px solid #deddd7; height: 38px; background:#f7f6f1; color:#111820;">
                <i data-lucide="user-check" style="color:#0b6b32;"></i>
                <span>${user.name || user.email || user.id} <small style="color:#0b6b32; text-transform:uppercase; font-weight:700;">(${user.role || 'Officer'})</small></span>
            </span>
            <button onclick="handleUserLogout()" class="outline-btn" style="height: 38px; padding: 0 14px; font-size: 12px; color: #dc2626; border: 1.5px solid rgba(220,38,38,0.3); background:#ffffff; display:inline-flex; align-items:center; gap:6px;" title="Sign Out">
                <i data-lucide="log-out"></i> Logout
            </button>
        ` : `
            <a href="login.html" class="portal-btn">
                <i data-lucide="shield"></i>
                <span>Official / Citizen Login</span>
            </a>
        `}
    `;

    if (typeof lucide !== 'undefined' && lucide.createIcons) {
        lucide.createIcons();
    }
}

document.addEventListener("DOMContentLoaded", () => {
    renderGlobalNavbar();
    if (typeof lucide !== 'undefined' && lucide.createIcons) {
        lucide.createIcons();
    }
});

function handleUserLogout() {
    localStorage.removeItem('durgam_user');
    localStorage.removeItem('durgam_token');
    window.location.href = 'login.html';
}

// =========================================================================
// CROSS-PORTAL REACTIVE EVENT BUS & STATE SYNCHRONIZER
// =========================================================================
class DurgamSyncBus {
    constructor() {
        this.listeners = {};
        this.broadcastChannel = null;
        try {
            this.broadcastChannel = new BroadcastChannel('durgam_sovereign_bus');
            this.broadcastChannel.onmessage = (event) => {
                const { type, payload } = event.data || {};
                this._dispatchLocal(type, payload);
            };
        } catch (e) {
            console.warn("BroadcastChannel unsupported, using localStorage fallback sync");
        }

        window.addEventListener('storage', (e) => {
            if (e.key === 'durgam_last_event') {
                try {
                    const evt = JSON.parse(e.newValue);
                    if (evt && evt.type) {
                        this._dispatchLocal(evt.type, evt.payload);
                    }
                } catch(err) {}
            }
        });
    }

    on(eventType, callback) {
        if (!this.listeners[eventType]) {
            this.listeners[eventType] = [];
        }
        this.listeners[eventType].push(callback);
    }

    emit(eventType, payload = {}) {
        // 1. Dispatch locally
        this._dispatchLocal(eventType, payload);

        // 2. Broadcast via BroadcastChannel
        if (this.broadcastChannel) {
            this.broadcastChannel.postMessage({ type: eventType, payload });
        }

        // 3. Broadcast via storage event for multi-tab support
        localStorage.setItem('durgam_last_event', JSON.stringify({
            type: eventType,
            payload,
            timestamp: Date.now()
        }));
    }

    _dispatchLocal(eventType, payload) {
        const cbs = this.listeners[eventType] || [];
        cbs.forEach(cb => {
            try { cb(payload); } catch(err) { console.error("Sync bus dispatch error:", err); }
        });
        // Also fire wildcard listeners
        const wildcards = this.listeners["*"] || [];
        wildcards.forEach(cb => {
            try { cb(eventType, payload); } catch(err) {}
        });
    }

    // Shared State Helpers
    getStoredComplaints() {
        const DEFAULT_5_COMPLAINTS = [
            {
                case_id: "DURGAM-DL-7782",
                ack_number: "NCRP-1930-77821940",
                complaint_id: "NCRP-1930-77821940",
                victim_name: "Ritik Singh",
                victim_phone: "9811029481",
                victim_city: "Delhi NCR",
                victim_state: "Delhi",
                utr_number: "582910481920",
                source_bank: "State Bank of India",
                source_account: "XXXX-XXXX-2948",
                suspect_account: "902148102941",
                loss_amount: 350000.0,
                amount: 350000.0,
                crime_category: "DIGITAL_ARREST",
                fraud_type: "Digital Arrest",
                narrative: "Counterfeit video call from fake law enforcement threatening digital arrest. Victim coerced into depositing funds into mule escrow.",
                status: "MICRO_HOLD_PLACED",
                hold_status: "ACTIVE_30_MIN_HOLD",
                execution_latency_ms: 89.2,
                filed_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
                created_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
                candidate_atms: [
                    { name: "SBI ATM Sector 29 Market", bank_name: "SBI ATM Sector 29", address: "Sector 29 Market, Gurugram", lat: 28.4595, lon: 77.0266, eta_minutes: 3, risk_score: "96.5%" }
                ],
                terminal_node: {
                    account_id: "ACC_MULE_9021",
                    masked_account: "902148102941",
                    bank_name: "Punjab National Bank",
                    ifsc: "PUNB0001024",
                    region: "Sector 29, Gurugram",
                    state: "Haryana",
                    latitude: 28.4595,
                    longitude: 77.0266,
                    atm_name: "SBI ATM Sector 29 Market"
                },
                evidence_certificate: {
                    sha256_case_hash: "0x7a8f9c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90",
                    merkle_root: "0x7a8f9c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90",
                    polygon_tx_hash: "0x4a920194810248a1c92847190284719284719284719284719284719284719284",
                    block_number: 4920194
                }
            },
            {
                case_id: "DURGAM-HR-6648",
                ack_number: "NCRP-1930-66481029",
                complaint_id: "NCRP-1930-66481029",
                victim_name: "Deepak Verma",
                victim_phone: "9822019482",
                victim_city: "Gurugram",
                victim_state: "Haryana",
                utr_number: "774102981234",
                source_bank: "HDFC Bank",
                source_account: "XXXX-XXXX-8812",
                suspect_account: "482910481024",
                loss_amount: 210000.0,
                amount: 210000.0,
                crime_category: "PART_TIME_JOB",
                fraud_type: "Part-Time Task Scam",
                narrative: "Telegram group promised high returns on hotel reviews. Funds layered through 3 mule hops within 6 minutes.",
                status: "MICRO_HOLD_PLACED",
                hold_status: "ACTIVE_30_MIN_HOLD",
                execution_latency_ms: 78.4,
                filed_at: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
                created_at: new Date(Date.now() - 1000 * 60 * 35).toISOString(),
                candidate_atms: [
                    { name: "HDFC Bank ATM Laxmi Nagar", bank_name: "HDFC ATM Laxmi Nagar", address: "Laxmi Nagar Metro, New Delhi", lat: 28.6304, lon: 77.2773, eta_minutes: 5, risk_score: "94.2%" }
                ],
                terminal_node: {
                    account_id: "ACC_MULE_4829",
                    masked_account: "482910481024",
                    bank_name: "ICICI Bank Ltd",
                    ifsc: "ICIC0002941",
                    region: "Laxmi Nagar, Delhi",
                    state: "Delhi",
                    latitude: 28.6304,
                    longitude: 77.2773,
                    atm_name: "HDFC Bank ATM Laxmi Nagar"
                },
                evidence_certificate: {
                    sha256_case_hash: "0x6b8c2d1a4e3f5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
                    merkle_root: "0x6b8c2d1a4e3f5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
                    polygon_tx_hash: "0x3b81928471928471928471928471928471928471928471928471928471928471",
                    block_number: 4920195
                }
            },
            {
                case_id: "DURGAM-KA-5591",
                ack_number: "NCRP-1930-55910248",
                complaint_id: "NCRP-1930-55910248",
                victim_name: "Suhani Sharma",
                victim_phone: "9833019483",
                victim_city: "Bengaluru",
                victim_state: "Karnataka",
                utr_number: "661029481233",
                source_bank: "ICICI Bank",
                source_account: "XXXX-XXXX-3341",
                suspect_account: "551029841923",
                loss_amount: 185000.0,
                amount: 185000.0,
                crime_category: "FAKE_LOAN_APP",
                fraud_type: "Fake Loan App",
                narrative: "Predatory instant loan app accessed contacts and blackmailed victim. Auto-lien locked terminal mule.",
                status: "MICRO_HOLD_PLACED",
                hold_status: "ACTIVE_30_MIN_HOLD",
                execution_latency_ms: 94.1,
                filed_at: new Date(Date.now() - 1000 * 60 * 55).toISOString(),
                created_at: new Date(Date.now() - 1000 * 60 * 55).toISOString(),
                candidate_atms: [
                    { name: "Axis Bank ATM Indiranagar", bank_name: "Axis Bank ATM", address: "100ft Road, Indiranagar, Bengaluru", lat: 12.9784, lon: 77.6408, eta_minutes: 6, risk_score: "91.8%" }
                ],
                terminal_node: {
                    account_id: "ACC_MULE_5510",
                    masked_account: "551029841923",
                    bank_name: "Canara Bank",
                    ifsc: "CNRB0008819",
                    region: "Indiranagar, Bengaluru",
                    state: "Karnataka",
                    latitude: 12.9784,
                    longitude: 77.6408,
                    atm_name: "Axis Bank ATM Indiranagar"
                },
                evidence_certificate: {
                    sha256_case_hash: "0x5c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d",
                    merkle_root: "0x5c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d",
                    polygon_tx_hash: "0x2c71928471928471928471928471928471928471928471928471928471928471",
                    block_number: 4920196
                }
            },
            {
                case_id: "DURGAM-MH-4482",
                ack_number: "NCRP-1930-44820194",
                complaint_id: "NCRP-1930-44820194",
                victim_name: "Himanshi Rawat",
                victim_phone: "9844019484",
                victim_city: "Mumbai",
                victim_state: "Maharashtra",
                utr_number: "229481029344",
                source_bank: "Punjab National Bank",
                source_account: "XXXX-XXXX-9901",
                suspect_account: "882019481022",
                loss_amount: 420000.0,
                amount: 420000.0,
                crime_category: "INVESTMENT_SCAM",
                fraud_type: "Investment Scam",
                narrative: "Fake institutional trading portal showing fabricated profits. Quarantined in PNB clearing switch within 89ms.",
                status: "MICRO_HOLD_PLACED",
                hold_status: "ACTIVE_30_MIN_HOLD",
                execution_latency_ms: 86.7,
                filed_at: new Date(Date.now() - 1000 * 60 * 75).toISOString(),
                created_at: new Date(Date.now() - 1000 * 60 * 75).toISOString(),
                candidate_atms: [
                    { name: "ICICI Bank ATM Nariman Point", bank_name: "ICICI ATM Nariman Point", address: "Nariman Point, South Mumbai", lat: 18.9256, lon: 72.8242, eta_minutes: 4, risk_score: "95.0%" }
                ],
                terminal_node: {
                    account_id: "ACC_MULE_8820",
                    masked_account: "882019481022",
                    bank_name: "Bank of Baroda",
                    ifsc: "BARB0NARIMA",
                    region: "Nariman Point, Mumbai",
                    state: "Maharashtra",
                    latitude: 18.9256,
                    longitude: 72.8242,
                    atm_name: "ICICI Bank ATM Nariman Point"
                },
                evidence_certificate: {
                    sha256_case_hash: "0x4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c",
                    merkle_root: "0x4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c",
                    polygon_tx_hash: "0x1b61928471928471928471928471928471928471928471928471928471928471",
                    block_number: 4920197
                }
            },
            {
                case_id: "DURGAM-JK-3371",
                ack_number: "NCRP-1930-33719028",
                complaint_id: "NCRP-1930-33719028",
                victim_name: "Eklavya Dhruv Malhotra",
                victim_phone: "9855019485",
                victim_city: "Jammu",
                victim_state: "Jammu & Kashmir",
                utr_number: "339102948110",
                source_bank: "Axis Bank",
                source_account: "XXXX-XXXX-6623",
                suspect_account: "771029481944",
                loss_amount: 290000.0,
                amount: 290000.0,
                crime_category: "AEPS_FRAUD",
                fraud_type: "AePS Biometric Scam",
                narrative: "Unauthorized biometric cashout alert triggered at Jammu corridor CSP kiosk. PCR Falcon 1 dispatched.",
                status: "MICRO_HOLD_PLACED",
                hold_status: "ACTIVE_30_MIN_HOLD",
                execution_latency_ms: 91.3,
                filed_at: new Date(Date.now() - 1000 * 60 * 95).toISOString(),
                created_at: new Date(Date.now() - 1000 * 60 * 95).toISOString(),
                candidate_atms: [
                    { name: "J&K Bank ATM Residency Road", bank_name: "J&K Bank ATM", address: "Residency Road, Jammu", lat: 32.7266, lon: 74.8570, eta_minutes: 3, risk_score: "97.4%" }
                ],
                terminal_node: {
                    account_id: "ACC_MULE_7710",
                    masked_account: "771029481944",
                    bank_name: "J&K Bank Ltd",
                    ifsc: "JAKO0RESIDN",
                    region: "Residency Road, Jammu",
                    state: "Jammu & Kashmir",
                    latitude: 32.7266,
                    longitude: 74.8570,
                    atm_name: "J&K Bank ATM Residency Road"
                },
                evidence_certificate: {
                    sha256_case_hash: "0x3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b",
                    merkle_root: "0x3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b",
                    polygon_tx_hash: "0x0a51928471928471928471928471928471928471928471928471928471928471",
                    block_number: 4920198
                }
            }
        ];

        try {
            const raw = localStorage.getItem("durgam_complaints");
            let list = raw ? JSON.parse(raw) : [];
            // Merge defaults if not present
            DEFAULT_5_COMPLAINTS.forEach(def => {
                const exists = list.some(item => item.ack_number === def.ack_number || item.case_id === def.case_id);
                if (!exists) {
                    list.push(def);
                }
            });
            localStorage.setItem("durgam_complaints", JSON.stringify(list));
            return list;
        } catch(e) {
            return DEFAULT_5_COMPLAINTS;
        }
    }

    saveComplaint(complaint) {
        const list = this.getStoredComplaints();
        const existingIdx = list.findIndex(c => c.ack_number === complaint.ack_number || c.complaint_id === complaint.complaint_id);
        if (existingIdx >= 0) {
            list[existingIdx] = { ...list[existingIdx], ...complaint };
        } else {
            list.unshift(complaint);
        }
        localStorage.setItem("durgam_complaints", JSON.stringify(list));
        this.emit("COMPLAINT_FILED", complaint);
    }

    updateCaseStatus(caseId, status, extra = {}) {
        const list = this.getStoredComplaints();
        const found = list.find(c => c.ack_number === caseId || c.complaint_id === caseId || c.case_id === caseId);
        if (found) {
            found.status = status;
            Object.assign(found, extra);
            localStorage.setItem("durgam_complaints", JSON.stringify(list));
        }
        this.emit("CASE_STATUS_UPDATED", { caseId, status, ...extra });
    }
}

window.DurgamSync = new DurgamSyncBus();

// =========================================================================
// REAL-TIME NOTIFICATION SOUND & HUD TOAST ENGINE
// =========================================================================

function playSovereignAlertChime(urgency = 'normal') {
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        if (ctx.state === 'suspended') {
            ctx.resume();
        }
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'sine';
        if (urgency === 'urgent' || urgency === 'police' || urgency === 'danger') {
            osc.frequency.setValueAtTime(587.33, now); // D5
            osc.frequency.setValueAtTime(880.00, now + 0.1); // A5
            osc.frequency.setValueAtTime(1174.66, now + 0.2); // D6
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.55);
        } else {
            osc.frequency.setValueAtTime(523.25, now); // C5
            osc.frequency.setValueAtTime(783.99, now + 0.12); // G5
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.45);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now);
            osc.stop(now + 0.45);
        }
    } catch(e) {
        // AudioContext silent fallback
    }
}

function showDepartmentNotificationToast(title, message, options = {}) {
    playSovereignAlertChime(options.urgency || options.type || 'normal');

    let container = document.getElementById('durgam-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'durgam-toast-container';
        container.style.cssText = `
            position: fixed;
            top: 24px;
            right: 24px;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 420px;
            width: calc(100% - 48px);
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }

    const typeConfig = {
        police: { icon: '🚨', label: 'POLICE PCR CAD ALERT', border: '#ff3d3d', bg: '#111317', badge: '#ff3d3d' },
        bank: { icon: '🔒', label: 'BANK PRE-SETTLEMENT HOLD', border: '#f59e0b', bg: '#111317', badge: '#f59e0b' },
        court: { icon: '⚖️', label: 'CYBER COURT DOCKET', border: '#00e676', bg: '#080e0b', badge: '#00e676' },
        judiciary: { icon: '⚖️', label: 'CYBER COURT DOCKET', border: '#00e676', bg: '#080e0b', badge: '#00e676' },
        command: { icon: '⚡', label: 'I4C COMMAND INTELLIGENCE', border: '#00e676', bg: '#080e0b', badge: '#00e676' },
        i4c: { icon: '⚡', label: 'I4C COMMAND INTELLIGENCE', border: '#00e676', bg: '#080e0b', badge: '#00e676' },
        citizen: { icon: '🛡️', label: 'CITIZEN RAPID INTERCEPT', border: '#00e676', bg: '#080e0b', badge: '#00e676' }
    };

    const cfg = typeConfig[options.type] || typeConfig.command;

    const toast = document.createElement('div');
    toast.style.cssText = `
        pointer-events: auto;
        background: rgba(10, 14, 18, 0.95);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1.5px solid ${cfg.border};
        box-shadow: 0 16px 36px rgba(0,0,0,0.5), 0 0 20px ${cfg.border}33;
        border-radius: 14px;
        padding: 16px 18px;
        color: #ffffff;
        font-family: 'DM Sans', -apple-system, sans-serif;
        display: flex;
        flex-direction: column;
        gap: 8px;
        animation: durgamSlideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    `;

    toast.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:16px;">${cfg.icon}</span>
                <span style="font-size:10px; font-weight:800; letter-spacing:0.8px; color:${cfg.badge}; text-transform:uppercase;">${cfg.label}</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:10.5px; color:#889096;">Just Now</span>
                <button type="button" style="background:none; border:none; color:#889096; cursor:pointer; font-size:16px; line-height:1; padding:0 4px;" onclick="this.closest('#durgam-toast-container > div').remove()">×</button>
            </div>
        </div>
        <div style="font-size:13.5px; font-weight:700; color:#ffffff; line-height:1.35;">${title}</div>
        <div style="font-size:12px; color:#b5bcc0; line-height:1.45;">${message}</div>
        ${options.actionLabel ? `
            <div style="margin-top:4px; display:flex; justify-content:flex-end;">
                <button type="button" style="background:${cfg.border}; color:#050708; border:none; border-radius:6px; padding:6px 12px; font-size:11px; font-weight:700; cursor:pointer; font-family:inherit;" onclick="${options.actionClick || ''}; this.closest('#durgam-toast-container > div').remove();">
                    ${options.actionLabel}
                </button>
            </div>
        ` : ''}
    `;

    container.appendChild(toast);

    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';
            setTimeout(() => toast.remove(), 400);
        }
    }, options.duration || 6500);
}

// Inject CSS keyframes for smooth toast transitions
if (!document.getElementById('durgam-toast-keyframes')) {
    const style = document.createElement('style');
    style.id = 'durgam-toast-keyframes';
    style.innerHTML = `
        @keyframes durgamSlideIn {
            from { opacity: 0; transform: translateX(40px) scale(0.96); }
            to { opacity: 1; transform: translateX(0) scale(1); }
        }
        @keyframes durgamBarrierFadeIn {
            from { opacity: 0; transform: scale(0.97); }
            to { opacity: 1; transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
}

// =========================================================================
// DEPARTMENTAL ACCESS BARRIER & ROLE ISOLATION (RBAC)
// =========================================================================

function enforcePortalRoleAccess(options = {}) {
    const {
        allowedRoles = [],
        portalName = "Restricted Operations Portal",
        departmentName = "Official Department",
        defaultOfficer = null
    } = options;

    const user = getLoggedInUser();

    // 1. If not logged in at all:
    if (!user) {
        if (defaultOfficer) {
            localStorage.setItem('durgam_user', JSON.stringify(defaultOfficer));
            if (typeof renderGlobalNavbar === 'function') renderGlobalNavbar();
            return true;
        } else {
            window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname)}`;
            return false;
        }
    }

    // 2. If logged in, check role authorization
    const currentRole = (user.role || '').toLowerCase();
    const normalizedAllowed = allowedRoles.map(r => r.toLowerCase());

    if (normalizedAllowed.includes(currentRole)) {
        return true;
    }

    // 3. User is logged in under another department's authority! Enforce Isolation Barrier!
    showAccessBarrierModal({
        currentRole: user.role,
        currentUserName: user.name || user.email || user.id,
        portalName,
        departmentName,
        allowedRoles,
        defaultOfficer
    });
    return false;
}

function showAccessBarrierModal(info) {
    // Blur and deactivate background operational page
    const mainEl = document.querySelector('main') || document.body;
    if (mainEl) {
        mainEl.style.filter = 'blur(6px)';
        mainEl.style.pointerEvents = 'none';
        mainEl.style.userSelect = 'none';
    }

    let barrier = document.getElementById('durgam-access-barrier-overlay');
    if (!barrier) {
        barrier = document.createElement('div');
        barrier.id = 'durgam-access-barrier-overlay';
        barrier.style.cssText = `
            position: fixed;
            inset: 0;
            z-index: 1000000;
            background: rgba(5, 7, 8, 0.88);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        `;
        document.body.appendChild(barrier);
    }

    const rolePortalMap = {
        citizen: { name: 'Citizen Assistance Desk', url: 'citizen.html' },
        user: { name: 'Citizen Assistance Desk', url: 'citizen.html' },
        bank: { name: 'Bank Switch Portal', url: 'bank.html' },
        bank_officer: { name: 'Bank Switch Portal', url: 'bank.html' },
        police: { name: 'Police PCR War Room', url: 'police.html' },
        police_officer: { name: 'Police PCR War Room', url: 'police.html' },
        judiciary: { name: 'Cyber Court Bench', url: 'judiciary.html' },
        court: { name: 'Cyber Court Bench', url: 'judiciary.html' },
        judge: { name: 'Cyber Court Bench', url: 'judiciary.html' },
        command: { name: 'I4C Command Center', url: 'command.html' },
        i4c: { name: 'I4C Command Center', url: 'command.html' }
    };

    const myPortal = rolePortalMap[(info.currentRole || '').toLowerCase()] || { name: 'My Home Portal', url: 'index.html' };

    barrier.innerHTML = `
        <div style="background:#0e1317; border:2px solid #ef4444; box-shadow:0 24px 64px rgba(0,0,0,0.8), 0 0 32px rgba(239,68,68,0.25); border-radius:20px; max-width:560px; width:100%; padding:32px 30px; text-align:center; color:#ffffff; font-family:'DM Sans',-apple-system,sans-serif; animation:durgamBarrierFadeIn 0.3s ease;">
            <div style="width:64px; height:64px; border-radius:50%; background:rgba(239,68,68,0.12); border:1.5px solid rgba(239,68,68,0.4); display:flex; align-items:center; justify-content:center; margin:0 auto 18px; font-size:28px;">
                🛡️
            </div>
            <div style="font-size:11px; font-weight:800; letter-spacing:1.2px; color:#ef4444; text-transform:uppercase; margin-bottom:6px;">
                DEPARTMENTAL ISOLATION PROTOCOL • ACCESS DENIED
            </div>
            <h2 style="font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:700; margin:0 0 12px; color:#ffffff;">
                ${info.portalName}
            </h2>
            <p style="font-size:13.5px; color:#9ba3a9; line-height:1.5; margin:0 0 20px;">
                This terminal is strictly restricted to verified <strong>${info.departmentName}</strong> personnel. Cross-departmental interference and data manipulation are prohibited under the IT Act 2000 and Section 106 BNSS.
            </p>

            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px 18px; margin-bottom:24px; text-align:left; font-size:12.5px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#7b8285;">Currently Signed In:</span>
                    <strong style="color:#ffffff;">${info.currentUserName}</strong>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span style="color:#7b8285;">Your Active Authority:</span>
                    <span style="background:rgba(239,68,68,0.18); color:#ff6b6b; padding:2px 8px; border-radius:4px; font-weight:700; font-size:11px; text-transform:uppercase;">${info.currentRole}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#7b8285;">Required Role:</span>
                    <span style="background:rgba(0,230,118,0.18); color:#00e676; padding:2px 8px; border-radius:4px; font-weight:700; font-size:11px; text-transform:uppercase;">${info.allowedRoles.join(' / ')}</span>
                </div>
            </div>

            <div style="display:flex; flex-direction:column; gap:10px;">
                ${info.defaultOfficer ? `
                    <button type="button" id="durgam-btn-switch-role" style="background:#00e676; color:#040608; border:none; border-radius:10px; height:42px; font-weight:700; font-size:13px; cursor:pointer; font-family:inherit; display:flex; align-items:center; justify-content:center; gap:8px; box-shadow:0 0 20px rgba(0,230,118,0.35);">
                        <span>Switch to Authorized ${info.departmentName} Officer</span>
                    </button>
                ` : ''}
                <div style="display:flex; gap:10px;">
                    <a href="${myPortal.url}" style="flex:1; text-decoration:none; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.16); color:#ffffff; border-radius:10px; height:40px; font-weight:600; font-size:12px; display:flex; align-items:center; justify-content:center; gap:6px;">
                        Return to ${myPortal.name}
                    </a>
                    <button type="button" onclick="handleUserLogout()" style="flex:1; background:transparent; border:1px solid rgba(239,68,68,0.4); color:#ef4444; border-radius:10px; height:40px; font-weight:600; font-size:12px; cursor:pointer; font-family:inherit;">
                        Sign In with Different ID
                    </button>
                </div>
            </div>
        </div>
    `;

    const switchBtn = document.getElementById('durgam-btn-switch-role');
    if (switchBtn && info.defaultOfficer) {
        switchBtn.onclick = () => {
            localStorage.setItem('durgam_user', JSON.stringify(info.defaultOfficer));
            window.location.reload();
        };
    }
}

document.addEventListener('DOMContentLoaded', () => {
    renderGlobalNavbar();
    _initDurgamPlatformChecks();
});

// =========================================================================
// PRODUCTION INFRASTRUCTURE: API HEALTH MONITOR & CONNECTIVITY LAYER
// =========================================================================

let _backendOnline = true;
let _healthCheckInterval = null;

/**
 * Checks backend health and shows/hides offline banner.
 * Called on DOMContentLoaded and every 30 seconds.
 */
async function _checkBackendHealth() {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 4000);
        const res = await fetch(`${API_BASE_URL}/health`, { signal: controller.signal, cache: 'no-store' });
        clearTimeout(timer);
        if (res.ok) {
            if (!_backendOnline) {
                _backendOnline = true;
                _hideOfflineBanner();
                if (typeof showDepartmentNotificationToast === 'function') {
                    showDepartmentNotificationToast(
                        'Backend Connection Restored',
                        'DURGAM Sovereign API is back online. All data is live.',
                        { type: 'success', urgency: 'normal', duration: 4000 }
                    );
                }
            }
            return true;
        }
    } catch (_) { /* Offline */ }
    if (_backendOnline) {
        _backendOnline = false;
        _showOfflineBanner();
    }
    return false;
}

function _showOfflineBanner() {
    if (document.getElementById('durgam-offline-banner')) return;
    const banner = document.createElement('div');
    banner.id = 'durgam-offline-banner';
    banner.style.cssText = `
        position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        color: #fff; padding: 10px 20px; font-size: 12.5px; font-weight: 600;
        display: flex; align-items: center; justify-content: space-between;
        gap: 12px; font-family: 'DM Sans', -apple-system, sans-serif;
        border-bottom: 2px solid #dc2626; box-shadow: 0 4px 16px rgba(220,38,38,0.3);
        animation: durgamSlideDown 0.3s ease;
    `;
    banner.innerHTML = `
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="width:8px; height:8px; border-radius:50%; background:#fca5a5; animation:blink 1s step-start infinite;"></span>
            <strong>⚠️ Backend Offline:</strong>&nbsp;DURGAM API unreachable. Operating on cached / local data. Retrying automatically...
        </div>
        <button onclick="document.getElementById('durgam-offline-banner').remove()" style="background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); color:#fff; border-radius:6px; padding:4px 10px; cursor:pointer; font-size:11px; font-family:inherit;">Dismiss</button>
    `;

    // Inject blink keyframe if not present
    if (!document.getElementById('durgam-blink-kf')) {
        const s = document.createElement('style');
        s.id = 'durgam-blink-kf';
        s.textContent = `@keyframes blink{0%,100%{opacity:1}50%{opacity:0}} @keyframes durgamSlideDown{from{transform:translateY(-100%)}to{transform:translateY(0)}}`;
        document.head.appendChild(s);
    }
    document.body.prepend(banner);
}

function _hideOfflineBanner() {
    const b = document.getElementById('durgam-offline-banner');
    if (b) b.remove();
}

/**
 * Production-grade fetch wrapper with automatic auth headers, timeout, and retry.
 * Use this instead of raw fetch() for all API calls.
 * @param {string} endpoint - API endpoint path (e.g. '/api/v1/citizen/report-incident')
 * @param {object} options - fetch options (method, body, etc.)
 * @param {number} retries - number of retries on network failure (default 1)
 * @returns {Promise<any>} - parsed JSON response
 */
async function durgamFetch(endpoint, options = {}, retries = 1) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    const headers = {
        ...(typeof getAuthHeaders === 'function' ? getAuthHeaders() : { 'Content-Type': 'application/json' }),
        ...(options.headers || {})
    };
    const controller = new AbortController();
    const timeoutMs = options.timeout || 15000;
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const res = await fetch(url, {
            ...options,
            headers,
            signal: controller.signal
        });
        clearTimeout(timer);
        if (!res.ok) {
            const errText = await res.text().catch(() => '');
            throw new Error(`HTTP ${res.status}: ${errText.slice(0, 200)}`);
        }
        return await res.json();
    } catch (err) {
        clearTimeout(timer);
        if (retries > 0 && err.name !== 'AbortError') {
            await new Promise(r => setTimeout(r, 1000));
            return durgamFetch(endpoint, options, retries - 1);
        }
        throw err;
    }
}

/**
 * Sync real DB incidents into the local DurgamSync cache on page load.
 * This ensures all portals see actual stored data even without explicit fetch calls.
 */
async function _syncDbToLocalCache() {
    try {
        const data = await durgamFetch('/api/v1/citizen/cases-summary', {}, 0);
        if (data && data.cases && Array.isArray(data.cases) && data.cases.length > 0 && window.DurgamSync) {
            const existing = window.DurgamSync.getStoredComplaints().map(c => c.ack_number);
            let added = 0;
            for (const c of data.cases) {
                if (!existing.includes(c.ack_number)) {
                    // Don't emit events for initial DB load — just populate silently
                    const list = window.DurgamSync.getStoredComplaints();
                    if (!list.find(x => x.ack_number === c.ack_number)) {
                        list.unshift(c);
                        try { localStorage.setItem('durgam_complaints', JSON.stringify(list)); } catch(_) {}
                        added++;
                    }
                }
            }
            if (added > 0) {
                console.info(`[DURGAM] Synced ${added} live DB records into local cache.`);
            }
        }
    } catch (_) {
        // Silently fail — local cache will be used
    }
}

/**
 * Master platform initialization — called on every page load.
 */
async function _initDurgamPlatformChecks() {
    // 1. Check API health and show banner if offline
    await _checkBackendHealth();

    // 2. Sync DB incidents to local cache (background)
    setTimeout(_syncDbToLocalCache, 500);

    // 3. Periodic health polling every 30 seconds
    if (_healthCheckInterval) clearInterval(_healthCheckInterval);
    _healthCheckInterval = setInterval(_checkBackendHealth, 30000);
}

/**
 * 3D Spatial Parallax Tilt Engine
 * Provides subtle, physical 3D reaction on mouse movement across cards
 */
function init3DCardParallax() {
    const cardSelectors = [
        '.card-3d',
        '.portal-hub-card',
        '.metric-card',
        '.stat-card-lite',
        '.agency-badge-card',
        '.step-card',
        '.chain-node-box',
        '.statutory-warning-card'
    ];

    const cards = document.querySelectorAll(cardSelectors.join(', '));
    cards.forEach(card => {
        if (card.dataset.tiltInit) return;
        card.dataset.tiltInit = 'true';
        card.style.transformStyle = 'preserve-3d';
        card.style.transition = 'transform 0.18s ease-out, box-shadow 0.22s ease';

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((centerY - y) / centerY) * 7.5;
            const rotateY = ((x - centerX) / centerX) * 7.5;

            card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
    });
}

/**
 * 3D Radial Percentage Gauge Component Builder
 * Generates an SVG 3D circular gauge with color-coded ring and glowing number
 */
function render3DRadialGauge(containerId, percentage, labelText = "Risk Score", size = 110) {
    const el = document.getElementById(containerId);
    if (!el) return;

    const strokeWidth = 8;
    const radius = (size - strokeWidth) / 2;
    const circumference = 2 * Math.PI * radius;
    const clampedPct = Math.min(100, Math.max(0, parseFloat(percentage) || 0));
    const offset = circumference - (clampedPct / 100) * circumference;

    let strokeColor = '#00e676';
    let badgeClass = 'safe';
    const isRecovery = (labelText || "").toLowerCase().includes('recovery') || (labelText || "").toLowerCase().includes('chance');
    if (isRecovery) {
        if (clampedPct >= 65) {
            strokeColor = '#00e676';
            badgeClass = 'safe';
        } else if (clampedPct >= 35) {
            strokeColor = '#f59e0b';
            badgeClass = 'warning';
        } else {
            strokeColor = '#f43f5e';
            badgeClass = 'danger';
        }
    } else {
        if (clampedPct >= 80) {
            strokeColor = '#f43f5e';
            badgeClass = 'danger';
        } else if (clampedPct >= 50) {
            strokeColor = '#f59e0b';
            badgeClass = 'warning';
        }
    }

    el.innerHTML = `
        <div class="radial-gauge-3d" style="width: ${size}px; height: ${size}px;">
            <svg width="${size}" height="${size}">
                <circle class="gauge-circle-bg" cx="${size/2}" cy="${size/2}" r="${radius}" stroke-width="${strokeWidth}"></circle>
                <circle class="gauge-circle-val" cx="${size/2}" cy="${size/2}" r="${radius}" stroke-width="${strokeWidth}"
                    style="stroke: ${strokeColor}; stroke-dasharray: ${circumference}; stroke-dashoffset: ${offset};"></circle>
            </svg>
            <div class="gauge-center-text">
                <div class="gauge-number" style="color: ${strokeColor};">${clampedPct.toFixed(1)}%</div>
                ${labelText ? `<div class="gauge-label">${labelText}</div>` : ''}
            </div>
        </div>
    `;
}

/**
 * Format and style all percentage badges dynamically across the web
 */
function autoStylePercentages() {
    // Check elements with class pct-value or risk-pct
    document.querySelectorAll('.risk-pct, .pct-value').forEach(el => {
        const text = el.innerText.trim();
        const num = parseFloat(text);
        if (!isNaN(num)) {
            el.classList.add('pct-badge-3d');
            if (num >= 80) {
                el.classList.add('danger');
            } else if (num >= 50) {
                el.classList.add('warning');
            } else {
                el.classList.add('safe');
            }
        }
    });
}

// Master initialization on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    _initDurgamPlatformChecks();
    init3DCardParallax();
    autoStylePercentages();
    // Re-initialize 3D cards after dynamic rendering
    setTimeout(init3DCardParallax, 800);
});

// Make utilities globally available
window.durgamFetch = durgamFetch;
window.init3DCardParallax = init3DCardParallax;
window.render3DRadialGauge = render3DRadialGauge;
window.autoStylePercentages = autoStylePercentages;


