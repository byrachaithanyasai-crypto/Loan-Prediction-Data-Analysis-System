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
    <div className="space-y-8 animate-fade-in pb-16 max-w-7xl mx-auto">
      <div>
        <h1 className="text-3xl font-black text-brand-navy mb-2 tracking-tight">Loan Risk Prediction</h1>
        <p className="text-slate-600 font-medium">Evaluate an applicant using trained machine learning models.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* LEFT COLUMN: FORM */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-slate-200">
            <form onSubmit={handleSubmit} className="space-y-8">
              
              <div>
                <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase mb-5 pb-3 border-b border-slate-100">Financial Details</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Annual Income ($)</label>
                    <input type="number" name="income" value={formData.income} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-medium text-brand-navy" required min="1"/>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Credit Score</label>
                    <input type="number" name="credit_score" value={formData.credit_score} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-medium text-brand-navy" required min="300" max="900"/>
                    <p className="text-[11px] font-bold text-slate-400 mt-2 uppercase tracking-wide">Range: 300–900</p>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Loan Amount ($)</label>
                    <input type="number" name="loan_amount" value={formData.loan_amount} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-medium text-brand-navy" required min="1"/>
                  </div>
                  <div>
                    <label className="block text-sm font-bold text-brand-navy mb-2">Loan Term (Months)</label>
                    <select name="loan_term_months" value={formData.loan_term_months} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-bold text-brand-navy">
                      <option value="12">12</option><option value="24">24</option><option value="36">36</option>
                      <option value="48">48</option><option value="60">60</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase mb-5 pb-3 border-b border-slate-100">Personal Details</h3>
                  <label className="block text-sm font-bold text-brand-navy mb-2">Age</label>
                  <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-medium text-brand-navy" required min="18" max="100"/>
                </div>
                <div>
                  <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase mb-5 pb-3 border-b border-slate-100">Employment</h3>
                  <label className="block text-sm font-bold text-brand-navy mb-2">Status</label>
                  <select name="employment_status" value={formData.employment_status} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-bold text-brand-navy">
                    <option>Employed</option><option>Self-Employed</option><option>Unemployed</option>
                  </select>
                </div>
              </div>

              <div>
                <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase mb-5 pb-3 border-b border-slate-100">Model Selection</h3>
                <select name="model" value={formData.model} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all outline-none font-bold text-brand-navy">
                  {models.map(m => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
              
              <button type="submit" disabled={loading} className="w-full bg-brand-navy hover:bg-slate-800 text-white font-black py-4 rounded-xl shadow-md transition-all flex justify-center items-center gap-3 text-lg tracking-wide">
                {loading ? <><Loader2 className="animate-spin" size={24}/> Analyzing applicant...</> : 'Analyze Loan Risk'}
              </button>
            </form>
          </div>

          {/* Local History */}
          {history.length > 0 && (
            <div className="bg-white p-6 rounded-2xl shadow-soft border border-slate-200 animate-fade-in">
              <div className="flex justify-between items-center mb-4 border-b border-slate-100 pb-3">
                <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase flex items-center gap-2"><History size={14}/> Recent Predictions</h3>
                <button onClick={clearHistory} className="text-[10px] font-black uppercase tracking-widest text-slate-400 hover:text-red-500 transition-colors flex items-center gap-1"><Trash2 size={12}/> Clear</button>
              </div>
              <div className="space-y-2">
                {history.map((h, i) => (
                  <div key={i} className="flex justify-between items-center px-4 py-3 bg-slate-50 rounded-lg border border-slate-100 text-sm font-medium">
                    <span className="text-slate-400 text-xs font-bold">{h.time}</span>
                    <span className="text-brand-navy font-bold">{h.model}</span>
                    <span className={`px-2 py-1 rounded font-black text-[10px] uppercase tracking-widest ${h.risk === 'Low Risk' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>{h.risk}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: RESULT */}
        <div className="lg:col-span-5">
          <div className="bg-white p-8 rounded-2xl shadow-soft border border-slate-200 sticky top-24 flex flex-col">
            <h3 className="text-[11px] font-black tracking-widest text-slate-400 uppercase mb-8 pb-3 border-b border-slate-100">Risk Assessment</h3>
            
            {error && (
              <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 flex items-start gap-3 animate-fade-in mb-4">
                <AlertCircle size={20} className="shrink-0 mt-0.5" />
                <p className="text-sm font-bold leading-relaxed">{error}</p>
              </div>
            )}
            
            {!result && !loading && !error && (
              <div className="py-16 flex flex-col justify-center items-center text-center px-4 animate-fade-in">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-6">
                  <ShieldCheck size={28} className="text-slate-300"/>
                </div>
                <h4 className="text-lg font-bold text-brand-navy mb-2">Ready for Analysis</h4>
                <p className="text-slate-500 text-sm font-medium max-w-[200px]">Enter applicant details and run the selected model.</p>
              </div>
            )}

            {result && !loading && (
              <div className="flex flex-col animate-fade-in">
                <div className="text-center mb-8">
                  <div className={`inline-flex items-center gap-2 px-6 py-2 rounded-full text-sm font-black tracking-widest mb-8 uppercase shadow-sm ${result.risk_status === 'Low Risk' ? 'bg-emerald-50 border border-emerald-200 text-emerald-700' : 'bg-red-50 border border-red-200 text-red-700'}`}>
                    {result.risk_status === 'Low Risk' ? <ShieldCheck size={18}/> : <ShieldAlert size={18}/>}
                    {result.risk_status}
                  </div>
                  
                  {result.probability != null && (
                    <div className="relative w-48 h-48 mx-auto flex items-center justify-center mb-4">
                      <svg className="absolute w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="46" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                        <circle cx="50" cy="50" r="46" fill="none" stroke={result.risk_status === 'Low Risk' ? '#10b981' : '#ef4444'} strokeWidth="8" strokeDasharray={`${result.probability * 2.89} 289`} strokeLinecap="round" className="transition-all duration-1000 ease-out" />
                      </svg>
                      <div className="flex flex-col items-center">
                        <span className="text-5xl font-black text-brand-navy tracking-tighter">{result.probability}%</span>
                        <span className="text-[10px] uppercase font-black text-slate-400 mt-1 tracking-widest">Probability</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-4 bg-slate-50 p-6 rounded-xl border border-slate-100 mb-8">
                  <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Input Snapshot</h4>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Model Used</span><span className="font-black text-brand-navy">{result.model_used || formData.model}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Credit Score</span><span className="font-black text-brand-navy">{formData.credit_score}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Annual Income</span><span className="font-black text-brand-navy">${formData.income}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Loan Amount</span><span className="font-black text-brand-navy">${formData.loan_amount}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Loan Term</span><span className="font-black text-brand-navy">{formData.loan_term_months} mos</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500 font-bold">Employment</span><span className="font-black text-brand-navy">{formData.employment_status}</span></div>
                </div>

                <div>
                  <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3">Risk Interpretation</h4>
                  <p className="text-sm text-slate-600 font-medium leading-relaxed bg-white border border-slate-200 p-4 rounded-lg">
                    The selected model classified this application as <strong className={result.risk_status === 'Low Risk' ? 'text-emerald-600 font-black' : 'text-red-600 font-black'}>{result.risk_status.toLowerCase()}</strong> based on the supplied applicant features.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
