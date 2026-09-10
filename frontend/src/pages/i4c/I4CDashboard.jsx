import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend,
} from 'recharts';
import { useAuth } from '../../context/AuthContext';
import {
  getI4CDashboard, getAllComplaints, getAllChains, getAllBankData,
  getAllUsers, getAllBanks, getAllNotifications, updateComplaintStatus
} from '../../api';

const COLORS = ['#7c3aed', '#059669', '#d97706', '#dc2626', '#2563eb', '#0891b2', '#ea580c'];
const TOOLTIP_STYLE = { background: '#fff', border: '1px solid #e4e9f0', color: '#0a0a14', borderRadius: 8, boxShadow: '0 4px 16px rgba(0,0,0,0.08)' };

function Sidebar({ activeTab, setActiveTab, officerName, logout }) {
  const items = [
    { key: 'dashboard', icon: '📊', label: 'Dashboard' },
    { key: 'complaints', icon: '📋', label: 'All Complaints' },
    { key: 'chains', icon: '🔗', label: 'Transfer Chains' },
    { key: 'bank-data', icon: '🏦', label: 'Bank Data' },
    { key: 'users', icon: '👥', label: 'Users' },
    { key: 'notifications', icon: '🔔', label: 'Notifications' },
    { key: 'analytics', icon: '📈', label: 'Analytics' },
  ];
  return (
    <div className="sidebar">
      <div className="sidebar-brand">
        <div className="logo-row">
          <div className="logo-icon" style={{ background: 'linear-gradient(135deg,#2563eb,#7c3aed)' }}>🛡️</div>
          <span className="logo-text">Durgam</span>
        </div>
        <div className="role-pill" style={{ background: '#eff6ff', color: '#2563eb' }}>I4C Officer</div>
        <div className="user-info">🛡️ {officerName}</div>
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

function StatCard({ icon, label, value, color = '#7c3aed', sub }) {
  return (
    <div className="stat-card" style={{ '--stat-color': color }}>
      <div className="stat-icon" style={{ background: `${color}15` }}>{icon}</div>
      <div className="stat-value" style={{ color }}>{value}</div>
      <div className="stat-label">{label}</div>
      {sub && <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>{sub}</div>}
    </div>
  );
}

function StatusBadge({ status }) {
  const map = {
    pending: 'badge-pending', under_investigation: 'badge-investigation',
    chain_detected: 'badge-chain', resolved: 'badge-resolved', closed: 'badge-resolved',
  };
  const label = {
    pending: '⏳ Pending', under_investigation: '🔍 Investigating',
    chain_detected: '🔗 Chain Detected', resolved: '✅ Resolved', closed: '🔒 Closed',
  };
  return <span className={`badge ${map[status] || 'badge-pending'}`}>{label[status] || status}</span>;
}

export default function I4CDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashData, setDashData] = useState(null);
  const [complaints, setComplaints] = useState([]);
  const [chains, setChains] = useState([]);
  const [bankData, setBankData] = useState([]);
  const [users, setUsers] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [expandedChain, setExpandedChain] = useState(null);

  const doLogout = () => { logout(); navigate('/'); };

  useEffect(() => {
    if (activeTab === 'dashboard') fetchDashboard();
    if (activeTab === 'complaints') fetchComplaints();
    if (activeTab === 'chains') fetchChains();
    if (activeTab === 'bank-data') fetchBankData();
    if (activeTab === 'users') fetchUsers();
    if (activeTab === 'notifications') fetchNotifications();
    if (activeTab === 'analytics') fetchDashboard();
  }, [activeTab]);

  const fetchDashboard = async () => {
    setLoading(true);
    try { const { data } = await getI4CDashboard(); setDashData(data); }
    catch { toast.error('Failed to load dashboard'); }
    finally { setLoading(false); }
  };
  const fetchComplaints = async () => {
    setLoading(true);
    try { const { data } = await getAllComplaints(); setComplaints(data.complaints); }
    catch { toast.error('Failed'); } finally { setLoading(false); }
  };
  const fetchChains = async () => {
    setLoading(true);
    try { const { data } = await getAllChains(); setChains(data); }
    catch { toast.error('Failed'); } finally { setLoading(false); }
  };
  const fetchBankData = async () => {
    setLoading(true);
    try { const { data } = await getAllBankData(); setBankData(data); }
    catch { toast.error('Failed'); } finally { setLoading(false); }
  };
  const fetchUsers = async () => {
    setLoading(true);
    try { const { data } = await getAllUsers(); setUsers(data); }
    catch { toast.error('Failed'); } finally { setLoading(false); }
  };
  const fetchNotifications = async () => {
    setLoading(true);
    try { const { data } = await getAllNotifications(); setNotifications(data); }
    catch { toast.error('Failed'); } finally { setLoading(false); }
  };

  const changeStatus = async (complaintNo, status) => {
    try {
      await updateComplaintStatus(complaintNo, status);
      toast.success('Status updated!');
      fetchComplaints();
    } catch { toast.error('Failed to update status'); }
  };

  const formatCurrency = (v) => `₹${(v || 0).toLocaleString('en-IN')}`;

  // Format daily data for line chart
  const dailyChartData = dashData?.daily_complaints?.map(d => ({
    date: `${d._id.day}/${d._id.month}`,
    complaints: d.count,
    amount: d.amount,
  })) || [];

  const fraudChartData = dashData?.fraud_breakdown?.map(f => ({
    name: f._id,
    count: f.count,
    amount: f.total_amount,
  })) || [];

  return (
    <div className="dashboard-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} officerName={user?.name} logout={doLogout} />
      <div className="main-content">

        {/* ── DASHBOARD ── */}
        {activeTab === 'dashboard' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>📊 I4C Command Dashboard</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>Real-time overview of cyber fraud activity</div>

            {loading || !dashData ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <>
                <div className="grid-4" style={{ marginBottom: 24 }}>
                  <StatCard icon="📋" label="Total Complaints" value={dashData.stats.total_complaints} color="#3b82f6" />
                  <StatCard icon="⏳" label="Pending" value={dashData.stats.pending} color="#f59e0b" />
                  <StatCard icon="🔗" label="Chains Detected" value={dashData.stats.chain_detected} color="#8b5cf6" />
                  <StatCard icon="✅" label="Resolved" value={dashData.stats.resolved} color="#10b981" />
                  <StatCard icon="💰" label="Total Amount" value={formatCurrency(dashData.stats.total_amount_involved)} color="#ef4444" sub="Across all complaints" />
                  <StatCard icon="🏦" label="Banks Registered" value={dashData.stats.total_banks} color="#06b6d4" />
                  <StatCard icon="🔔" label="Notifications Sent" value={dashData.stats.total_notifications} color="#f97316" />
                  <StatCard icon="👥" label="Registered Users" value={dashData.stats.total_users} color="#10b981" />
                </div>

                <div className="grid-2" style={{ marginBottom: 24 }}>
                  <div className="card">
                    <div className="section-title">Complaints Over Last 30 Days</div>
                    <div className="chart-wrapper">
                      <ResponsiveContainer width="100%" height={200}>
                        <LineChart data={dailyChartData}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e4e9f0" />
                          <XAxis dataKey="date" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                          <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
                          <Tooltip contentStyle={TOOLTIP_STYLE} />
                          <Line type="monotone" dataKey="complaints" stroke="#7c3aed" strokeWidth={2} dot={{ fill: '#7c3aed' }} />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="card">
                    <div className="section-title">Fraud Type Breakdown</div>
                    <div className="chart-wrapper">
                      <ResponsiveContainer width="100%" height={200}>
                        <PieChart>
                          <Pie data={fraudChartData} dataKey="count" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, percent }) => `${name.split(' ')[0]} ${(percent * 100).toFixed(0)}%`} labelLine={false}>
                            {fraudChartData.map((_, i) => (
                              <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip contentStyle={TOOLTIP_STYLE} />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>

                {fraudChartData.length > 0 && (
                  <div className="card">
                    <div className="section-title">Amount by Fraud Type (₹)</div>
                    <div className="chart-wrapper">
                      <ResponsiveContainer width="100%" height={220}>
                        <BarChart data={fraudChartData}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                          <XAxis dataKey="name" stroke="#64748b" tick={{ fontSize: 11 }} angle={-15} textAnchor="end" height={50} />
                          <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                          <Tooltip formatter={(v) => formatCurrency(v)} contentStyle={{ background: '#1e293b', border: '1px solid #334155', color: '#f1f5f9' }} />
                          <Bar dataKey="amount" radius={[4, 4, 0, 0]}>
                            {fraudChartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* ── ALL COMPLAINTS ── */}
        {activeTab === 'complaints' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>📋 All Complaints</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>Manage all filed complaints across the system</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <div className="card">
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Complaint No</th>
                        <th>User</th>
                        <th>Amount</th>
                        <th>Fraud Type</th>
                        <th>Mule Account</th>
                        <th>Status</th>
                        <th>Filed</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {complaints.map(c => (
                        <tr key={c.id}>
                          <td style={{ fontFamily: 'monospace', fontSize: 12, color: 'var(--accent)' }}>{c.complaint_no}</td>
                          <td>
                            <div style={{ fontWeight: 600 }}>{c.user_name}</div>
                            <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>{c.user_mobile}</div>
                          </td>
                          <td style={{ color: 'var(--danger)', fontWeight: 700 }}>₹{c.amount?.toLocaleString()}</td>
                          <td><span className="badge badge-danger" style={{ fontSize: 10 }}>{c.fraud_type}</span></td>
                          <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{c.to_account}</td>
                          <td><StatusBadge status={c.status} /></td>
                          <td style={{ fontSize: 12 }}>{new Date(c.created_at).toLocaleDateString('en-IN')}</td>
                          <td>
                            <select className="form-select" style={{ padding: '4px 8px', fontSize: 12, width: 'auto' }}
                              value={c.status}
                              onChange={e => changeStatus(c.complaint_no, e.target.value)}>
                              <option value="pending">Pending</option>
                              <option value="under_investigation">Investigating</option>
                              <option value="chain_detected">Chain Detected</option>
                              <option value="resolved">Resolved</option>
                              <option value="closed">Closed</option>
                            </select>
                          </td>
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
            <div className="page-subtitle" style={{ marginBottom: 24 }}>Full money transfer chains across the system</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : chains.length === 0 ? (
              <div className="empty-state">
                <div className="icon">🔗</div>
                <h3>No Transfer Chains</h3>
                <p>Chains will appear once bank data is submitted.</p>
              </div>
            ) : (
              chains.map(chain => (
                <div key={chain.id} className="card" style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', cursor: 'pointer' }}
                    onClick={() => setExpandedChain(expandedChain === chain.id ? null : chain.id)}>
                    <div>
                      <span className="complaint-no">{chain.root_complaint_no}</span>
                      <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                        Hops: {chain.chain_nodes?.length || 0} · Root: <span style={{ fontFamily: 'monospace' }}>{chain.root_mule_account}</span>
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      <span className={`badge ${chain.status === 'active' ? 'badge-investigation' : 'badge-resolved'}`}>{chain.status}</span>
                      <span style={{ color: 'var(--text-muted)', fontSize: 18 }}>{expandedChain === chain.id ? '▲' : '▼'}</span>
                    </div>
                  </div>

                  {expandedChain === chain.id && (
                    <div className="chain-container" style={{ marginTop: 16 }}>
                      {chain.chain_nodes?.map((node, i) => (
                        <div key={i}>
                          <div className="chain-node">
                            <div className={`chain-node-icon ${i === 0 ? 'root' : 'mid'}`}>
                              {String.fromCharCode(65 + i)}
                            </div>
                            <div className="chain-node-body" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <div>
                                <div className="chain-account">{node.account_no}</div>
                                <div className="chain-bank">IFSC: {node.bank_ifsc_prefix || '?'} · Depth: {node.depth}</div>
                                <div className="chain-amount">₹{node.amount?.toLocaleString()}</div>
                              </div>
                              <span className={`badge ${node.status === 'pending' ? 'badge-pending' : 'badge-resolved'}`} style={{ fontSize: 10 }}>
                                {node.status}
                              </span>
                            </div>
                          </div>
                          {i < chain.chain_nodes.length - 1 && <div className="chain-connector" />}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}

        {/* ── BANK DATA ── */}
        {activeTab === 'bank-data' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>🏦 Submitted Bank Data</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>All account holder data submitted by banks</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <div className="card">
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Account No</th>
                        <th>Holder Name</th>
                        <th>Mobile</th>
                        <th>Address</th>
                        <th>Aadhaar</th>
                        <th>PAN</th>
                        <th>Bank</th>
                        <th>Submitted</th>
                      </tr>
                    </thead>
                    <tbody>
                      {bankData.map(a => (
                        <tr key={a.id}>
                          <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{a.account_no}</td>
                          <td style={{ fontWeight: 600 }}>{a.account_holder_name}</td>
                          <td>{a.mobile}</td>
                          <td style={{ maxWidth: 180, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: 12 }}>{a.address}</td>
                          <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{a.aadhar_no || '—'}</td>
                          <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{a.pan_no || '—'}</td>
                          <td><span className="badge badge-submitted" style={{ fontSize: 10 }}>{a.bank_name || a.bank_ifsc_prefix}</span></td>
                          <td style={{ fontSize: 12 }}>{new Date(a.submitted_at).toLocaleDateString('en-IN')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {bankData.length === 0 && (
                    <div className="empty-state">
                      <div className="icon">🏦</div>
                      <h3>No Bank Data Yet</h3>
                      <p>Bank data will appear here once banks upload statements.</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── USERS ── */}
        {activeTab === 'users' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>👥 Registered Users</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>All citizens registered on the Durgam platform</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <div className="card">
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr><th>Name</th><th>Email</th><th>Mobile</th><th>Address</th><th>Joined</th></tr>
                    </thead>
                    <tbody>
                      {users.map(u => (
                        <tr key={u.id}>
                          <td style={{ fontWeight: 600 }}>{u.name}</td>
                          <td>{u.email}</td>
                          <td>{u.mobile}</td>
                          <td style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: 12 }}>{u.address}</td>
                          <td style={{ fontSize: 12 }}>{new Date(u.created_at).toLocaleDateString('en-IN')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── NOTIFICATIONS ── */}
        {activeTab === 'notifications' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>🔔 All Bank Notifications</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>All mule account alerts sent to banks</div>
            {loading ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <div className="card">
                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr><th>Account No</th><th>Bank IFSC</th><th>Complaint No</th><th>Amount</th><th>Depth</th><th>Status</th><th>Date</th></tr>
                    </thead>
                    <tbody>
                      {notifications.map(n => (
                        <tr key={n.id}>
                          <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{n.account_no}</td>
                          <td>{n.bank_ifsc_prefix || n.bank_name}</td>
                          <td style={{ fontFamily: 'monospace', fontSize: 11, color: 'var(--accent)' }}>{n.complaint_no}</td>
                          <td style={{ color: 'var(--danger)', fontWeight: 700 }}>₹{n.amount?.toLocaleString()}</td>
                          <td>{n.depth === 0 ? <span className="badge badge-danger">Direct</span> : `Hop ${n.depth}`}</td>
                          <td>
                            {n.status === 'pending' && <span className="badge badge-pending">⏳ Pending</span>}
                            {n.status === 'data_submitted' && <span className="badge badge-submitted">📤 Submitted</span>}
                            {n.status === 'chain_tracked' && <span className="badge badge-resolved">🔗 Tracked</span>}
                          </td>
                          <td style={{ fontSize: 12 }}>{new Date(n.created_at).toLocaleDateString('en-IN')}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── ANALYTICS ── */}
        {activeTab === 'analytics' && (
          <div>
            <div className="page-title" style={{ marginBottom: 4 }}>📈 Analytics & Intelligence</div>
            <div className="page-subtitle" style={{ marginBottom: 24 }}>Data-driven insights for proactive cybercrime prevention</div>
            {loading || !dashData ? (
              <div className="loader-inline"><div className="spinner" /></div>
            ) : (
              <>
                <div className="grid-2" style={{ marginBottom: 24 }}>
                  <div className="card">
                    <div className="section-title">Complaint Volume Trend (30 days)</div>
                    <ResponsiveContainer width="100%" height={240}>
                      <BarChart data={dailyChartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
                        <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                        <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', color: '#f1f5f9' }} />
                        <Bar dataKey="complaints" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="card">
                    <div className="section-title">Financial Impact by Fraud Type</div>
                    <ResponsiveContainer width="100%" height={240}>
                      <BarChart data={fraudChartData} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                        <XAxis type="number" stroke="#64748b" tick={{ fontSize: 11 }} />
                        <YAxis dataKey="name" type="category" stroke="#64748b" tick={{ fontSize: 10 }} width={100} />
                        <Tooltip formatter={(v) => formatCurrency(v)} contentStyle={{ background: '#1e293b', border: '1px solid #334155', color: '#f1f5f9' }} />
                        <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
                          {fraudChartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="card">
                  <div className="section-title">Case Status Overview</div>
                  <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                    {[
                      { label: 'Pending', value: dashData.stats.pending, color: '#f59e0b' },
                      { label: 'Under Investigation', value: dashData.stats.under_investigation, color: '#3b82f6' },
                      { label: 'Chain Detected', value: dashData.stats.chain_detected, color: '#8b5cf6' },
                      { label: 'Resolved', value: dashData.stats.resolved, color: '#10b981' },
                    ].map(item => {
                      const pct = dashData.stats.total_complaints
                        ? Math.round((item.value / dashData.stats.total_complaints) * 100)
                        : 0;
                      return (
                        <div key={item.label} style={{ flex: '1 1 180px' }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: 13 }}>
                            <span style={{ color: 'var(--text-secondary)' }}>{item.label}</span>
                            <span style={{ color: item.color, fontWeight: 700 }}>{item.value}</span>
                          </div>
                          <div style={{ height: 6, background: 'var(--bg-secondary)', borderRadius: 3, overflow: 'hidden' }}>
                            <div style={{ width: `${pct}%`, height: '100%', background: item.color, borderRadius: 3, transition: 'width 1s' }} />
                          </div>
                          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4 }}>{pct}% of total</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

function formatCurrency(v) { return `₹${(v || 0).toLocaleString('en-IN')}`; }
