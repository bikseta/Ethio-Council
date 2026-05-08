import { useEffect, useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { Bar, BarChart, Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { useTranslation } from 'react-i18next';

import { analyticsApi } from '../api/client';

const colors = ['#1565C0', '#2E7D32', '#F9A825', '#8E24AA', '#EF6C00'];

const Analytics = () => {
  const { t } = useTranslation();
  const [byRegion, setByRegion] = useState<any[]>([]);
  const [byDenomination, setByDenomination] = useState<any[]>([]);
  const [byMinistryType, setByMinistryType] = useState<any[]>([]);

  useEffect(() => {
    analyticsApi.get('/dashboard/by-region').then(({ data }) => setByRegion(data)).catch(() => undefined);
    analyticsApi.get('/dashboard/by-denomination').then(({ data }) => setByDenomination(data)).catch(() => undefined);
    analyticsApi.get('/dashboard/ministry-types').then(({ data }) => setByMinistryType(data)).catch(() => undefined);
  }, []);

  const growthTrend = [
    { year: '2021', churches: 2200 },
    { year: '2022', churches: 2410 },
    { year: '2023', churches: 2650 },
    { year: '2024', churches: 2890 },
  ];

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}><Typography variant="h4">{t('navigation.analytics')}</Typography></Grid>
      <Grid item xs={12} md={6}>
        <Card><CardContent><Typography variant="h6">Churches by Region</Typography><ResponsiveContainer width="100%" height={280}><BarChart data={byRegion}><XAxis dataKey="region" /><YAxis /><Tooltip /><Legend /><Bar dataKey="church_count" fill="#1565C0" /></BarChart></ResponsiveContainer></CardContent></Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card><CardContent><Typography variant="h6">Churches by Denomination</Typography><ResponsiveContainer width="100%" height={280}><PieChart><Pie data={byDenomination} dataKey="church_count" nameKey="denomination" outerRadius={90}>{byDenomination.map((_: any, index: number) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /><Legend /></PieChart></ResponsiveContainer></CardContent></Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card><CardContent><Typography variant="h6">Growth Trend</Typography><ResponsiveContainer width="100%" height={280}><LineChart data={growthTrend}><XAxis dataKey="year" /><YAxis /><Tooltip /><Legend /><Line type="monotone" dataKey="churches" stroke="#2E7D32" strokeWidth={3} /></LineChart></ResponsiveContainer></CardContent></Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card><CardContent><Typography variant="h6">Ministry Types</Typography><ResponsiveContainer width="100%" height={280}><PieChart><Pie data={byMinistryType} dataKey="total" nameKey="ministry_type" outerRadius={90}>{byMinistryType.map((_: any, index: number) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /><Legend /></PieChart></ResponsiveContainer></CardContent></Card>
      </Grid>
    </Grid>
  );
};

export default Analytics;
