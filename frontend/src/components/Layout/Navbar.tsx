import { AppBar, Box, Button, MenuItem, Select, Toolbar, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

import { authStore } from '../../store/authStore';

const Navbar = () => {
  const { i18n, t } = useTranslation();
  const navigate = useNavigate();

  return (
    <AppBar position="fixed" sx={{ zIndex: 1201 }}>
      <Toolbar sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">ECFE Digital Platform</Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Select size="small" value={i18n.language.startsWith('am') ? 'am' : i18n.language.startsWith('om') ? 'om' : 'en'} onChange={(event) => i18n.changeLanguage(event.target.value)}>
            <MenuItem value="en">EN</MenuItem>
            <MenuItem value="am">አማ</MenuItem>
            <MenuItem value="om">OM</MenuItem>
          </Select>
          <Button color="inherit" onClick={() => { authStore.clear(); navigate('/login'); }}>{t('buttons.logout')}</Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
