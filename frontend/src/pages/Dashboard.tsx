import { useEffect, useState } from 'react';
import { Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { useTranslation } from 'react-i18next';

import { analyticsApi } from '../api/client';

const Dashboard = () => {
  const { t } = useTranslation();
  const [overview, setOverview] = useState({ total_churches: 0, total_ministries: 0, regions_covered: 0, active_crises: 0 });

  useEffect(() => {
    analyticsApi.get('/dashboard/overview').then(({ data }) => setOverview(data)).catch(() => undefined);
  }, []);

  const cards = [
    ['dashboard.totalChurches', overview.total_churches],
    ['dashboard.totalMinistries', overview.total_ministries],
    ['dashboard.regionsCovered', overview.regions_covered],
    ['dashboard.activeCrises', overview.active_crises],
  ] as const;

  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.dashboard')}</Typography>
      <Grid container spacing={2}>
        {cards.map(([label, value]) => (
          <Grid item xs={12} md={3} key={label}>
            <Card>
              <CardContent>
                <Typography color="text.secondary">{t(label)}</Typography>
                <Typography variant="h4">{value}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Card>
        <CardContent>
          <Typography variant="h6">{t('dashboard.recentActivity')}</Typography>
          <List>
            <ListItem><ListItemText primary="New church registration received from Addis Ababa" /></ListItem>
            <ListItem><ListItemText primary="Diaspora partnership proposal submitted from Washington, DC" /></ListItem>
            <ListItem><ListItemText primary="Volunteer deployment opened for flood response" /></ListItem>
          </List>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default Dashboard;
