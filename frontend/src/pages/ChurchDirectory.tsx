import { useEffect, useState } from 'react';
import { Card, CardContent, Stack, TextField, Typography } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useTranslation } from 'react-i18next';

import { coreApi } from '../api/client';

const columns: GridColDef[] = [
  { field: 'name', headerName: 'Church', flex: 1.4 },
  { field: 'community', headerName: 'Community', flex: 1 },
  { field: 'membership_size', headerName: 'Members', flex: 0.8 },
  { field: 'verification_status', headerName: 'Status', flex: 0.8 },
];

const ChurchDirectory = () => {
  const { t } = useTranslation();
  const [rows, setRows] = useState<any[]>([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    coreApi.get('/churches').then(({ data }) => setRows(data)).catch(() => undefined);
  }, []);

  const filtered = rows.filter((row) => row.name?.toLowerCase().includes(search.toLowerCase()));

  return (
    <Stack spacing={3}>
      <Typography variant="h4">{t('navigation.churchDirectory')}</Typography>
      <Card>
        <CardContent>
          <Stack spacing={2}>
            <TextField value={search} onChange={(e) => setSearch(e.target.value)} placeholder={t('placeholders.searchChurches')} />
            <div style={{ height: 520, width: '100%' }}>
              <DataGrid rows={filtered} columns={columns} getRowId={(row) => row.id} disableRowSelectionOnClick />
            </div>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );
};

export default ChurchDirectory;
