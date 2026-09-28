import os

files = {
    'src/pages/About.jsx': '''
import React from 'react';
import { Target, BarChart2, CheckCircle2, ShieldCheck, Cpu } from 'lucide-react';

export default function About() {
  return (
    <div className="space-y-12 max-w-6xl mx-auto animate-fade-in pb-16">
      
      {/* HERO SECTION */}
      <div className="bg-gradient-to-br from-brand-navy to-slate-800 text-white rounded-[24px] p-12 shadow-2xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-[400px] h-[400px] bg-brand-blue/20 rounded-full blur-3xl -translate-y-1/3 translate-x-1/3 pointer-events-none"></div>
        <div className="relative z-10 flex justify-between items-center">
          <div className="max-w-2xl">
            <span className="inline-block text-[10px] font-black tracking-widest uppercase text-slate-400 mb-4 border border-slate-700 bg-slate-800/50 px-3 py-1 rounded-full">
              LoanPredict Platform
            </span>
            <h1 className="text-4xl md:text-5xl font-black mb-6 leading-tight tracking-tight text-white">
              Loan Prediction Data Analysis System
            </h1>
            <p className="text-lg text-slate-300 mb-8 font-medium max-w-xl">
              An intelligent machine-learning platform for loan risk prediction, applicant analytics and model evaluation.
            </p>
            <div className="flex gap-4">
              <span className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-xs font-bold uppercase tracking-wider text-white">AI-Powered Risk Analysis</span>
              <span className="px-4 py-2 bg-white/10 border border-white/20 rounded-lg text-xs font-bold uppercase tracking-wider text-white">Machine Learning Analytics</span>
            </div>
          </div>
          <div className="hidden lg:flex flex-col items-center justify-center relative w-64 h-64 border border-white/10 rounded-full bg-white/5">
            <svg className="w-48 h-48 absolute animate-[spin_60s_linear_infinite]" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="48" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" strokeDasharray="4 4" />
            </svg>
            <ShieldCheck size={64} className="text-brand-blue drop-shadow-[0_0_15px_rgba(37,99,235,0.5)]" />
          </div>
        </div>
      </div>

      {/* SECTION 1 - PLATFORM OVERVIEW */}
      <div className="space-y-6">
        <h2 className="text-2xl font-black text-brand-navy tracking-tight">Built for Intelligent Loan Risk Analysis</h2>
        <p className="text-lg text-slate-600 font-medium max-w-3xl mb-8">
          LoanPredict combines applicant data analysis, machine learning models and interactive analytics to evaluate loan risk and support data-driven analysis.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-8 bg-white rounded-2xl shadow-soft border border-slate-200 hover:border-brand-blue/30 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-blue-50 text-brand-blue rounded-xl"><ShieldCheck size={24}/></div>
              <span className="text-4xl font-black text-slate-100">01</span>
            </div>
            <h3 className="text-lg font-bold text-brand-navy mb-3">Risk Prediction</h3>
            <p className="text-sm text-slate-600 font-medium">Evaluate applicant risk using trained classification models.</p>
          </div>
          <div className="p-8 bg-white rounded-2xl shadow-soft border border-slate-200 hover:border-emerald-500/30 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl"><BarChart2 size={24}/></div>
              <span className="text-4xl font-black text-slate-100">02</span>
            </div>
            <h3 className="text-lg font-bold text-brand-navy mb-3">Data Analytics</h3>
            <p className="text-sm text-slate-600 font-medium">Explore financial and applicant-level patterns.</p>
          </div>
          <div className="p-8 bg-white rounded-2xl shadow-soft border border-slate-200 hover:border-indigo-500/30 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl"><Target size={24}/></div>
              <span className="text-4xl font-black text-slate-100">03</span>
            </div>
            <h3 className="text-lg font-bold text-brand-navy mb-3">Model Evaluation</h3>
            <p className="text-sm text-slate-600 font-medium">Compare classification models using standard metrics.</p>
          </div>
        </div>
      </div>

      {/* SECTION 2 - CORE CAPABILITIES */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {['Loan Risk Prediction', 'Applicant Data Analysis', 'Risk Probability Assessment', 'Model Comparison', 'Interactive Visualizations', 'Financial Analytics'].map((t, i) => (
          <div key={i} className="flex items-center gap-3 p-5 bg-white border border-slate-200 rounded-xl shadow-sm">
            <CheckCircle2 size={20} className="text-emerald-500 shrink-0" />
            <span className="text-sm font-bold text-brand-navy">{t}</span>
          </div>
        ))}
      </div>

      {/* SECTION 3 - TECHNOLOGY STACK */}
      <div className="bg-slate-50 border border-slate-200 rounded-[24px] p-10 w-full">
        <h2 className="text-2xl font-black text-brand-navy mb-2">Technology Stack</h2>
        <p className="text-slate-600 font-medium mb-10">Built with modern tools across the frontend, backend and machine learning layers.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-4">Frontend</h3>
            <div className="flex flex-wrap gap-2">
              {['React', 'Vite', 'Tailwind CSS', 'React Router', 'Axios', 'Recharts'].map(t => (
                <span key={t} className="px-3 py-1.5 bg-white border border-slate-200 rounded-md text-xs font-bold text-slate-700 shadow-sm">{t}</span>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-4">Backend</h3>
            <div className="flex flex-wrap gap-2">
              {['FastAPI', 'Python', 'Pydantic'].map(t => (
                <span key={t} className="px-3 py-1.5 bg-white border border-slate-200 rounded-md text-xs font-bold text-slate-700 shadow-sm">{t}</span>
              ))}
            </div>
          </div>
          <div>
            <h3 className="text-[11px] font-black text-slate-400 uppercase tracking-widest mb-4">Machine Learning & Data</h3>
            <div className="flex flex-wrap gap-2">
              {['Pandas', 'NumPy', 'Scikit-learn', 'Joblib'].map(t => (
                <span key={t} className="px-3 py-1.5 bg-white border border-slate-200 rounded-md text-xs font-bold text-slate-700 shadow-sm">{t}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* SECTION 4 - SYSTEM ARCHITECTURE */}
      <div className="bg-white p-10 rounded-[24px] shadow-soft border border-slate-200">
        <h2 className="text-xl font-black text-brand-navy mb-8 text-center">System Architecture</h2>
        <div className="flex flex-col lg:flex-row items-center justify-between gap-3 text-[11px] font-black uppercase tracking-wider text-slate-700">
          <div className="px-6 py-4 bg-slate-50 border border-slate-200 rounded-lg text-center w-full lg:w-40 shadow-sm">User</div>
          <div className="text-brand-blue lg:-rotate-90 text-lg">↓</div>
          <div className="px-6 py-4 bg-blue-50 border border-blue-200 rounded-lg text-center w-full lg:w-48 shadow-sm">React Frontend</div>
          <div className="text-brand-blue lg:-rotate-90 text-lg">↓</div>
          <div className="px-6 py-4 bg-indigo-50 border border-indigo-200 rounded-lg text-center w-full lg:w-48 shadow-sm">FastAPI API Layer</div>
          <div className="text-brand-blue lg:-rotate-90 text-lg">↓</div>
          <div className="px-6 py-4 bg-purple-50 border border-purple-200 rounded-lg text-center w-full lg:w-56 shadow-sm">Prediction & Analytics Engine</div>
          <div className="text-brand-blue lg:-rotate-90 text-lg">↓</div>
          <div className="px-6 py-4 bg-emerald-50 border border-emerald-200 rounded-lg text-center w-full lg:w-56 shadow-sm">Machine Learning Models</div>
          <div className="text-brand-blue lg:-rotate-90 text-lg">↓</div>
          <div className="px-6 py-4 bg-amber-50 border border-amber-200 rounded-lg text-center w-full lg:w-48 shadow-sm">Loan Dataset</div>
        </div>
      </div>

      {/* SECTION 5 - HOW IT WORKS */}
      <div className="space-y-6">
        <h2 className="text-xl font-black text-brand-navy">How the Platform Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {[
            { step: '01', title: 'Enter Applicant Details' },
            { step: '02', title: 'Select Prediction Model' },
            { step: '03', title: 'Run Risk Analysis' },
            { step: '04', title: 'Review Prediction & Analytics' }
          ].map((s, i) => (
            <div key={i} className="bg-white border border-slate-200 rounded-xl p-6 text-center shadow-sm hover:shadow-md transition-shadow">
              <div className="text-2xl font-black text-brand-blue mb-3">{s.step}</div>
              <h4 className="text-sm font-bold text-brand-navy">{s.title}</h4>
            </div>
          ))}
        </div>
      </div>

      {/* SECTION 6 - PLATFORM HIGHLIGHTS */}
      <div className="bg-brand-navy text-white rounded-[24px] overflow-hidden flex flex-col md:flex-row shadow-lg">
        <div className="p-10 md:w-1/2 flex flex-col justify-center border-b md:border-b-0 md:border-r border-white/10">
          <h2 className="text-2xl font-black mb-2 text-white">One Platform.</h2>
          <h2 className="text-2xl font-black text-brand-blue">Multiple Analytics Capabilities.</h2>
        </div>
        <div className="p-10 md:w-1/2 grid grid-cols-2 gap-6 bg-slate-800">
          <div className="flex flex-col gap-1">
            <span className="text-3xl font-black text-white">3</span>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">ML Classification Models</span>
          </div>
          <div className="flex flex-col gap-1 justify-center">
            <span className="text-sm font-bold text-white flex items-center gap-2"><ShieldCheck size={16} className="text-brand-blue"/> Risk Prediction</span>
          </div>
          <div className="flex flex-col gap-1 justify-center">
            <span className="text-sm font-bold text-white flex items-center gap-2"><BarChart2 size={16} className="text-emerald-400"/> Data Analytics</span>
          </div>
          <div className="flex flex-col gap-1 justify-center">
            <span className="text-sm font-bold text-white flex items-center gap-2"><Target size={16} className="text-indigo-400"/> Interactive Visualizations</span>
          </div>
        </div>
      </div>

      {/* SECTION 7 - PRODUCT INFORMATION */}
      <div className="bg-white border border-slate-200 rounded-xl p-8 grid grid-cols-2 md:grid-cols-6 gap-6 text-sm">
        <div className="col-span-1"><span className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Product</span><span className="font-bold text-brand-navy">LoanPredict</span></div>
        <div className="col-span-2"><span className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">System</span><span className="font-bold text-brand-navy">Loan Prediction Data Analysis System</span></div>
        <div className="col-span-1"><span className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Frontend</span><span className="font-bold text-brand-navy">React + Vite</span></div>
        <div className="col-span-1"><span className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Backend</span><span className="font-bold text-brand-navy">FastAPI + Python</span></div>
        <div className="col-span-1"><span className="block text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">ML</span><span className="font-bold text-brand-navy">Scikit-learn</span></div>
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
'''
}

base_dir = os.path.join(os.getcwd(), 'frontend')
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

print("FinTech UI v4 updated successfully.")
