import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, AlertTriangle, CheckCircle, DollarSign } from 'lucide-react';
import axios from 'axios';

const PIE_COLORS = ['#3b82f6', '#8b5cf6', '#f43f5e'];

export default function DataAnalysis() {
  const [stats, setStats] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      axios.get('http://127.0.0.1:8000/api/dashboard/stats').then(res => res.data),
      axios.get('http://127.0.0.1:8000/api/analysis/summary').then(res => res.data)
    ]).then(([statsData, summaryData]) => {
      setStats(statsData);
      setSummary(summaryData);
      setLoading(false);
    }).catch(console.error);
  }, []);

  if (loading) {
    return <div className="h-64 flex items-center justify-center text-slate-400 font-medium">Loading analysis data...</div>;
  }

  return (
    <div className="space-y-8 animate-fade-in pb-10">
      <div>
        <h1 className="text-3xl font-black text-brand-navy mb-2">Data Analysis Dashboard</h1>
        <p className="text-slate-500 font-medium">Interactive dataset insights and statistical summaries.</p>
      </div>

      {stats && !stats.error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-center gap-4">
            <div className="p-4 rounded-xl bg-blue-50 text-blue-600"><Users size={24}/></div>
            <div>
              <p className="text-sm font-semibold text-slate-500">Total Applicants</p>
              <h3 className="text-2xl font-black text-brand-navy">{stats.total_applicants}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-center gap-4">
            <div className="p-4 rounded-xl bg-emerald-50 text-emerald-600"><CheckCircle size={24}/></div>
            <div>
              <p className="text-sm font-semibold text-slate-500">Low Risk</p>
              <h3 className="text-2xl font-black text-brand-navy">{stats.low_risk}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-center gap-4">
            <div className="p-4 rounded-xl bg-rose-50 text-rose-600"><AlertTriangle size={24}/></div>
            <div>
              <p className="text-sm font-semibold text-slate-500">High Risk</p>
              <h3 className="text-2xl font-black text-brand-navy">{stats.high_risk}</h3>
            </div>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-soft border border-brand-border flex items-center gap-4">
            <div className="p-4 rounded-xl bg-amber-50 text-amber-600"><DollarSign size={24}/></div>
            <div>
              <p className="text-sm font-semibold text-slate-500">Avg Income</p>
              <h3 className="text-2xl font-black text-brand-navy">${stats.avg_income ? stats.avg_income.toLocaleString() : 0}</h3>
            </div>
          </div>
        </div>
      )}

      {summary && !summary.error && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-navy mb-6">Employment Distribution</h2>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={summary.employment_distribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={70}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label
                  >
                    {summary.employment_distribution && summary.employment_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px -2px rgba(0,0,0,0.1)'}} />
                  <Legend iconType="circle" verticalAlign="bottom"/>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-soft border border-brand-border">
            <h2 className="text-xl font-bold text-brand-navy mb-6">Risk by Income Group</h2>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={summary.risk_by_income} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="bucket" tick={{fill: '#64748b', fontWeight: 600}} axisLine={false} tickLine={false} />
                  <YAxis tick={{fill: '#64748b'}} axisLine={false} tickLine={false} />
                  <RechartsTooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px -2px rgba(0,0,0,0.1)'}} />
                  <Legend iconType="circle" wrapperStyle={{paddingTop: '20px'}}/>
                  <Bar dataKey="Low Risk" fill="#10b981" radius={[4,4,0,0]} stackId="a" />
                  <Bar dataKey="High Risk" fill="#ef4444" radius={[4,4,0,0]} stackId="a" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
