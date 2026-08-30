import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    const name = localStorage.getItem('name');
    const bankName = localStorage.getItem('bankName');
    if (token && role) {
      setUser({ token, role, name, bankName });
    }
    setLoading(false);
  }, []);

  const login = (data) => {
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('role', data.role);
    localStorage.setItem('name', data.name || data.bank_name || 'Officer');
    if (data.bank_name) localStorage.setItem('bankName', data.bank_name);
    setUser({
      token: data.access_token,
      role: data.role,
      name: data.name || data.bank_name || 'Officer',
      bankName: data.bank_name,
    });
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
