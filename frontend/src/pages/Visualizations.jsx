import React from 'react';

export default function Visualizations() {
  const images = [
    { title: 'Risk Distribution', src: '/visualizations/risk_distribution.png' },
    { title: 'Credit Score Distribution', src: '/visualizations/credit_score_distribution.png' },
    { title: 'Credit Score vs Risk', src: '/visualizations/credit_score_vs_risk.png' },
    { title: 'Income Distribution', src: '/visualizations/income_distribution.png' },
    { title: 'Income vs Risk', src: '/visualizations/income_vs_risk.png' },
    { title: 'Loan Amount Distribution', src: '/visualizations/loan_amount_distribution.png' },
    { title: 'Loan Amount vs Risk', src: '/visualizations/loan_amount_vs_risk.png' },
    { title: 'Age Distribution', src: '/visualizations/age_distribution.png' },
    { title: 'Age vs Risk', src: '/visualizations/age_vs_risk.png' },
    { title: 'Employment vs Risk', src: '/visualizations/employment_vs_risk.png' },
    { title: 'Loan Term Distribution', src: '/visualizations/loan_term_distribution.png' },
    { title: 'Credit Score vs Income', src: '/visualizations/credit_score_vs_income.png' },
    { title: 'Credit Score vs Loan Amount', src: '/visualizations/credit_score_vs_loan_amount.png' },
    { title: 'Correlation Heatmap', src: '/visualizations/correlation_heatmap.png' }
  ];

  return (
    <div className="space-y-8 animate-fade-in pb-10">
      <div>
        <h1 className="text-3xl font-black text-brand-navy mb-2">Exploratory Data Analysis</h1>
        <p className="text-slate-500 font-medium">Visual insights from the loan dataset features and distributions.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {images.map((img, idx) => (
          <div key={idx} className="bg-white rounded-2xl shadow-soft border border-brand-border overflow-hidden">
            <div className="p-4 border-b border-slate-100 bg-slate-50/50">
              <h3 className="font-bold text-brand-dark">{img.title}</h3>
            </div>
            <div className="p-6 flex justify-center items-center bg-white min-h-[300px]">
              <img
                src={`${img.src}?t=${Date.now()}`}
                alt={img.title}
                className="max-w-full h-auto object-contain hover:scale-105 transition-transform duration-300"
                loading="lazy"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
