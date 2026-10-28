import { Link, useNavigate } from 'react-router-dom';
import { ArrowRight, Heart, LogOut, Moon, Music2, Sun } from 'lucide-react';
import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { useAuth } from '../auth';

const themeKey = 'hapa-live-theme';
function useTheme() {
  const [dark, setDark] = useState(() => localStorage.getItem(themeKey) === 'dark' || (!localStorage.getItem(themeKey) && window.matchMedia('(prefers-color-scheme: dark)').matches));
  useEffect(() => { document.documentElement.dataset.theme = dark ? 'dark' : 'light'; localStorage.setItem(themeKey, dark ? 'dark' : 'light'); }, [dark]);
  return { dark, toggle: () => setDark(v => !v) };
}

function Header({ dark, toggle }: { dark: boolean; toggle: () => void }) {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  async function signOut() { await logout(); navigate('/'); }
  return <header className="site-header"><div className="nav-wrap">
    <Link to="/" className="brand"><span className="brand-icon"><Music2 size={17} /></span> hapa<span>live</span></Link>
    <nav className="nav-links"><a href="/#discover">Discover</a><a href="/#how-it-works">How it works</a></nav>
    <div className="nav-actions"><button className="theme-button" onClick={toggle} aria-label={`Switch to ${dark ? 'light' : 'dark'} mode`} title={`Switch to ${dark ? 'light' : 'dark'} mode`}>{dark ? <Sun size={17} /> : <Moon size={17} />}<span>{dark ? 'Light' : 'Dark'}</span></button>
      {user ? <><Link to="/my-plans" className="nav-my-plans"><Heart size={15} /> My plans</Link><button className="avatar" onClick={signOut} title={`Sign out ${user.name}`} aria-label="Sign out"><span>{user.name.slice(0,1).toUpperCase()}</span><LogOut size={13} /></button></> : <><Link to="/login" className="login-link">Log in</Link><Link to="/signup" className="button button-small">Join free <ArrowRight size={14} /></Link></>}
    </div>
  </div></header>;
}
function Footer() { return <footer className="footer"><div className="container footer-inner"><Link to="/" className="brand footer-brand"><span className="brand-icon"><Music2 size={17}/></span> hapa<span>live</span></Link><span>Find your people. Find your next live moment.</span><small>Ticket purchases happen on the event organiser’s site.</small></div></footer>; }
export function Shell({ children }: { children: ReactNode }) { const theme = useTheme(); return <><Header dark={theme.dark} toggle={theme.toggle}/>{children}<Footer/></>; }
