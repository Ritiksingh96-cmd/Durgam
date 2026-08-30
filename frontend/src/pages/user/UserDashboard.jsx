import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import { fileComplaint, listMyComplaints, trackComplaint } from '../../api';

const FRAUD_TYPES = [
  'UPI Fraud', 'ATM Fraud', 'Online Banking Fraud',
  'Credit Card Fraud', 'Investment Scam', 'Job Scam', 'Lottery Scam', 'Other',
];

function StatusBadge({ status }) {
  const map = {
    pending: ['badge-pending', '⏳ Pending'],
    under_investigation: ['badge-investigation', '🔍 Investigating'],
    chain_detected: ['badge-chain', '🔗 Chain Found'],
    resolved: ['badge-resolved', '✅ Resolved'],
    closed: ['badge-resolved', '🔒 Closed'],
  };
  const [cls, lbl] = map[status] || ['badge-pending', status];
  return <span className={`badge ${cls}`}>{lbl}</span>;
}

function Sidebar({ activeTab, setActiveTab, userName, logout }) {
  const items = [
    { key: 'complaints', icon: '📋', label: 'My Complaints' },
    { key: 'file', icon: '✍️', label: 'File Complaint' },
    { key: 'track', icon: '🔍', label: 'Track Complaint' },
  ];
  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="logo-row">
          <div className="logo-icon">🛡️</div>
          <span className="logo-text">Durgam</span>
        </div>
        <div className="role-pill" style={{ background: '#f3f0ff', color: '#7c3aed' }}>Citizen Portal</div>
        <div className="user-info">👤 {userName}</div>
      </div>
      <nav className="sidebar-nav">
        {items.map(item => (
          <button key={item.key}
            className={activeTab === item.key ? 'active' : ''}
            onClick={() => setActiveTab(item.key)}>
            <span className="nav-icon">{item.icon}</span> {item.label}
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <button onClick={logout}>🚪 Logout</button>
      </div>
    </div>
  );
}

export default function UserDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('complaints');
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(false);
  const [trackNo, setTrackNo] = useState('');
  const [trackedData, setTrackedData] = useState(null);
  const [filedResult, setFiledResult] = useState(null);
  const [form, setForm] = useState({
    description: '', amount: '', to_account: '', to_bank_ifsc: '',
    transaction_id: '', fraud_type: 'UPI Fraud', transaction_date: '',
  });

  const doLogout = () => { logout(); navigate('/'); };

  useEffect(() => {
    if (activeTab === 'complaints') fetchComplaints();
  }, [activeTab]);

  const fetchComplaints = async () => {
    setLoading(true);
    try { const { data } = await listMyComplaints(); setComplaints(data); }
    catch { toast.error('Failed to load'); } finally { setLoading(false); }
  };

  const submitComplaint = async (e) => {
    e.preventDefault(); setLoading(true);
    try {
      const payload = { ...form, amount: parseFloat(form.amount), transaction_date: form.transaction_date || undefined };
      const { data } = await fileComplaint(payload);
      setFiledResult(data);
      toast.success('Complaint filed!');
      setForm({ description: '', amount: '', to_account: '', to_bank_ifsc: '', transaction_id: '', fraud_type: 'UPI Fraud', transaction_date: '' });
    } catch (err) { toast.error(err.response?.data?.detail || 'Failed'); }
    finally { setLoading(false); }
  };

  const doTrack = async () => {
    if (!trackNo.trim()) return toast.error('Enter a complaint number');
    setLoading(true); setTrackedData(null);
    try { const { data } = await trackComplaint(trackNo.trim()); setTrackedData(data); }
    catch { toast.error('Complaint not found'); } finally { setLoading(false); }
  };

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  return (
    <div className="dashboard-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} userName={user?.name} logout={doLogout} />
      <div className="main-content">

        {/* ── MY COMPLAINTS ── */}
        {activeTab === 'complaints' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 24 }}>
              <div className="page-header" style={{ marginBottom: 0 }}>
                <div className="page-title">My Complaints</div>
                <div className="page-subtitle">Track all your filed complaints</div>
              </div>
              <button className="btn btn-primary" onClick={() => setActiveTab('file')}>
                ✍️ File New Complaint
              </button>
            </div>

            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : complaints.length === 0 ? (
              <div className="empty-state">
                <div className="icon">📋</div>
                <h3>No Complaints Yet</h3>
                <p>File a complaint to get started tracking cyber fraud cases.</p>
                <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setActiveTab('file')}>
                  ✍️ File a Complaint
                </button>
              </div>
            ) : complaints.map(c => (
              <div key={c.id} className="complaint-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                  <span className="complaint-no">{c.complaint_no}</span>
                  <StatusBadge status={c.status} />
                </div>
                <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 8, flexWrap: 'wrap' }}>
                  <span className="complaint-amount">₹{c.amount?.toLocaleString('en-IN')}</span>
                  <span className="badge badge-danger" style={{ fontSize: 11 }}>{c.fraud_type}</span>
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 6, lineHeight: 1.5 }}>{c.description}</div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                  To account: <span style={{ fontFamily: 'monospace', color: 'var(--text-primary)', fontWeight: 600 }}>{c.to_account}</span>
                  {c.to_bank_ifsc && <> · IFSC: {c.to_bank_ifsc}</>}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
                  Filed {new Date(c.created_at).toLocaleDateString('en-IN', { dateStyle: 'long' })}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ── FILE COMPLAINT ── */}
        {activeTab === 'file' && (
          <div>
            <div className="page-header">
              <div className="page-title">File a Complaint</div>
              <div className="page-subtitle">Report a financial cyber fraud — takes under 2 minutes</div>
            </div>

            {filedResult && (
              <div className="complaint-number-box" style={{ marginBottom: 20 }}>
                <div className="cnb-label">🎉 Complaint Filed Successfully!</div>
                <div className="cnb-number">{filedResult.complaint_no}</div>
                <div className="cnb-hint">Save this number to track your complaint anytime.</div>
                <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginTop: 12 }}>
                  <button className="btn btn-primary btn-sm" onClick={() => {
                    setTrackNo(filedResult.complaint_no);
                    setActiveTab('track');
                    setFiledResult(null);
                  }}>Track →</button>
                  <button className="btn btn-secondary btn-sm" onClick={() => navigator.clipboard.writeText(filedResult.complaint_no).then(() => toast.success('Copied!'))}>
                    Copy No.
                  </button>
                </div>
              </div>
            )}

            <div className="card">
              <form onSubmit={submitComplaint}>
                <div className="form-group">
                  <label className="form-label">Type of Fraud *</label>
                  <select className="form-select" value={form.fraud_type} onChange={set('fraud_type')} required>
                    {FRAUD_TYPES.map(t => <option key={t}>{t}</option>)}
                  </select>
                </div>
                <div className="form-grid-2">
                  <div className="form-group">
                    <label className="form-label">Amount Lost (₹) *</label>
                    <input className="form-input" type="number" min="1" placeholder="25000"
                      value={form.amount} onChange={set('amount')} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Date &amp; Time of Transaction</label>
                    <input className="form-input" type="datetime-local"
                      value={form.transaction_date} onChange={set('transaction_date')} />
                  </div>
                </div>
                <div className="form-grid-2">
                  <div className="form-group">
                    <label className="form-label">Fraudster's Account No. *</label>
                    <input className="form-input" placeholder="Account you sent money to"
                      value={form.to_account} onChange={set('to_account')} required />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Bank IFSC Code</label>
                    <input className="form-input" placeholder="e.g. SBIN0001234"
                      value={form.to_bank_ifsc} onChange={set('to_bank_ifsc')}
                      style={{ textTransform: 'uppercase', fontFamily: 'monospace' }} />
                  </div>
                </div>
                <div className="form-group">
                  <label className="form-label">Transaction / UTR ID</label>
                  <input className="form-input" placeholder="Reference / UTR number (optional)"
                    value={form.transaction_id} onChange={set('transaction_id')} />
                </div>
                <div className="form-group">
                  <label className="form-label">Describe the Fraud *</label>
                  <textarea className="form-textarea" placeholder="Describe exactly how the fraud occurred..."
                    value={form.description} onChange={set('description')} required />
                </div>
                <div className="alert alert-info">
                  ℹ️ Your complaint will automatically notify the bank holding the fraudster's account and trigger chain detection.
                </div>
                <button className="btn-submit" type="submit" disabled={loading}>
                  {loading ? 'Submitting...' : '📤 Submit Complaint'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* ── TRACK COMPLAINT ── */}
        {activeTab === 'track' && (
          <div>
            <div className="page-header">
              <div className="page-title">Track Complaint</div>
              <div className="page-subtitle">Enter your complaint number to check real-time status</div>
            </div>

            <div className="card" style={{ marginBottom: 20 }}>
              <div style={{ display: 'flex', gap: 10 }}>
                <input className="form-input" placeholder="e.g. DURGAM-2024-123456" style={{ flex: 1, fontFamily: 'monospace' }}
                  value={trackNo} onChange={e => setTrackNo(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && doTrack()} />
                <button className="btn btn-primary" onClick={doTrack} disabled={loading}>
                  {loading ? '...' : '🔍 Track'}
                </button>
              </div>
            </div>

            {trackedData && (
              <div>
                <div className="complaint-card" style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <span className="complaint-no">{trackedData.complaint?.complaint_no}</span>
                    <StatusBadge status={trackedData.complaint?.status} />
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 10 }}>
                    <div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Amount Lost</div>
                      <div className="complaint-amount" style={{ fontSize: 22 }}>₹{trackedData.complaint?.amount?.toLocaleString('en-IN')}</div>
                    </div>
                    <div>
                      <div style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Fraud Type</div>
                      <div style={{ fontWeight: 700, marginTop: 4, fontSize: 14 }}>{trackedData.complaint?.fraud_type}</div>
                    </div>
                  </div>
                  <div style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    {trackedData.complaint?.description}
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8 }}>
                    Filed: {new Date(trackedData.complaint?.created_at).toLocaleString('en-IN')}
                  </div>
                </div>

                {trackedData.chain ? (
                  <div className="card">
                    <div className="section-title">🔗 Transfer Chain Detected</div>
                    <div className="chain-container">
                      {trackedData.chain.chain_nodes?.map((node, i) => (
                        <div key={i}>
                          <div className="chain-node">
                            <div className={`chain-node-icon ${i === 0 ? 'root' : ''}`}>
                              {String.fromCharCode(65 + i)}
                            </div>
                            <div className="chain-node-body">
                              <div className="chain-account">{node.account_no}</div>
                              <div className="chain-bank">Bank IFSC: {node.bank_ifsc_prefix || '?'} · Hop {node.depth}</div>
                              <div className="chain-amount">₹{node.amount?.toLocaleString('en-IN')}</div>
                            </div>
                          </div>
                          {i < trackedData.chain.chain_nodes.length - 1 && <div className="chain-connector" />}
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="card">
                    <div style={{ textAlign: 'center', padding: '20px 0', color: 'var(--text-muted)' }}>
                      <div style={{ fontSize: 32, marginBottom: 8 }}>🔍</div>
                      <div style={{ fontWeight: 600, marginBottom: 4 }}>Investigation in Progress</div>
                      <div style={{ fontSize: 13 }}>No transfer chain detected yet. Check back soon.</div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
