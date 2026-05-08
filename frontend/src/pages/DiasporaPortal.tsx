import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';

import { diasporaApi } from '../api/client';

interface Community {
  id: number;
  name: string;
  country: string;
  city?: string;
  member_count: number;
  partnerships_count?: number;
}

interface Partnership {
  id: number;
  community_name?: string;
  church_name?: string;
  partnership_type?: string;
  description?: string;
}

const DiasporaPortal: React.FC = () => {
  const [communities, setCommunities] = useState<Community[]>([]);
  const [partnerships, setPartnerships] = useState<Partnership[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([diasporaApi.communities(), diasporaApi.partnerships()])
      .then(([communityResponse, partnershipResponse]) => {
        setCommunities(communityResponse.data);
        setPartnerships(partnershipResponse.data);
      })
      .catch(() => setError('Unable to load diaspora data.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Diaspora Partnerships</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', mb: 3 }}>
        {communities.map((community) => (
          <Card key={community.id}>
            <CardContent>
              <Typography variant="h6">{community.name}</Typography>
              <Typography color="text.secondary">{community.city ? `${community.city}, ` : ''}{community.country}</Typography>
              <Typography variant="body2">Members: {community.member_count}</Typography>
              <Typography variant="body2">Partnerships: {community.partnerships_count || 0}</Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
      <Typography variant="h5" gutterBottom>Active Partnerships</Typography>
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))' }}>
        {partnerships.map((partnership) => (
          <Card key={partnership.id}>
            <CardContent>
              <Typography variant="h6">{partnership.community_name}</Typography>
              <Typography color="text.secondary">{partnership.church_name}</Typography>
              <Typography variant="body2">{partnership.partnership_type}</Typography>
              {partnership.description && <Typography variant="body2" sx={{ mt: 1 }}>{partnership.description}</Typography>}
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default DiasporaPortal;
