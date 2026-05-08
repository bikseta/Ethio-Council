import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';

import { analyticsPortalApi } from '../api/client';

interface DashboardPayload {
  church_stats: {
    total_churches: number;
    total_members: number;
    active_churches: number;
    denominations_count: number;
  };
  top_regions: Array<{
    region_name: string;
    church_count: number;
    member_count: number;
  }>;
  denomination_breakdown: Array<{
    denomination_name: string;
    church_count: number;
    member_count: number;
  }>;
  incident_stats?: {
    total_incidents: number;
    active_incidents: number;
    resolved_incidents: number;
    total_volunteers: number;
  };
}

const Analytics: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    analyticsPortalApi.dashboard()
      .then((response) => setDashboard(response.data))
      .catch(() => setError('Unable to load analytics dashboard.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>ECFE Dashboard</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {dashboard && (
        <>
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', mb: 3 }}>
            {[
              { label: 'Total Churches', value: dashboard.church_stats.total_churches },
              { label: 'Total Members', value: dashboard.church_stats.total_members },
              { label: 'Active Churches', value: dashboard.church_stats.active_churches },
              { label: 'Denominations', value: dashboard.church_stats.denominations_count },
            ].map((item) => (
              <Card key={item.label}><CardContent><Typography variant="h4">{item.value}</Typography><Typography color="text.secondary">{item.label}</Typography></CardContent></Card>
            ))}
          </Box>
          {dashboard.incident_stats && (
            <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', mb: 3 }}>
              {[
                { label: 'Incidents', value: dashboard.incident_stats.total_incidents },
                { label: 'Active Incidents', value: dashboard.incident_stats.active_incidents },
                { label: 'Resolved Incidents', value: dashboard.incident_stats.resolved_incidents },
                { label: 'Volunteers', value: dashboard.incident_stats.total_volunteers },
              ].map((item) => (
                <Card key={item.label}><CardContent><Typography variant="h5">{item.value}</Typography><Typography color="text.secondary">{item.label}</Typography></CardContent></Card>
              ))}
            </Box>
          )}
          <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(2, minmax(0, 1fr))' }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Top Regions</Typography>
                {dashboard.top_regions.map((region) => (
                  <Typography key={region.region_name} variant="body2">
                    {region.region_name}: {region.church_count} churches / {region.member_count} members
                  </Typography>
                ))}
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Denomination Breakdown</Typography>
                {dashboard.denomination_breakdown.map((item) => (
                  <Typography key={item.denomination_name} variant="body2">
                    {item.denomination_name}: {item.church_count} churches / {item.member_count} members
                  </Typography>
                ))}
              </CardContent>
            </Card>
          </Box>
        </>
      )}
    </Box>
  );
};

export default Analytics;
