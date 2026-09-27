# Sovereign Dual-Contrast UI/UX Guardrails & Statutory Terminology

## 1. Light Canvas & Elevated White Surfaces
- The primary canvas is `--cream: #f4f5ee` with white surface cards (`#ffffff`).
- Never use white or light-grey text (`#ffffff`, `#e2e8f0`, `#cbd5e1`, `#94a3b8`) directly on white or light-cream surfaces.
- Primary typography on light surfaces MUST use `#111820` for headings and `#626b70` or `#475569` for body text.

## 2. Accessible Status Badge Tokens
- Do NOT use raw `#00e676` for text on light backgrounds.
- Success / Sealed Badges on light surfaces:
  - Text color: `#0b6b32` (dark forest green)
  - Background: `rgba(11, 107, 50, 0.08)`
  - Border: `1px solid rgba(11, 107, 50, 0.22)`
- Warning / In-Progress Badges:
  - Text color: `#92400e` (dark amber)
  - Background: `rgba(245, 158, 11, 0.1)`
  - Border: `1px solid rgba(245, 158, 11, 0.25)`

## 3. Dynamic Script Injections
- When injecting markup into `.navbar`, `.ui-card`, or modal boxes via JavaScript, always verify that text styles match the enclosing background color scheme.

## 4. Action Triggers & Touch Targets
- Jet-black primary buttons (`#050708`) with white text and green icon accents (`#00e676`) must have minimum height of 42px (44px on mobile) and clear cursor pointer.

## 5. Indian Statutory & Agency Nomenclature
- "Pre-settlement hold / micro-hold" -> **Instant Account Freeze & Lien (Sec 106 BNSS 2023)**
- "Merkle proof / blockchain proof" -> **Digital Evidence Certificate (Section 63 BSA 2023)**
- "GNN mule classification" -> **AI Mule Syndicate Detector**
- "CAD dispatch / Patrol Car 1" -> **PCR Patrol Unit (ERSS 112)**
- "Citizen Restitution Desk" -> **Citizen Reporting & Restitution Desk (CFCFRMS / 1930 Helpline)**
- "Bank Node Switch" -> **Bank Nodal Officer Desk**
- "War Room" -> **I4C National Cybercrime Command (MHA)**
- "Special Cyber Court" -> **Judicial Magistrate Cyber Court (Sec 106 BNSS)**
- "1-Tap Unblock Desk" -> **Bona Fide Account Unfreeze Desk (Aadhaar e-KYC)**
- "False Claim Disclaimer" -> **Statutory Legal Affirmation (Sec 217 BNS 2023)**
