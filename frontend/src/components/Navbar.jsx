import React from 'react';
import { useLocation } from 'react-router-dom';
import { Menu } from 'lucide-react';

export default function Navbar({ isOnline, toggleMenu }) {
  const location = useLocation();
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': return 'Dashboard';
      case '/predict': return 'Risk Prediction';
      case '/analysis': return 'Data Analysis';
      case '/performance': return 'Model Performance';
      case '/visualizations': return 'Visualizations';
      case '/about': return 'About';
      default: return '';
    }
  };

  return (
    <header className="h-16 bg-white border-b border-brand-border flex items-center justify-between px-4 md:px-8 sticky top-0 z-10 shadow-sm">
      <div className="flex items-center gap-3 md:gap-4">
        <button onClick={toggleMenu} className="md:hidden p-2 text-slate-500 hover:text-brand-navy rounded-lg hover:bg-slate-50 transition-colors">
          <Menu size={20} />
        </button>
        <h2 className="text-lg font-bold text-brand-navy tracking-tight">{getPageTitle()}</h2>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-[10px] md:text-xs font-bold px-2 md:px-3 py-1 md:py-1.5 bg-slate-50 rounded-full border border-slate-100 uppercase tracking-wider">
          <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className={isOnline ? 'text-emerald-700' : 'text-red-600'}>{isOnline ? 'API Connected' : 'Offline'}</span>
        </div>
      </div>
    </header>
  );
}
