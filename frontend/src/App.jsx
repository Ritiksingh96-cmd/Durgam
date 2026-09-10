import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';

import Landing from './pages/Landing';
import About from './pages/public/About';
import LiveMapPage from './pages/public/LiveMapPage';
import Portals from './pages/public/Portals';
import Resources from './pages/public/Resources';
import Contact from './pages/public/Contact';

import UserLogin from './pages/user/UserLogin';
import UserRegister from './pages/user/UserRegister';
import UserDashboard from './pages/user/UserDashboard';
import BankLogin from './pages/bank/BankLogin';
import BankRegister from './pages/bank/BankRegister';
import BankDashboard from './pages/bank/BankDashboard';
import I4CLogin from './pages/i4c/I4CLogin';
import I4CDashboard from './pages/i4c/I4CDashboard';

function ProtectedRoute({ children, requiredRole }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loader-fullscreen"><div className="spinner" /></div>;
  if (!user) return <Navigate to="/" replace />;
  if (requiredRole && user.role !== requiredRole) return <Navigate to="/" replace />;
  return children;
}

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/" element={user ? <Navigate to={`/${user.role}/dashboard`} /> : <Landing />} />
      <Route path="/about" element={<About />} />
      <Route path="/live-map" element={<LiveMapPage />} />
      <Route path="/portals" element={<Portals />} />
      <Route path="/resources" element={<Resources />} />
      <Route path="/contact" element={<Contact />} />

      {/* User */}
      <Route path="/user/login" element={<UserLogin />} />
      <Route path="/user/register" element={<UserRegister />} />
      <Route path="/user/dashboard" element={
        <ProtectedRoute requiredRole="user"><UserDashboard /></ProtectedRoute>
      } />

      {/* Bank */}
      <Route path="/bank/login" element={<BankLogin />} />
      <Route path="/bank/register" element={<BankRegister />} />
      <Route path="/bank/dashboard" element={
        <ProtectedRoute requiredRole="bank"><BankDashboard /></ProtectedRoute>
      } />

      {/* I4C */}
      <Route path="/i4c/login" element={<I4CLogin />} />
      <Route path="/i4c/dashboard" element={
        <ProtectedRoute requiredRole="i4c"><I4CDashboard /></ProtectedRoute>
      } />

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster position="top-right" toastOptions={{
          style: { background: '#1e293b', color: '#f1f5f9', border: '1px solid #334155' },
        }} />
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
