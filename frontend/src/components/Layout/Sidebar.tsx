import React from 'react';
import { AccountTree, Analytics, Church, CrisisAlert, Group, Hub, LocationOn, Public } from '@mui/icons-material';
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const drawerWidth = 260;

const navItems = [
  { text: 'Dashboard', icon: <Analytics />, path: '/dashboard' },
  { text: 'Church Directory', icon: <Church />, path: '/churches' },
  { text: 'Register Church', icon: <Church />, path: '/churches/register' },
  { text: 'Denominations', icon: <Hub />, path: '/denominations' },
  { text: 'Ministries', icon: <Group />, path: '/ministries' },
  { text: 'Leaders', icon: <Group />, path: '/leaders' },
  { text: 'Admin Hierarchy', icon: <AccountTree />, path: '/hierarchy' },
  { text: 'Diaspora', icon: <Public />, path: '/diaspora' },
  { text: 'GIS Registration', icon: <LocationOn />, path: '/gis-registration' },
  { text: 'Crisis Response', icon: <CrisisAlert />, path: '/crisis-response' },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          borderRight: '1px solid rgba(0,0,0,0.08)',
        },
      }}
    >
      <Toolbar />
      <List>
        {navItems.map((item) => (
          <ListItemButton
            key={item.path}
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
