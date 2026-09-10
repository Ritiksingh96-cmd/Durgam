import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuth } from '../../context/AuthContext';
import {
  getBankNotifications, uploadBankStatement, getBankChains, getBankAccounts, updateNotificationStatus
} from '../../api';

function StatusBadge({ status }) {
  const map = { pending: 'badge-pending', data_submitted: 'badge-submitted', chain_tracked: 'badge-resolved' };
  const label = { pending: '⏳ Pending', data_submitted: '📤 Data Submitted', chain_tracked: '🔗 Chain Tracked' };
  return <span className={`badge ${map[status] || 'badge-pending'}`}>{label[status] || status}</span>;
}

function Sidebar({ activeTab, setActiveTab, bankName, logout }) {
  const items = [
    { key: 'notifications', icon: '🔔', label: 'Mule Alerts' },
    { key: 'upload', icon: '📤', label: 'Upload Statement' },
    { key: 'accounts', icon: '👥', label: 'Submitted Data' },
    { key: 'chains', icon: '🔗', label: 'Transfer Chains' },
  ];
  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="logo-row">
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg,#059669,#10b981)' }}>🏦</div>
          <span className="logo-text">Durgam</span>
        </div>
        <div className="role-pill" style={{ background: '#ecfdf5', color: '#059669' }}>Bank Portal</div>
        <div className="user-info">🏦 {bankName}</div>
      </div>
      <nav className="sidebar-nav">
        {items.map(item => (
          <button key={item.key}
            className={activeTab === item.key ? 'active' : ''}
            onClick={() => setActiveTab(item.key)}
            style={activeTab === item.key ? { background: '#ecfdf5', color: '#059669' } : {}}>
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

// ─── UPLOAD FORM ───────────────────────────────────
function UploadForm() {
  const [form, setForm] = useState({ account_no: '', account_holder_name: '', mobile: '', address: '', aadhar_no: '', pan_no: '' });
  const [transactions, setTransactions] = useState([{ to_account: '', to_bank_ifsc: '', amount: '', timestamp: '', transaction_id: '', description: '' }]);
  const [loading, setLoading] = useState(false);

  const addTxn = () => setTransactions([...transactions, { to_account: '', to_bank_ifsc: '', amount: '', timestamp: '', transaction_id: '', description: '' }]);
  const removeTxn = (i) => setTransactions(transactions.filter((_, idx) => idx !== i));
  const setTxn = (i, k, v) => {
    const t = [...transactions];
    t[i][k] = v;
    setTransactions(t);
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...form,
        transactions: transactions.filter(t => t.to_account && t.amount).map(t => ({
          ...t,
          amount: parseFloat(t.amount),
          timestamp: t.timestamp ? new Date(t.timestamp).toISOString() : new Date().toISOString(),
        })),
      };
      await uploadBankStatement(payload);
      toast.success('Statement uploaded! Chain detection triggered.');
      setForm({ account_no: '', account_holder_name: '', mobile: '', address: '', aadhar_no: '', pan_no: '' });
      setTransactions([{ to_account: '', to_bank_ifsc: '', amount: '', timestamp: '', transaction_id: '', description: '' }]);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed');
    } finally { setLoading(false); }
  };

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  return (
    <form onSubmit={submit}>
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="section-title">👤 Account Holder Details</div>
        <div className="form-grid-2">
          <div className="form-group">
            <label className="form-label">Account Number *</label>
            <input className="form-input" placeholder="Account No." value={form.account_no} onChange={set('account_no')} required />
          </div>
          <div className="form-group">
            <label className="form-label">Account Holder Name *</label>
            <input className="form-input" placeholder="Full Name" value={form.account_holder_name} onChange={set('account_holder_name')} required />
          </div>
          <div className="form-group">
            <label className="form-label">Mobile Number *</label>
            <input className="form-input" placeholder="Mobile" value={form.mobile} onChange={set('mobile')} required />
          </div>
          <div className="form-group">
            <label className="form-label">Aadhaar No.</label>
            <input className="form-input" placeholder="XXXX-XXXX-XXXX" value={form.aadhar_no} onChange={set('aadhar_no')} />
          </div>
          <div className="form-group">
            <label className="form-label">PAN No.</label>
            <input className="form-input" placeholder="ABCDE1234F" value={form.pan_no} onChange={set('pan_no')} />
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Address *</label>
          <textarea className="form-textarea" placeholder="Full address" value={form.address} onChange={set('address')} required />
        </div>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div className="section-title" style={{ marginBottom: 0 }}>💸 Outgoing Transactions</div>
          <button type="button" className="btn btn-secondary btn-sm" onClick={addTxn}>+ Add Row</button>
        </div>
        {transactions.map((t, i) => (
          <div key={i} style={{ background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 8, padding: 16, marginBottom: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
              <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)' }}>Transaction #{i + 1}</span>
              {transactions.length > 1 && (
                <button type="button" className="btn btn-danger btn-sm" onClick={() => removeTxn(i)}>Remove</button>
              )}
            </div>
            <div className="form-grid-2">
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">To Account *</label>
                <input className="form-input" placeholder="Recipient account" value={t.to_account} onChange={e => setTxn(i, 'to_account', e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">To Bank IFSC</label>
                <input className="form-input" placeholder="HDFC0001234" value={t.to_bank_ifsc} onChange={e => setTxn(i, 'to_bank_ifsc', e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">Amount (₹) *</label>
                <input className="form-input" type="number" placeholder="Amount" value={t.amount} onChange={e => setTxn(i, 'amount', e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">Timestamp *</label>
                <input className="form-input" type="datetime-local" value={t.timestamp} onChange={e => setTxn(i, 'timestamp', e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">Transaction ID</label>
                <input className="form-input" placeholder="UTR/Ref No." value={t.transaction_id} onChange={e => setTxn(i, 'transaction_id', e.target.value)} />
              </div>
              <div className="form-group" style={{ marginBottom: 8 }}>
                <label className="form-label">Description</label>
                <input className="form-input" placeholder="Transfer note" value={t.description} onChange={e => setTxn(i, 'description', e.target.value)} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="alert alert-warning">
        ⚠️ Submitting this data will trigger automatic chain detection. Relevant banks will be notified.
      </div>
      <button className="btn btn-full" type="submit" disabled={loading}
        style={{ background: '#10b981', color: 'white', borderRadius: 8, fontWeight: 600, padding: '12px 20px', border: 'none', cursor: 'pointer', fontSize: 14 }}>
        {loading ? 'Submitting...' : '📤 Submit Account Data'}
      </button>
    </form>
  );
}

// ─── MAIN BANK DASHBOARD ───────────────────────────
export default function BankDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('notifications');
  const [notifications, setNotifications] = useState([]);
  const [chains, setChains] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedNotif, setSelectedNotif] = useState(null);

  const doLogout = () => { logout(); navigate('/'); };

  useEffect(() => {
    if (activeTab === 'notifications') fetchNotifications();
    if (activeTab === 'chains') fetchChains();
    if (activeTab === 'accounts') fetchAccounts();
  }, [activeTab]);

  const fetchNotifications = async () => {
    setLoading(true);
    try { const { data } = await getBankNotifications(); setNotifications(data); }
    catch { toast.error('Failed to load notifications'); }
    finally { setLoading(false); }
  };

  const fetchChains = async () => {
    setLoading(true);
    try { const { data } = await getBankChains(); setChains(data); }
    catch { toast.error('Failed to load chains'); }
    finally { setLoading(false); }
  };

  const fetchAccounts = async () => {
    setLoading(true);
    try { const { data } = await getBankAccounts(); setAccounts(data); }
    catch { toast.error('Failed to load accounts'); }
    finally { setLoading(false); }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} bankName={user?.bankName || user?.name} logout={doLogout} />
      <div className="main-content">

        {/* ── NOTIFICATIONS ── */}
        {activeTab === 'notifications' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
              <div>
                <div className="page-title">🔔 Mule Account Alerts</div>
                <div className="page-subtitle">Accounts flagged in your bank for suspicious activity</div>
              </div>
              <button className="btn btn-secondary btn-sm" onClick={fetchNotifications}>↻ Refresh</button>
            </div>

            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : notifications.length === 0 ? (
              <div className="empty-state">
                <div className="icon">✅</div>
                <h3>No Alerts</h3>
                <p>No mule account notifications for your bank right now.</p>
              </div>
            ) : (
              notifications.map(n => (
                <div key={n.id} className={`notif-card ${n.status}`}
                  onClick={() => setSelectedNotif(selectedNotif?.id === n.id ? null : n)}>
                  <div className="notif-header">
                    <span className="notif-account">Account: {n.account_no}</span>
                    <StatusBadge status={n.status} />
                  </div>
                  <div className="notif-meta">
                    <span>Complaint: <strong>{n.complaint_no}</strong></span>
                    <span>Amount: <strong style={{ color: 'var(--danger)' }}>₹{n.amount?.toLocaleString()}</strong></span>
                    <span>Depth: {n.depth === 0 ? 'Direct Mule' : `Hop ${n.depth}`}</span>
                    <span>{new Date(n.created_at).toLocaleDateString('en-IN')}</span>
                  </div>

                  {selectedNotif?.id === n.id && (
                    <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border)' }}>
                      {n.parent_account && (
                        <div style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 8 }}>
                          🔗 Received funds from: <span style={{ fontFamily: 'monospace', color: 'var(--accent)' }}>{n.parent_account}</span>
                        </div>
                      )}
                      {n.status === 'pending' && (
                        <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
                          <button className="btn btn-success btn-sm" onClick={(e) => {
                            e.stopPropagation();
                            setActiveTab('upload');
                          }}>
                            📤 Upload Account Data
                          </button>
                          <button className="btn btn-secondary btn-sm" onClick={async (e) => {
                            e.stopPropagation();
                            await updateNotificationStatus(n.id, 'data_submitted');
                            fetchNotifications();
                          }}>
                            Mark Reviewed
                          </button>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {/* ── UPLOAD STATEMENT ── */}
        {activeTab === 'upload' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>📤 Upload Bank Statement</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>
              Submit account holder data and transaction history for investigation
            </div>
            <UploadForm />
          </div>
        )}

        {/* ── SUBMITTED ACCOUNTS ── */}
        {activeTab === 'accounts' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>👥 Submitted Account Data</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>All account data you have submitted to I4C</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : accounts.length === 0 ? (
              <div className="empty-state">
                <div className="icon">📂</div>
                <h3>No Data Submitted Yet</h3>
                <p>Upload bank statements to see them here.</p>
              </div>
            ) : (
              <div className="card">
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Account No</th>
                        <th>Holder Name</th>
                        <th>Mobile</th>
                        <th>Aadhaar</th>
                        <th>PAN</th>
                        <th>Submitted</th>
                      </tr>
                    </thead>
                    <tbody>
                      {accounts.map(a => (
                        <tr key={a.id}>
                          <td style={{ fontFamily: 'monospace' }}>{a.account_no}</td>
                          <td>{a.account_holder_name}</td>
                          <td>{a.mobile}</td>
                          <td>{a.aadhar_no || '—'}</td>
                          <td>{a.pan_no || '—'}</td>
                          <td style={{ fontSize: 12 }}>{new Date(a.submitted_at).toLocaleDateString('en-IN')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── TRANSFER CHAINS ── */}
        {activeTab === 'chains' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>🔗 Transfer Chains</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>Money transfer chains involving your bank's accounts</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : chains.length === 0 ? (
              <div className="empty-state">
                <div className="icon">🔗</div>
                <h3>No Chains Yet</h3>
                <p>Transfer chains will appear here as data is submitted.</p>
              </div>
            ) : (
              chains.map(chain => (
                <div key={chain.id} className="card" style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <div>
                      <span className="complaint-no">{chain.root_complaint_no}</span>
                      <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                        Root: <span style={{ fontFamily: 'monospace' }}>{chain.root_mule_account}</span>
                      </div>
                    </div>
                    <span className={`badge ${chain.status === 'active' ? 'badge-investigation' : 'badge-resolved'}`}>
                      {chain.status}
                    </span>
                  </div>
                  <div className="chain-container">
                    {chain.chain_nodes?.map((node, i) => (
                      <div key={i}>
                        <div className="chain-node">
                          <div className={`chain-node-icon ${i === 0 ? 'root' : 'mid'}`}>
                            {String.fromCharCode(65 + i)}
                          </div>
                          <div className="chain-node-body">
                            <div className="chain-account">{node.account_no}</div>
                            <div className="chain-bank">IFSC: {node.bank_ifsc_prefix || '?'}</div>
                            <div className="chain-amount">₹{node.amount?.toLocaleString()}</div>
                          </div>
                        </div>
                        {i < chain.chain_nodes.length - 1 && <div className="chain-connector" />}
                      </div>
                    ))}
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}
