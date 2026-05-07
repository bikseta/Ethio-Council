import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useTranslation } from 'react-i18next';
import { membersApi } from '../api/client';

const Members: React.FC = () => {
  const { t } = useTranslation();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    membersApi.list().then((res) => setRows(res.data)).catch(() => setRows([])).finally(() => setLoading(false));
  }, []);

  const columns: GridColDef[] = [
    { field: 'full_name', headerName: t('members.fullName'), flex: 1 },
    { field: 'gender', headerName: t('members.gender'), width: 100 },
    { field: 'phone', headerName: t('members.phone'), width: 150 },
    { field: 'status', headerName: t('members.status'), width: 120 },
  ];

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>{t('members.title')}</Typography>
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>
      ) : (
        <DataGrid rows={rows} columns={columns} getRowId={(row) => row.id} autoHeight pageSizeOptions={[25, 50]} />
      )}
    </Box>
  );
};

export default Members;
