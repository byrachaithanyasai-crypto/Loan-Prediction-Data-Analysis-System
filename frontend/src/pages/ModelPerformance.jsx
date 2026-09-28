import React, { useEffect, useState } from 'react';
import { getModelPerformance } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import { Activity, Info } from 'lucide-react';

export default function ModelPerformance() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModelPerformance().then(setMetrics).catch(console.error).finally(() => setLoading(false));
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
