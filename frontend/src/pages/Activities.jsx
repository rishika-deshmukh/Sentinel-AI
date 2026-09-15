import React, { useEffect, useState } from 'react';
import client from '../api/client';

export default function Activities() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    client.get('/api/activities/recent')
      .then(res => setLogs(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-8 space-y-6">
      <div className="border border-gray-800 rounded-lg p-6 bg-gray-900/50">
        <h2 className="text-lg font-bold text-white mb-4">Audit Telemetry Records</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-gray-800 text-gray-500 uppercase">
                <th className="pb-2">Timestamp</th>
                <th className="pb-2">User ID</th>
                <th className="pb-2">Action</th>
                <th className="pb-2">Transferred (MB)</th>
                <th className="pb-2">Sensitive File</th>
                <th className="pb-2">Failed Attempts</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800 font-mono">
              {logs.map((log) => (
                <tr key={log.id}>
                  <td className="py-2.5 text-gray-400">{new Date(log.timestamp).toLocaleTimeString()}</td>
                  <td className="py-2.5 text-gray-300">#{log.user_id}</td>
                  <td className="py-2.5 text-blue-400">{log.action_type}</td>
                  <td className="py-2.5 text-gray-300">{log.bytes_transferred}</td>
                  <td className="py-2.5">{log.is_sensitive_file ? <span className="text-red-400">TRUE</span> : <span className="text-gray-500">FALSE</span>}</td>
                  <td className="py-2.5 text-gray-400">{log.failed_attempts}</td>
                </tr>
              ))}
              {logs.length === 0 && (
                <tr>
                  <td colSpan="6" className="py-4 text-center text-gray-500">
                    No activity logs recorded.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}