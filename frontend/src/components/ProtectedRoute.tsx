import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useStore } from '../store';

const ProtectedRoute: React.FC = () => {
  const { auth } = useStore();
  return auth.isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

export default ProtectedRoute;
