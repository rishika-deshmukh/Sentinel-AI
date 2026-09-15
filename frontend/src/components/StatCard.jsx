import React from 'react';

export default function StatCard({ label, value, subtext, alert, icon: Icon }) {
  const borderClass = alert
    ? 'border-red-500/40 bg-gradient-to-b from-red-950/20 to-sentinel-900/60 shadow-lg shadow-red-950/20'
    : 'border-sentinel-800 bg-sentinel-900/50 hover:border-sentinel-700';

  return (
    <div className={`p-4 rounded-xl border ${borderClass} transition-all duration-300 relative overflow-hidden group`}>
      <div className="flex justify-between items-start">
        <div className="text-[11px] font-mono tracking-wider uppercase text-gray-400">{label}</div>
        {Icon && (
          <div className="p-2 rounded-lg bg-sentinel-800/60 border border-sentinel-700/50 text-gray-300 group-hover:text-blue-400 transition-colors">
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="text-2xl font-black mt-2 font-mono text-white tracking-tight">{value}</div>

      {subtext && (
        <div className="text-[11px] text-gray-500 mt-2 font-mono flex items-center space-x-1">
          <span>{subtext}</span>
        </div>
      )}

      <div className={`absolute bottom-0 left-0 right-0 h-[2px] ${alert ? 'bg-red-500' : 'bg-blue-500/40'}`} />
    </div>
  );
}