import React, { useState } from 'react';
import { Alert, Box, Button, Card, CardContent, CircularProgress, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { authApi } from '../api/client';
import { useAuthStore } from '../store/authStore';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('Admin@2024!');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    try {
      const loginResponse = await authApi.login(username, password);
      const token = loginResponse.data.access_token as string;
      const meResponse = await authApi.me(token);
      setAuth(meResponse.data, token);
      navigate('/dashboard');
    } catch {
      setError('Unable to sign in with the provided credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', bgcolor: '#F5F7FA', p: 2 }}>
      <Card sx={{ width: '100%', maxWidth: 460 }}>
        <CardContent>
          <Typography variant="h4" gutterBottom>ECFE Platform Login</Typography>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Use the scaffold seed account to access the platform.
          </Typography>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          <Box component="form" onSubmit={handleSubmit}>
            <TextField fullWidth margin="normal" label="Username" value={username} onChange={(event) => setUsername(event.target.value)} />
            <TextField fullWidth margin="normal" label="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            <Button fullWidth type="submit" variant="contained" sx={{ mt: 2 }} disabled={loading}>
              {loading ? <CircularProgress size={20} color="inherit" /> : 'Sign In'}
            </Button>
          </Box>
          <Typography variant="caption" color="text.secondary" display="block" mt={2}>
            Seed credentials: admin / Admin@2024!
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Login;
