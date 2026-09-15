import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function ShapChart({ attributions }) {
  if (!attributions || Object.keys(attributions).length === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-gray-500 font-mono text-xs">
        [NO REAL-TIME SHAP ATTRIBUTIONS PROCESSED]
      </div>
    );
  }

  const data = Object.entries(attributions).map(([key, val]) => ({
    name: key.replace(/_/g, ' '),
    score: val,
  })).sort((a, b) => Math.abs(b.score) - Math.abs(a.score));

  return (
    <div className="space-y-2">
      <div className="h-56 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 70, bottom: 5 }}>
            <XAxis type="number" stroke="#4b5563" tick={{ fill: '#9ca3af', fontSize: 10, fontFamily: 'monospace' }} />
            <YAxis
              dataKey="name"
              type="category"
              stroke="#4b5563"
              tick={{ fill: '#9ca3af', fontSize: 10, fontFamily: 'monospace' }}
              width={130}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#0c1017', borderColor: '#222f46', borderRadius: '8px' }}
              itemStyle={{ fontFamily: 'monospace', fontSize: '11px' }}
              formatter={(value) => [`${value}`, 'SHAP Impact']}
            />
            <Bar dataKey="score" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.score < 0 ? '#ef4444' : '#10b981'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="flex justify-center space-x-6 text-[10px] font-mono text-gray-400 pt-2 border-t border-sentinel-800">
        <span className="flex items-center space-x-1.5">
          <span className="h-2 w-2 rounded-full bg-red-500"></span>
          <span>Malicious Insider Driver (Pushes toward Anomaly)</span>
        </span>
        <span className="flex items-center space-x-1.5">
          <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
          <span>Normal Baseline Driver (Pushes toward Inlier)</span>
        </span>
      </div>
    </div>
  );
}