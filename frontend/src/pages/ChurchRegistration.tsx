import { useState } from 'react';
import { Button, Card, CardContent, Stack, TextField, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { useTranslation } from 'react-i18next';

import { coreApi } from '../api/client';

const ChurchRegistration = () => {
  const { t } = useTranslation();
  const [form, setForm] = useState({ name: '', denomination_id: '', community: '', address: '', phone: '', email: '' });
  const [message, setMessage] = useState('');

  const update = (field: string, value: string) => setForm((current) => ({ ...current, [field]: value }));
  const submit = async () => {
    try {
      await coreApi.post('/churches', { ...form, languages_used: ['English'], service_schedules: [] });
      setMessage('Church registration submitted successfully.');
    } catch {
      setMessage('Unable to submit registration.');
    }
  };

  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.churchRegistration')}</Typography>
      <Card>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.name')} fullWidth value={form.name} onChange={(e) => update('name', e.target.value)} /></Grid>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.denomination')} fullWidth value={form.denomination_id} onChange={(e) => update('denomination_id', e.target.value)} /></Grid>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.community')} fullWidth value={form.community} onChange={(e) => update('community', e.target.value)} /></Grid>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.address')} fullWidth value={form.address} onChange={(e) => update('address', e.target.value)} /></Grid>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.phone')} fullWidth value={form.phone} onChange={(e) => update('phone', e.target.value)} /></Grid>
            <Grid item xs={12} md={6}><TextField label={t('churchFields.email')} fullWidth value={form.email} onChange={(e) => update('email', e.target.value)} /></Grid>
          </Grid>
          <Stack direction="row" justifyContent="space-between" sx={{ mt: 3 }}>
            <Typography color="text.secondary">{message}</Typography>
            <Button variant="contained" onClick={submit}>{t('buttons.submit')}</Button>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default ChurchRegistration;
