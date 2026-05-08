import { useEffect, useState } from 'react';
import { Button, Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';

import { coreApi } from '../api/client';

const DiasporaPortal = () => {
  const { t } = useTranslation();
  const [communities, setCommunities] = useState<any[]>([]);

  useEffect(() => {
    coreApi.get('/diaspora/communities').then(({ data }) => setCommunities(data)).catch(() => undefined);
  }, []);

  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.diasporaPortal')}</Typography>
      <Card>
        <CardContent>
          <Typography variant="h6">Diaspora Communities</Typography>
          <List>
            {communities.map((community) => (
              <ListItem key={community.id} divider>
                <ListItemText primary={`${community.name} - ${community.country}`} secondary={`${community.city || ''} • ${community.membership_count || 0} members`} />
                <Button variant="outlined">{t('buttons.requestPartnership')}</Button>
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default DiasporaPortal;
