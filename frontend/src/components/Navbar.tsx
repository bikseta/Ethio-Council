import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useStore } from '../store';

const NAV_ITEMS = [
  { label: 'nav.dashboard', path: '/dashboard' },
  { label: 'nav.members', path: '/members' },
  { label: 'nav.churches', path: '/churches' },
  { label: 'nav.reports', path: '/reports' },
  { label: 'nav.map', path: '/map' },
];

const Navbar: React.FC = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const { logout, auth } = useStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ mr: 4, fontWeight: 700 }}>
          {t('app.name')}
        </Typography>
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          {NAV_ITEMS.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              onClick={() => navigate(item.path)}
              sx={{ fontWeight: location.pathname === item.path ? 700 : 400, textDecoration: location.pathname === item.path ? 'underline' : 'none' }}
            >
              {t(item.label)}
            </Button>
          ))}
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button color="inherit" size="small" onClick={() => i18n.changeLanguage('en')}>EN</Button>
          <Button color="inherit" size="small" onClick={() => i18n.changeLanguage('am')}>አማ</Button>
          <Button color="inherit" size="small" onClick={() => i18n.changeLanguage('om')}>OM</Button>
          {auth.fullName && (
            <Typography variant="body2" sx={{ ml: 1 }}>{auth.fullName}</Typography>
          )}
          <Button color="inherit" onClick={handleLogout}>{t('nav.logout')}</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
