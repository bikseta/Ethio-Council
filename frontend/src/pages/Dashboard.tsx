import React, { useEffect, useState } from 'react';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { useTranslation } from 'react-i18next';
import { coreClient } from '../api/client';
import { analyticsApi } from '../api/client';

interface Stats {
  total_users: number;
  total_churches: number;
  total_members: number;
  total_denominations: number;
  open_crisis_reports: number;
}

const StatCard: React.FC<{ label: string; value: number | string; color?: string }> = ({ label, value, color = 'primary.main' }) => (
  <Card>
    <CardContent>
      <Typography variant="h3" color={color} fontWeight={700}>{value}</Typography>
      <Typography variant="body1" color="text.secondary">{label}</Typography>
    </CardContent>
  </Card>
);

const Dashboard: React.FC = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    coreClient.get('/api/v1/admin/stats')
      .then((res) => setStats(res.data))
      .catch(() => setStats({ total_users: 0, total_churches: 0, total_members: 0, total_denominations: 0, open_crisis_reports: 0 }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <Box display="flex" justifyContent="center" mt={8}><CircularProgress /></Box>;

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>{t('dashboard.title')}</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label={t('dashboard.totalMembers')} value={stats?.total_members ?? 0} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label={t('dashboard.totalChurches')} value={stats?.total_churches ?? 0} color="secondary.main" />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label={t('dashboard.totalDenominations')} value={stats?.total_denominations ?? 0} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label={t('dashboard.openCrisisReports')} value={stats?.open_crisis_reports ?? 0} color="error.main" />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
