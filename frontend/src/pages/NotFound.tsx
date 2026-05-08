import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', textAlign: 'center' }}>
      <Box>
        <Typography variant="h2" color="primary">404</Typography>
        <Typography variant="h5" gutterBottom>Page Not Found</Typography>
        <Button variant="contained" onClick={() => navigate('/')}>Return to Dashboard</Button>
      </Box>
    </Box>
  );
};

export default NotFound;
