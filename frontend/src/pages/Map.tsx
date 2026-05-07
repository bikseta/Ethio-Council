import React, { useRef, useEffect } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { useTranslation } from 'react-i18next';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || '';

const Map: React.FC = () => {
  const { t } = useTranslation();
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);

  useEffect(() => {
    if (!MAPBOX_TOKEN || map.current || !mapContainer.current) return;
    mapboxgl.accessToken = MAPBOX_TOKEN;
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [38.7578, 9.0320], // Addis Ababa
      zoom: 5,
    });
    map.current.addControl(new mapboxgl.NavigationControl());
    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  return (
    <Box>
      <Typography variant="h4" fontWeight={700} gutterBottom>{t('nav.map')}</Typography>
      {!MAPBOX_TOKEN && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Set REACT_APP_MAPBOX_TOKEN in your .env to enable the map.
        </Alert>
      )}
      <Box ref={mapContainer} sx={{ height: 600, borderRadius: 2, overflow: 'hidden' }} />
    </Box>
  );
};

export default Map;
