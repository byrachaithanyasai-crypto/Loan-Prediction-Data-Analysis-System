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
          light: '#f8fafc',
          blue: '#2563eb',
          low: '#22c55e',
          high: '#ef4444'
        }
      }
    },
  },
  plugins: [],
}
''',
    'src/styles/global.css': '''
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-brand-light text-brand-dark font-sans antialiased;
}
''',
    'src/services/api.js': '''
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const getHealth = async () => (await api.get('/api/health')).data;
export const getDashboardStats = async () => (await api.get('/api/dashboard/stats')).data;
export const predictRisk = async (data) => (await api.post('/api/predict', data)).data;
export const getModelPerformance = async () => (await api.get('/api/models/performance')).data;
export const getModels = async () => (await api.get('/api/models')).data;
export const getAnalysisSummary = async () => (await api.get('/api/analysis/summary')).data;
''',
    'src/components/MetricCard.jsx': '''
import React from 'react';

export default function MetricCard({ title, value, icon: Icon }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center space-x-4">
      <div className="p-3 bg-blue-50 rounded-xl text-brand-blue">
        <Icon size={24} />
      </div>
      <div>
        <p className="text-sm text-gray-500 font-medium">{title}</p>
        <p className="text-2xl font-bold text-brand-dark">{value}</p>
      </div>
    </div>
  );
}
''',
    'src/components/Sidebar.jsx': '''
import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, ShieldAlert, BarChart3, Activity, PieChart, Info } from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/predict', label: 'Risk Prediction', icon: ShieldAlert },
  { path: '/analysis', label: 'Data Analysis', icon: BarChart3 },
  { path: '/performance', label: 'Model Performance', icon: Activity },
  { path: '/visualizations', label: 'Visualizations', icon: PieChart },
  { path: '/about', label: 'About', icon: Info },
];

export default function Sidebar() {
  return (
    <div className="w-64 bg-white border-r border-gray-200 h-screen fixed left-0 top-0 flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold text-brand-dark flex items-center gap-2">
          <span className="text-2xl">🏦</span> Loan Prediction Data Analysis System
        </h1>
      </div>
      <nav className="flex-1 px-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-colors font-medium ${
                isActive 
                  ? 'bg-brand-blue text-white shadow-md' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-brand-dark'
              }`
            }
          >
            <item.icon size={20} />
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="p-6 border-t border-gray-100">
        <p className="text-xs text-gray-400 text-center font-medium">DAE Academic Project</p>
      </div>
    </div>
  );
}
''',
    'src/components/Navbar.jsx': '''
import React, { useEffect, useState } from 'react';
import { getHealth } from '../services/api';

export default function Navbar() {
  const [status, setStatus] = useState('Checking...');
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    getHealth().then(() => {
      setStatus('API Connected');
      setIsOnline(true);
    }).catch(() => {
      setStatus('API Offline');
      setIsOnline(false);
    });
  }, []);

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 sticky top-0 z-10">
      <h2 className="text-lg font-semibold text-gray-800">Analytics Dashboard</h2>
      <div className="flex items-center gap-2 text-sm font-medium">
        <div className={`w-2.5 h-2.5 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
        <span className={isOnline ? 'text-gray-600' : 'text-red-500'}>{status}</span>
      </div>
    </header>
  );
}
''',
    'src/components/Layout.jsx': '''
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-brand-light">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col h-full">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
''',
    'src/pages/Dashboard.jsx': '''
import React, { useEffect, useState } from 'react';
import { getDashboardStats } from '../services/api';
import MetricCard from '../components/MetricCard';
import { Users, ShieldCheck, ShieldAlert, CreditCard, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    getDashboardStats().then(setStats).catch(console.error);
  }, []);

  return (
    <div className="space-y-8 animate-fade-in">
      <section className="bg-brand-dark text-white rounded-3xl p-10 shadow-lg relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <h1 className="text-4xl font-bold mb-4">Loan Prediction Data Analysis System</h1>
          <p className="text-lg text-gray-300 mb-8">AI-powered insights for intelligent loan risk assessment. Leverage machine learning to make data-driven lending decisions.</p>
          <div className="flex gap-4">
            <Link to="/predict" className="bg-brand-blue hover:bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold transition flex items-center gap-2 shadow-md">
              Analyze Loan Risk <ArrowRight size={18}/>
            </Link>
            <Link to="/analysis" className="bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-xl font-semibold transition border border-white/20">
              Explore Analytics
            </Link>
          </div>
        </div>
      </section>

      {stats ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard title="Total Applicants" value={stats.total_applicants} icon={Users} />
          <MetricCard title="Low Risk" value={stats.low_risk} icon={ShieldCheck} />
          <MetricCard title="High Risk" value={stats.high_risk} icon={ShieldAlert} />
          <MetricCard title="Avg Credit Score" value={Math.round(stats.avg_credit_score)} icon={CreditCard} />
        </div>
      ) : (
        <div className="text-gray-500">Loading analytics...</div>
      )}
    </div>
  );
}
''',
    'src/pages/RiskPrediction.jsx': '''
import React, { useState, useEffect } from 'react';
import { predictRisk, getModels } from '../services/api';
import { ShieldCheck, ShieldAlert, Loader2 } from 'lucide-react';

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
      setError(err.response?.data?.detail || "Unable to complete risk assessment.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-brand-dark">Risk Assessment</h1>
        <p className="text-gray-500 mt-1">Enter applicant details to generate an AI-driven risk evaluation.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue focus:border-brand-blue outline-none" required min="18" max="100"/>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Income ($)</label>
                <input type="number" name="income" value={formData.income} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue focus:border-brand-blue outline-none" required min="1"/>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Credit Score</label>
                <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue focus:border-brand-blue outline-none" required min="300" max="900"/>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Loan Amount ($)</label>
                <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue focus:border-brand-blue outline-none" required min="1"/>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Loan Term (Months)</label>
                <select name="loan_term_months" value={formData.loan_term_months} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue outline-none">
                  <option value="12">12</option><option value="24">24</option><option value="36">36</option>
                  <option value="48">48</option><option value="60">60</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Employment</label>
                <select name="employment_status" value={formData.employment_status} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue outline-none">
                  <option>Employed</option><option>Self-Employed</option><option>Unemployed</option>
                </select>
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">ML Model</label>
                <select name="model" value={formData.model} onChange={handleChange} className="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-blue outline-none bg-gray-50">
                  {models.map(m => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
            </div>
            
            <button type="submit" disabled={loading} className="w-full bg-brand-dark hover:bg-gray-800 text-white font-semibold py-3 rounded-xl transition flex justify-center items-center gap-2">
              {loading ? <><Loader2 className="animate-spin" size={20}/> Analyzing...</> : 'Predict Loan Risk'}
            </button>
          </form>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center items-center text-center min-h-[400px]">
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 w-full mb-4">
              {error}
            </div>
          )}
          
          {!result && !loading && !error && (
            <div className="text-gray-400">
              <ShieldCheck size={64} className="mx-auto mb-4 opacity-20"/>
              <p>Enter applicant details to generate a risk assessment.</p>
            </div>
          )}

          {result && !loading && (
            <div className="w-full animate-fade-in">
              <h3 className="text-sm font-bold tracking-widest text-gray-400 uppercase mb-6">Risk Assessment</h3>
              <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-full text-xl font-bold mb-8 ${result.risk_status === 'Low Risk' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {result.risk_status === 'Low Risk' ? <ShieldCheck size={28}/> : <ShieldAlert size={28}/>}
                {result.risk_status.toUpperCase()}
              </div>
              {result.probability && (
                <div className="mb-8">
                  <div className="text-5xl font-black text-brand-dark">{result.probability}%</div>
                  <div className="text-sm text-gray-500 mt-1">Prediction Confidence</div>
                </div>
              )}
              <div className="pt-6 border-t border-gray-100 flex justify-between items-center text-sm">
                <span className="text-gray-500">Model Used:</span>
                <span className="font-semibold text-brand-dark">{result.model_used}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
''',
    'src/pages/DataAnalysis.jsx': '''
import React from 'react';

export default function DataAnalysis() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-brand-dark">Data Analysis</h1>
      <p className="text-gray-500">Dataset statistics and insights.</p>
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 h-64 flex items-center justify-center">
         <p className="text-gray-400">Charts would render here via Recharts. Check the Visualizations page for static assets.</p>
      </div>
    </div>
  );
}
''',
    'src/pages/ModelPerformance.jsx': '''
import React, { useEffect, useState } from 'react';
import { getModelPerformance } from '../services/api';

export default function ModelPerformance() {
  const [perf, setPerf] = useState([]);

  useEffect(() => {
    getModelPerformance().then(setPerf).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-brand-dark">Machine Learning Model Performance</h1>
        <p className="text-gray-500 mt-1">Comparison of classification models used for loan risk prediction.</p>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-xl text-sm">
        <strong>Academic Disclaimer:</strong> Evaluation is based on a 100-record educational dataset with a 20-record test set. These results should not be interpreted as real-world financial performance.
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {perf.map((m, i) => (
          <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h3 className="font-bold text-lg text-brand-dark mb-4">{m.Model || 'Unknown Model'}</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span className="text-gray-500">Accuracy</span><span className="font-semibold">{m.Accuracy}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Precision</span><span className="font-semibold">{m.Precision}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">Recall</span><span className="font-semibold">{m.Recall}</span></div>
              <div className="flex justify-between"><span className="text-gray-500">F1 Score</span><span className="font-semibold">{m.F1_Score}</span></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
''',
    'src/pages/Visualizations.jsx': '''
import React from 'react';

export default function Visualizations() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-brand-dark">Visualizations</h1>
      <p className="text-gray-500">Pre-computed exploratory data analysis charts.</p>
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
         <p className="text-gray-500 mb-4">The static images from the backend visualizations directory should be served here or migrated to the frontend public folder.</p>
      </div>
    </div>
  );
}
''',
    'src/pages/About.jsx': '''
import React from 'react';

export default function About() {
  return (
    <div className="space-y-6 max-w-4xl">
      <h1 className="text-3xl font-bold text-brand-dark">About the Project</h1>
      
      <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 space-y-6 text-gray-600">
        <section>
          <h2 className="text-xl font-bold text-brand-dark mb-2">Project Overview</h2>
          <p>Loan Prediction Data Analysis System is built as a Data Analytics Essentials academic project. It uses machine learning to assess the default risk of loan applicants based on financial history.</p>
        </section>
        
        <section>
          <h2 className="text-xl font-bold text-brand-dark mb-2">Technology Stack</h2>
          <div className="flex flex-wrap gap-2">
            {['React', 'Vite', 'Tailwind CSS', 'FastAPI', 'Python', 'Scikit-learn', 'Pandas'].map(t => (
              <span key={t} className="px-3 py-1 bg-gray-100 rounded-full text-sm font-medium">{t}</span>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
''',
    'src/App.jsx': '''
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import RiskPrediction from './pages/RiskPrediction';
import DataAnalysis from './pages/DataAnalysis';
import ModelPerformance from './pages/ModelPerformance';
import Visualizations from './pages/Visualizations';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="predict" element={<RiskPrediction />} />
          <Route path="analysis" element={<DataAnalysis />} />
          <Route path="performance" element={<ModelPerformance />} />
          <Route path="visualizations" element={<Visualizations />} />
          <Route path="about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
'''
}

base_dir = os.path.join(os.getcwd(), 'frontend')
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\\n')

print("Frontend files scaffolded successfully.")
