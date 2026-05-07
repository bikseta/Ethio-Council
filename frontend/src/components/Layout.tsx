import React from 'react';
import { Outlet } from 'react-router-dom';
import Box from '@mui/material/Box';
import Navbar from './Navbar';

const Layout: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, bgcolor: 'background.default' }}>
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;
