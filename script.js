// DURGAM Unified Role Router & Navbar Engine
const API_BASE_URL = (!window.location.origin || window.location.origin === "null" || !window.location.origin.startsWith("http")) 
    ? "http://127.0.0.1:8000" 
    : window.location.origin;

const ROLE_NAV_SCHEMA = {
    citizen: {
        portalUrl: "citizen.html",
        features: [
            { label: "File Report", targetTab: "report" },
            { label: "My Complaints", targetTab: "complaints" },
            { label: "Live Tracker", targetTab: "track" },
            { label: "1-Tap Unblock", targetTab: "unblock" }
        ]
    },
    user: {
        portalUrl: "citizen.html",
        features: [
            { label: "File Report", targetTab: "report" },
            { label: "My Complaints", targetTab: "complaints" },
            { label: "Live Tracker", targetTab: "track" },
            { label: "1-Tap Unblock", targetTab: "unblock" }
        ]
    },
    bank: {
        portalUrl: "bank.html",
        features: [
            { label: "Mule Alerts", targetTab: "alerts" },
            { label: "Upload Statement", targetTab: "upload" },
            { label: "Submitted Data", targetTab: "accounts" },
            { label: "Transfer Chains", targetTab: "chains" }
        ]
    },
    command: {
        portalUrl: "command.html",
        features: [
            { label: "Dashboard", targetTab: "dashboard" },
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
            { label: "CAD Dispatch", action: "triggerPatrolDispatch('ATM_SBI_101')" }
        ]
    },
    judiciary: {
        portalUrl: "judiciary.html",
        features: [
            { label: "Evidence Dossiers", action: "window.scrollTo({top: 0, behavior: 'smooth'})" }
        ]
    }
};

function getLoggedInUser() {
    try {
        const u = localStorage.getItem('durgam_user');
        return u ? JSON.parse(u) : null;
    } catch (e) {
        return null;
    }
}

function renderGlobalNavbar() {
    const user = getLoggedInUser();
    const navLinks = document.querySelector('.nav-links');
    const navRight = document.querySelector('.nav-right');

    if (!navLinks || !navRight) return;

    const currentPath = window.location.pathname.split('/').pop() || 'index.html';

    if (!user) {
        // --- GUEST NAVBAR ---
        navLinks.innerHTML = `
            <a href="index.html" class="${currentPath === 'index.html' ? 'active' : ''}">Home</a>
            <a href="index.html#how-it-works">How It Works</a>
            <a href="index.html#estimator">Recovery Estimator</a>
            <a href="index.html#faqs">FAQs</a>
            <a href="login.html?role=i4c">Command Portal</a>
        `;

        navRight.innerHTML = `
            <a href="tel:1930" class="outline-btn" style="height: 42px; padding: 0 14px; font-size: 12px; color: #fff; border-color: rgba(255,255,255,0.2);">
                <i data-lucide="phone-call"></i> 1930 Helpline
            </a>
            <a href="login.html" class="portal-btn">
                <i data-lucide="user-round"></i> Sign In
            </a>
        `;
    } else {
        // --- LOGGED-IN NAVBAR: HOME + EXCLUSIVE ROLE TASKS ---
        const roleKey = (user.role || 'citizen').toLowerCase();
        const roleData = ROLE_NAV_SCHEMA[roleKey] || ROLE_NAV_SCHEMA.citizen;
        const isCurrentPortal = currentPath === roleData.portalUrl;

        const featureItemsHtml = roleData.features.map(f => {
            if (isCurrentPortal) {
                if (f.targetTab) {
                    if (roleKey === 'citizen' || roleKey === 'user') {
                        return `<a href="javascript:void(0);" onclick="showCitizenTab('${f.targetTab}')" id="navTab_${f.targetTab}" class="nav-task-item">${f.label}</a>`;
                    }
                    if (roleKey === 'bank') {
                        return `<a href="javascript:void(0);" onclick="showBankTab('${f.targetTab}')" id="navTab_${f.targetTab}" class="nav-task-item">${f.label}</a>`;
                    }
                    if (roleKey === 'command' || roleKey === 'i4c') {
                        return `<a href="javascript:void(0);" onclick="showCmdTab('${f.targetTab}')" id="navTab_${f.targetTab}" class="nav-task-item">${f.label}</a>`;
                    }
                }
                return `<a href="javascript:void(0);" onclick="${f.action}" class="nav-task-item">${f.label}</a>`;
            } else {
                return `<a href="${roleData.portalUrl}?tab=${f.targetTab || ''}" class="nav-task-item">${f.label}</a>`;
            }
        }).join('');

        navLinks.innerHTML = `
            <a href="index.html" class="${currentPath === 'index.html' ? 'active' : ''}">Home</a>
            ${featureItemsHtml}
        `;

        navRight.innerHTML = `
            <span class="portal-btn" style="cursor: default; border-color: rgba(183,255,0,0.35);">
                <i data-lucide="user-check"></i>
                <span>${user.name || user.email || user.id} <small style="color:var(--lime); text-transform:uppercase; font-weight:700;">(${user.role})</small></span>
            </span>
            <button onclick="handleUserLogout()" class="outline-btn" style="height: 40px; padding: 0 14px; font-size: 12px; color: #ff4d4d; border-color: rgba(255,77,77,0.4);">
                <i data-lucide="log-out"></i> Logout
            </button>
        `;
    }

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function handleUserLogout() {
    localStorage.removeItem('durgam_user');
    localStorage.removeItem('durgam_token');
    window.location.href = 'index.html';
}

document.addEventListener('DOMContentLoaded', () => {
    renderGlobalNavbar();
});