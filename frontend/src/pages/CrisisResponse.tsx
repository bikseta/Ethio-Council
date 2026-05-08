import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, Chip, CircularProgress, List, ListItem, ListItemText, Typography } from '@mui/material';

import { crisisPortalApi } from '../api/client';

interface Summary {
  incidents: number;
  active_incidents: number;
  volunteers: number;
  available_volunteers: number;
  distributions: number;
}

interface Incident {
  id: number;
  title: string;
  severity: string;
  status: string;
  location?: string;
  affected_count: number;
}

interface Volunteer {
  id: number;
  full_name: string;
  status: string;
  skills?: string;
}

const CrisisResponse: React.FC = () => {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([crisisPortalApi.summary(), crisisPortalApi.incidents(), crisisPortalApi.volunteers()])
      .then(([summaryResponse, incidentsResponse, volunteersResponse]) => {
        setSummary(summaryResponse.data);
        setIncidents(incidentsResponse.data);
        setVolunteers(volunteersResponse.data);
      })
      .catch(() => setError('Unable to load crisis response data.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Crisis Response</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {summary && (
        <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', mb: 3 }}>
          {Object.entries(summary).map(([label, value]) => (
            <Card key={label}><CardContent><Typography variant="h5">{value}</Typography><Typography color="text.secondary">{label}</Typography></CardContent></Card>
          ))}
        </Box>
      )}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(2, minmax(0, 1fr))' }}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Incidents</Typography>
            <List>
              {incidents.map((incident) => (
                <ListItem key={incident.id} divider>
                  <ListItemText primary={incident.title} secondary={`${incident.location || 'Unknown location'} • Affected: ${incident.affected_count}`} />
                  <Chip label={incident.severity} color={incident.severity === 'HIGH' || incident.severity === 'CRITICAL' ? 'warning' : 'default'} size="small" sx={{ mr: 1 }} />
                  <Chip label={incident.status} variant="outlined" size="small" />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>Volunteers</Typography>
            {volunteers.map((volunteer) => (
              <Box key={volunteer.id} sx={{ mb: 2 }}>
                <Typography variant="body1">{volunteer.full_name}</Typography>
                <Typography variant="body2" color="text.secondary">{volunteer.skills || 'Skills not listed'}</Typography>
                <Chip label={volunteer.status} size="small" sx={{ mt: 0.5 }} />
              </Box>
            ))}
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
};

export default CrisisResponse;
