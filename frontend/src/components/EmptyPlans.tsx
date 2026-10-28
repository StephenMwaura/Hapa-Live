import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import type { ReactNode } from 'react';

export default function EmptyPlans({icon,title,text,cta,href}:{icon:ReactNode,title:string,text:string,cta:string,href:string}){return <div className="empty-plans"><span className="empty-plans-icon">{icon}</span><h3>{title}</h3><p>{text}</p><Link className="button" to={href}>{cta}<ArrowRight size={15}/></Link></div>}