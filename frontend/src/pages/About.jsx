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
              <span className="text-4xl font-black text-slate-400">01</span>
            </div>
            <h3 className="text-lg font-bold text-brand-navy mb-3">Risk Prediction</h3>
            <p className="text-sm text-slate-600 font-medium">Evaluate applicant risk using trained classification models.</p>
          </div>
          <div className="p-8 bg-white rounded-2xl shadow-soft border border-slate-200 hover:border-emerald-500/30 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl"><BarChart2 size={24}/></div>
              <span className="text-4xl font-black text-slate-400">02</span>
            </div>
            <h3 className="text-lg font-bold text-brand-navy mb-3">Data Analytics</h3>
            <p className="text-sm text-slate-600 font-medium">Explore financial and applicant-level patterns.</p>
          </div>
          <div className="p-8 bg-white rounded-2xl shadow-soft border border-slate-200 hover:border-indigo-500/30 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl"><Target size={24}/></div>
              <span className="text-4xl font-black text-slate-400">03</span>
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
