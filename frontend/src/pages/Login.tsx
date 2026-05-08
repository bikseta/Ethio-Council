import { useState } from 'react';
import { Alert, Box, Button, MenuItem, Paper, Select, Stack, TextField, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

import { coreApi } from '../api/client';
import { authStore } from '../store/authStore';

const Login = () => {
  const { i18n, t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@ecfe.org');
  const [password, setPassword] = useState('Admin@2024!');
  const [error, setError] = useState('');

  const submit = async () => {
    try {
      const { data } = await coreApi.post('/auth/login', { email, password });
      authStore.set({ token: data.access_token, email, fullName: 'ECFE User' });
      navigate('/');
    } catch (err) {
      setError(t('placeholders.loginError'));
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', bgcolor: 'background.default' }}>
      <Paper sx={{ p: 4, width: 420 }}>
        <Stack spacing={2}>
          <Typography variant="h4">{t('navigation.login')}</Typography>
          <Select value={i18n.language.startsWith('am') ? 'am' : i18n.language.startsWith('om') ? 'om' : 'en'} onChange={(e) => i18n.changeLanguage(e.target.value)}>
            <MenuItem value="en">English</MenuItem>
            <MenuItem value="am">አማርኛ</MenuItem>
            <MenuItem value="om">Afaan Oromo</MenuItem>
          </Select>
          {error ? <Alert severity="error">{error}</Alert> : null}
          <TextField label={t('churchFields.email')} value={email} onChange={(e) => setEmail(e.target.value)} fullWidth />
          <TextField label={t('churchFields.password')} type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth />
          <Button variant="contained" onClick={submit}>{t('buttons.login')}</Button>
        </Stack>
      </Paper>
    </Box>
  );
};

export default Login;
