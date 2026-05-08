import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom';
import { Box, CssBaseline, Toolbar } from '@mui/material';

import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import ChurchDirectory from './pages/ChurchDirectory';
import ChurchRegistration from './pages/ChurchRegistration';
import GISMap from './pages/GISMap';
import Analytics from './pages/Analytics';
import DiasporaPortal from './pages/DiasporaPortal';
import CrisisResponse from './pages/CrisisResponse';
import Login from './pages/Login';
import NotFound from './pages/NotFound';
import theme from './theme';
import { ThemeProvider } from '@mui/material/styles';
import { authStore } from './store/authStore';

const PrivateLayout = () => {
  const auth = authStore.get();
  if (!auth.token) {
    return <Navigate to="/login" replace />;
  }
  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Navbar />
      <Box component="nav" sx={{ width: 260, flexShrink: 0 }}>
        <Sidebar />
      </Box>
      <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: 'background.default', minHeight: '100vh' }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

const App = () => (
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<PrivateLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/churches" element={<ChurchDirectory />} />
          <Route path="/church-registration" element={<ChurchRegistration />} />
          <Route path="/gis" element={<GISMap />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/diaspora" element={<DiasporaPortal />} />
          <Route path="/crisis-response" element={<CrisisResponse />} />
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </ThemeProvider>
);

export default App;
