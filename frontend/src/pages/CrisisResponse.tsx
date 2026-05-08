import { useEffect, useState } from 'react';
import { Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { useTranslation } from 'react-i18next';

import ChurchMap from '../components/Map/ChurchMap';
import { crisisApi } from '../api/client';

const CrisisResponse = () => {
  const { t } = useTranslation();
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    crisisApi.get('/incidents').then(({ data }) => setIncidents(data)).catch(() => undefined);
  }, []);

  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.crisisResponse')}</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}><ChurchMap /></Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6">Active Incidents</Typography>
              <List>
                {incidents.map((incident) => (
                  <ListItem key={incident.id} divider>
                    <ListItemText primary={incident.title} secondary={`${incident.incident_type} • ${incident.status}`} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Stack>
  );
};

export default CrisisResponse;
