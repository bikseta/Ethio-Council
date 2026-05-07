import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import { StoreContext, AuthState } from './store';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Members from './pages/Members';
import Churches from './pages/Churches';
import Reports from './pages/Reports';
import Map from './pages/Map';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  const [auth, setAuthState] = useState<AuthState>({
    token: localStorage.getItem('access_token'),
    userId: localStorage.getItem('user_id'),
    userRole: localStorage.getItem('user_role'),
    fullName: localStorage.getItem('full_name'),
    isAuthenticated: !!localStorage.getItem('access_token'),
  });

  const setAuth = (newAuth: Partial<AuthState>) => {
    const updated = { ...auth, ...newAuth };
    setAuthState(updated);
    if (newAuth.token) localStorage.setItem('access_token', newAuth.token);
    if (newAuth.userId) localStorage.setItem('user_id', newAuth.userId);
    if (newAuth.userRole) localStorage.setItem('user_role', newAuth.userRole);
    if (newAuth.fullName) localStorage.setItem('full_name', newAuth.fullName);
  };

  const logout = () => {
    localStorage.clear();
    setAuthState({ token: null, userId: null, userRole: null, fullName: null, isAuthenticated: false });
  };

  return (
    <StoreContext.Provider value={{ auth, setAuth, logout }}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<ProtectedRoute />}>
              <Route element={<Layout />}>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/members" element={<Members />} />
                <Route path="/churches" element={<Churches />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/map" element={<Map />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </StoreContext.Provider>
  );
}

export default App;
