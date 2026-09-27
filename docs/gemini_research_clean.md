# Gemini Research Analysis: Tracking Mule Accounts & Durgam Architecture

‎Gemini - direct access to Google AI
Sign in
Gemini
Sign in
Tracking Mule Accounts Across Jurisdictions
https://share.gemini.google/f9dZzmnf41Pt
Created with
3.7 Flash
August 25, 2026 at 12:02 AM
Published August 26, 2026 at 12:38 AM
Durgam Project
Uploaded file not shown
You said
analyze this and tell me how to track mule account if a fraud happens in delhi and withdrawal initia…
analyze this and tell me how to track mule account if a fraud happens in delhi and withdrawal initiated in jammu how my system track that and how
Project DURGAM tracks multi-hop mule accounts and cross-state cash-out attempts (such as a fraud initiated in Delhi with withdrawal targeted in Jammu) through an integrated, sub-180ms pipeline connecting graph analysis, geospatial forecasting, and automated banking hooks
:
PDF
End-to-End Tracking & Interception Workflow
[ Delhi Citizen Complaint (1930 / UTR) ]
│ (<15ms)
▼
[ Ingestion Gateway & DPDP Masking ]
│ (<85ms)
▼
[ GNN Multi-Hop Graph Traversal (NetworkX/PyTorch) ]
├── Traces Delhi Victim ➔ Mule Layer 1 ➔ Layer 2 ➔ Terminal Jammu Account
└── Triggers Sub-500ms Bank Micro-Hold via ISO 20022 camt.056
│ (<80ms)
▼
[ Spatiotemporal KDE & Uber H3 Hotspot Prediction ]
└── Pinpoints Top 3–5 candidate ATM Kiosks in Jammu
│
─────────────┴─────────────
│                           │
▼                           ▼
[ Automated Patrol Dispatch ]   [ Section 63 BSA Evidence Locker ]
• Geo-fenced alerts to Jammu    • SHA-256 state Merkle Root sealed
PCR vans (PWA / Telegram /      on Polygon Amoy for court trials
encrypted SMS fallback)
Step-by-Step Tracking Mechanism
Complaint Ingestion & PII Masking (<15 ms):
When the victim in Delhi files a complaint via Helpline 1930, Web, or WhatsApp, the system captures the initial Transaction Reference (UTR/UPI ID) and amount
. PII is tokenized/hashed to remain compliant with the Digital Personal Data Protection (DPDP) Act 2023
.
PDF
+ 1
Cross-Bank Graph Traversal & Velocity Scoring (<85 ms):
The
GNN / Mule Graph Engine
(PyTorch Geometric + NetworkX) traces the directed money flow across intermediary accounts
:
PDF
Victim (Delhi)
IMPS/UPI
​
Layer 1
​
Layer 2
​
Terminal Mule (Jammu)
The system computes the
Mule Layering Velocity Score
:
V
m
u
l
e
​
(
P
)
=
∑
[
Δ
t
(
v
j
−
1
​
,
v
j
​
)
+
ϵ
Amount
(
v
j
−
1
​
,
v
j
​
)
​
]
⋅
exp
(
−
λ
⋅
HopLevel
(
v
j
​
))
This isolates rapid fan-out/fan-in circular laundering loops across different banking networks in real time
.
PDF
Sub-Second Automated Banking Micro-Hold (<500 ms):
Once the terminal mule card/account in Jammu is flagged, DURGAM triggers an automated
30-Minute Pre-Settlement Micro-Lien
via ISO 20022
camt.056
webhooks directly to the bank's Core Banking Switch (CBS)
.
PDF
The hold temporarily locks outbound cash dispenses and IMPS transfers at the switch level.
Operates under Sections 8.2 & 14 of the RBI Master Direction on Digital Payment Security Controls and Section 106 BNSS 2023.
Spatiotemporal Cash-Out Hotspot Forecasting (<80 ms):
The
Spatiotemporal KDE Engine
and Uber H3 spatial indexing query the PostGIS database of geocoded ATMs to calculate the specific physical withdrawal risk:
S
r
i
s
k
​
(
A
k
​
)
=
σ
[
w
1
​
⋅
f
^
​
(
x
k
​
,
y
k
​
,
t
p
re
d
​
)
+
w
2
​
⋅
V
m
u
l
e
​
(
P
)
+
1
+
d
(
A
k
​
,
Branch
m
u
l
e
​
)
w
3
​
​
+
w
4
​
⋅
Hist
r
i
s
k
​
(
A
k
​
)
]
The model forecasts the top 3–5 ATM kiosks in Jammu where the mule runner will attempt cash-out within a 15–45 minute lead window
.
PDF
Tactical Patrol Dispatch & Field Interception (<2 min):
The backend pushes geo-fenced tactical action cards with turn-by-turn navigation deep-links to Jammu police PCR units and beat constables within a 2 km radius via the
Beat Patrol PWA
, Telegram Bot, or encrypted SMS fallback
.
PDF
Cryptographic Evidence Sealing (BSA Sec 63):
All telemetry—including victim logs, GNN graph states, predicted Jammu ATM IDs, and timestamps—is hashed and batched into an off-chain Merkle tree, committing the root to the Polygon blockchain
. This generates an immutable Section 63 BSA legal dossier for prosecution
.
PDF
+ 1
You said
why banks gives access to durgam
why banks gives access to durgam
Banks grant integration and access to the DURGAM platform based on regulatory mandates, legal authority, risk containment, and privacy preservation architectures
:
PDF
Regulatory Mandate from the Reserve Bank of India (RBI):
Under Sections 8.2 & 14 of the
RBI Master Direction on Digital Payment Security Controls
and Section 35A of the
Banking Regulation Act, 1949
, all scheduled commercial banks are legally mandated to implement automated Fraud Risk Management (FRM) systems capable of real-time velocity monitoring, transaction throttling, and adaptive step-up authentication
.
PDF
Algorithmic Micro-Lien vs. Illegal Account Freezes:
Banks cannot execute full, indefinite judicial account freezes without a magistrate or SHO order under Section 106 BNSS 2023 (formerly Sec 102 CrPC)
. DURGAM solves this by triggering an automated, temporary
30-Minute Pre-Settlement Micro-Lien
(via ISO 20022
camt.056
webhooks) strictly on the disputed amount
. Outbound ATM/IMPS cash-out is quarantined while standard inbound transactions remain unaffected, automatically dissolving after 30 minutes if unverified
.
PDF
+ 2
Zero-Knowledge DPDP Act 2023 Compliance:
Banks cannot share raw customer databases or balance sheets with other banks or external vendors due to data protection regulations
. DURGAM employs a
Zero-Knowledge (ZK) Consortium Mule Registry
using salted SHA-256 hashes:
PDF
AccountHash
=
SHA256
(
Account Number
∥
Bank IFSC
∥
Salt
)
This allows banks to query whether an incoming transfer matches a flagged mule network without revealing any non-fraud customer names, phone numbers, or account balances
.
PDF
Protection of Innocent Merchants & MSMEs:
Conventional blanket police freezes shut down legitimate high-volume merchant accounts
. DURGAM uses Graph Neural Networks (GNN) and GSTN/PAN whitelisting to distinguish legitimate high-volume business inflows from rapidly structured mule ring patterns (fan-out/fan-in/circular loops), cutting false-positive merchant freezes by 85%
.
PDF
+ 1
Eliminating Inter-Bank Blind Spots:
Individual bank AML software (such as NICE Actimize or Falcon) only tracks internal account movements, leaving banks blind when stolen funds hop across multiple external institutions within minutes
. Integrating with DURGAM gives banks centralized, cross-institutional visibility into layered money flows before funds are converted into untraceable cash at physical ATMs
.
PDF
+ 1
You said
but for my prototype purpose how i get that informations
but for my prototype purpose how i get that informations
For your prototype and hackathon phase, DURGAM utilizes a dedicated
Hackathon Test Data Pipeline
to safely simulate live government and banking feeds using free APIs and generated datasets
.
PDF
Real ATM Geodata:
Use the
OpenStreetMap Overpass API
to fetch actual Indian ATM and bank coordinates
. This service is 100% free, requires no API key, and can be queried directly using tags like
node["amenity"="atm"]
.
PDF
+ 1
Geospatial UI & Maps:
Use
Mapbox GL JS
to render 3D vector maps and KDE heatmaps, which requires signing up for a free public token
. Alternatively, you can use
Leaflet.js
which requires zero keys
.
PDF
+ 1
Transaction Data (Multi-Hop Graph):
Since you cannot access real core banking switch (CBS) data for a prototype, you must build a
Synthetic Multi-Hop NCRP
pipeline
. Use an In-Memory NetworkX Graph generator to synthetically create 50,000 multi-hop financial transactions
. This allows you to simulate classic money laundering motifs like Fan-Out, Fan-In, and Circular Loops for your AI model to train on
.
PDF
+ 2
Blockchain Evidence Sealing:
To test the Section 63 BSA evidence locker, connect to the
Polygon Amoy Testnet RPC
via Web3 providers like Alchemy or Infura
. You can sign up for a 100% free tier (up to 50k loads), create a testnet app, and copy the RPC URL
.
PDF
+ 1
Tactical Patrol Dispatch:
To prototype the geo-fenced mobile push alerts for police, use the
Telegram Bot API
. It is entirely free and can be generated instantly by messaging
@BotFather/newbot
on Telegram to retrieve an API token
.
PDF
+ 1
You said
TELL ME MODELS I NEED TO CREATE AND THERE TECH STACK AND INFORMATION RELATED TO MODEL HOW CAN WE CRE…
TELL ME MODELS I NEED TO CREATE AND THERE TECH STACK AND INFORMATION RELATED TO MODEL HOW CAN WE CREATE THEM
The core AI/ML engine for Project DURGAM requires three custom-built machine learning models and one lightweight pretrained NLP pipeline
:
PDF
Core Model Breakdown & Tech Stack
Model Name
Problem Type & Algorithm
Tech Stack & Libraries
Input Features & Target Output
1. Multi-Hop Mule Layering Engine
PDF
Graph Deep Learning
(Directed Graph Convolutional Network / GraphSAGE / GCN)
PDF
PyTorch Geometric (PyG)
,
NetworkX
,
DGL
,
CUDA
PDF
Input:
Node features (account age, velocity, degree) & Edge weights (amount,
Δ
t
)
.
PDF
Output:
Mule probability score per node, detecting Fan-Out/Fan-In/Circular loops
.
PDF
2. Spatiotemporal ATM Hotspot Predictor
PDF
Spatial Statistics + GBDT Classifier
(Spatiotemporal KDE + XGBoost)
PDF
Scipy
,
Uber H3-py
(Res 8),
PostgreSQL/PostGIS
,
XGBoost
PDF
Input:
ATM coordinates, syndicate historical withdrawal clusters, branch distance, operational status
.
PDF
Output:
Ranked list of Top 3–5 candidate ATM kiosks
.
PDF
3. Time-to-Cashout Regressor
PDF
Time-Series Regression
(Gradient Boosted Trees)
PDF
LightGBM
/
XGBoost
,
Pandas
,
NumPy
PDF
Input:
Inter-hop transfer velocities (
Δ
t
), hop count decay, time of day
.
PDF
Output:
Estimated minutes remaining (
T
remain
​
, e.g., 15–45 min window)
.
PDF
4. 1930 Call / Grievance Parser
(Optional)
PDF
Text Classification / NER
(Pretrained Transformer)
PDF
transformers
(
all-MiniLM-L6-v2
),
HuggingFace
PDF
Input:
Raw citizen grievance text or voice-to-text transcript
.
PDF
Output:
Extracted UTR, amounts, handles, and crime category
.
PDF
How to Create & Implement the Models
1. Building the GNN Mule Graph Engine
Synthetic Graph Construction:
Use
networkx.DiGraph
to simulate 50,000 multi-hop transactions modeling common laundering archetypes (1 victim
→
5 mules
→
1 cash-out card)
.
PDF
Node & Edge Feature Engineering:
Compute in-degree/out-degree ratios, transaction burst frequency, and velocity:
V
=
Δ
t
Δ
Amount
​
Training with PyTorch Geometric:
Convert the graph into a
torch_geometric.data.Data
object. Train a 2-layer
GraphSAGE
or
GCNConv
network with binary cross-entropy loss to classify nodes as
MULE
(
1
) vs.
LEGITIMATE
(
0
)
.
PDF
2. Building the Spatiotemporal ATM Hotspot Model
Spatial Discretization:
Query ATM coordinates via OSM Overpass API into PostGIS
. Convert latitude/longitude pairs to Uber H3 Hexagonal Grid indices (
h3.geo_to_h3(lat, lng, resolution=8)
)
.
PDF
+ 1
ST-KDE Computation:
Implement the Gaussian kernel function across spatial distance (
h
s
​
=
1.5
–
4.0
 km
) and time delta (
h
t
​
=
15
–
60
 mins
)
:
PDF
f
^
​
(
x
,
y
,
t
)
=
n
⋅
h
s
2
​
⋅
h
t
​
1
​
∑
K
s
​
(
h
s
​
x
−
x
i
​
​
,
h
s
​
y
−
y
i
​
​
)
⋅
K
t
​
(
h
t
​
t
−
t
i
​
​
)
Ranking Classifier:
Train an XGBoost model on top of the KDE density score, historical ATM cash-out counts, and distance to the registered mule branch (
d
(
A
k
​
,
Branch
m
u
l
e
​
)
) to output a composite score (
S
r
i
s
k
​
)
.
PDF
3. Building the Time-to-Cashout Regressor
Target Variable:
T
remain
​
(minutes elapsed between final layer credit and physical ATM cash-out)
.
PDF
Features:
Number of hops, average velocity per hop, transaction amount, and payment protocol (UPI vs. IMPS/RTGS)
.
PDF
Training:
Fit an
XGBRegressor
optimizing RMSE to give dispatchers a live countdown timer
.
PDF
4. Real-Time Active Learning Loop
Store model weights in an inference server running FastAPI and PyTorch
.
PDF
Ingest field ground-truth: when patrol officers click
[SUSPECT DETAINED]
(
y
=
1
) or when a hold expires without incident (
y
=
0
), log the vector to trigger nightly retraining pipelines to eliminate concept drift
.
PDF
You said
DETAILED ABOUT MODELS I NEED TO CREATE IN POINTS
DETAILED ABOUT MODELS I NEED TO CREATE IN POINTS
1. Multi-Hop Mule Layering Graph Engine
PDF
Objective:
Trace cross-bank, multi-tier fund dispersion and identify criminal laundering graph topologies in sub-second timeframes
.
PDF
Core Algorithm:
Graph Neural Networks (GNN) using Graph Convolutional Networks (
GCNConv
) or
GraphSAGE
over directed multigraphs
.
PDF
Input Node & Edge Features:
In-degree and out-degree ratios
.
PDF
Rapid dormancy-to-burst frequency flags
.
PDF
Layering velocity gradient:
V
=
Δ
t
Δ
Amount
​
PDF
Hop decay factor:
exp
(
−
λ
⋅
HopLevel
)
PDF
Target Output:
Binary node classification (
0 = Legitimate/Merchant
,
1 = Flagged Mule Account
) and ring subgraph isolation
.
PDF
Tech Stack:
PyTorch Geometric (PyG)
,
NetworkX
,
DGL
,
CUDA
.
PDF
Implementation Steps:
Generate a directed graph dataset representing multi-tier fund distributions (e.g., 1 victim account
→
5 intermediary hops
→
1 terminal debit card)
.
PDF
Engineer transaction velocity edge weights and account-level node feature tensors
.
PDF
Train a 2-layer
GraphSAGE
network with binary cross-entropy loss to isolate Fan-Out, Fan-In, and Circular Laundering loops
.
PDF
2. Spatiotemporal ATM Hotspot Predictor
PDF
Objective:
Forecast the top 3–5 high-probability physical ATM kiosks where cash withdrawal will be attempted
.
PDF
Core Algorithm:
Spatiotemporal Kernel Density Estimation (ST-KDE) combined with an XGBoost Ranking Classifier
.
PDF
Input Features:
Historical cash-out geospatial density coordinates
(
x
i
​
,
y
i
​
)
and temporal offsets
t
i
​
.
PDF
Haversine road distance between the candidate ATM node and the registered terminal mule bank branch (
d
(
A
k
​
,
Branch
m
u
l
e
​
)
)
.
PDF
ATM operational status and historical syndicate cluster frequency
.
PDF
Mathematical Function:
f
^
​
(
x
,
y
,
t
)
=
n
⋅
h
s
2
​
⋅
h
t
​
1
​
∑
K
s
​
(
h
s
​
x
−
x
i
​
​
,
h
s
​
y
−
y
i
​
​
)
⋅
K
t
​
(
h
t
​
t
−
t
i
​
​
)
PDF
S
r
i
s
k
​
(
A
k
​
)
=
σ
[
w
1
​
⋅
f
^
​
(
x
k
​
,
y
k
​
,
t
p
re
d
​
)
+
w
2
​
⋅
V
m
u
l
e
​
(
P
)
+
1
+
d
(
A
k
​
,
Branch
m
u
l
e
​
)
w
3
​
​
+
w
4
​
⋅
Hist
r
i
s
k
​
(
A
k
​
)
]
PDF
Target Output:
Ranked list of target ATM nodes with associated probability scores (
S
r
i
s
k
​
) and bounding geometry
.
PDF
Tech Stack:
SciPy
,
Uber H3-py
(Resolution 8),
PostgreSQL/PostGIS
,
XGBoost
.
PDF
Implementation Steps:
Ingest physical ATM nodes via OpenStreetMap Overpass API and store them as spatial points in PostGIS
.
PDF
Convert geographic coordinates into hexagonal H3 spatial cells for rapid spatial binning
.
PDF
Compute the adaptive Gaussian KDE surface across spatial bandwidth (
h
s
​
=
1.5
–
4.0
 km
) and temporal bandwidth (
h
t
​
=
15
–
60
 mins
)
.
PDF
Train an XGBoost model over the composite feature set to rank ATM nodes within candidate bounding polygons
.
PDF
3. Time-to-Cashout Regressor (
T
remain
​
)
PDF
Objective:
Estimate the remaining operational window (in minutes) before funds are physically withdrawn from an ATM
.
PDF
Core Algorithm:
Gradient Boosted Decision Trees (GBDT Regressor)
.
PDF
Input Features:
Inter-hop transfer velocities (
Δ
t
) across intermediary layers
.
PDF
Current hop depth (layer count)
.
PDF
Total debited amount and transaction protocol type (UPI vs. IMPS/RTGS)
.
PDF
Time-of-day and operational banking window metrics
.
PDF
Target Output:
Continuous value representing remaining minutes (
T
remain
​
, typically within a 15–45 minute lead window)
.
PDF
Tech Stack:
LightGBM
/
XGBoost
,
Pandas
,
NumPy
,
Scikit-Learn
.
PDF
Implementation Steps:
Construct a training tabular matrix linking multi-hop transfer timestamps to final ATM cash-dispense events
.
PDF
Train the regression model using Root Mean Squared Error (RMSE) loss
.
PDF
Expose an inference endpoint to drive the live "Golden Hour" countdown ticker on dispatch dashboards
.
PDF
4. 1930 Call & Grievance Semantic Extractor
(Optional)
PDF
Objective:
Parse unstructured citizen voice-to-text transcripts or written complaint descriptions into structured telemetry payloads
.
PDF
Core Algorithm:
Fine-tuned Transformer / Named Entity Recognition (NER)
.
PDF
Input Features:
Unstructured citizen complaint strings, SMS debit alerts, or call logs
.
PDF
Target Output:
Extracted transaction metadata (UTR number, debited amount, beneficiary handle) and fraud classification label (e.g., Digital Arrest, Loan App, Task Scam)
.
PDF
Tech Stack:
transformers
(
all-MiniLM-L6-v2
),
HuggingFace
,
PyTorch
.
PDF
Implementation Steps:
Load the lightweight pretrained MiniLM model
.
PDF
Fine-tune a classification head on labeled Indian cyber fraud grievance summaries to categorize modus operandi and structure incoming parameters in
<
15
 ms
.
PDF
You said
HOW MODELS WORKS
HOW MODELS WORKS
The three core custom machine learning models in Project DURGAM work sequentially to detect laundering paths, forecast physical cash-out locations, and estimate interception timelines
:
PDF
End-to-End Inference Flow
[ New Complaint (UTR / Beneficiary) ]
│
▼
┌────────────────────────────────────────────────────────┐
│ 1. GNN Multi-Hop Mule Layering Engine                  │
│    • Ingests directed transaction subgraph             │
│    • Computes velocity: V = ΔAmount / Δt               │
│    • Flags laundering motifs (Fan-Out/Fan-In)          │
│    • Outputs: High-risk terminal mule account          │
└───────────────────────┬────────────────────────────────┘
│
┌───────────────┴───────────────┐
▼                               ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ 2. ST-KDE & XGBoost Hotspot  │ │ 3. Time-to-Cashout Regressor │
│    • Uber H3 spatial binning │ │    • Analyzes hop count &    │
│    • Computes spatial density│ │      inter-hop velocity      │
│    • Combines branch distance│ │    • Outputs: Estimated      │
│    • Outputs: Top 3–5 ATMs   │ │      minutes (T_remain)      │
└───────────────┬──────────────┘ └──────────────┬───────────────┘
│                               │
└───────────────┬───────────────┘
▼
[ Automated Bank Micro-Hold (<500ms) & Patrol Dispatch (<2min) ]
1. Multi-Hop Mule Layering Graph Engine (GNN)
Graph Representation:
Financial transactions are structured as a dynamic directed multigraph
G
=
(
V
,
E
,
W
)
, where vertices (
V
) represent bank accounts/wallets, directed edges (
E
) denote fund transfers, and weights (
W
) capture amounts and timestamps
.
PDF
Neighborhood Aggregation (Message Passing):
Using Graph Convolutional Networks (GCN) or GraphSAGE, each node aggregates embedding features from its
k
-hop inbound and outbound neighbors
:
PDF
Node features include account age, daily turnover baseline, and degree ratios
.
PDF
Edge features incorporate transfer volume and the inter-hop time delta (
Δ
t
)
.
PDF
Laundering Motif Isolation:
The network evaluates the
Mule Layering Velocity Score
:
V
m
u
l
e
​
(
P
)
=
∑
[
Δ
t
(
v
j
−
1
​
,
v
j
​
)
+
ϵ
Amount
(
v
j
−
1
​
,
v
j
​
)
​
]
⋅
exp
(
−
λ
⋅
HopLevel
(
v
j
​
))
PDF
This allows the model to differentiate rapid dormancy-to-burst multi-tier layering (Fan-Out/Fan-In loops) from legitimate merchant hub patterns
.
PDF
Operational Action:
Flags the terminal node (e.g., active debit card) in
<
85
 ms
to trigger the automated 30-minute micro-hold
.
PDF
2. Spatiotemporal ATM Hotspot Predictor (ST-KDE + XGBoost)
Spatial Indexing via Uber H3:
PostGIS ATM coordinates are converted into hexagonal H3 bins (Resolution 8) to enable sub-millisecond candidate filtering
.
PDF
Spatiotemporal Gaussian KDE:
Estimates the continuous spatial probability density of withdrawal across a geographical area using historical syndicate coordinates:
f
^
​
(
x
,
y
,
t
)
=
n
⋅
h
s
2
​
⋅
h
t
​
1
​
∑
K
s
​
(
h
s
​
x
−
x
i
​
​
,
h
s
​
y
−
y
i
​
​
)
⋅
K
t
​
(
h
t
​
t
−
t
i
​
​
)
PDF
h
s
​
: Adaptive spatial bandwidth (
1.5
–
4.0
 km
)
.
PDF
h
t
​
: Temporal bandwidth (
15
–
60
 mins
)
.
PDF
Composite Risk Scoring (
S
r
i
s
k
​
):
An XGBoost ranking classifier computes a unified probability score for every candidate ATM node (
A
k
​
):
S
r
i
s
k
​
(
A
k
​
)
=
σ
[
w
1
​
⋅
f
^
​
(
x
k
​
,
y
k
​
,
t
p
re
d
​
)
+
w
2
​
⋅
V
m
u
l
e
​
(
P
)
+
1
+
d
(
A
k
​
,
Branch
m
u
l
e
​
)
w
3
​
​
+
w
4
​
⋅
Hist
r
i
s
k
​
(
A
k
​
)
]
PDF
Operational Action:
Dispatches precise GPS coordinates of the top 3–5 ranked ATMs to the nearest patrol units
.
PDF
3. Time-to-Cashout Regressor (
T
remain
​
)
Feature Vector Ingestion:
Ingests the velocity gradient (
V
), transfer protocol (UPI/IMPS), hop depth, and total debited sum
.
PDF
GBDT Regression:
A gradient boosted decision tree (LightGBM/XGBoost) calculates the remaining operational interval (
T
remain
​
) before a mule runner reaches a physical ATM terminal
.
PDF
Operational Action:
Drives the "Golden Hour" countdown ticker on the command war room dashboard to prioritize live field units before cash dispense occurs
.
PDF
You said
how trained model or make that best ways
how trained model or make that best ways
Building high-accuracy, low-latency models for Project DURGAM requires a structured lifecycle covering dataset generation, architecture tuning, and deployment optimization
.
PDF
1. Data Pipeline & Feature Engineering
Because raw transaction logs are confidential, training begins with synthetically generated graph topologies combined with real geospatial data
:
PDF
Synthetic Graph Simulation (
NetworkX
):
Synthesize 50,000+ multi-hop transaction paths modeling key money laundering motifs
:
PDF
Fan-Out:
1 victim
→
5 mule accounts
.
PDF
Fan-In:
5 intermediary mules
→
1 terminal debit card/CSP
.
PDF
Circular Loops:
A
→
B
→
C
→
A
structuring
.
PDF
Real-World ATM Spatial Ground Truth:
Query real Indian ATM coordinates via the OpenStreetMap Overpass API (
amenity=atm
) and index them in PostGIS using
Uber H3 Resolution 8
hexagons
.
PDF
Feature Vector Formulation:
Node level: In/out degree ratio, account age, transaction burst velocity
.
PDF
Edge level: Transfer amount, velocity gradient
V
=
Δ
t
Δ
Amount
​
, and hop depth decay
exp
(
−
λ
⋅
HopLevel
)
.
PDF
Spatial level: Spatiotemporal density score
f
^
​
(
x
,
y
,
t
)
, road network distance
d
(
A
k
​
,
Branch
m
u
l
e
​
)
, and ATM operational status
.
PDF
2. Model Architecture & Training Best Practices
Model Component
Architecture & Loss Function
Optimization & Tuning Strategies
GNN Mule Detector
PDF
2-Layer
GraphSAGE / GCN
with Binary Cross-Entropy (BCE) Loss
PDF
• Use
Neighborhood Sampling
(
NeighborLoader
in PyG) to handle large graphs.
• Apply
Class Weighting / Focal Loss
to counter extreme class imbalance (mules vs. normal accounts).
• Use Dropout (0.2–0.3) to prevent overfitting on graph structures
.
PDF
ST-KDE Hotspot Predictor
PDF
Gaussian ST-KDE + XGBoost Classifier
PDF
• Dynamically tune spatial bandwidth (
h
s
​
=
1.5
–
4.0
 km
) and temporal bandwidth (
h
t
​
=
15
–
60
 mins
) based on urban vs. rural density
.
PDF
• Optimize XGBoost ranking with Bayesian Optimization (
Optuna
).
Time-to-Cashout Regressor
PDF
LightGBM / XGBoost Regressor
(RMSE / Huber Loss)
PDF
• Train on historical transaction timestamps vs. physical cash-out intervals
.
PDF
• Apply early stopping (50 rounds) on a holdout validation set to prevent drift.
3. Production Serving & Sub-180ms Optimization
To meet the sub-180ms execution target, implement the following deployment practices
:
PDF
ONNX & TensorRT Export:
Convert PyTorch GNN models to ONNX/TensorRT runtimes for accelerated GPU inference on NVIDIA L4/A10G instances
.
PDF
Spatial In-Memory Caching:
Cache candidate ATM clusters and rolling 15-minute transaction velocity metrics in
Redis 7
to eliminate redundant database round-trips
.
PDF
Sub-millisecond Spatial Indexing:
Restrict ATM queries to local bounding boxes using Uber H3 Resolution 8 spatial cells rather than performing brute-force distance scans across all 250,000+ national ATMs
.
PDF
4. Continuous Active Learning Loop
To eliminate concept drift as syndicates rotate locations or adjust cash-out speeds
:
PDF
[ Field Police Interception ]
├── Patrol taps [SUSPECT DETAINED] ────► Ground Truth Positive (y = 1)
└── 30-Min Hold Expires Unclaimed ────► Ground Truth Negative (y = 0)
│
▼
[ Nightly Retraining Pipeline ]
• Airflow DAG updates GNN weights
• Recalibrates XGBoost thresholds
Ground-Truth Logging:
Feedback from the Beat Patrol PWA (
[SUSPECT DETAINED]
or false alarms) automatically labels edge states
.
PDF
Automated Nightly Pipeline:
An Apache Airflow DAG retrains node embeddings and recalibrates classification decision thresholds nightly
.
PDF
Would you like a sample Python script using PyTorch Geometric and XGBoost to generate synthetic transaction data and train the initial baseline models?
You said
in detailed how to trained models
in detailed how to trained models
The step-by-step implementation and training procedures for the three custom AI/ML models in Project DURGAM are detailed below
:
PDF
1. Multi-Hop Mule Layering Engine (GraphSAGE / GCN)
Step A: Synthetic Graph Generation
Construct directed multigraphs using
NetworkX
to generate training samples of legitimate merchant hubs vs. illicit money-laundering motifs
:
PDF
Laundering Motifs:
Fan-Out:
1 victim node
→
5 intermediary mule nodes within
Δ
t
≤
3
 minutes
.
PDF
Fan-In:
5 intermediary mules
→
1 terminal debit card/CSP account
.
PDF
Circular Structuring:
A
→
B
→
C
→
A
loops to evade static threshold limits
.
PDF
Legitimate Baseline (Negative Class):
Normal merchant accounts exhibiting steady, continuous fan-in and predictable disbursement cadences
.
PDF
Step B: Feature Engineering
Node Feature Matrix (
X
∈
R
N
×
d
):
Account age (in days).
Normalized in-degree and out-degree ratios (
deg
−
+
1
deg
+
​
).
Burst transaction count in a rolling 15-minute window
.
PDF
Daily turnover deviation compared to historical baseline.
Edge Attributes (
E
∈
R
M
×
e
):
Transaction amount in INR (
Amount
).
Inter-transfer time delta (
Δ
t
)
.
PDF
Calculated velocity:
V
=
Δ
t
+
ϵ
Δ
Amount
​
.
PDF
Hop depth decay:
exp
(
−
λ
⋅
HopLevel
)
.
PDF
Step C: Model Architecture & Training Loop (
PyTorch Geometric
)
Architecture:
2-layer
SAGEConv
(GraphSAGE) with ReLU activations, Dropout (
p
=
0.25
), and an MLP binary classification head (
Sigmoid
output)
.
PDF
Loss Function:
Weighted Binary Cross-Entropy (BCE) or Focal Loss to manage class imbalance (e.g., pos_weight = 10.0)
.
PDF
Training Code Structure:
Python
import
torch
import
torch.nn
as
nn
from
torch_geometric.nn
import
SAGEConv
class
MuleGNN
(
nn.Module
):
def
__init__
(
self, in_feats, hidden_dim
):
super
().__init__()
self.conv1 = SAGEConv(in_feats, hidden_dim, aggr=
'mean'
)
self.conv2 = SAGEConv(hidden_dim, hidden_dim, aggr=
'max'
)
self.classifier = nn.Sequential(
nn.Linear(hidden_dim,
32
),
nn.ReLU(),
nn.Dropout(
0.25
),
nn.Linear(
32
,
1
)
)
def
forward
(
self, x, edge_index
):
h = torch.relu(self.conv1(x, edge_index))
h = torch.relu(self.conv2(h, edge_index))
out = torch.sigmoid(self.classifier(h))
return
out
# Training execution loop
model = MuleGNN(in_feats=
6
, hidden_dim=
64
).to(device)
criterion = nn.BCELoss(weight=class_weights)
optimizer = torch.optim.Adam(model.parameters(), lr=
0.001
, weight_decay=
1e-5
)
for
epoch
in
range
(
150
):
model.train()
optimizer.zero_grad()
preds = model(data.x, data.edge_index)
loss = criterion(preds[data.train_mask], data.y[data.train_mask])
loss.backward()
optimizer.step()
2. Spatiotemporal ATM Hotspot Predictor (ST-KDE + XGBoost)
Step A: Spatial Indexing & Dataset Preparation
Extract real Indian ATM points via the OpenStreetMap Overpass API (
node["amenity"="atm"]
) and persist them in PostGIS
.
PDF
Discretize coordinates into
Uber H3 Resolution 8
hexagonal cells (~0.7 km² area) for low-latency candidate lookups
.
PDF
Construct negative candidates by sampling nearby operational ATMs within an adaptive 5 km radius of the mule branch location
.
PDF
Step B: Spatiotemporal Density Function (ST-KDE)
Compute the continuous spatial probability density function:
f
^
​
(
x
,
y
,
t
)
=
n
⋅
h
s
2
​
⋅
h
t
​
1
​
i
=
1
∑
n
​
K
s
​
(
h
s
​
x
−
x
i
​
​
,
h
s
​
y
−
y
i
​
​
)
⋅
K
t
​
(
h
t
​
t
−
t
i
​
​
)
PDF
h
s
​
: Spatial bandwidth (
1.5
–
4.0
 km
)
.
PDF
h
t
​
: Temporal bandwidth (
15
–
60
 minutes
)
.
PDF
K
s
​
,
K
t
​
: Standard Gaussian kernels evaluating historical syndicate cash-out clusters
.
PDF
Step C: Tabular Feature Matrix & XGBoost Training
Features per candidate ATM (
A
k
​
):
Spatiotemporal KDE score (
f
^
​
(
x
k
​
,
y
k
​
,
t
p
re
d
​
)
)
.
PDF
Mule Layering Velocity Score (
V
m
u
l
e
​
(
P
)
) from the GNN output
.
PDF
Haversine distance to terminal mule account branch:
d
(
A
k
​
,
Branch
m
u
l
e
​
)
.
PDF
Historical syndicate cash-out count at this specific kiosk (
Hist
r
i
s
k
​
)
.
PDF
ATM operational status (e.g., active status, 24/7 lobby)
.
PDF
Training Implementation:
Python
import
xgboost
as
xgb
from
sklearn.model_selection
import
StratifiedKFold
params = {
'objective'
:
'binary:logistic'
,
'eval_metric'
:
'aucpr'
,
'max_depth'
:
5
,
'learning_rate'
:
0.03
,
'subsample'
:
0.8
,
'colsample_bytree'
:
0.8
,
'scale_pos_weight'
:
5.0
}
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(X_val, label=y_val)
bst = xgb.train(
params,
dtrain,
num_boost_round=
1000
,
evals=[(dtrain,
'train'
), (dval,
'val'
)],
early_stopping_rounds=
40
,
verbose_eval=
False
)
# Rank candidates and return top 3-5 ATMs by predicted probability
3. Time-to-Cashout Regressor (
T
remain
​
)
Step A: Temporal Dataset Construction
Create a tabular time-series dataset measuring the elapsed minutes between the primary victim transfer (
t
0
​
) and terminal physical ATM cash dispense (
t
cashout
​
)
:
PDF
T
remain
​
=
t
cashout
​
−
t
current
​
Step B: Feature Engineering
Inter-hop velocity: Average duration taken per hop (
hop
Δ
t
​
)
.
PDF
Current hop count (depth in graph)
.
PDF
Total siphoned amount (
INR
)
.
PDF
Payment network channel (UPI vs. IMPS/RTGS)
.
PDF
Time-of-day feature (hour encoded cyclically using
sin
/
cos
).
Step C: Model Training (
LightGBM
)
Train a gradient boosted regressor optimizing for Root Mean Squared Error (RMSE) / Huber Loss to output live countdown values
:
PDF
Python
import
lightgbm
as
lgb
reg_train = lgb.Dataset(X_time_train, label=y_time_train)
reg_val = lgb.Dataset(X_time_val, label=y_time_val, reference=reg_train)
reg_params = {
'objective'
:
'regression_l1'
,
# Robust to outliers
'metric'
:
'rmse'
,
'num_leaves'
:
31
,
'learning_rate'
:
0.05
,
'feature_fraction'
:
0.9
}
time_model = lgb.train(
reg_params,
reg_train,
num_boost_round=
500
,
valid_sets=[reg_train, reg_val],
callbacks=[lgb.early_stopping(stopping_rounds=
30
)]
)
4. Continuous Active Learning Retraining Pipeline
To maintain high precision in production without model degradation
:
PDF
Automated Labeling via Police Feedback:
When a patrol unit detains the suspect on-site (
[SUSPECT DETAINED]
), assign ground-truth label
y
=
1
.
PDF
If a 30-minute hold expires or a citizen clears a step-up challenge (
[FALSE ALARM]
), assign ground-truth label
y
=
0
.
PDF
Nightly Airflow Pipeline:
Ingest labeled operational logs from PostgreSQL/PostGIS
.
PDF
Fine-tune the GNN node embeddings and recalibrate the XGBoost ranking thresholds
.
PDF
Export models to TensorRT/ONNX runtimes for deployment on FastAPI inference workers
.
PDF
You said
from where i get data to trained my models
from where i get data to trained my models
To train the models in Project DURGAM, you obtain data through a combination of open geodata APIs, public benchmark datasets, and synthetic transaction generators
:
PDF
Data Sources by Model & Component
Component / Model
Data Source & Repository
Access Method & Cost
Data Output & Format
Real Indian ATM Geospatial Data
OpenStreetMap (OSM) via Overpass API
PDF
100% Free
(No API Key required)
PDF
Endpoint:
[https://overpass-api.de/api/interpreter](https://overpass-api.de/api/interpreter)
PDF
Coordinates (
lat
,
lon
), bank names, ATM amenities, and street addresses
.
PDF
Benchmark Multi-Hop AML Graphs
Elliptic AML Dataset
(available directly in
torch_geometric.datasets.EllipticBitcoinDataset
)
100% Free
(Open Source / PyG / Kaggle)
200k+ directed transaction graph nodes, edge lists, and binary labels (
licit
vs.
illicit
).
Synthetic Multi-Hop NCRP Transaction Generator
Custom NetworkX Simulation Script
PDF
Self-Generated
(Local Python environment)
PDF
50,000+ multi-tier Indian banking hops (Fan-Out, Fan-In, Circular Loops, UPI/IMPS time deltas)
.
PDF
Historical Hotspot Training Labels
Synthetic Spatiotemporal Case Logs
PDF
Self-Generated via Scipy/Numpy
Tuple data:
(timestamp, lat, lon, mule_branch_id, cashout_flag)
mapped to Uber H3 cells
.
PDF
1. Fetching Real Indian ATM Geodata (OpenStreetMap Overpass API)
Execute a direct Overpass QL query using Python
requests
to fetch actual bank ATM coordinates across target states or districts
:
PDF
Python
import
requests
import
json
import
pandas
as
pd
overpass_url =
"https://overpass-api.de/api/interpreter"
# Overpass query to fetch ATMs within a geographic bounding box (e.g., Delhi-NCR or Jammu)
overpass_query =
"""
[out:json][timeout:60];
area["ISO3166-1"="IN"][admin_level=2]->.india;
(
node["amenity"="atm"](area.india);
node["amenity"="bank"](area.india);
);
out body;
"""
response = requests.get(overpass_url, params={
'data'
: overpass_query})
data = response.json()
# Parse into DataFrame for PostGIS / Spatial DB ingestion
atms = []
for
element
in
data[
'elements'
]:
atms.append({
"osm_id"
: element[
'id'
],
"lat"
: element[
'lat'
],
"lon"
: element[
'lon'
],
"bank_name"
: element.get(
'tags'
, {}).get(
'operator'
,
'Unknown'
),
"amenity"
: element.get(
'tags'
, {}).get(
'amenity'
,
'atm'
)
})
df_atms = pd.DataFrame(atms)
df_atms.to_csv(
"indian_atms.csv"
, index=
False
)
2. Loading the Elliptic AML Benchmark Dataset (PyTorch Geometric)
Use PyG's built-in loader to train and evaluate baseline GNN architectures against real directed financial laundering subgraphs:
Python
from
torch_geometric.datasets
import
EllipticBitcoinDataset
# Automatically downloads and parses 203,769 nodes and 234,355 directed payment edges
dataset = EllipticBitcoinDataset(root=
"./data/elliptic"
)
data = dataset[
0
]
print(
f"Nodes:
{data.num_nodes}
, Edges:
{data.num_edges}
"
)
print(
f"Features per node:
{data.num_node_features}
"
)
3. Generating Synthetic Indian Multi-Hop Transaction Data (
NetworkX
)
Because real Core Banking System (CBS) transaction feeds are strictly confidential, use a Python generator to create 50,000 multi-hop paths simulating Indian banking topologies
:
PDF
Python
import
networkx
as
nx
import
numpy
as
np
import
random
import
time
def
generate_mule_network
(
num_cases=
1000
):
G = nx.MultiDiGraph()
current_time = time.time()
for
case_id
in
range
(num_cases):
victim =
f"VICTIM_
{case_id}
"
amount = random.randint(
50000
,
1500000
)
# INR
# 1. Simulate Fan-Out (Victim -> 3 to 5 Layer-1 Accounts)
l1_mules = [
f"L1_
{case_id}
_
{i}
"
for
i
in
range
(random.randint(
3
,
5
))]
split_amount = amount /
len
(l1_mules)
t0 = current_time + random.randint(
0
,
180
)
for
mule
in
l1_mules:
G.add_edge(victim, mule, amount=split_amount, timestamp=t0, hop=
1
)
# 2. Simulate Layering & Fan-In (Layer-1 -> Terminal Mule ATM Card)
terminal_mule =
f"TERMINAL_
{case_id}
"
t1 = t0 + random.randint(
180
,
600
)
# 3 to 10 mins delta
for
mule
in
l1_mules:
G.add_edge(mule, terminal_mule, amount=split_amount *
0.98
, timestamp=t1, hop=
2
)
return
G
synthetic_graph = generate_mule_network()
4. Constructing Spatiotemporal & Time-to-Cashout Tabular Data
Synthesize historical ground truth by pairing synthetic transaction velocities (
V
m
u
l
e
​
) with the geocoded ATM coordinates:
Combine ATM points with candidate terminal mule account home branches
.
PDF
Assign withdrawal intervals (
T
remain
​
) sampled from empirical distribution curves (
15
–
45
 minutes
)
.
PDF
Save the resulting matrix as a CSV file to train the
XGBoost Classifier
and
LightGBM Regressor
.
PDF
You said
point to point for better understanding with highlighted heading
point to point for better understanding with highlighted heading
1. Real-World Indian ATM Geospatial Data
Data Source:
OpenStreetMap (OSM) via the Overpass API
.
PDF
Cost & Access:
100% free with no API key or subscription required
.
PDF
Query Method:
Run direct Overpass QL queries filtering for
amenity=atm
and
amenity=bank
across Indian administrative boundaries
.
PDF
Extracted Attributes:
Exact latitude and longitude coordinates, ATM operator/bank brand, branch address, and operational amenity tags
.
PDF
Storage Target:
Ingest directly into PostgreSQL with PostGIS extension and index using Uber H3 Resolution 8 spatial hexagons for sub-millisecond querying
.
PDF
2. Baseline Graph Neural Network (GNN) Benchmark Data
Data Source:
Elliptic AML Dataset (available directly inside
torch_geometric.datasets
)
.
PDF
Cost & Access:
Free, open-source dataset maintained by researchers for financial graph learning
.
PDF
Extracted Attributes:
200,000+ directed transaction nodes, 230,000+ payment edges, and verified ground-truth labels (
licit
vs.
illicit
)
.
PDF
Operational Purpose:
Used to train, benchmark, and validate baseline Graph Convolutional Network (
GCN
) and
GraphSAGE
message-passing layers prior to custom synthetic data fine-tuning
.
PDF
3. Synthetic Multi-Hop Transaction Graph Data
Data Source:
Custom Python generation script using
NetworkX
.
PDF
Cost & Access:
Generated locally with zero infrastructure or licensing costs
.
PDF
Simulated Laundering Topologies:
Fan-Out:
1 victim node distributing funds across 3 to 5 Layer-1 mule accounts within minutes
.
PDF
Fan-In:
Multiple Layer-1/Layer-2 mule accounts aggregating funds into 1 terminal mule card/CSP point
.
PDF
Circular Loops:
Cyclical transactions (
A
→
B
→
C
→
A
) structured to bypass single-bank static thresholds
.
PDF
Generated Edge Features:
Transaction amount in INR, transfer timestamps, inter-hop time delta (
Δ
t
), and velocity gradient (
V
=
Δ
t
Δ
Amount
​
)
.
PDF
4. Historical ATM Hotspot & Time-to-Cashout Training Data
Data Source:
Synthesized spatiotemporal case matrices combining OSM ATM nodes with synthetic multi-hop transaction logs
.
PDF
Cost & Access:
Self-generated using Python (
NumPy
,
Pandas
,
SciPy
)
.
PDF
Hotspot Predictor Features:
Spatiotemporal Gaussian Kernel Density score (
f
^
​
(
x
,
y
,
t
)
)
.
PDF
Haversine road distance from the candidate ATM to the registered terminal mule bank branch (
d
(
A
k
​
,
Branch
m
u
l
e
​
)
)
.
PDF
Mule Layering Velocity Score (
V
m
u
l
e
​
) passed from the GNN output
.
PDF
Historical syndicate cash-out frequency per kiosk
.
PDF
Time-to-Cashout Regressor Features:
Inter-hop velocity, hop depth, transaction method (UPI vs. IMPS), total amount, and actual elapsed minutes until physical cash-out (
T
remain
​
, sampled across a 15–45 minute window)
.
PDF
5. Continuous Active Learning & Ground-Truth Production Feedback
Data Source:
Real-time feedback emitted from law enforcement field operations
.
PDF
Positive Labels (
y
=
1
):
Recorded when a beat patrol officer taps
[SUSPECT DETAINED]
or confirms fund recovery at the predicted ATM kiosk
.
PDF
Negative Labels (
y
=
0
):
Recorded when a 30-minute micro-hold dissolves automatically without police action or an account owner clears an authentication challenge
.
PDF
Model Updating:
An automated nightly pipeline retrains GNN node embeddings and recalibrates XGBoost decision thresholds to eliminate concept drift over time
.
PDF
You said
how its help in digital fraud its main focus on atm i guess
how its help in digital fraud its main focus on atm i guess
While ATM cash-out is the primary physical bottleneck where recovery normally collapses from ~70% to under 3%, Project DURGAM intervenes directly across the digital lifecycle of online cyber fraud
:
PDF
Cross-Bank Digital Multi-Hop Layering Interception:
In digital scams (such as Digital Arrests, Telegram tasks, fake loan apps, or phishing), syndicates route funds across 3 to 7 layers of intermediary accounts within 8 to 15 minutes
. DURGAM’s Graph Neural Network (GNN) tracks cross-bank UPI and IMPS transactions in real time (<85 ms), detecting fan-out, fan-in, and circular laundering patterns across separate financial institutions
.
PDF
+ 1
Automated Pre-Settlement Micro-Holds (<500 ms):
Instead of waiting 2 to 6 hours for manual bank ticketing, the platform issues automated ISO 20022
camt.056
webhooks to Core Banking Switches (CBS)
. This places a 30-minute temporary settlement hold on the scammer’s digital ledger and virtual debit cards while funds are still hopping digitally between bank accounts
.
PDF
+ 1
On-Chain Fiat-to-Crypto / VASP Monitoring:
When digital syndicates attempt to convert stolen INR into cryptocurrency (e.g., P2P USDT on Tron or Ethereum), DURGAM links fiat banking hops to public blockchain ledgers to trace suspect deposit endpoints and trigger virtual asset service provider (VASP) freeze hooks
.
PDF
AePS Biometric Fraud & Settlement Wallet Freezes:
For digital frauds exploiting Aadhaar-Enabled Payment Systems (AePS) via cloned silicone thumbprints, DURGAM detects geographic withdrawal anomalies across rural Customer Service Points (CSPs) and auto-freezes the fraudulent operator’s digital settlement wallet within 15 minutes
.
PDF
Protection of Legitimate Digital Commerce (MSMEs):
Traditional police responses often result in blanket freezes of innocent e-commerce accounts and merchants
. DURGAM uses graph topology filtering and GSTN/PAN correlation to separate normal high-volume digital business inflows from rapid dormancy-to-burst mule operations, reducing false merchant freezes by 85%
.
PDF
+ 1
Court-Admissible Evidence for Digital Cyber Crime (BSA Sec 63):
Every digital transaction trace, API payload, and timestamp is hashed into an off-chain Merkle tree and sealed on the Polygon blockchain
. This creates a tamper-proof Section 63 BSA certificate that prevents defense lawyers from claiming digital logs or IP records were modified during prosecution
.
PDF
+ 1
You said
whole everything work who can access it and how fully functional all pages how pages must exist in p…
whole everything work who can access it and how fully functional all pages how pages must exist in project durgam
Project DURGAM is structured as a sovereign, multi-portal web application where access is strictly partitioned by
Role-Based Access Control (RBAC)
, asymmetric signed JWTs (ED25519), and Government Single Sign-On (SSO / Parichay)
.
PDF
User Access Control & Permissions Matrix
User Role
Target Stakeholder
Authentication Method
Assigned Scope & Access Level
1. Citizen / Victim
PDF
General public reporting cyber fraud
PDF
Passwordless Mobile OTP (5-min TTL)
PDF
Public reporting form, live case status tracker, and bank dispute kit download
.
PDF
2. Cyber Police Commander
PDF
I4C Directors, State Cyber Cell SPs, Cyber Cell Officers
PDF
Parichay / Meri Pehchaan SSO + PKI token
PDF
SCOPE_NATIONAL_COMMAND
(3D GIS War Room, GNN Money Trail Graph, Golden Hour queue)
.
PDF
3. Beat Patrol Officer
PDF
PCR van drivers, sub-inspectors, on-field beat constables
PDF
Belt Number / Phone + Mobile OTP
PDF
SCOPE_BEAT_PATROL
(Tactical action cards, turn-by-turn navigation deep-links, on-site status toggles)
.
PDF
4. Bank Nodal Officer
PDF
Fraud Risk Management (FRM) teams at banks (SBI, HDFC, etc.)
PDF
Bank AD / LDAP SSO + OTP / PKI Token
PDF
SCOPE_BANK_NODAL
(Core Banking Stream, 1-click micro-hold approval, Zero-Knowledge lookup)
.
PDF
5. Trial Court Judge / Legal Auditor
PDF
Magistrates, judicial auditors, defense attorneys
PDF
Public Case FIR / CNR Number + Captcha
PDF
SCOPE_COURT_AUDIT
(Read-only Polygon blockchain Section 63 BSA certificate verifier)
.
PDF
Mandatory Frontend Pages & UI Specifications
durgam.gov.in (Landing Portal)
│
┌────────────────────────────────┼────────────────────────────────┐
│                                │                                │
▼                                ▼                                ▼
1. /report                      2. /track/:id                   3. /auth/login
(60-Sec Express Filing)         (Live Recovery Tracker)         (Sovereign Gateway)
│
┌─────────────────────────────────────────────────┼──────────────────────────────┐
▼                                                 ▼                              ▼
4. /command/war-room                              5. /patrol/cad                 6. /bank/risk-portal
(3D Map & GNN Graph)                              (Field Action Card)            (Micro-Hold & ZK Search)
1. Public Landing & Express Complaint Filing (
/
&
/report
)
Target Audience:
Citizens reporting unauthorized debit incidents
.
PDF
Core Components:
4-Field Express Form:
Victim Phone, Victim Bank Name, Debited Amount (₹), and Transaction Reference (UTR / UPI Ref ID)
.
PDF
AI OCR Screenshot Parser:
Drag-and-drop box for bank SMS screenshots or UPI payment receipts to extract UTR automatically
.
PDF
Zero-Password OTP Login:
1-minute express authentication verifying the victim's mobile number
.
PDF
2. Citizen Live Recovery Dashboard (
/track/:complaintId
)
Target Audience:
Aggrieved citizens tracking fund recovery progress
.
PDF
Core Components:
4-Stage Visual Progress Bar:
[Grievance Filed]
→
[Banking Micro-Hold Active]
→
[ATM Intercepted]
→
[Bank Refund In Progress]
.
PDF
Live Fund Protection Status:
Real-time badge indicating whether stolen funds are quarantined in banking escrow
.
PDF
1-Click Bank Dispute Kit:
Button to download a pre-filled, Section 63 BSA-certified PDF to present to the home bank for escrow reversal
.
PDF
3. Sovereign Login & Role Gateway (
/auth/login
)
Target Audience:
Police officers, bank nodal authorities, and judicial auditors
.
PDF
Core Components:
Multi-Role Switcher Tabs:
Directs to Parichay (Govt SSO), Bank Active Directory, or Police Belt ID login
.
PDF
Middleware Router:
Inspects the issued JWT claims (
SCOPE_*
) to route the user to their designated dashboard
.
PDF
4. Cyber Police Command War Room (
/command/war-room
)
Target Audience:
Central and State Cyber Cell Directors, District SPs
.
PDF
Core Components:
3D Mapbox GL / Deck.gl Map:
Interactive dark-mode GIS showing pulsing red high-risk ATM hotspots, jurisdictional boundaries, and live PCR van telemetry
.
PDF
Force-Directed Graph Viewer (Cytoscape.js):
Visual diagram animating fund paths from Victim
→
Layer 1
→
Layer 2
→
Terminal Cash-Out Kiosks
.
PDF
Live "Golden Hour" Countdown Queue:
Prioritized list of active cases showing estimated minutes remaining (
T
remain
​
) before cash-out
.
PDF
1-Click Forensic Export:
Generates court-admissible dossiers with cryptographic SHA-256 Polygon block receipts
.
PDF
5. Mobile Beat Patrol CAD Interface (
/patrol/cad
)
Target Audience:
PCR van drivers and beat constables on street patrol (Mobile PWA & Telegram bot)
.
PDF
Core Components:
Tactical Action Card:
Displays Target ATM Name, Exact Address, Distance (e.g., "1.4 km - 4 min drive"), and Risk Score (
S
r
i
s
k
​
)
.
PDF
1-Tap Navigation Trigger:
Deep-links directly into Google Maps/MapMyIndia with optimized emergency routing
.
PDF
Status Toggle Buttons:
Quick action triggers:
[UNIT ON-SITE]
,
[SUSPECT DETAINED]
,
[ATM SECURED]
(feeds directly into the active learning loop)
.
PDF
Offline/SMS Fallback Mode:
Operates using IndexedDB cached vector tiles when cell service drops below 3G
.
PDF
6. Bank Nodal FRM Terminal (
/bank/risk-portal
)
Target Audience:
Fraud Risk Management (FRM) officers across participating banks
.
PDF
Core Components:
Core Banking Stream:
Real-time audit list of accounts flagged by the GNN velocity engine
.
PDF
1-Click Micro-Hold Trigger:
Review and confirm 30-minute provisional liens (ISO 20022
camt.056
) with automatic 30-minute auto-release timers
.
PDF
Zero-Knowledge Mule Search:
Salted hash lookup field to query incoming account numbers against the national blacklist without exposing client PII
.
PDF
You said
Mandatory Frontend Pages & UI Specifications regenerate new one
Mandatory Frontend Pages & UI Specifications regenerate new one
Mandatory Frontend Pages & UI Specifications
durgam.gov.in (Landing Portal)
│
┌────────────────────────────────┼────────────────────────────────┐
│                                │                                │
▼                                ▼                                ▼
1. /report
2. /track/:id
3. /auth/login
(60-Sec Express Filing)
(Live Recovery Tracker)
(Sovereign Gateway)
│
┌─────────────────────────────────────────────────┼──────────────────────────────┐
▼                                                 ▼                              ▼
4. /command/war-room
5. /patrol/cad
6. /bank/risk-portal
(3D Map & GNN Graph)
(Field Action Card)
(Micro-Hold & ZK Search)
1. Public Landing & Express Incident Reporting (
/
&
/report
)
Target Audience:
Citizens reporting financial fraud in real time
.
PDF
4-Field Express Form:
Collects the essential incident parameters: victim mobile number, bank name, debited sum, and transaction reference (UTR / UPI Ref ID)
.
PDF
AI OCR Screenshot Parser:
Automated intake box allowing users to upload bank debit SMS screenshots or transaction slips to extract UTR and beneficiary handles within seconds
.
PDF
Passwordless Verification:
Mobile OTP-based authorization with ephemeral sessions to allow sub-minute reporting without cumbersome multi-page FIR paperwork
.
PDF
2. Citizen Live Fund Recovery Dashboard (
/track/:complaintId
)
Target Audience:
Victims tracking fund interception and reversal status
.
PDF
4-Stage Visual Progress Ticker:
Real-time lifecycle bar tracking:
[Grievance Filed]
⟶
[Banking Micro-Hold Active]
⟶
[ATM Intercepted]
⟶
[Bank Refund In Progress]
 
\cite
: 1
Live Escrow Status Card:
Visual indicator verifying whether the siphoned amount is currently protected under a pre-settlement micro-lien across intermediary beneficiary accounts
.
PDF
1-Click Bank Dispute Kit:
Generates a pre-filled, downloadable PDF claim package embedded with cryptographic blockchain block receipts for submission to the victim's home branch
.
PDF
3. Sovereign Authentication Gateway (
/auth/login
)
Target Audience:
Law enforcement commanders, field beat officers, bank FRM managers, and judicial auditors
.
PDF
Multi-Role Selector:
Separate entry options for Government Parichay SSO, Bank Active Directory/LDAP, Police Belt ID verification, and e-Courts case verification
.
PDF
Role-Based Scope Router:
Verifies cryptographic asymmetric JWT tokens (ED25519) and automatically directs the user to their permitted role interface (
SCOPE_NATIONAL_COMMAND
,
SCOPE_BEAT_PATROL
,
SCOPE_BANK_NODAL
, or
SCOPE_COURT_AUDIT
)
.
PDF
4. Cyber Police Command War Room (
/command/war-room
)
Target Audience:
Central 14C directors, State Cyber Cell chiefs, and District SPs
.
PDF
3D Geospatial GIS Map (Mapbox GL / Deck.gl):
Interactive dark-mode map overlay rendering pulsing high-risk ATM hotspots, jurisdictional boundaries, and live patrol unit coordinates
[cite: 1]
.
Interactive GNN Graph Visualizer (Cytoscape.js):
Force-directed transaction topology tracing the real-time money trail across intermediary multi-hop mule tiers from initial victim to terminal debit card
[cite: 1]
.
"Golden Hour" Priority Queue:
Live countdown ledger highlighting active high-priority cases with calculated minutes remaining (
T
remain
​
) before physical cash withdrawal occurs
[cite: 1]
.
Section 63 BSA Dossier Export:
One-click tool compiling verified chain-of-custody reports with SHA-256 smart contract block hashes for court prosecution
[cite: 1]
.
5. Mobile Beat Patrol CAD Interface (
/patrol/cad
)
Target Audience:
PCR van drivers, sub-inspectors, and on-street beat constables (Mobile PWA & Telegram bot)
[cite: 1]
.
Tactical Action Card:
Displays exact target ATM name, street address, estimated driving time/distance, and calculated interception risk probability (
S
r
i
s
k
​
)
[cite: 1]
.
1-Tap GPS Dispatch:
Direct deep-link launching pre-routed turn-by-turn emergency navigation in Google Maps or MapMyIndia
[cite: 1]
.
Field Action Triggers:
Real-time state toggles (
[UNIT ON-SITE]
,
[SUSPECT DETAINED]
,
[ATM SECURED]
) that close the operational loop and provide ground truth to the retraining pipeline
[cite: 1]
.
Offline Resilience Mode:
Client-side Service Worker utilizing IndexedDB to store cached district vector tiles and ATM nodes during network dropouts, paired with SMS dispatch failover
[cite: 1]
.
6. Bank Nodal FRM Terminal (
/bank/risk-portal
)
Target Audience:
Fraud Risk Management (FRM) officers across scheduled commercial banks
[cite: 1]
.
Core Banking Ingestion Stream:
Live tabular stream of incoming transactions flagged with anomalous velocity gradients and structural laundering motifs
[cite: 1]
.
1-Click Micro-Hold Enforcement:
Direct interface to review and execute automated 30-minute pre-settlement liens (ISO 20022
camt.056
) at the Core Banking Switch level
[cite: 1]
.
Zero-Knowledge Mule Lookup:
Search tool using salted hashes (
SHA256
(
Account
∥
IFSC
∥
Salt
)
) to query the consortium blacklist registry without compromising customer data under the DPDP Act 2023
[cite: 1]
.
You said
for prototype i need to it genuine or dynamix
for prototype i need to it genuine or dynamix
For a winning prototype, you should build a
Dynamic System operating on Genuine Real-World Data
.
Judges and technical evaluators can immediately spot purely hardcoded static screens (which feel like clickable mockups), but they do not expect full production bank server access. Implementing dynamic backend logic using real geodata provides the necessary technical depth
.
PDF
What Must Be Genuine (Real-World Anchors)
Real Indian ATM & Bank Coordinates:
Query actual ATM locations via the OpenStreetMap Overpass API so map coordinates, bank brands, and street names in your target city (e.g., Delhi, Jammu, or Taoru) are authentic
.
PDF
Live Testnet Blockchain Transactions:
Deploy your
EvidenceLocker.sol
or
MerkleEvidenceLocker.sol
smart contract on the
Polygon Amoy Testnet
. When a test incident is reported, write a real on-chain transaction and provide the clickable Polygonscan block receipt URL in your UI
.
PDF
+ 1
Real Mobile Dispatch via Telegram / PWA:
Connect the actual Telegram Bot API to send live, real-time push alerts with working Google Maps deep-links to your phone during the demonstration
.
PDF
Standards-Compliant Messaging Payloads:
Use standard ISO 20022
camt.056
JSON/XML webhook schemas and Section 63 BSA legal certificate formatting
.
PDF
What Must Be Dynamic (Functional Code & Logic)
Dynamic Ingestion & Routing:
When a user submits an arbitrary UTR number, debited amount, and beneficiary handle on
/report
, the FastAPI backend must dynamically process that exact input without returning hardcoded static text
.
PDF
Live Graph Construction & Velocity Calculation:
The backend should dynamically construct an in-memory directed NetworkX graph, calculate
V
=
Δ
t
Δ
Amount
​
, and execute model inference on the fly
.
PDF
Dynamic Geospatial Scoring & Bounding:
Run the ST-KDE and XGBoost scoring dynamically to select candidate ATMs nearest to the input transaction's terminal branch rather than displaying a static pre-saved pin
.
PDF
Real WebSocket State Synchronization:
Use WebSockets or Server-Sent Events (SSE) so that when a simulated bank hold triggers, the War Room map pulses, the citizen progress tracker increments to
[Banking Micro-Hold Active]
, and the beat patrol interface updates simultaneously
.
PDF
What You Should Safely Simulate (Mock Layer)
Core Banking Switch (CBS) Settlement Engine:
Simulate the bank switch (e.g., Finacle/BaNCS) using a local FastAPI mock endpoint that accepts the ISO 20022
camt.056
micro-lien payload and returns an automated
200 OK
with a 30-minute expiration timestamp
.
PDF
NCRP 1930 Upstream Feed:
Simulate the raw telephonic grievance intake by providing a quick "Seed Demo Case" button on your intake form that pre-populates typical scam scenarios (e.g., Digital Arrest, Task Fraud)
.
PDF
Architecture for Demo Flow
[ Enter Dynamic Form Data / Select Preset Scenario ]
│
▼
[ Real FastAPI Ingestion & GNN Calculation ]
│
─────────────────┴─────────────────
│                                   │
▼                                   ▼
[ Dynamic PostGIS ST-KDE Query ]  [ Real Polygon Amoy Web3 Call ]
(Actual OSM Indian ATM Pins)      (Live On-Chain Transaction Hash)
│                                   │
▼                                   ▼
[ Live WebSocket Map Update ]      [ Real Telegram Alert to Phone ]
Combining dynamic Python computation with genuine OpenStreetMap locations and live testnet smart contracts delivers a fully demonstrable, high-impact prototype without requiring restricted banking credentials
.
PDF
You said
design how much Pages  button on home page everything all pages i need to make
design how much Pages  button on home page everything all pages i need to make
Project DURGAM requires
6 core application pages
plus 1 optional public verification view to cover all citizen, police, banking, and judicial workflows
:
PDF
Page Architecture & Routing Matrix
Page Route
Page Name
Primary User Persona
Core Functionality
/
Public Landing Page
PDF
General Citizens & Visitors
PDF
Platform overview, emergency hotline link, and quick entry points
.
PDF
/report
60-Sec Express Filing
PDF
Victims of Cyber Fraud
PDF
Rapid incident intake with OCR screenshot ingestion
.
PDF
/track/:id
Citizen Live Recovery Tracker
PDF
Aggrieved Citizens
PDF
4-stage fund tracking and bank refund kit download
.
PDF
/auth/login
Sovereign Login Gateway
PDF
Police, Bank Officers, Judges
PDF
Multi-role SSO routing by cryptographic JWT scopes
.
PDF
/command/war-room
Cyber Command War Room
PDF
State/Central Cyber Police
PDF
3D Mapbox GIS, GNN money trail graph, Golden Hour queue
.
PDF
/patrol/cad
Beat Patrol Field CAD
PDF
PCR Vans & Beat Constables
PDF
Mobile tactical action cards and 1-tap Google Maps siren navigation
.
PDF
/bank/risk-portal
Bank Nodal FRM Terminal
PDF
Bank Risk Management Officers
PDF
Live transaction feed, 1-click 30-min micro-holds, ZK search
.
PDF
/verify
(Optional)
BSA Sec 63 Blockchain Audit
PDF
Judges, Lawyers, Public
PDF
Independent SHA-256 Merkle proof inspector on Polygon Amoy
.
PDF
Home Page (
/
) Layout & Interactive Elements
┌────────────────────────────────────────────────────────────────────────┐
│  [DURGAM LOGO]     National Cybercrime Defense Grid     [Official SSO] │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│       EMERGENCY CYBER FRAUD DEFENSE: SUB-SECOND INTERCEPTION           │
│                                                                        │
│   [ 🚨 REPORT FRAUD (60s EXPRESS) ]      [ 🔍 TRACK COMPLAINT STATUS ] │
│                                                                        │
├────────────────────────────────────────────────────────────────────────┤
│  ⚡ Live Metrics: ₹6,000+ Cr Protected | <500ms Freeze | >88% Forecast  │
├────────────────────────────────────────────────────────────────────────┤
│  Demo Scenarios: [Digital Arrest] [Telegram VIP] [AePS CSP] [Loan App] │
├────────────────────────────────────────────────────────────────────────┤
│  Quick Links: [Helpline 1930]  [Section 63 Verifier]  [Bank FRM Portal]│
└────────────────────────────────────────────────────────────────────────┘
Header Navigation Buttons
[DURGAM Logo / Home]
: Resets view to landing page.
[Helpline 1930 Direct Dial]
: Triggers a
tel:1930
call protocol prompt
.
PDF
[Official Sovereign Login]
: Routes directly to
/auth/login
for law enforcement and banking authorities
.
PDF
Hero Section Action Buttons
[🚨 Report Fraud Now (60-Sec Express)]
: Primary prominent button routing to
/report
.
PDF
[🔍 Track Recovery Status]
: Input field with a
[Track]
button routing to
/track/{complaintId}
.
PDF
Hackathon Interactive Demo Switcher
[Demo: Digital Arrest]
: Pre-populates a simulated ₹15,00,000 RTGS fraud scenario
.
PDF
[Demo: Telegram VIP Task]
: Pre-populates a 4-hop merchant QR scam scenario
.
PDF
[Demo: AePS Biometric Spike]
: Pre-populates rural CSP cloned withdrawal telemetry
.
PDF
Detailed Page-by-Page Feature Blueprint
1. Express Grievance Filing Page (
/report
)
Form Inputs:
Victim Mobile Number & OTP input
.
PDF
Victim Bank Name dropdown
.
PDF
Debited Amount (₹)
.
PDF
Transaction Reference (UTR / UPI Ref ID)
.
PDF
Beneficiary UPI ID or Account Number
.
PDF
Interactive Ingestion Card:
Drag-and-drop box for bank SMS screenshots; triggers optical character recognition (OCR) to parse UTR and amounts automatically
.
PDF
Submit Button:
[⚡ Trigger Sub-Second Defense]
; initiates backend GNN traversal and outputs tracking token in
<
180
 ms
.
PDF
2. Citizen Live Recovery Dashboard (
/track/:id
)
Visual Progress Ticker:
4 horizontal checkpoints:
[Grievance Filed]
→
[Banking Micro-Hold Active]
→
[ATM Intercepted]
→
[Bank Refund In Progress]
.
PDF
Fund Escrow Badge:
Visual card displaying current protected balance (e.g.,
₹15,00,000 Quarantined in Escrow
)
.
PDF
Action Buttons:
[📥 Download 1-Click Bank Dispute Kit]
: Downloads Section 63 BSA-certified PDF claim packet
.
PDF
[💬 Open 24/7 Recovery Assistant]
: Launches AI guidance chat modal
.
PDF
3. Sovereign Role Gateway (
/auth/login
)
Role Switcher Tabs:
[Parichay / Meri Pehchaan SSO]
(Police Commanders)
.
PDF
[Beat Patrol Belt ID + OTP]
(Field Officers)
.
PDF
[Bank Active Directory / LDAP]
(Bank FRM Nodal Officers)
.
PDF
[e-Courts Case CNR Lookup]
(Magistrates & Legal Auditors)
.
PDF
Submit Action:
[Authenticate & Enter Secure Grid]
; validates credentials and issues an ED25519 asymmetric scoped JWT token
.
PDF
4. Cyber Police Command War Room (
/command/war-room
)
3D Geospatial GIS Map (Mapbox GL / Deck.gl):
Interactive dark-mode map rendering pulsing red ATM target pins and jurisdiction overlays
.
PDF
Live PCR van telemetry icons with ETA indicators
.
PDF
GNN Money Trail Graph (Cytoscape.js):
Force-directed node graph animating fund flows across Layer 1, Layer 2, and terminal mule nodes
.
PDF
"Golden Hour" Priority Queue:
Live side ledger displaying active cases sorted by estimated cash-out minutes remaining (
T
remain
​
)
.
PDF
Action Buttons:
[🚨 Force Instant Micro-Hold]
: Manually pushes emergency hold requests to banks
.
PDF
[📡 Dispatch Nearest PCR Unit]
: Sends turn-by-turn routing to field units
.
PDF
[📜 Export Section 63 BSA Court Dossier]
: Downloads verified charge-sheet evidence package with SHA-256 Polygon transaction receipt
.
PDF
5. Mobile Beat Patrol CAD Interface (
/patrol/cad
)
Tactical Action Card:
High-contrast card showing Target ATM Name, Exact Street Address, Calculated Risk Probability (
S
r
i
s
k
​
), and Suspect Profile indicators
.
PDF
Primary Navigation Button:
[🚨 1-Tap Google Maps Siren Route]
; launches native turn-by-turn emergency navigation
.
PDF
Field Status Toggles:
[📍 UNIT ON-SITE]
PDF
[👮 SUSPECT DETAINED]
(Feeds positive label
y
=
1
into the retraining loop)
.
PDF
[🏧 ATM SECURED]
PDF
Offline Status Indicator:
Shows whether the client is syncing over WebSockets or fallback Encrypted SMS/USSD
.
PDF
6. Bank Nodal FRM Terminal (
/bank/risk-portal
)
Core Banking Feed Table:
Live tabular list of flagged high-velocity incoming transfers across accounts
.
PDF
Action Buttons per Row:
[🔒 Apply 30-Min Pre-Settlement Micro-Lien]
: Executes ISO 20022
camt.056
hold via simulated Core Banking Switch (CBS) API
.
PDF
[🔓 Release Hold]
: Manually unlocks accounts after verified step-up OTP challenge
.
PDF
Zero-Knowledge Search Box:
Salted hash lookup search bar (
SHA256(Account || IFSC || Salt)
) to verify accounts against the national consortium blacklist without exposing customer balances
.
PDF
Google Privacy Policy
Opens in a new window
Google Terms of Service
Opens in a new window
Your privacy & Gemini Apps
Opens in a new window
Gemini may display inaccurate info, including about people, so double-check its responses.
Sign in
Google apps
Uploaded file not shown
Copy public link
Report
Not included in response: Durgam Project
Copy prompt
Download code
Copy code