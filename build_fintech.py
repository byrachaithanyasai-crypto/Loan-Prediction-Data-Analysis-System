import os

files = {
    'tailwind.config.js': '''
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0f172a',
          navy: '#1e293b',
          light: '#f8fafc',
          blue: '#2563eb',
          low: '#10b981',
          high: '#ef4444',
          warning: '#f59e0b',
          border: '#e2e8f0'
        }
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [],
}
''',
    'src/components/Sidebar.jsx': '''
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

export default function Sidebar() {
  return (
    <div className="w-64 bg-white border-r border-brand-border h-screen fixed left-0 top-0 flex flex-col z-20">
      <div className="p-6 flex items-center gap-3">
        <Hexagon className="text-brand-blue fill-brand-blue/10" size={28} />
        <div>
          <h1 className="text-lg font-bold text-brand-dark leading-tight">LoanPredict</h1>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto px-4 py-2 space-y-6">
        {navGroups.map((group, idx) => (
          <div key={idx}>
            <h2 className="text-xs font-bold text-slate-400 tracking-wider mb-2 px-3">{group.title}</h2>
            <nav className="space-y-1">
              {group.items.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all font-medium text-sm ${
                      isActive 
                        ? 'bg-blue-50 text-brand-blue' 
                        : 'text-slate-600 hover:bg-slate-50 hover:text-brand-dark'
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
  );
}
''',
    'src/components/Navbar.jsx': '''
import React from 'react';
import { useLocation } from 'react-router-dom';

export default function Navbar({ isOnline }) {
  const location = useLocation();
  const getPageTitle = () => {
    switch (location.pathname) {
      case '/': return 'Dashboard';
      case '/predict': return 'Risk Prediction';
      case '/analysis': return 'Data Analysis';
      case '/performance': return 'Model Performance';
      case '/visualizations': return 'Visualizations';
      case '/about': return 'About Platform';
      default: return '';
    }
  };

  return (
    <header className="h-16 bg-white border-b border-brand-border flex items-center justify-between px-8 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-brand-dark">{getPageTitle()}</h2>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-sm font-medium px-3 py-1.5 bg-slate-50 rounded-full border border-slate-100">
          <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className={isOnline ? 'text-emerald-700' : 'text-red-600'}>{isOnline ? 'Live' : 'Offline'}</span>
        </div>
      </div>
    </header>
  );
}
''',
    'src/components/Layout.jsx': '''
import React, { useEffect, useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { getHealth } from '../services/api';

export default function Layout() {
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    getHealth().then(() => setIsOnline(true)).catch(() => setIsOnline(false));
  }, []);

  return (
    <div className="flex h-screen overflow-hidden bg-brand-light font-sans text-brand-dark">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col h-full overflow-hidden">
        <Navbar isOnline={isOnline} />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
''',
    'src/pages/Dashboard.jsx': '''
import React, { useEffect, useState } from 'react';
import { getDashboardStats } from '../services/api';
import { Users, ShieldCheck, ShieldAlert, CreditCard, ArrowRight, RefreshCw, Activity, Layers, PlayCircle, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';

function StatCard({ title, value, subtitle, icon: Icon, colorClass }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-start gap-4 transition-transform hover:-translate-y-1">
      <div className={`p-3 rounded-xl ${colorClass}`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-sm font-medium text-slate-500 mb-1">{title}</p>
        <p className="text-2xl font-bold text-brand-dark">{value}</p>
        {subtitle && <p className="text-xs text-slate-400 mt-1">{subtitle}</p>}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadStats = () => {
    setLoading(true);
    getDashboardStats().then(setStats).catch(console.error).finally(() => setLoading(false));
  };

  useEffect(() => { loadStats(); }, []);

  return (
    <div className="space-y-10 animate-fade-in pb-10">
      
      {/* HERO SECTION */}
      <div className="bg-brand-navy rounded-3xl p-10 shadow-lg flex flex-col lg:flex-row gap-10 items-center overflow-hidden relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-blue/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
        <div className="flex-1 relative z-10 text-white">
          <h1 className="text-4xl lg:text-5xl font-bold mb-4 tracking-tight leading-tight">Loan Risk Analytics <br/><span className="text-brand-blue">& Prediction</span></h1>
          <p className="text-lg text-slate-300 mb-8 max-w-xl">Evaluate loan applications using machine learning models and explore data-driven risk insights across your entire portfolio.</p>
          <div className="flex gap-4">
            <Link to="/predict" className="bg-brand-blue hover:bg-blue-600 text-white px-7 py-3.5 rounded-xl font-semibold transition flex items-center gap-2 shadow-md">
              Predict Loan Risk <ArrowRight size={18}/>
            </Link>
            <Link to="/analysis" className="bg-white/10 hover:bg-white/20 text-white px-7 py-3.5 rounded-xl font-semibold transition border border-white/20">
              Explore Analytics
            </Link>
          </div>
        </div>
        <div className="w-full lg:w-1/3 relative z-10">
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20">
            <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2"><Activity size={16}/> Risk Intelligence</h3>
            {stats ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center"><span className="text-slate-300">Total Applicants</span><span className="font-bold text-white text-lg">{stats.total_applicants}</span></div>
                <div className="flex justify-between items-center"><span className="text-slate-300">Low Risk Portfolio</span><span className="font-bold text-emerald-400 text-lg">{Math.round((stats.low_risk / (stats.total_applicants || 1)) * 100)}%</span></div>
                <div className="flex justify-between items-center"><span className="text-slate-300">High Risk Portfolio</span><span className="font-bold text-red-400 text-lg">{Math.round((stats.high_risk / (stats.total_applicants || 1)) * 100)}%</span></div>
              </div>
            ) : (
              <div className="h-32 flex items-center justify-center text-slate-400">Loading data...</div>
            )}
          </div>
        </div>
      </div>

      <div className="flex justify-between items-end border-b border-brand-border pb-4">
        <div>
          <h2 className="text-xl font-bold text-brand-dark mb-1">Portfolio Overview</h2>
        </div>
        <button onClick={loadStats} className="flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-brand-blue transition-colors">
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          Last updated: Just now
        </button>
      </div>

      {stats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Total Applications" value={stats.total_applicants || 'No historical data available'} icon={Users} colorClass="bg-blue-50 text-blue-600" />
          <StatCard title="Low Risk" value={stats.total_applicants ? `${Math.round((stats.low_risk / stats.total_applicants) * 100)}%` : 'N/A'} icon={ShieldCheck} colorClass="bg-emerald-50 text-emerald-600" />
          <StatCard title="High Risk" value={stats.total_applicants ? `${Math.round((stats.high_risk / stats.total_applicants) * 100)}%` : 'N/A'} icon={ShieldAlert} colorClass="bg-red-50 text-red-600" />
          <StatCard title="Average Credit Score" value={stats.avg_credit_score ? Math.round(stats.avg_credit_score) : 'N/A'} icon={CreditCard} colorClass="bg-indigo-50 text-indigo-600" />
        </div>
      ) : (
        <div className="h-28 bg-slate-100 rounded-2xl animate-pulse flex items-center justify-center text-slate-400">Loading metrics...</div>
      )}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl shadow-soft border border-brand-border p-8">
          <h3 className="font-bold text-brand-dark mb-6 text-lg">Risk Intelligence Insights</h3>
          {stats ? (
             <div className="space-y-4">
               <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-slate-700 text-sm">
                 <strong>Fact:</strong> High-risk applicants currently represent {Math.round((stats.high_risk / stats.total_applicants) * 100)}% of the total recorded applications.
               </div>
               <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-slate-700 text-sm">
                 <strong>Fact:</strong> The system has processed a total of {stats.total_applicants} application profiles.
               </div>
               <div className="text-xs text-slate-400 mt-4">Insights are strictly derived from actual dataset responses.</div>
             </div>
          ) : (
            <div className="text-sm text-slate-500">No historical data available.</div>
          )}
        </div>

        <div className="bg-white rounded-2xl shadow-soft border border-brand-border p-8">
          <h3 className="font-bold text-brand-dark mb-6 text-lg">Quick Actions</h3>
          <div className="space-y-4">
            <Link to="/predict" className="flex items-center justify-between p-4 rounded-xl border border-slate-200 hover:border-brand-blue hover:shadow-md transition-all group bg-white">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-blue-50 text-brand-blue rounded-lg"><PlayCircle size={24}/></div>
                <div>
                  <div className="font-semibold text-brand-dark">Predict Loan Risk</div>
                  <div className="text-sm text-slate-500">Evaluate an applicant</div>
                </div>
              </div>
              <ArrowRight size={20} className="text-slate-300 group-hover:text-brand-blue" />
            </Link>
            <Link to="/analysis" className="flex items-center justify-between p-4 rounded-xl border border-slate-200 hover:border-brand-blue hover:shadow-md transition-all group bg-white">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg"><Layers size={24}/></div>
                <div>
                  <div className="font-semibold text-brand-dark">Explore Data</div>
                  <div className="text-sm text-slate-500">Analyze applicant patterns</div>
                </div>
              </div>
              <ArrowRight size={20} className="text-slate-300 group-hover:text-brand-blue" />
            </Link>
            <Link to="/performance" className="flex items-center justify-between p-4 rounded-xl border border-slate-200 hover:border-brand-blue hover:shadow-md transition-all group bg-white">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Settings size={24}/></div>
                <div>
                  <div className="font-semibold text-brand-dark">Model Performance</div>
                  <div className="text-sm text-slate-500">Compare ML models</div>
                </div>
              </div>
              <ArrowRight size={20} className="text-slate-300 group-hover:text-brand-blue" />
            </Link>
          </div>
        </div>
      </div>
      
      <div className="mt-10">
        <h3 className="text-center font-bold text-brand-dark mb-8 text-xl">How It Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { step: '01', title: 'Enter Applicant Details', desc: 'Input financial & personal data.' },
            { step: '02', title: 'Select ML Model', desc: 'Choose a classification algorithm.' },
            { step: '03', title: 'Generate Risk Prediction', desc: 'Analyze data via API.' },
            { step: '04', title: 'Review Risk Probability', desc: 'Get data-driven insights.' }
          ].map((s, i) => (
            <div key={i} className="text-center p-6 bg-white border border-brand-border rounded-2xl">
              <div className="text-3xl font-black text-slate-100 mb-4">{s.step}</div>
              <h4 className="font-bold text-brand-dark mb-2">{s.title}</h4>
              <p className="text-sm text-slate-500">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
''',
    'src/pages/RiskPrediction.jsx': '''
import React, { useState, useEffect } from 'react';
import { predictRisk, getModels } from '../services/api';
import { ShieldCheck, ShieldAlert, Loader2, AlertCircle } from 'lucide-react';

export default function RiskPrediction() {
  const [formData, setFormData] = useState({
    age: 35, income: 75000, credit_score: 650, 
    loan_amount: 20000, loan_term_months: 36, 
    employment_status: 'Employed', model: 'Random Forest'
  });
  const [models, setModels] = useState(['Random Forest', 'Logistic Regression', 'Decision Tree']);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    getModels().then(setModels).catch(console.error);
  }, []);

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); setError(''); setResult(null);
    try {
      const data = {
        ...formData,
        age: Number(formData.age),
        income: Number(formData.income),
        credit_score: Number(formData.credit_score),
        loan_amount: Number(formData.loan_amount),
        loan_term_months: Number(formData.loan_term_months),
      };
      const res = await predictRisk(data);
      setResult(res);
    } catch (err) {
      console.error("Prediction Error:", err);
      setError("Unable to generate the prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-brand-dark mb-1">Loan Risk Prediction</h1>
        <p className="text-slate-500">Evaluate an applicant using trained machine learning models.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
        
        {/* LEFT COLUMN: FORM */}
        <div className="lg:col-span-3 bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
          <form onSubmit={handleSubmit} className="space-y-8">
            
            {/* Sections */}
            <div>
              <h3 className="text-sm font-bold tracking-wider text-slate-400 uppercase mb-4 pb-2 border-b border-slate-100">Financial Details</h3>
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-brand-navy mb-1.5">Annual Income ($)</label>
                  <input type="number" name="income" value={formData.income} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none" required min="1"/>
                </div>
                <div>
                  <label className="block text-sm font-medium text-brand-navy mb-1.5">Credit Score</label>
                  <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none" required min="300" max="900"/>
                  <p className="text-xs text-slate-400 mt-1.5">Credit score range: 300–900</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-brand-navy mb-1.5">Loan Amount ($)</label>
                  <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none" required min="1"/>
                </div>
                <div>
                  <label className="block text-sm font-medium text-brand-navy mb-1.5">Loan Term</label>
                  <select name="loan_term_months" value={formData.loan_term_months} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none">
                    <option value="12">12 Months</option><option value="24">24 Months</option><option value="36">36 Months</option>
                    <option value="48">48 Months</option><option value="60">60 Months</option>
                  </select>
                  <p className="text-xs text-slate-400 mt-1.5">Loan term: 12–60 months</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-bold tracking-wider text-slate-400 uppercase mb-4 pb-2 border-b border-slate-100">Personal Details</h3>
                <label className="block text-sm font-medium text-brand-navy mb-1.5">Age</label>
                <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none" required min="18" max="100"/>
              </div>
              <div>
                <h3 className="text-sm font-bold tracking-wider text-slate-400 uppercase mb-4 pb-2 border-b border-slate-100">Employment</h3>
                <label className="block text-sm font-medium text-brand-navy mb-1.5">Status</label>
                <select name="employment_status" value={formData.employment_status} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none">
                  <option>Employed</option><option>Self-Employed</option><option>Unemployed</option>
                </select>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-bold tracking-wider text-slate-400 uppercase mb-4 pb-2 border-b border-slate-100">Model</h3>
              <select name="model" value={formData.model} onChange={handleChange} className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium">
                {models.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            
            <button type="submit" disabled={loading} className="w-full bg-brand-blue hover:bg-blue-700 text-white font-semibold py-4 rounded-xl shadow-md shadow-blue-500/20 transition flex justify-center items-center gap-2 text-lg">
              {loading ? <><Loader2 className="animate-spin" size={24}/> Analyzing applicant...</> : 'Analyze Loan Risk'}
            </button>
          </form>
        </div>

        {/* RIGHT COLUMN: RESULT */}
        <div className="lg:col-span-2">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border sticky top-24 min-h-[500px] flex flex-col">
            <h3 className="text-sm font-bold tracking-wider text-slate-400 uppercase mb-6 pb-2 border-b border-slate-100">Risk Assessment</h3>
            
            {error && (
              <div className="bg-red-50 text-brand-high p-4 rounded-xl border border-red-100 flex items-start gap-3 animate-fade-in mb-4">
                <AlertCircle size={20} className="shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
            
            {!result && !loading && !error && (
              <div className="flex-1 flex flex-col justify-center items-center text-center px-4 animate-fade-in">
                <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                  <ShieldCheck size={32} className="text-slate-300"/>
                </div>
                <h4 className="text-lg font-bold text-brand-dark mb-2">Ready for Analysis</h4>
                <p className="text-slate-500 text-sm">Enter applicant information and run the model to generate a risk assessment.</p>
              </div>
            )}

            {result && !loading && (
              <div className="flex-1 flex flex-col animate-fade-in">
                <div className="text-center mb-8">
                  <div className={`inline-flex items-center gap-2 px-6 py-2 rounded-full text-sm font-black tracking-widest mb-6 ${result.risk_status === 'Low Risk' ? 'bg-emerald-100 text-brand-low' : 'bg-red-100 text-brand-high'}`}>
                    {result.risk_status === 'Low Risk' ? <ShieldCheck size={20}/> : <ShieldAlert size={20}/>}
                    {result.risk_status.toUpperCase()}
                  </div>
                  
                  {result.probability != null && (
                    <div className="relative w-48 h-48 mx-auto flex items-center justify-center mb-2">
                      <svg className="absolute w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                        <circle cx="50" cy="50" r="45" fill="none" stroke={result.risk_status === 'Low Risk' ? '#10b981' : '#ef4444'} strokeWidth="8" strokeDasharray={`${result.probability * 2.82} 282`} strokeLinecap="round" className="transition-all duration-1000 ease-out" />
                      </svg>
                      <div className="flex flex-col items-center">
                        <span className="text-4xl font-black text-brand-dark">{result.probability}%</span>
                        <span className="text-[10px] uppercase font-bold text-slate-400 mt-1 tracking-widest">Probability</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-4 bg-slate-50 p-6 rounded-xl border border-slate-100 mb-6 flex-1">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Model Details</h4>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Model Used</span><span className="font-semibold text-brand-dark">{result.model_used || formData.model}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Credit Score</span><span className="font-medium text-brand-dark">{formData.credit_score}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Income</span><span className="font-medium text-brand-dark">${formData.income}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Loan Amount</span><span className="font-medium text-brand-dark">${formData.loan_amount}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Loan Term</span><span className="font-medium text-brand-dark">{formData.loan_term_months} mos</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Employment</span><span className="font-medium text-brand-dark">{formData.employment_status}</span></div>
                </div>

                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Risk Interpretation</h4>
                  <p className="text-sm text-slate-600 bg-white p-4 border border-slate-200 rounded-lg">
                    The selected model classified this application as <strong className={result.risk_status === 'Low Risk' ? 'text-brand-low' : 'text-brand-high'}>{result.risk_status.toLowerCase()}</strong> based on the supplied applicant features.
                  </p>
                </div>
                
                <button onClick={() => setResult(null)} className="mt-6 w-full py-3 border border-slate-200 text-brand-dark rounded-xl hover:bg-slate-50 font-bold transition text-sm">
                  Run Another Prediction
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
''',
    'src/pages/About.jsx': '''
import React from 'react';
import { Database, Code, Server, Info } from 'lucide-react';

export default function About() {
  return (
    <div className="space-y-10 max-w-5xl mx-auto animate-fade-in pb-10">
      
      {/* HERO */}
      <div className="bg-brand-navy text-white rounded-3xl p-12 shadow-lg overflow-hidden relative">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-blue/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>
        <div className="relative z-10">
          <h1 className="text-4xl font-bold mb-4">Loan Prediction Data Analysis System</h1>
          <p className="text-slate-300 max-w-2xl text-xl leading-relaxed">An intelligent analytics platform for loan risk assessment and applicant data analysis.</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* LEFT COLUMN */}
        <div className="space-y-8">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-dark mb-4 flex items-center gap-3"><Info size={24} className="text-brand-blue"/> About the Platform</h2>
            <p className="text-slate-600 leading-relaxed">
              This system provides an end-to-end Machine Learning pipeline designed to evaluate the default risk of loan applicants based on historical financial metrics. It offers a secure, high-performance environment for data exploration, real-time prediction, and analytical reporting.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-dark mb-5 flex items-center gap-3"><Database size={24} className="text-brand-blue"/> Core Capabilities</h2>
            <ol className="space-y-4 text-slate-600 font-medium list-decimal list-inside marker:text-brand-blue marker:font-bold">
              <li className="pl-2">Loan Risk Prediction</li>
              <li className="pl-2">Applicant Data Analysis</li>
              <li className="pl-2">Machine Learning Model Comparison</li>
              <li className="pl-2">Interactive Visualizations</li>
              <li className="pl-2">Risk Probability Assessment</li>
            </ol>
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="space-y-8">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-dark mb-5 flex items-center gap-3"><Server size={24} className="text-brand-blue"/> Architecture</h2>
            <div className="flex flex-col items-center space-y-3 text-sm font-semibold text-slate-700">
              <div className="w-full text-center py-3.5 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">React Frontend</div>
              <div className="text-brand-blue">↓</div>
              <div className="w-full text-center py-3.5 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">FastAPI API Layer</div>
              <div className="text-brand-blue">↓</div>
              <div className="w-full text-center py-3.5 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">Prediction & Analytics Services</div>
              <div className="text-brand-blue">↓</div>
              <div className="w-full text-center py-3.5 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">Machine Learning Models</div>
              <div className="text-brand-blue">↓</div>
              <div className="w-full text-center py-3.5 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">Loan Dataset</div>
            </div>
          </div>
          
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-dark mb-4 flex items-center gap-3"><Code size={24} className="text-brand-blue"/> Technology</h2>
            <div className="flex flex-wrap gap-2.5">
              {['React', 'Vite', 'Tailwind CSS', 'FastAPI', 'Python', 'Pandas', 'Scikit-learn', 'Joblib', 'Recharts'].map(t => (
                <span key={t} className="px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm font-semibold text-slate-700 hover:bg-slate-100 transition-colors">{t}</span>
              ))}
            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
}
'''
}

base_dir = os.path.join(os.getcwd(), 'frontend')
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\\n')

print("FinTech UI files rescaffolded successfully.")
