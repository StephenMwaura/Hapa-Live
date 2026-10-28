import { Navigate, Route, Routes } from 'react-router-dom';
import type { ReactNode } from 'react';
import { useAuth } from './auth';
import Dashboard from './pages/Dashboard';
import Home from './pages/Home';
import { Login, Signup } from './pages/Auth';

function ProtectedRoute({children}:{children:ReactNode}){const {user,loading}=useAuth();if(loading)return <div className="route-loading">Opening Hapa Live…</div>;return user?<>{children}</>:<Navigate to="/login" replace/>}

export default function App() {
  const { user, loading } = useAuth();
  if (loading) return <div className="route-loading">Opening Hapa Live…</div>;
  return <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/signup" element={user ? <Navigate to="/my-plans" replace /> : <Signup />} />
    <Route path="/login" element={user ? <Navigate to="/my-plans" replace /> : <Login />} />
    <Route path="/my-plans" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>;
}
