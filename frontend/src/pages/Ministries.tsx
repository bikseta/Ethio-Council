import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';

import { ministriesApi } from '../api/client';

interface Ministry {
  id: number;
  name: string;
  description?: string;
  church_name?: string;
  leader_name?: string;
}

const Ministries: React.FC = () => {
  const [items, setItems] = useState<Ministry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    ministriesApi.list()
      .then((response) => setItems(response.data))
      .catch(() => setError('Unable to load ministries.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Ministries</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))' }}>
        {items.map((item) => (
          <Card key={item.id}>
            <CardContent>
              <Typography variant="h6">{item.name}</Typography>
              <Typography color="text.secondary">{item.church_name || 'Church not linked'}</Typography>
              {item.leader_name && <Typography variant="body2">Lead: {item.leader_name}</Typography>}
              {item.description && <Typography variant="body2" sx={{ mt: 1 }}>{item.description}</Typography>}
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default Ministries;
