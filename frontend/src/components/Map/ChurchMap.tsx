import React from 'react';
import { Box, Typography } from '@mui/material';

interface Marker {
  id: number;
  latitude: number;
  longitude: number;
  label?: string;
}

interface ChurchMapProps {
  markers?: Marker[];
}

const ChurchMap: React.FC<ChurchMapProps> = ({ markers = [] }) => {
  return (
    <Box sx={{ border: '1px solid #ccc', borderRadius: 1, p: 2, minHeight: 400, backgroundColor: '#f5f5f5' }}>
      <Typography variant="h6" gutterBottom>Church Locations</Typography>
      <Typography variant="body2" color="text.secondary">
        {markers.length} location(s) registered
      </Typography>
      {markers.map((marker) => (
        <Box key={marker.id} p={1} border="1px solid #ddd" borderRadius={1} mb={1}>
          <Typography variant="body2">
            {marker.label || `Church #${marker.id}`}: ({marker.latitude.toFixed(4)}, {marker.longitude.toFixed(4)})
          </Typography>
        </Box>
      ))}
      {markers.length === 0 && (
        <Typography variant="body2" color="text.secondary" mt={2}>
          No church locations to display. Add Mapbox token to enable interactive map.
        </Typography>
      )}
    </Box>
  );
};

export default ChurchMap;
