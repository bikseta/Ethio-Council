import React from 'react';
import { BrowserRouter as Router, Navigate, Outlet, Route, Routes } from 'react-router-dom';
import { Box, ThemeProvider, createTheme } from '@mui/material';

import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import ProtectedRoute from './components/ProtectedRoute';
import AdminHierarchy from './pages/AdminHierarchy';
import Analytics from './pages/Analytics';
import ChurchDirectory from './pages/ChurchDirectory';
import ChurchRegistration from './pages/ChurchRegistration';
import CrisisResponse from './pages/CrisisResponse';
import Denominations from './pages/Denominations';
import DiasporaPortal from './pages/DiasporaPortal';
import GISMap from './pages/GISMap';
import Leaders from './pages/Leaders';
import Login from './pages/Login';
import Ministries from './pages/Ministries';
import NotFound from './pages/NotFound';

const theme = createTheme({
  palette: {
    primary: { main: '#1565C0' },
    secondary: { main: '#2E7D32' },
    background: { default: '#F5F7FA' },
  },
});

const AppShell: React.FC = () => (
  <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
    <Sidebar />
    <Box sx={{ flex: 1, ml: '260px' }}>
      <Navbar />
      <Box component="main" sx={{ p: 3 }}>
        <Outlet />
      </Box>
    </Box>
  </Box>
);

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<AppShell />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Analytics />} />
              <Route path="/churches" element={<ChurchDirectory />} />
              <Route path="/churches/register" element={<ChurchRegistration />} />
              <Route path="/denominations" element={<Denominations />} />
              <Route path="/ministries" element={<Ministries />} />
              <Route path="/leaders" element={<Leaders />} />
              <Route path="/hierarchy" element={<AdminHierarchy />} />
              <Route path="/diaspora" element={<DiasporaPortal />} />
              <Route path="/gis-registration" element={<GISMap />} />
              <Route path="/gis" element={<Navigate to="/gis-registration" replace />} />
              <Route path="/crisis-response" element={<CrisisResponse />} />
              <Route path="/crisis" element={<Navigate to="/crisis-response" replace />} />
            </Route>
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;
