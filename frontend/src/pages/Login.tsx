import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import { useTranslation } from 'react-i18next';
import { authApi } from '../api/client';
import { useStore } from '../store';

const Login: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { setAuth } = useStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await authApi.login(email, password);
      const { access_token, user_role, user_id, full_name } = response.data;
      setAuth({ token: access_token, userRole: user_role, userId: user_id, fullName: full_name, isAuthenticated: true });
      navigate('/dashboard');
    } catch {
      setError(t('auth.loginError'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Card sx={{ maxWidth: 400, width: '100%', mx: 2 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" color="primary" fontWeight={700} textAlign="center" gutterBottom>
            {t('app.name')}
          </Typography>
          <Typography variant="body2" color="text.secondary" textAlign="center" mb={3}>
            {t('app.tagline')}
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField fullWidth label={t('auth.email')} type="email" value={email} onChange={(e) => setEmail(e.target.value)} margin="normal" required autoComplete="email" />
            <TextField fullWidth label={t('auth.password')} type="password" value={password} onChange={(e) => setPassword(e.target.value)} margin="normal" required autoComplete="current-password" />
            <Button fullWidth variant="contained" type="submit" size="large" sx={{ mt: 2 }} disabled={loading}>
              {loading ? <CircularProgress size={24} color="inherit" /> : t('auth.loginButton')}
            </Button>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Login;
