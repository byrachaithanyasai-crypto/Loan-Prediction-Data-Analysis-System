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
                  <span className="font-bold text-emerald-400">{stats.low_risk} <span className="text-xs text-emerald-400/70 font-normal">({stats.total_applicants > 0 ? Math.round((stats.low_risk / stats.total_applicants) * 100) : 0}%)</span></span>
                </div>
                <div className="flex justify-between items-center border-b border-white/5 pb-3">
                  <span className="text-slate-300 text-sm font-medium">High Risk</span>
                  <span className="font-bold text-red-400">{stats.high_risk} <span className="text-xs text-red-400/70 font-normal">({stats.total_applicants > 0 ? Math.round((stats.high_risk / stats.total_applicants) * 100) : 0}%)</span></span>
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
        <StatCard title="Total Applications" value={stats ? stats.total_applicants : 'N/A'} icon={Users} colorClass="bg-blue-50 text-brand-blue" />
        <StatCard title="Low Risk" value={stats ? stats.low_risk : 'N/A'} icon={ShieldCheck} colorClass="bg-emerald-50 text-emerald-600" />
        <StatCard title="High Risk" value={stats ? stats.high_risk : 'N/A'} icon={ShieldAlert} colorClass="bg-red-50 text-red-600" />
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
