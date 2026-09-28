import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ShieldAlert, BarChart3, Activity, PieChart, Info, Hexagon } from 'lucide-react';

const navGroups = [
  {
    title: 'OVERVIEW',
    items: [{ path: '/', label: 'Dashboard', icon: LayoutDashboard }]
  },
  {
    title: 'RISK MANAGEMENT',
    items: [
      { path: '/predict', label: 'Risk Prediction', icon: ShieldAlert },
      { path: '/performance', label: 'Model Performance', icon: Activity }
    ]
  },
  {
    title: 'ANALYTICS',
    items: [
      { path: '/analysis', label: 'Data Analysis', icon: BarChart3 },
      { path: '/visualizations', label: 'Visualizations', icon: PieChart }
    ]
  },
  {
    title: 'SYSTEM',
    items: [{ path: '/about', label: 'About', icon: Info }]
  }
];

export default function Sidebar({ isOpen, closeMenu }) {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-brand-navy/20 backdrop-blur-sm z-30 md:hidden animate-fade-in"
          onClick={closeMenu}
        />
      )}
      
      {/* Sidebar container */}
      <div className={`w-64 bg-white border-r border-brand-border h-screen fixed left-0 top-0 flex flex-col z-40 shadow-soft transition-transform duration-300 ease-in-out md:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-6 flex items-center justify-between border-b border-slate-50">
          <div className="flex items-center gap-3">
            <Hexagon className="text-brand-blue fill-brand-blue/10" size={28} />
            <h1 className="text-xl font-bold text-brand-dark leading-tight tracking-tight">LoanPredict</h1>
          </div>
        </div>
      
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-8">
        {navGroups.map((group, idx) => (
          <div key={idx}>
            <h2 className="text-[11px] font-bold text-slate-400 tracking-widest mb-3 px-3 uppercase">{group.title}</h2>
            <nav className="space-y-1">
              {group.items.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={closeMenu}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all font-semibold text-sm ${
                      isActive 
                        ? 'bg-blue-50 text-brand-blue shadow-sm' 
                        : 'text-slate-500 hover:bg-slate-50 hover:text-brand-dark'
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      <item.icon size={18} className={isActive ? 'text-brand-blue' : 'text-slate-400'} />
                      {item.label}
                    </>
                  )}
                </NavLink>
              ))}
            </nav>
          </div>
        ))}
      </div>
    </div>
    </>
  );
}
