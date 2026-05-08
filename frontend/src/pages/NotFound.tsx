import { Box, Button, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

const NotFound = () => (
  <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center' }}>
    <Box sx={{ textAlign: 'center' }}>
      <Typography variant="h2">404</Typography>
      <Typography variant="h5" sx={{ mb: 2 }}>Page not found</Typography>
      <Button component={Link} to="/" variant="contained">Go Home</Button>
    </Box>
  </Box>
);

export default NotFound;
