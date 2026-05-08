import { Box, List, ListItemButton, ListItemText, Paper } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { NavLink } from 'react-router-dom';

const links = [
  ['/', 'navigation.dashboard'],
  ['/churches', 'navigation.churchDirectory'],
  ['/church-registration', 'navigation.churchRegistration'],
  ['/gis', 'navigation.gisMap'],
  ['/analytics', 'navigation.analytics'],
  ['/diaspora', 'navigation.diasporaPortal'],
  ['/crisis-response', 'navigation.crisisResponse'],
] as const;

const Sidebar = () => {
  const { t } = useTranslation();
  return (
    <Paper square elevation={2} sx={{ width: 260, minHeight: '100vh', position: 'fixed', top: 0, left: 0, pt: 9, zIndex: 1200 }}>
      <Box sx={{ px: 2 }}>
        <List>
          {links.map(([to, key]) => (
            <ListItemButton key={to} component={NavLink} to={to}>
              <ListItemText primary={t(key)} />
            </ListItemButton>
          ))}
        </List>
      </Box>
    </Paper>
  );
};

export default Sidebar;
