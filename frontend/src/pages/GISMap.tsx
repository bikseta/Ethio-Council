import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, List, ListItem, ListItemText, Typography } from '@mui/material';

import { registrationsApi } from '../api/client';
import ChurchMap from '../components/Map/ChurchMap';

interface Summary {
  registrations: number;
  verified: number;
  pending: number;
}

interface Registration {
  id: number;
  church_id: number;
  latitude: number;
  longitude: number;
  status: string;
  address?: string;
}

const GISMap: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([registrationsApi.summary(), registrationsApi.list()])
      .then(([summaryResponse, registrationsResponse]) => {
        setSummary(summaryResponse.data);
        setRegistrations(registrationsResponse.data);
      })
      .catch(() => setError('Unable to load GIS registrations.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>GIS Registration</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {summary && (
        <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', mb: 3 }}>
          {Object.entries(summary).map(([label, value]) => (
            <Card key={label}><CardContent><Typography variant="h5">{value}</Typography><Typography color="text.secondary">{label}</Typography></CardContent></Card>
          ))}
        </Box>
      )}
      <ChurchMap markers={registrations.map((item) => ({ id: item.id, latitude: item.latitude, longitude: item.longitude, label: `Church #${item.church_id}` }))} />
      <List>
        {registrations.map((item) => (
          <ListItem key={item.id} divider>
            <ListItemText primary={`Church #${item.church_id}`} secondary={`${item.address || 'Address unavailable'} • ${item.status}`} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default GISMap;
