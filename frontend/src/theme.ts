import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: { main: '#1565C0' },
    secondary: { main: '#2E7D32' },
    background: { default: '#F4F7FB', paper: '#FFFFFF' },
  },
  shape: { borderRadius: 12 },
});

export default theme;
