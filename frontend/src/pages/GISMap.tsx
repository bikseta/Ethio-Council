import { Card, CardContent, Stack, Typography } from '@mui/material';
import Grid from '@mui/material/GridLegacy';
import { useTranslation } from 'react-i18next';

import ChurchMap from '../components/Map/ChurchMap';

const GISMap = () => {
  const { t } = useTranslation();
  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.gisMap')}</Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} md={9}>
          <ChurchMap />
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6">Map Filters</Typography>
              <Typography variant="body2">Verified churches</Typography>
              <Typography variant="body2">Registration density</Typography>
              <Typography variant="body2">Diaspora-linked churches</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Stack>
  );
};

export default GISMap;
