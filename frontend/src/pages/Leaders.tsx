import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, Chip, CircularProgress, Typography } from '@mui/material';

import { leadersApi } from '../api/client';

interface Leader {
  id: number;
  full_name: string;
  title?: string;
  church_name?: string;
  email?: string;
  phone?: string;
  is_active: boolean;
}

const Leaders: React.FC = () => {
  const [items, setItems] = useState<Leader[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    leadersApi.list()
      .then((response) => setItems(response.data))
      .catch(() => setError('Unable to load leaders.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Church Leaders</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
        {items.map((item) => (
          <Card key={item.id}>
            <CardContent>
              <Typography variant="h6">{item.full_name}</Typography>
              <Typography color="text.secondary">{item.title || 'Leader'}</Typography>
              <Typography variant="body2">{item.church_name || 'Church not linked'}</Typography>
              {item.email && <Typography variant="body2">{item.email}</Typography>}
              {item.phone && <Typography variant="body2">{item.phone}</Typography>}
              <Chip label={item.is_active ? 'Active' : 'Inactive'} size="small" color={item.is_active ? 'success' : 'default'} sx={{ mt: 1 }} />
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default Leaders;
