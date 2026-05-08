import React, { useEffect, useState } from 'react';
import { Alert, Box, Card, CardContent, CircularProgress, Typography } from '@mui/material';

import { denominationsApi } from '../api/client';

interface Denomination {
  id: number;
  name: string;
  code: string;
  founded_year?: number;
  description?: string;
  churches_count?: number;
}

const Denominations: React.FC = () => {
  const [items, setItems] = useState<Denomination[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    denominationsApi.list()
      .then((response) => setItems(response.data))
      .catch(() => setError('Unable to load denominations.'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Denominations</Typography>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Box sx={{ display: 'grid', gap: 2, gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
        {items.map((item) => (
          <Card key={item.id}>
            <CardContent>
              <Typography variant="h6">{item.name}</Typography>
              <Typography color="text.secondary">{item.code}</Typography>
              <Typography variant="body2">Founded: {item.founded_year || 'N/A'}</Typography>
              <Typography variant="body2">Churches: {item.churches_count || 0}</Typography>
              {item.description && <Typography variant="body2" sx={{ mt: 1 }}>{item.description}</Typography>}
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

export default Denominations;
