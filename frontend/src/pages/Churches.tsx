import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useTranslation } from 'react-i18next';
import { churchesApi } from '../api/client';

const Churches: React.FC = () => {
  const { t } = useTranslation();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    churchesApi.list().then((res) => setRows(res.data)).catch(() => setRows([])).finally(() => setLoading(false));
  }, []);

  const columns: GridColDef[] = [
    { field: 'name', headerName: t('churches.name'), flex: 1 },
    { field: 'pastor_name', headerName: t('churches.pastor'), flex: 1 },
    { field: 'member_count', headerName: t('churches.memberCount'), width: 120 },
  ];

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>{t('churches.title')}</Typography>
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>
      ) : (
        <DataGrid rows={rows} columns={columns} getRowId={(row) => row.id} autoHeight pageSizeOptions={[25, 50]} />
      )}
    </Box>
  );
};

export default Churches;
