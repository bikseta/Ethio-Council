import React, { useEffect, useState } from 'react';
import { Alert, Box, Button, MenuItem, Paper, TextField, Typography } from '@mui/material';

import { churchesApi, denominationsApi, hierarchyApi } from '../api/client';

interface SelectOption {
  id: number;
  name: string;
}

const ChurchRegistration: React.FC = () => {
  const [denominations, setDenominations] = useState<SelectOption[]>([]);
  const [woredas, setWoredas] = useState<SelectOption[]>([]);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    name: '',
    denomination_id: '',
    woreda_id: '',
    address: '',
    phone: '',
    email: '',
    established_year: '',
    member_count: '0',
  });

  useEffect(() => {
    Promise.all([denominationsApi.list(), hierarchyApi.woredas()])
      .then(([denominationResponse, woredaResponse]) => {
        setDenominations(denominationResponse.data);
        setWoredas(woredaResponse.data);
      })
      .catch(() => setError('Unable to load form options.'));
  }, []);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSuccess('');
    setError('');
    try {
      await churchesApi.create({
        name: form.name,
        denomination_id: Number(form.denomination_id),
        woreda_id: Number(form.woreda_id),
        address: form.address,
        phone: form.phone,
        email: form.email,
        established_year: form.established_year ? Number(form.established_year) : null,
        member_count: Number(form.member_count),
        is_active: true,
      });
      setSuccess('Church registered successfully.');
      setForm({
        name: '',
        denomination_id: '',
        woreda_id: '',
        address: '',
        phone: '',
        email: '',
        established_year: '',
        member_count: '0',
      });
    } catch {
      setError('Unable to register church.');
    }
  };

  return (
    <Paper sx={{ p: 3, maxWidth: 760 }}>
      <Typography variant="h4" gutterBottom>Register Church</Typography>
      <Typography variant="body2" color="text.secondary" mb={2}>
        Create a new ECFE church record aligned with the core-platform-service schema.
      </Typography>
      {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'grid', gap: 2 }}>
        <TextField label="Church Name" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
        <TextField select label="Denomination" value={form.denomination_id} onChange={(event) => setForm({ ...form, denomination_id: event.target.value })} required>
          {denominations.map((denomination) => <MenuItem key={denomination.id} value={denomination.id}>{denomination.name}</MenuItem>)}
        </TextField>
        <TextField select label="Woreda" value={form.woreda_id} onChange={(event) => setForm({ ...form, woreda_id: event.target.value })} required>
          {woredas.map((woreda) => <MenuItem key={woreda.id} value={woreda.id}>{woreda.name}</MenuItem>)}
        </TextField>
        <TextField label="Address" value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} />
        <TextField label="Phone" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
        <TextField label="Email" type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} />
        <TextField label="Established Year" type="number" value={form.established_year} onChange={(event) => setForm({ ...form, established_year: event.target.value })} />
        <TextField label="Member Count" type="number" value={form.member_count} onChange={(event) => setForm({ ...form, member_count: event.target.value })} />
        <Button type="submit" variant="contained">Save Church</Button>
      </Box>
    </Paper>
  );
};

export default ChurchRegistration;
