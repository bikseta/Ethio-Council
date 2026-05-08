import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';

import { hierarchyApi } from '../api/client';

interface Item {
  id: number;
  name: string;
  code: string;
}

interface Summary {
  regions: number;
  zones: number;
  woredas: number;
  kebeles: number;
}

const AdminHierarchy: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [regions, setRegions] = useState<Item[]>([]);
  const [zones, setZones] = useState<Item[]>([]);
  const [woredas, setWoredas] = useState<Item[]>([]);
  const [kebeles, setKebeles] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      hierarchyApi.summary(),
      hierarchyApi.regions(),
      hierarchyApi.zones(),
      hierarchyApi.woredas(),
      hierarchyApi.kebeles(),
    ])
      .then(([summaryResponse, regionResponse, zoneResponse, woredaResponse, kebeleResponse]) => {
        setSummary(summaryResponse.data);
        setRegions(regionResponse.data);
        setZones(zoneResponse.data);
        setWoredas(woredaResponse.data);
        setKebeles(kebeleResponse.data);
      })
      .catch(() => setError('Unable to load hierarchy data.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Administrative Hierarchy</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {summary && (
        <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', mb: 3 }}>
          {Object.entries(summary).map(([label, value]) => (
            <Card key={label}><CardContent><Typography variant="h5">{value}</Typography><Typography color="text.secondary">{label}</Typography></CardContent></Card>
          ))}
        </Box>
      )}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))' }}>
        <Card><CardContent><Typography variant="h6">Regions</Typography>{regions.map((item) => <Typography key={item.id} variant="body2">{item.name} ({item.code})</Typography>)}</CardContent></Card>
        <Card><CardContent><Typography variant="h6">Zones</Typography>{zones.map((item) => <Typography key={item.id} variant="body2">{item.name} ({item.code})</Typography>)}</CardContent></Card>
        <Card><CardContent><Typography variant="h6">Woredas</Typography>{woredas.map((item) => <Typography key={item.id} variant="body2">{item.name} ({item.code})</Typography>)}</CardContent></Card>
        <Card><CardContent><Typography variant="h6">Kebeles</Typography>{kebeles.map((item) => <Typography key={item.id} variant="body2">{item.name} ({item.code})</Typography>)}</CardContent></Card>
      </Box>
    </Box>
  );
};

export default AdminHierarchy;
