import React, { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Chip from '@mui/material/Chip';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useTranslation } from 'react-i18next';
import { crisisApi } from '../api/client';

const severityColor: Record<string, 'default' | 'error' | 'warning' | 'info' | 'success'> = {
  CRITICAL: 'error', HIGH: 'error', MEDIUM: 'warning', LOW: 'info',
};

const Reports: React.FC = () => {
  const { t } = useTranslation();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    crisisApi.list().then((res) => setRows(res.data?.alerts ?? [])).catch(() => setRows([])).finally(() => setLoading(false));
  }, []);

  const columns: GridColDef[] = [
    { field: 'title', headerName: 'Title', flex: 1 },
    { field: 'severity', headerName: t('crisis.severity'), width: 120, renderCell: (params) => <Chip label={params.value} color={severityColor[params.value] || 'default'} size="small" /> },
    { field: 'status', headerName: t('crisis.status'), width: 130 },
    { field: 'affected_count', headerName: t('crisis.affected'), width: 110 },
  ];

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>{t('crisis.title')}</Typography>
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}><CircularProgress /></Box>
      ) : (
        <DataGrid rows={rows} columns={columns} getRowId={(row) => row.id || Math.random()} autoHeight pageSizeOptions={[25, 50]} />
      )}
    </Box>
  );
};

export default Reports;
