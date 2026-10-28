import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { api } from './api';
import type { User } from './types';

type AuthContextValue = { user: User | null; loading: boolean; signup: (name: string, email: string, password: string) => Promise<void>; login: (email: string, password: string) => Promise<void>; logout: () => Promise<void> };
const AuthContext = createContext<AuthContextValue | null>(null);
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.me().then(setUser).catch(() => setUser(null)).finally(() => setLoading(false)); }, []);
  const value: AuthContextValue = {
    user, loading,
    signup: async (name, email, password) => setUser((await api.signup(name, email, password)).user),
    login: async (email, password) => setUser((await api.login(email, password)).user),
    logout: async () => { await api.logout(); setUser(null); },
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export function useAuth() { const value = useContext(AuthContext); if (!value) throw new Error('useAuth must be used inside AuthProvider'); return value; }
