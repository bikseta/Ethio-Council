import { Box, Typography } from '@mui/material';
import Map, { Marker, NavigationControl } from 'react-map-gl/mapbox';

import { mapboxToken } from '../../api/client';

type MarkerItem = {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
};

type ChurchMapProps = {
  markers?: MarkerItem[];
};

const defaultMarkers: MarkerItem[] = [
  { id: '1', name: 'Addis Ababa Central Church', latitude: 8.9806, longitude: 38.7578 },
  { id: '2', name: 'Adama Fellowship', latitude: 8.5414, longitude: 39.268 },
];

const ChurchMap = ({ markers = defaultMarkers }: ChurchMapProps) => (
  <Box sx={{ height: 520, borderRadius: 3, overflow: 'hidden' }}>
    <Map
      initialViewState={{ latitude: 8.8, longitude: 39.1, zoom: 5.6 }}
      style={{ width: '100%', height: '100%' }}
      mapStyle="mapbox://styles/mapbox/streets-v12"
      mapboxAccessToken={mapboxToken}
    >
      <NavigationControl position="top-right" />
      {markers.map((marker) => (
        <Marker key={marker.id} latitude={marker.latitude} longitude={marker.longitude} anchor="bottom">
          <Box sx={{ bgcolor: 'primary.main', color: 'white', px: 1, py: 0.5, borderRadius: 2 }}>
            <Typography variant="caption">{marker.name}</Typography>
          </Box>
        </Marker>
      ))}
    </Map>
  </Box>
);

export default ChurchMap;
