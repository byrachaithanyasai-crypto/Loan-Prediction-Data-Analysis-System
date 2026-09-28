import os

files = {
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
    <div className="w-64 bg-white border-r border-brand-border h-screen fixed left-0 top-0 flex flex-col z-20 shadow-soft hidden md:flex">
      <div className="p-6 flex items-center gap-3 border-b border-slate-50">
        <Hexagon className="text-brand-blue fill-brand-blue/10" size={28} />
        <div>
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
      case '/about': return 'About';
      default: return '';
    }
  };

  return (
    <header className="h-16 bg-white border-b border-brand-border flex items-center justify-between px-8 sticky top-0 z-10 shadow-sm">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-bold text-brand-navy tracking-tight">{getPageTitle()}</h2>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2 text-xs font-bold px-3 py-1.5 bg-slate-50 rounded-full border border-slate-100 uppercase tracking-wider">
          <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className={isOnline ? 'text-emerald-700' : 'text-red-600'}>{isOnline ? 'API Connected' : 'Offline'}</span>
        </div>
      </div>
    </header>
  );
}
''',
    'src/pages/Dashboard.jsx': '''
import React, { useEffect, useState } from 'react';
import { getDashboardStats } from '../services/api';
import { Users, ShieldCheck, ShieldAlert, CreditCard, ArrowRight, PlayCircle, Layers, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

function StatCard({ title, value, icon: Icon, colorClass }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-start gap-4 transition-transform hover:-translate-y-1">
      <div className={`p-3 rounded-xl ${colorClass}`}>
        <Icon size={24} />
      </div>
      <div>
        <p className="text-sm font-semibold text-slate-500 mb-1">{title}</p>
        <p className="text-2xl font-black text-brand-navy">{value}</p>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboardStats().then(setStats).catch(console.error).finally(() => setLoading(false));
  }, []);

  const riskData = stats ? [
    { name: 'Low Risk', value: stats.low_risk, color: '#10b981' },
    { name: 'High Risk', value: stats.high_risk, color: '#ef4444' }
  ] : [];

  return (
    <div className="space-y-10 animate-fade-in pb-10">
      
      {/* HERO SECTION */}
      <div className="bg-brand-navy rounded-3xl p-10 shadow-lg flex flex-col lg:flex-row gap-10 items-center overflow-hidden relative">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-brand-blue/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 pointer-events-none"></div>
        <div className="flex-1 relative z-10 text-white">
          <h1 className="text-4xl lg:text-5xl font-black mb-4 tracking-tight leading-tight">Loan Risk Analytics <br/><span className="text-brand-blue">& Prediction</span></h1>
          <p className="text-lg text-slate-300 mb-8 max-w-xl font-medium">Evaluate loan applications with machine learning and explore data-driven risk insights.</p>
          <div className="flex gap-4">
            <Link to="/predict" className="bg-brand-blue hover:bg-blue-600 text-white px-7 py-3.5 rounded-xl font-bold transition flex items-center gap-2 shadow-md">
              Predict Loan Risk <ArrowRight size={18}/>
            </Link>
            <Link to="/analysis" className="bg-white/10 hover:bg-white/20 text-white px-7 py-3.5 rounded-xl font-bold transition border border-white/20">
              Explore Analytics
            </Link>
          </div>
        </div>
        <div className="w-full lg:w-[350px] relative z-10">
          <div className="bg-slate-900/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10 shadow-2xl">
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-6">Risk Intelligence</h3>
            {stats ? (
              <div className="space-y-5">
                <div className="flex justify-between items-center border-b border-white/5 pb-3">
                  <span className="text-slate-300 text-sm font-medium">Total Applications</span>
                  <span className="font-bold text-white">{stats.total_applicants}</span>
                </div>
                <div className="flex justify-between items-center border-b border-white/5 pb-3">
                  <span className="text-slate-300 text-sm font-medium">Low Risk</span>
                  <span className="font-bold text-emerald-400">{Math.round((stats.low_risk / stats.total_applicants) * 100)}%</span>
                </div>
                <div className="flex justify-between items-center border-b border-white/5 pb-3">
                  <span className="text-slate-300 text-sm font-medium">High Risk</span>
                  <span className="font-bold text-red-400">{Math.round((stats.high_risk / stats.total_applicants) * 100)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-slate-300 text-sm font-medium">Avg Credit Score</span>
                  <span className="font-bold text-white">{Math.round(stats.avg_credit_score)}</span>
                </div>
              </div>
            ) : (
              <div className="h-48 flex items-center justify-center text-slate-500 text-sm font-medium">No historical data available</div>
            )}
          </div>
        </div>
      </div>

      {/* KPI ROW */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
        <StatCard title="Total Applications" value={stats?.total_applicants || 'N/A'} icon={Users} colorClass="bg-blue-50 text-brand-blue" />
        <StatCard title="Low Risk" value={stats ? `${Math.round((stats.low_risk/stats.total_applicants)*100)}%` : 'N/A'} icon={ShieldCheck} colorClass="bg-emerald-50 text-emerald-600" />
        <StatCard title="High Risk" value={stats ? `${Math.round((stats.high_risk/stats.total_applicants)*100)}%` : 'N/A'} icon={ShieldAlert} colorClass="bg-red-50 text-red-600" />
        <StatCard title="Average Credit" value={stats ? Math.round(stats.avg_credit_score) : 'N/A'} icon={CreditCard} colorClass="bg-indigo-50 text-indigo-600" />
        <StatCard title="Average Income" value={stats ? `$${Math.round(stats.avg_income).toLocaleString()}` : 'N/A'} icon={Layers} colorClass="bg-amber-50 text-amber-600" />
      </div>
      
      {/* RISK ANALYTICS & ACTIONS */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Risk Analytics */}
        <div className="lg:col-span-2 bg-white rounded-2xl shadow-soft border border-brand-border p-8 flex flex-col md:flex-row gap-8 items-center">
          <div className="w-full md:w-1/2 h-64">
            <h3 className="font-bold text-brand-dark mb-4">Risk Distribution</h3>
            {stats && stats.total_applicants > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={riskData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value" stroke="none">
                    {riskData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-400 text-sm">No historical data available</div>
            )}
          </div>
          <div className="w-full md:w-1/2">
            <h3 className="font-bold text-brand-dark mb-4">Risk Profile</h3>
            {stats ? (
              <div className="space-y-4">
                 <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-sm text-slate-700">
                    <span className="font-bold text-brand-navy">Insight: </span>
                    High-risk applicants have a lower average credit score than low-risk applicants based on historical data.
                 </div>
                 <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-sm text-slate-700">
                    <span className="font-bold text-brand-navy">Volume: </span>
                    {stats.high_risk} applications flagged as high risk.
                 </div>
              </div>
            ) : (
              <div className="text-slate-400 text-sm">No historical data available</div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-2xl shadow-soft border border-brand-border p-8">
          <h3 className="font-bold text-brand-dark mb-6">Quick Actions</h3>
          <div className="space-y-4">
            <Link to="/predict" className="flex items-center gap-4 p-4 rounded-xl border border-slate-200 hover:border-brand-blue hover:shadow-md transition-all group">
              <div className="p-2.5 bg-blue-50 text-brand-blue rounded-lg"><PlayCircle size={20}/></div>
              <div>
                <div className="font-bold text-brand-navy text-sm">Predict Loan Risk</div>
                <div className="text-xs text-slate-500 font-medium">Evaluate an applicant</div>
              </div>
            </Link>
            <Link to="/analysis" className="flex items-center gap-4 p-4 rounded-xl border border-slate-200 hover:border-emerald-500 hover:shadow-md transition-all group">
              <div className="p-2.5 bg-emerald-50 text-emerald-600 rounded-lg"><Layers size={20}/></div>
              <div>
                <div className="font-bold text-brand-navy text-sm">Explore Data</div>
                <div className="text-xs text-slate-500 font-medium">Analyze applicant patterns</div>
              </div>
            </Link>
            <Link to="/performance" className="flex items-center gap-4 p-4 rounded-xl border border-slate-200 hover:border-indigo-500 hover:shadow-md transition-all group">
              <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-lg"><Settings size={20}/></div>
              <div>
                <div className="font-bold text-brand-navy text-sm">Compare Models</div>
                <div className="text-xs text-slate-500 font-medium">View evaluation metrics</div>
              </div>
            </Link>
          </div>
        </div>
      </div>
      
      {/* HOW IT WORKS */}
      <div className="mt-8">
        <h3 className="text-xl font-bold text-brand-dark mb-6">How It Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-slate-100 -z-10 -translate-y-1/2"></div>
          {[
            { step: '01', title: 'Enter Applicant Details', desc: 'Input financial & personal data.' },
            { step: '02', title: 'Select Model', desc: 'Choose a classification algorithm.' },
            { step: '03', title: 'Run Prediction', desc: 'Analyze data via API.' },
            { step: '04', title: 'Review Risk Result', desc: 'View probability & insights.' }
          ].map((s, i) => (
            <div key={i} className="bg-white border border-brand-border rounded-2xl p-6 text-center shadow-soft">
              <div className="w-12 h-12 bg-brand-navy text-white rounded-full flex items-center justify-center font-black text-lg mx-auto mb-4">{s.step}</div>
              <h4 className="font-bold text-brand-dark mb-2">{s.title}</h4>
              <p className="text-sm text-slate-500 font-medium">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
''',
    'src/pages/About.jsx': '''
import React from 'react';
import { Target, BarChart2, CheckCircle2, ShieldCheck, Cpu } from 'lucide-react';

export default function About() {
  return (
    <div className="space-y-10 max-w-6xl mx-auto animate-fade-in pb-10">
      
      <div className="text-center mb-12">
        <h1 className="text-4xl font-black text-brand-navy mb-4">About LoanPredict</h1>
        <p className="text-lg text-slate-500 max-w-2xl mx-auto font-medium">An intelligent platform for loan risk prediction, applicant analytics and machine learning model evaluation.</p>
      </div>

      {/* SECTION A - PRODUCT OVERVIEW */}
      <div className="bg-white p-10 rounded-2xl shadow-soft border border-brand-border">
        <h2 className="text-2xl font-bold text-brand-navy mb-4">Loan Prediction Data Analysis System</h2>
        <p className="text-slate-600 mb-8 max-w-3xl leading-relaxed text-lg">
          A machine-learning-powered analytics platform designed to evaluate loan applicant risk, analyze applicant data and compare classification models.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-5 bg-slate-50 rounded-xl border border-slate-100 font-bold text-brand-dark flex items-center gap-3"><ShieldCheck className="text-brand-blue"/> Risk Prediction</div>
          <div className="p-5 bg-slate-50 rounded-xl border border-slate-100 font-bold text-brand-dark flex items-center gap-3"><BarChart2 className="text-emerald-500"/> Data Analytics</div>
          <div className="p-5 bg-slate-50 rounded-xl border border-slate-100 font-bold text-brand-dark flex items-center gap-3"><Target className="text-indigo-500"/> Model Evaluation</div>
        </div>
      </div>

      {/* SECTION B - CORE CAPABILITIES */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        {[
          { title: 'Loan Risk Prediction', desc: 'Predict applicant risk levels', num: '01' },
          { title: 'Applicant Data Analysis', desc: 'Explore detailed data patterns', num: '02' },
          { title: 'ML Model Comparison', desc: 'Evaluate algorithm performance', num: '03' },
          { title: 'Interactive Visualizations', desc: 'Visual analytics dashboard', num: '04' },
          { title: 'Probability Assessment', desc: 'Confidence-based scoring', num: '05' }
        ].map(item => (
          <div key={item.num} className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex flex-col items-center text-center">
            <div className="text-3xl font-black text-slate-100 mb-3">{item.num}</div>
            <h3 className="font-bold text-brand-dark mb-2 text-sm">{item.title}</h3>
            <p className="text-xs text-slate-500 font-medium">{item.desc}</p>
          </div>
        ))}
      </div>

      {/* SECTION C - TECHNOLOGY */}
      <div className="bg-brand-navy text-white p-10 rounded-2xl shadow-lg w-full">
        <h2 className="text-xl font-bold mb-8 flex items-center gap-2"><Cpu size={24} className="text-brand-blue"/> Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div>
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 border-b border-slate-700 pb-2">Frontend</h3>
            <ul className="space-y-3 font-semibold text-slate-200">
              <li>React</li><li>Vite</li><li>Tailwind CSS</li><li>React Router</li><li>Axios</li><li>Recharts</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 border-b border-slate-700 pb-2">Backend</h3>
            <ul className="space-y-3 font-semibold text-slate-200">
              <li>FastAPI</li><li>Python</li><li>Pydantic</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4 border-b border-slate-700 pb-2">Data & ML</h3>
            <ul className="space-y-3 font-semibold text-slate-200">
              <li>Pandas</li><li>NumPy</li><li>Scikit-learn</li><li>Joblib</li>
            </ul>
          </div>
        </div>
      </div>

      {/* SECTION D - ARCHITECTURE */}
      <div className="bg-white p-10 rounded-2xl shadow-soft border border-brand-border">
        <h2 className="text-xl font-bold text-brand-navy mb-8">System Architecture</h2>
        <div className="flex flex-col md:flex-row items-center justify-between text-sm font-bold text-slate-700 gap-4">
          <div className="px-6 py-4 bg-blue-50 border border-blue-100 rounded-xl text-center w-full md:w-auto">React Frontend</div>
          <div className="text-slate-300 md:-rotate-90">↓</div>
          <div className="px-6 py-4 bg-emerald-50 border border-emerald-100 rounded-xl text-center w-full md:w-auto">FastAPI API Layer</div>
          <div className="text-slate-300 md:-rotate-90">↓</div>
          <div className="px-6 py-4 bg-indigo-50 border border-indigo-100 rounded-xl text-center w-full md:w-auto">Prediction Services</div>
          <div className="text-slate-300 md:-rotate-90">↓</div>
          <div className="px-6 py-4 bg-purple-50 border border-purple-100 rounded-xl text-center w-full md:w-auto">Machine Learning</div>
          <div className="text-slate-300 md:-rotate-90">↓</div>
          <div className="px-6 py-4 bg-amber-50 border border-amber-100 rounded-xl text-center w-full md:w-auto">Loan Dataset</div>
        </div>
      </div>

      {/* SECTION E - SYSTEM CAPABILITIES */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {[
          { t: 'Prediction Engine', d: 'Generate applicant-level risk predictions.' },
          { t: 'Analytics Engine', d: 'Explore patterns across applicant and financial data.' },
          { t: 'Model Evaluation', d: 'Compare classification models using standard evaluation metrics.' },
          { t: 'Visualization Layer', d: 'Understand data through interactive charts and visual analytics.' }
        ].map((item, idx) => (
          <div key={idx} className="p-6 bg-white border border-brand-border rounded-xl shadow-sm flex gap-4 items-start">
            <CheckCircle2 className="text-brand-low shrink-0"/>
            <div>
              <h4 className="font-bold text-brand-dark mb-1">{item.t}</h4>
              <p className="text-sm text-slate-500 font-medium">{item.d}</p>
            </div>
          </div>
        ))}
      </div>

      {/* SECTION F - PRODUCT INFO */}
      <div className="bg-slate-50 border border-slate-200 rounded-xl p-8 flex flex-col md:flex-row justify-between text-sm font-semibold text-slate-600 gap-6">
        <div><span className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Platform</span>LoanPredict</div>
        <div><span className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Application Type</span>Loan Risk Analytics & Prediction</div>
        <div><span className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-1">ML Models</span>3 Classification Models</div>
        <div><span className="block text-xs font-black text-slate-400 uppercase tracking-widest mb-1">Analytics</span>Applicant & Risk Analysis</div>
      </div>
    </div>
  );
}
''',
    'src/pages/ModelPerformance.jsx': '''
import React, { useEffect, useState } from 'react';
import { getEvaluationMetrics } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Info } from 'lucide-react';

export default function ModelPerformance() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEvaluationMetrics().then(setMetrics).catch(console.error).finally(() => setLoading(false));
  }, []);

  const chartData = metrics ? Object.keys(metrics).map(model => ({
    name: model,
    Accuracy: metrics[model].Accuracy * 100,
    Precision: metrics[model].Precision * 100,
    Recall: metrics[model].Recall * 100,
    'F1 Score': metrics[model]['F1 Score'] * 100,
  })) : [];

  return (
    <div className="space-y-10 animate-fade-in pb-10">
      <div>
        <h1 className="text-3xl font-black text-brand-navy mb-2">Model Performance</h1>
        <p className="text-slate-500 font-medium">Compare the performance of the trained machine learning models used for loan risk prediction.</p>
      </div>

      {loading ? (
        <div className="h-64 flex items-center justify-center text-slate-400 font-medium">Loading evaluation metrics...</div>
      ) : metrics ? (
        <>
          {/* TOP MODEL SUMMARY */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(metrics).map(([model, data]) => (
              <div key={model} className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border">
                <h3 className="font-bold text-brand-dark mb-4 text-lg border-b border-slate-100 pb-3">{model}</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center"><span className="text-slate-500 text-sm font-medium">Accuracy</span><span className="font-bold text-brand-navy">{(data.Accuracy * 100).toFixed(1)}%</span></div>
                  <div className="flex justify-between items-center"><span className="text-slate-500 text-sm font-medium">Precision</span><span className="font-bold text-brand-navy">{(data.Precision * 100).toFixed(1)}%</span></div>
                  <div className="flex justify-between items-center"><span className="text-slate-500 text-sm font-medium">Recall</span><span className="font-bold text-brand-navy">{(data.Recall * 100).toFixed(1)}%</span></div>
                  <div className="flex justify-between items-center"><span className="text-slate-500 text-sm font-medium">F1 Score</span><span className="font-bold text-brand-navy">{(data['F1 Score'] * 100).toFixed(1)}%</span></div>
                </div>
              </div>
            ))}
          </div>

          {/* MODEL COMPARISON CHART */}
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-navy mb-8">Metrics Comparison</h2>
            <div className="h-[400px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="name" tick={{fill: '#64748b', fontWeight: 600}} axisLine={false} tickLine={false} />
                  <YAxis tick={{fill: '#64748b'}} axisLine={false} tickLine={false} domain={[0, 100]} />
                  <RechartsTooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px -2px rgba(0,0,0,0.1)'}} />
                  <Legend iconType="circle" wrapperStyle={{paddingTop: '20px'}}/>
                  <Bar dataKey="Accuracy" fill="#1e293b" radius={[4,4,0,0]} />
                  <Bar dataKey="Precision" fill="#3b82f6" radius={[4,4,0,0]} />
                  <Bar dataKey="Recall" fill="#10b981" radius={[4,4,0,0]} />
                  <Bar dataKey="F1 Score" fill="#8b5cf6" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-center text-sm text-slate-500 mt-6 font-medium">Model metrics are calculated from the available evaluation dataset.</p>
          </div>
          
          {/* MODEL INSIGHTS */}
          <div className="bg-slate-50 p-8 rounded-2xl border border-slate-200">
            <h2 className="text-lg font-bold text-brand-navy mb-4 flex items-center gap-2"><Activity size={20} className="text-brand-blue"/> Model Insights</h2>
            <div className="space-y-3 text-sm text-slate-700 font-medium">
              <p>Random Forest achieved the highest F1 score among the evaluated models, indicating a strong balance between precision and recall for loan risk classification.</p>
            </div>
          </div>
        </>
      ) : (
        <div className="h-64 flex items-center justify-center text-slate-400 font-medium">No historical data available</div>
      )}

      {/* DISCLAIMER */}
      <div className="flex items-start gap-3 p-4 bg-slate-100 rounded-xl border border-slate-200 text-xs font-semibold text-slate-500">
        <Info size={16} className="shrink-0 text-slate-400" />
        <p>Evaluation metrics are based on the available educational dataset and test set and should not be interpreted as real-world financial performance.</p>
      </div>
    </div>
  );
}
''',
    'src/pages/RiskPrediction.jsx': '''
import React, { useState, useEffect } from 'react';
import { predictRisk } from '../services/api';
import { ShieldCheck, ShieldAlert, Loader2, AlertCircle, History, Trash2 } from 'lucide-react';

export default function RiskPrediction() {
  const [formData, setFormData] = useState({
    age: 35, income: 75000, credit_score: 650, 
    loan_amount: 20000, loan_term_months: 36, 
    employment_status: 'Employed', model: 'Random Forest'
  });
  const models = ['Random Forest', 'Logistic Regression', 'Decision Tree'];
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('loanpredict_history');
    if (saved) setHistory(JSON.parse(saved));
  }, []);

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

  const saveHistory = (res) => {
    const newEntry = {
      time: new Date().toLocaleTimeString(),
      model: formData.model,
      risk: res.risk_status,
      probability: res.probability
    };
    const newHistory = [newEntry, ...history].slice(0, 5);
    setHistory(newHistory);
    localStorage.setItem('loanpredict_history', JSON.stringify(newHistory));
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('loanpredict_history');
  };

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
      if (res.error) throw new Error(res.error);
      setResult(res);
      saveHistory(res);
    } catch (err) {
      console.error(err);
      setError("Unable to generate the prediction. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-10">
      <div>
        <h1 className="text-3xl font-black text-brand-navy mb-2">Loan Risk Prediction</h1>
        <p className="text-slate-500 font-medium">Evaluate an applicant using trained machine learning models.</p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        {/* LEFT COLUMN: FORM */}
        <div className="xl:col-span-2 space-y-6">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <form onSubmit={handleSubmit} className="space-y-8">
              
              <div>
                <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase mb-5 pb-2 border-b border-slate-100">Financial Details</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Annual Income ($)</label>
                    <input type="number" name="income" value={formData.income} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium" required min="1"/>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Credit Score</label>
                    <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium" required min="300" max="900"/>
                    <p className="text-xs text-slate-400 mt-2 font-medium">Range: 300–900</p>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Loan Amount ($)</label>
                    <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium" required min="1"/>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Loan Term (Months)</label>
                    <select name="loan_term_months" value={formData.loan_term_months} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium">
                      <option value="12">12</option><option value="24">24</option><option value="36">36</option>
                      <option value="48">48</option><option value="60">60</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase mb-5 pb-2 border-b border-slate-100">Personal Details</h3>
                  <label className="block text-sm font-bold text-brand-navy mb-2">Age</label>
                  <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium" required min="18" max="100"/>
                </div>
                <div>
                  <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase mb-5 pb-2 border-b border-slate-100">Employment</h3>
                  <label className="block text-sm font-bold text-brand-navy mb-2">Status</label>
                  <select name="employment_status" value={formData.employment_status} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-medium">
                    <option>Employed</option><option>Self-Employed</option><option>Unemployed</option>
                  </select>
                </div>
              </div>

              <div>
                <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase mb-5 pb-2 border-b border-slate-100">Model Selection</h3>
                <select name="model" value={formData.model} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/20 focus:border-brand-blue transition-all outline-none font-bold text-brand-navy">
                  {models.map(m => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
              
              <button type="submit" disabled={loading} className="w-full bg-brand-navy hover:bg-slate-800 text-white font-bold py-4 rounded-xl shadow-md transition-all flex justify-center items-center gap-3 text-lg">
                {loading ? <><Loader2 className="animate-spin" size={24}/> Analyzing applicant...</> : 'Analyze Loan Risk'}
              </button>
            </form>
          </div>

          {/* Local History */}
          {history.length > 0 && (
            <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border animate-fade-in">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-sm font-bold text-brand-navy flex items-center gap-2"><History size={18}/> Recent Predictions</h3>
                <button onClick={clearHistory} className="text-xs font-bold text-slate-400 hover:text-red-500 transition-colors flex items-center gap-1"><Trash2 size={14}/> Clear</button>
              </div>
              <div className="space-y-3">
                {history.map((h, i) => (
                  <div key={i} className="flex justify-between items-center p-3 bg-slate-50 rounded-lg border border-slate-100 text-sm font-medium">
                    <span className="text-slate-500">{h.time}</span>
                    <span className="text-brand-navy">{h.model}</span>
                    <span className={`px-2 py-1 rounded font-bold text-xs ${h.risk === 'Low Risk' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>{h.risk}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: RESULT */}
        <div className="xl:col-span-1">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border sticky top-24 min-h-[500px] flex flex-col">
            <h3 className="text-xs font-black tracking-widest text-slate-400 uppercase mb-6 pb-2 border-b border-slate-100">Risk Assessment</h3>
            
            {error && (
              <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 flex items-start gap-3 animate-fade-in mb-4">
                <AlertCircle size={20} className="shrink-0 mt-0.5" />
                <p className="text-sm font-bold">{error}</p>
              </div>
            )}
            
            {!result && !loading && !error && (
              <div className="flex-1 flex flex-col justify-center items-center text-center px-4 animate-fade-in">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                  <ShieldCheck size={28} className="text-slate-300"/>
                </div>
                <h4 className="text-lg font-bold text-brand-navy mb-2">Ready for Analysis</h4>
                <p className="text-slate-500 text-sm font-medium">Enter applicant details and run the selected model.</p>
              </div>
            )}

            {result && !loading && (
              <div className="flex-1 flex flex-col animate-fade-in">
                <div className="text-center mb-8">
                  <div className={`inline-flex items-center gap-2 px-6 py-2 rounded-full text-sm font-black tracking-widest mb-6 uppercase ${result.risk_status === 'Low Risk' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                    {result.risk_status === 'Low Risk' ? <ShieldCheck size={18}/> : <ShieldAlert size={18}/>}
                    {result.risk_status}
                  </div>
                  
                  {result.probability != null && (
                    <div className="relative w-48 h-48 mx-auto flex items-center justify-center mb-2">
                      <svg className="absolute w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                        <circle cx="50" cy="50" r="45" fill="none" stroke={result.risk_status === 'Low Risk' ? '#10b981' : '#ef4444'} strokeWidth="8" strokeDasharray={`${result.probability * 2.82} 282`} strokeLinecap="round" className="transition-all duration-1000 ease-out" />
                      </svg>
                      <div className="flex flex-col items-center">
                        <span className="text-4xl font-black text-brand-navy">{result.probability}%</span>
                        <span className="text-[10px] uppercase font-bold text-slate-400 mt-1 tracking-widest">Probability</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-4 bg-slate-50 p-6 rounded-xl border border-slate-100 mb-6 flex-1">
                  <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3">Input Snapshot</h4>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-medium">Model Used</span><span className="font-bold text-brand-navy">{result.model_used || formData.model}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-medium">Credit Score</span><span className="font-bold text-brand-navy">{formData.credit_score}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-medium">Income</span><span className="font-bold text-brand-navy">${formData.income}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-medium">Loan Amount</span><span className="font-bold text-brand-navy">${formData.loan_amount}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-medium">Employment</span><span className="font-bold text-brand-navy">{formData.employment_status}</span></div>
                </div>

                <div>
                  <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Risk Interpretation</h4>
                  <p className="text-sm text-slate-600 bg-white p-4 border border-slate-200 rounded-lg font-medium leading-relaxed">
                    The selected model classified this application as <strong className={result.risk_status === 'Low Risk' ? 'text-emerald-600' : 'text-red-600'}>{result.risk_status.toLowerCase()}</strong> based on the supplied applicant features.
                  </p>
                </div>
                
                <button onClick={() => setResult(null)} className="mt-6 w-full py-3 border border-slate-200 text-brand-navy rounded-xl hover:bg-slate-50 font-bold transition text-sm">
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
'''
}

base_dir = os.path.join(os.getcwd(), 'frontend')
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        # Crucial to use '\\n' without escaping it if interpreted literally,
        # but in Python literal strings `\n` is safe.
        f.write(content.strip() + '\n')

print("FinTech UI v3 updated successfully.")
