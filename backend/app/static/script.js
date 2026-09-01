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
    { name: "Citizen Desk", href: "citizen.html", match: ["citizen.html"] },
    { name: "Police War Room", href: "police.html", match: ["police.html"] },
    { name: "Bank Switch", href: "bank.html", match: ["bank.html"] },
    { name: "Cyber Court", href: "judiciary.html", match: ["judiciary.html"] },
    { name: "I4C Command", href: "command.html", match: ["command.html"] },
    { name: "AI Threat Lab", href: "ai.html", match: ["ai.html"] },
    { name: "BSA Vault", href: "verify.html", match: ["verify.html"] },
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

    // 2. OFFICER PORTAL NAVBAR SPECIFICATION (Clean, non-duplicated header)
    const portalTitles = {
        "bank.html": { name: "Bank Nodal Operations", role: "Bank Nodal Desk" },
        "citizen.html": { name: "Citizen Cyber Response", role: "Citizen Assistance" },
        "command.html": { name: "I4C Command Center", role: "National War Room" },
        "police.html": { name: "Police PCR War Room", role: "Law Enforcement CAD" },
        "judiciary.html": { name: "Special Cyber Court", role: "Judicial Bench" },
        "ai.html": { name: "AI Threat Intelligence Lab", role: "Threat Modeling" },
        "verify.html": { name: "Section 63 BSA Digital Vault", role: "Evidence Verification" }
    };

    if (portalTitles[currentPath]) {
        // Render high-level portal switcher and operational status badge (no duplicate internal tabs)
        navLinks.innerHTML = `
            <div style="display:flex; align-items:center; gap:16px; font-size:12.5px; font-weight:600; color:#889096;">
                <span style="color:#ffffff; font-weight:700; display:flex; align-items:center; gap:6px;">
                    <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#8dcc00; box-shadow:0 0 8px rgba(141,204,0,0.8);"></span>
                    ${portalTitles[currentPath].name}
                </span>
                <span style="color:rgba(255,255,255,0.25);">|</span>
                <span style="font-size:11.5px; color:#5c8000; font-family:monospace; letter-spacing:0.3px;">SEC. 106 BNSS / RBI PRE-SETTLEMENT MESH</span>
            </div>
        `;

        navRight.innerHTML = `
            <a href="index.html" class="outline-btn" style="height:34px; padding:0 12px; font-size:12px; display:inline-flex; align-items:center; gap:6px; color:#ffffff; border-color:rgba(255,255,255,0.25);">
                <i data-lucide="home"></i> Home
            </a>
            ${user ? `
                <span class="portal-btn" style="cursor: default; border-color: rgba(141,204,0,0.4); height: 34px; padding: 0 12px; font-size:12px; white-space: nowrap; background:rgba(141,204,0,0.08);">
                    <i data-lucide="shield-check" style="color:var(--lime);"></i>
                    <span>${user.name || user.email || user.id} <small style="color:var(--lime); text-transform:uppercase; font-weight:700;">(${user.role || 'Officer'})</small></span>
                </span>
                <button onclick="handleUserLogout()" class="outline-btn" style="height: 34px; padding: 0 12px; font-size: 12px; color: #ff4d4d; border-color: rgba(255,77,77,0.4); display:inline-flex; align-items:center; gap:6px;" title="Logout and Switch Portal">
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
            <span class="portal-btn" style="cursor: default; border-color: rgba(183,255,0,0.35); height: 38px;">
                <i data-lucide="user-check"></i>
                <span>${user.name || user.email || user.id} <small style="color:var(--lime); text-transform:uppercase; font-weight:700;">(${user.role || 'Officer'})</small></span>
            </span>
            <button onclick="handleUserLogout()" class="outline-btn" style="height: 38px; padding: 0 14px; font-size: 12px; color: #ff4d4d; border-color: rgba(255,77,77,0.4);" title="Sign Out">
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

document.addEventListener('DOMContentLoaded', () => {
    renderGlobalNavbar();
});
