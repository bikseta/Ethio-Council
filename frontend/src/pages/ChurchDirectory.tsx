import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, Chip, CircularProgress, Typography } from '@mui/material';

import { churchesApi } from '../api/client';

interface Church {
  id: number;
  name: string;
  denomination_name?: string;
  woreda_name?: string;
  member_count: number;
  address?: string;
  is_active: boolean;
}

const ChurchDirectory: React.FC = () => {
  const [churches, setChurches] = useState<Church[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    churchesApi.list()
      .then((response) => setChurches(response.data))
      .catch(() => setError('Unable to load churches.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Church Directory</Typography>
      <Typography variant="body2" color="text.secondary" mb={3}>
        Browse seeded ECFE churches by denomination and woreda.
      </Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))' }}>
        {churches.map((church) => (
          <Card key={church.id}>
            <CardContent>
              <Typography variant="h6">{church.name}</Typography>
              <Typography color="text.secondary">{church.denomination_name || 'Denomination unavailable'}</Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>{church.woreda_name || 'Unknown woreda'}</Typography>
              <Typography variant="body2">Members: {church.member_count}</Typography>
              {church.address && <Typography variant="body2">{church.address}</Typography>}
              <Chip label={church.is_active ? 'Active' : 'Inactive'} color={church.is_active ? 'success' : 'default'} size="small" sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default ChurchDirectory;
