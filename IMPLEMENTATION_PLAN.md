# Master Implementation Plan: Project DURGAM (Dynamic Unified Risk-Grid & Geospatial Analytics Module)

**Platform:** DURGAM (National Cybercrime Real-Time Interception & Mule Account Risk-Grid)  
**Initiative:** Smart India Hackathon (SIH) 2026 / National Cybercrime Reporting Portal (NCRP / Helpline 1930 / I4C)  
**Author Baseline:** Ritik Singh (DURGAM Project PDF & Gemini Research)  
**Target Domain:** `durgam.gov.in` / National Sovereign Cyber Infrastructure  

---

## Executive Summary & System Overview

India's National Cybercrime Reporting Portal (NCRP) and Helpline 1930 receive over **8,000+ complaints daily**, with annual citizen losses exceeding **₹10,000 Crores**. Currently, financial recovery rates hover below **3%** because traditional responses take **12 to 72 hours**, whereas cyber syndicates execute multi-hop fund layering and cash-out at physical ATMs within the **"Golden Hour" (15 to 45 minutes)**.

**Project DURGAM** replaces retroactive manual policing with an automated, sub-180 millisecond AI-driven defense pipeline:
1. **Sub-15ms Ingestion & Tokenization:** Ingests Helpline 1930 / Web / WhatsApp complaints with DPDP Act 2023 compliant salted SHA-256 tokenization.
2. **Sub-85ms Multi-Hop Graph Traversal:** Graph Neural Networks (GNN / GraphSAGE / NetworkX) trace stolen fund dispersal across 4–6 intermediary mule tiers across distinct banks.
3. **Sub-500ms Bank Micro-Hold:** Issues automated ISO 20022 (`camt.056`) 30-minute pre-settlement micro-liens directly into Core Banking Switches (CBS) under Section 106 BNSS 2023 & RBI Master Directions.
4. **Sub-80ms Spatiotemporal ATM Forecasting:** Spatiotemporal Kernel Density Estimation (ST-KDE) + Uber H3 + XGBoost forecast the top 3–5 candidate ATM kiosks where the mule runner will attempt physical cash-out.
5. **Sub-2min Tactical Dispatch:** Geo-fenced dispatches push turn-by-turn navigation directly to beat patrol vehicles within a 2 km radius.
6. **Section 63 BSA Digital Evidence Sealing:** Batches 500 complaints / hourly Merkle roots on Polygon blockchain (`MerkleEvidenceLocker.sol`), slashing gas costs to under ₹1.25/day for all of India while producing 1-click court-admissible forensic dossiers under Section 63 Bharatiya Sakshya Adhiniyam (BSA) 2023.

---

## Complete Production Technology Stack Matrix

| Layer | Component | Production Stack Specification | Prototype / Hackathon Stack |
| :--- | :--- | :--- | :--- |
| **Frontend / Web Portals** | Multi-Portal Web Suite | React 18 + TypeScript + Vite, Tailwind CSS / Vanilla CSS (NIC/GoI Clean Gov Style) | React 18 + Vite + Tailwind CSS + Lucide Icons |
| **Graph Visualization** | Fund Trail Topology | Cytoscape.js (Force-Directed / Breadth-First Layering Layout) | Cytoscape.js + Dagre Layout |
| **Geospatial & Mapping** | 3D GIS & ATM Risk Grid | Mapbox GL JS / Leaflet.js with Uber H3 Hexagonal Layering | Leaflet.js + OpenStreetMap Vector Tiles + H3-js |
| **Backend API** | High-Throughput Core | Python 3.11 + FastAPI (Asynchronous ASGI, uvloop, Pydantic v2) | FastAPI + Uvicorn |
| **Primary Database** | Sovereign Relational DB | PostgreSQL 16 + PostGIS 3.4 (GIST spatial indexes for ATMs & GPS) | PostgreSQL 16 / SQLite with SpatiaLite / PostGIS |
| **Cache & Real-Time Stream** | In-Memory Velocity Store | Redis 7.2 (Rolling 15-min velocity keys, Pub/Sub WebSockets) | Redis 7.2 |
| **Graph Engine** | Inter-Bank Multi-Hop Hops | In-Memory NetworkX Directed Graph + Neo4j Graph DB | NetworkX DiGraph + PyTorch Geometric Data Object |
| **AI / GNN Engine** | Mule Ring Classification | PyTorch Geometric (PyG 2.4+), 2-layer GraphSAGE / GCNConv | PyTorch Geometric + PyTorch 2.2+ |
| **Spatial ML & Regression** | ATM Predictor & Time Regressor | XGBoost 2.0 / LightGBM 4.0, Scipy ST-KDE, Uber H3-py (Res 8) | XGBoost + Scikit-Learn + H3-py |
| **NLP / Grievance Parser** | 1930 Transcript Extraction | HuggingFace Transformers (`all-MiniLM-L6-v2` / IndicBERT / Spacy NER) | HuggingFace Transformers + Regex Extractor |
| **Blockchain / Evidentiary** | Section 63 BSA Locker | Solidity 0.8.20, Polygon Amoy Testnet / Hyperledger Besu (Merkle Batching) | Polygon Amoy RPC + Web3.py + Ethers.js |
| **Banking Protocol** | Core Banking Switch Hooks | ISO 20022 XML Messaging (`camt.056`, `pacs.008`, `pacs.002`) | Mock ISO 20022 REST/Webhook Switch Gateway |
| **Field Dispatch** | Beat Patrol PWA & Alerts | Progressive Web App (PWA), Web SMS Receiver API, Telegram Bot API | Telegram Bot API + Mobile-Responsive PWA |

---

## AI/ML Models Architecture & Training Specifications

```
                     ┌──────────────────────────────────────────────────┐
                     │          RAW INCIDENT COMPLAINT (1930/UTR)       │
                     └─────────────────────────┬────────────────────────┘
                                               │
                                               ▼
                     ┌──────────────────────────────────────────────────┐
                     │ MODEL 4: 1930 Grievance Parser & NER (IndicBERT) │
                     │  Extracts: UTR, Source Bank, Amount, Timestamp   │
                     └─────────────────────────┬────────────────────────┘
                                               │
                                               ▼
                     ┌──────────────────────────────────────────────────┐
                     │ MODEL 1: Multi-Hop Mule Graph Engine (GraphSAGE) │
                     │  Classifies: Node Mule Prob, Fan-Out/Fan-In Rings│
                     └─────────────────────────┬────────────────────────┘
                                               │
                                               ▼
                     ┌──────────────────────────────────────────────────┐
                     │ MODEL 3: Time-to-Cashout Regressor (LightGBM)    │
                     │  Predicts: Tremain (Minutes before ATM cash-out) │
                     └─────────────────────────┬────────────────────────┘
                                               │
                                               ▼
                     ┌──────────────────────────────────────────────────┐
                     │ MODEL 2: ST-KDE + XGBoost ATM Hotspot Forecaster │
                     │  Pinpoints: Top 3-5 Candidate ATM Kiosks & GPS   │
                     └──────────────────────────────────────────────────┘
```

### 1. Multi-Hop Mule Layering Graph Engine (GNN / GraphSAGE)
- **Objective:** Detect multi-tier cross-bank money mule syndicates within $< 85\text{ ms}$.
- **Architecture:** 2-Layer GraphSAGE / Relational GCN (RGCN) with message passing over directed multigraphs.
- **Node Features (8 dimensions):**
  1. Normalized In-Degree / Out-Degree ratio
  2. Dormancy-to-burst frequency ($\text{Transactions}_{15\text{min}} / \text{Transactions}_{30\text{days}}$)
  3. Total volume throughput in current 1-hour window
  4. Average inter-transaction interval ($\Delta t$)
  5. KYC age & account tier (Jan Dhan, Savings, Current, Merchant)
  6. Account-to-device binding hash uniqueness
  7. Geographic dispersion index of incoming funds
  8. Historical complaint association score
- **Edge Features (4 dimensions):**
  1. Transaction amount (INR)
  2. Time delta since parent hop ($\Delta t$)
  3. Layering velocity score: $V = \frac{\Delta \text{Amount}}{\Delta t + \epsilon}$
  4. Channel type (UPI, IMPS, NEFT, RTGS)
- **Loss Function:** Weighted Binary Cross-Entropy with Hard Negative Mining (accounting for 1:50 mule imbalance).
- **Target Output:** Node classification probability $P(\text{Mule}) \in [0, 1]$ and Ring Subgraph Isolation.

### 2. Spatiotemporal ATM Hotspot Forecaster (ST-KDE + XGBoost)
- **Objective:** Forecast the exact Top 3–5 physical ATM kiosks where the mule runner will attempt cash withdrawal within 15–45 minutes.
- **Mathematical Foundation:**
  $$\hat{f}(x, y, t) = \frac{1}{n \cdot h_s^2 \cdot h_t} \sum_{i=1}^n K_s\left(\frac{x - x_i}{h_s}, \frac{y - y_i}{h_s}\right) \cdot K_t\left(\frac{t - t_i}{h_t}\right)$$
  - Spatial bandwidth $h_s = 1.5\text{ to } 4.0\text{ km}$ adaptive radius; temporal bandwidth $h_t = 15\text{ to } 60\text{ mins}$.
- **Composite Interception Probability Scoring:**
  $$S_{\text{risk}}(A_k) = \sigma\left[ w_1 \cdot \hat{f}(x_k, y_k, t_{\text{pred}}) + w_2 \cdot V_{\text{mule}}(P) + \frac{w_3}{1 + d(A_k, \text{Branch}_{\text{mule}})} + w_4 \cdot \text{Hist}_{\text{risk}}(A_k) \right]$$
- **Spatial Indexing:** Uber H3 Hexagonal Grid (Resolution 8, ~460m edge length) for sub-10ms spatial lookups in PostGIS.

### 3. Time-to-Cashout Regressor (GBDT / XGBoost / LightGBM)
- **Objective:** Predict the exact remaining minutes ($T_{\text{remain}}$) before cash withdrawal to power the "Golden Hour" tactical countdown clock.
- **Input Features:** Current hop level ($k$), cumulative velocity $\sum V_i$, total layered amount, payment channel, time of day, day of week, city congestion index.
- **Output:** Continuous estimate $T_{\text{remain}} \in [5, 120]\text{ minutes}$ with 90% confidence intervals.

### 4. 1930 Grievance & Voice Parser (NLP / Pretrained Transformer)
- **Objective:** Extract structured forensic entities from unstructured citizen complaints, call transcripts, or WhatsApp messages.
- **Architecture:** HuggingFace `all-MiniLM-L6-v2` / `IndicBERT` fine-tuned for Named Entity Recognition (NER).
- **Extracted Entities:** Transaction UTR/RRN, Remitter Account, Beneficiary VPA/UPI ID, Loss Amount, Incident Timestamp, Modus Operandi (Part-Time Job, Sextortion, Digital Arrest, APK Scam, Investment Ponzi).

---

## Massive Dataset Generation & Bootstrapping Strategy

To train the AI models effectively without violating citizen banking privacy:

### 1. Synthetic Financial Laundering Graph Pipeline (1,000,000+ Transactions)
We will build a procedural graph generator simulating **12 distinct Indian financial cybercrime archetypes**:
1. **Classic Fan-Out (Layering 1 ➔ 5):** Stolen ₹5,00,000 split into 5 accounts of ₹1,00,000 within 3 minutes.
2. **Aggregated Fan-In (Layering 5 ➔ 1):** 5 intermediary mules funneling funds into a single terminal debit card.
3. **Circular Smurfing Loop:** Funds cycled $A \to B \to C \to D \to A$ to obscure audit trails.
4. **Dormant Jan-Dhan Burst:** Low-activity rural accounts suddenly receiving high-velocity metro inflows.
5. **Cross-State Migration (Delhi ➔ Jammu / Mewat ➔ Bengaluru / Jamtara ➔ Mumbai):** Inter-state layering hops.
6. **Legitimate Merchant Hubs (False Positive Controls):** Swiggy/Zomato delivery partners, grocery vendors, high fan-in with normal disbursement intervals.
7. **MSME Payroll Disbursements:** Legitimate bulk transfers to prevent false merchant lien placements.

### 2. Real-World Indian ATM Geospatial Repository
- **Data Source:** OpenStreetMap (OSM) Overpass API queried across all 36 Indian States and Union Territories.
- **Tags Extracted:** `node["amenity"="atm"]`, `node["amenity"="bank"]`, `operator` (SBI, PNB, HDFC, ICICI, Axis, Indicash, Tata Indicash).
- **Enrichment:** Spatial clustering, 24x7 vs. shuttered status, CCTV coverage indicator, proximity to major transport hubs and highways.

### 3. Open Benchmark Datasets Integration
- **Elliptic Bitcoin Dataset:** Graph topology benchmarks for anti-money laundering node classification.
- **PaySim / BankSim Financial Datasets:** Synthetic mobile money transaction distributions.
- **NCRB Crime in India Open Datasets:** District-wise cybercrime incidence rates for prior probability weighting.

### 4. Continuous Active Learning & Feedback Loop
- **Positive Label ($y=1$):** Field patrol marks `[SUSPECT DETAINED]` or `[CASH RECOVERED]`.
- **Negative Label ($y=0$):** Micro-hold expires after 30 mins without dispute or citizen completes 1-tap "Not a Fraud" Aadhaar OTP challenge.
- **Nightly Retraining:** Automated pipeline recalibrates classification thresholds to prevent concept drift.

---

## Government-Standard UI/UX Design System

The platform adopts a **clean, authoritative, accessible Government of India / NIC aesthetic**:

- **Color Scheme (Indian Sovereign / NIC Standard):**
  - **Primary Navy:** `#0b2545` (Official Government Navy)
  - **Emblem Gold:** `#b38a38` (Ashok Stambh Accent)
  - **Tricolor Saffron:** `#ff9933` (Alerts / Priority Highlights)
  - **Tricolor Green:** `#138808` (Safe / Verified / Active Status)
  - **Background Clean Light:** `#f4f6f9` / `#ffffff` (Crisp readability)
  - **War Room Tactical Dark Mode:** `#0d1b2a` / `#1b263b` (For command center map view)
- **Typography:** Inter, Roboto, and Noto Sans Devanagari (Clean, modern, highly legible).
- **Layout & Usability:** High contrast, clear tabular data, zero unnecessary animations, responsive across devices.
- **Accessibility:** WCAG 2.1 AA compliant, bilingual toggle (English / हिंदी).

---

## Comprehensive Portal & Page Architecture

DURGAM provides 4 purpose-built portals with real-time dynamic data feeds:

```
PROJECT DURGAM PLATFORM
│
├── 1. CITIZEN & 1930 HELPLINE PORTAL (Public & Citizen Self-Service)
│   ├── / (Home / Landing Page with Live National Stats & 1930 Quick Dial)
│   ├── /report (Fast 60-Second Incident Complaint Ingestion)
│   ├── /track (Real-Time UTR/Ack Number Freeze Status Tracker)
│   ├── /verify-certificate (Public Section 63 BSA Digital Certificate Verifier)
│   └── /dispute (Citizen 1-Tap "Not a Fraud" Aadhaar OTP Dual-Factor Resolution)
│
├── 2. LAW ENFORCEMENT (LEA) & POLICE COMMAND WAR ROOM (Role: Police / SP / I4C)
│   ├── /police/login (Government SSO / Jan Parichay / ED25519 Secure Auth)
│   ├── /police/dashboard (National & District Command War Room & Golden Hour Queue)
│   ├── /police/investigate/:caseId (Cytoscape.js Multi-Hop Mule Trail Graph & Telemetry)
│   ├── /police/risk-grid (3D GIS Leaflet/Mapbox Tactical ATM Heatmap & Hotspots)
│   ├── /police/patrol-dispatch (Beat Patrol CAD Live Telemetry & Unit Tracking)
│   ├── /police/evidence/:caseId (1-Click Section 63 BSA Forensic Dossier Generator)
│   └── /police/mobile-patrol (Field Beat Constable Mobile PWA Tactical Action Card)
│
├── 3. BANK NODAL & FINANCIAL INSTITUTION PORTAL (Role: Bank FRM / Nodal Officer)
│   ├── /bank/login (Bank Corporate SSO & Two-Factor Authentication)
│   ├── /bank/dashboard (Live ISO 20022 camt.056 Inbound Micro-Lien Feed)
│   ├── /bank/micro-holds (Active 30-Minute Temporary Settlement Hold Queue)
│   ├── /bank/zk-search (DPDP Compliant Zero-Knowledge Hash Mule Registry Lookup)
│   └── /bank/merchants (MSME & High-Velocity Merchant Whitelist Management)
│
└── 4. CENTRAL ADMIN, SOVEREIGN INFRASTRUCTURE & BLOCKCHAIN LEDGER
    ├── /admin/login (Master System Administration)
    ├── /admin/overview (System Health, 180ms Latency SLA, Kafka/Redis Telemetry)
    ├── /admin/blockchain (Merkle Tree Batching Protocol & Polygon Contract Explorer)
    └── /admin/ai-models (Active Learning Performance, GNN Precision-Recall, Drift Monitor)
```

---

## Detailed Page Specifications & Dynamic Data

### 1. Citizen & 1930 Helpline Portal
- **`/` (Public Landing):** Live ticker of national funds protected (e.g. ₹42.8 Cr in last 24h), 1930 Helpline direct dialer, fraud awareness bulletins, simple navigation.
- **`/report` (Fast Complaint Form):** Minimal, frictionless inputs: Complaint Category, Victim Name & Mobile, Transaction Reference (UTR / UPI Ref Number / Bank Account), Amount, Date & Time, Brief Narrative. Submits in $< 15\text{ms}$.
- **`/track` (Live Case Status):** Real-time step progress bar: *Complaint Lodged* ➔ *Graph Analyzed* ➔ *Layer 2 Micro-Hold Placed (₹X Frozen)* ➔ *Jammu Police Dispatched* ➔ *Court Evidence Sealed*.
- **`/verify-certificate`:** Citizens and bank legal officers can input a Certificate Hash or upload a PDF to verify its SHA-256 Merkle proof against the on-chain Polygon contract.

### 2. Law Enforcement Agency (LEA) Command War Room
- **`/police/dashboard`:** 
  - **Live "Golden Hour" Priority Ticker:** Cases sorted by remaining cash-out window ($T_{\text{remain}}$). Red pulsating cards for $< 15\text{ min}$ cases.
  - **Key Metrics:** Total Complaints Today, Active Multi-Hop Traces, Total Micro-Hold Value (₹), Units On-Site, Suspects Detained.
- **`/police/investigate/:caseId` (Multi-Hop Graph Viewer):**
  - Interactive Cytoscape.js canvas showing the full directed fund trail: `Victim (Delhi)` $\to$ `Mule Layer 1 (SBI)` $\to$ `Mule Layer 2 (HDFC)` $\to$ `Terminal ATM Card (J&K Bank, Jammu)`.
  - Node inspection card showing account holder name (masked per DPDP), IFSC, Velocity, GNN risk score, and hold status.
- **`/police/risk-grid` (GIS Hotspot Map):**
  - Leaflet / Mapbox interactive map with dynamic Uber H3 hexagonal density layer.
  - Top 3–5 candidate ATM kiosks highlighted with exact GPS coordinates, bank brand, distance, and 1-tap route calculation.
- **`/police/mobile-patrol` (Beat Constable PWA):**
  - Tactical Action Card: "URGENT INTERCEPTION ALERT: State Bank ATM, Residency Road, Jammu (1.4 km away - 4 min drive). Target Amount: ₹1,50,000."
  - Action buttons: `[ UNIT EN ROUTE ]`, `[ AT LOCATION ]`, `[ SUSPECT DETAINED ]`, `[ CASH RECOVERED ]`.
- **`/police/evidence/:caseId`:**
  - Automated generation and preview of the **Section 63 Bharatiya Sakshya Adhiniyam (BSA) Digital Evidence Certificate** with cryptographic SHA-256 hash, Merkle proof branch, block receipt, and digital signature watermark.

### 3. Bank Nodal Officer Portal
- **`/bank/dashboard` & `/bank/micro-holds`:**
  - Inbound stream of ISO 20022 `camt.056` modification requests.
  - Live 30-minute auto-release countdown clock for each held account.
  - 1-click confirmation or override with mandatory reasoning audit.
- **`/bank/zk-search`:**
  - Privacy-preserving consortium search: Input an Account Number / Mobile Number $\to$ Backend calculates $\text{SHA256}(\text{Acc} \parallel \text{IFSC} \parallel \text{Salt})$ $\to$ Returns whether the entity is associated with active cyber syndicates without leaking PII or balances.
- **`/bank/merchants`:**
  - Whitelist dashboard for verified GSTIN merchants (Amazon, Swiggy, Flipkart, local retailers) to prevent false-positive holds during high-velocity sales.

### 4. Central Sovereign Admin & Blockchain Portal
- **`/admin/blockchain`:**
  - Hourly Merkle Tree batching monitor (`MerkleEvidenceLocker.sol`).
  - Batch ID, Complaint Count per Batch (e.g. 500), Merkle Root Hash (`0x...`), Polygon Amoy Transaction Hash, Gas Used ($0.032\text{ POL/day}$), and On-Chain Confirmation Status.
- **`/admin/ai-models`:**
  - Live performance dashboards for GraphSAGE (Precision: 94.2%, Recall: 91.8%), XGBoost ATM Hotspot Top-3 Accuracy (88.4%), and Airflow retraining pipeline status.

---

## Step-by-Step Cross-Jurisdiction Workflow (Delhi to Jammu Case Study)

```
[ 00:00 ] Citizen in Delhi files complaint via Helpline 1930 / DURGAM portal with UTR.
    │ (<15 ms)
[ 00:01 ] DURGAM Gateway tokenizes PII under DPDP Act 2023 & builds initial graph node.
    │ (<85 ms)
[ 00:02 ] GNN Engine executes multi-hop traversal:
          Victim (Delhi) ➔ Mule Layer 1 (SBI) ➔ Mule Layer 2 (ICICI) ➔ Terminal Mule (J&K Bank, Jammu).
    │ (<500 ms)
[ 00:03 ] Automated ISO 20022 camt.056 webhook triggers 30-min micro-lien on terminal account.
    │ (<80 ms)
[ 00:04 ] ST-KDE & Uber H3 engine calculates spatial withdrawal probability in Jammu:
          Top candidate: SBI ATM, Residency Road, Jammu (Risk Score: 0.93).
    │ (<2 mins)
[ 00:06 ] Jammu Police Beat Patrol unit receives geo-fenced tactical alert on Mobile PWA.
    │ (12 mins)
[ 00:18 ] Jammu PCR van intercepts suspect at ATM kiosk; taps [SUSPECT DETAINED].
    │ (Immediate)
[ 00:19 ] Off-chain Merkle tree commits batch root to Polygon smart contract.
    │ (Immediate)
[ 00:20 ] System generates watermarked Section 63 BSA Digital Evidence Dossier for trial court.
```

---

## Statutory, Regulatory & Privacy Compliance Matrix

1. **Digital Personal Data Protection (DPDP) Act 2023:**
   - **Zero Commercial Cloud Telemetry:** No third-party trackers (Google Analytics, Mixpanel, Firebase).
   - **PII Masking:** Names and account numbers tokenized using salted SHA-256 hashes ($\text{AccountHash} = \text{SHA256}(\text{Acc} \parallel \text{IFSC} \parallel \text{Salt})$).
   - **Data at Rest & Transit:** AES-256-GCM encryption with HSM-managed sovereign keys.
2. **Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 (Section 106 / Former Sec 102 CrPC):**
   - Authorizes algorithmic 30-minute micro-holds as temporary provisional seizure while beat patrol units verify physical withdrawal.
3. **Bharatiya Sakshya Adhiniyam (BSA) 2023 (Section 63):**
   - Replaces Section 65B of the Indian Evidence Act. The automated PDF dossier contains verifiable SHA-256 cryptographic hashes and Merkle root receipts matching on-chain Polygon ledger records.
4. **RBI Master Direction on Digital Payment Security Controls (Sections 8.2 & 14):**
   - Mandates commercial scheduled banks to maintain real-time automated fraud risk management (FRM) and velocity throttling mechanisms.

---

## Phased Implementation Roadmap & Verification Plan

### Phase 1: Core Foundation, Synthetic Datasets & Database Setup
- [ ] Initialize project structure, environment configuration, and Python dependencies.
- [ ] Implement synthetic graph generator creating 1,000,000+ multi-hop transactions across 12 laundering archetypes.
- [ ] Fetch and seed real Indian ATM geodata from OpenStreetMap Overpass API into PostGIS / SQLite spatial database.
- [ ] Configure Redis in-memory velocity cache and PostgreSQL schema with spatial indexing.

### Phase 2: AI/ML Models Development & Training
- [ ] Build & train **Multi-Hop Mule Graph Engine** using PyTorch Geometric (2-Layer GraphSAGE).
- [ ] Build & train **Spatiotemporal ATM Hotspot Predictor** using Scipy ST-KDE + Uber H3 + XGBoost.
- [ ] Build & train **Time-to-Cashout Regressor** using LightGBM / XGBoost.
- [ ] Build **1930 Grievance & NER Parser** using HuggingFace Transformers / Spacy.
- [ ] Implement the Continuous Active Learning feedback loop and model evaluation metrics.

### Phase 3: Blockchain Evidence Locker & Banking Switch Integration
- [ ] Implement `MerkleEvidenceLocker.sol` smart contract with off-chain Merkle batching (500 complaints / hourly batches).
- [ ] Deploy contract to Polygon Amoy Testnet and build Web3.py / Ethers.js cryptographic verification service.
- [ ] Implement Section 63 BSA Digital Evidence Dossier PDF generator with SHA-256 block proofs.
- [ ] Build mock ISO 20022 Banking Gateway (`camt.056` micro-lien placement & 30-min auto-release timer).

### Phase 4: Government-Style Frontend Multi-Portal Web Suite
- [ ] Build clean, accessible Government of India / NIC style design system in React 18 + Vite + Tailwind/CSS.
- [ ] Implement **Citizen Portal** (`/`, `/report`, `/track`, `/verify-certificate`, `/dispute`).
- [ ] Implement **Police Command War Room** (`/police/dashboard`, `/police/investigate/:caseId`, `/police/risk-grid`, `/police/patrol-dispatch`, `/police/evidence/:caseId`).
- [ ] Implement **Field Beat Patrol Mobile PWA** (`/police/mobile-patrol`) with GPS deep-linking and offline sync.
- [ ] Implement **Bank Nodal Portal** (`/bank/dashboard`, `/bank/micro-holds`, `/bank/zk-search`, `/bank/merchants`).
- [ ] Implement **Central Admin & Sovereign Infrastructure Portal** (`/admin/overview`, `/admin/blockchain`, `/admin/ai-models`).

### Phase 5: End-to-End Simulation, Testing & Verification
- [ ] **Cross-Jurisdiction Simulation Test:** Execute the full Delhi citizen UTR $\to$ 4-hop GNN trace $\to$ Jammu ATM prediction $\to$ beat patrol alert $\to$ Polygon evidence sealing.
- [ ] **Latency SLA Benchmark:** Verify end-to-end processing executes within $< 180\text{ ms}$.
- [ ] **Micro-Hold Auto-Decay Test:** Verify 30-minute timer automatically dissolves unverified holds.
- [ ] **Section 63 BSA Verification:** Validate generated PDF SHA-256 hash against live Polygon smart contract.
