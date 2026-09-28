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
