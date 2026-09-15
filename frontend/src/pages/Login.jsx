import React, { useState } from 'react';
import client from '../api/client';

export default function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('AdminSecurePass123!');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const res = await client.post('/api/auth/login', formData);
      localStorage.setItem('sentinel_token', res.data.access_token);
      localStorage.setItem('sentinel_role', res.data.role);
      onLoginSuccess(res.data.role);
    } catch (err) {
      setError('Invalid username or password.');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 px-4">
      <div className="max-w-md w-full bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <div className="inline-block p-3 rounded-lg bg-blue-600/10 border border-blue-500/20 text-blue-400 font-black text-2xl mb-2">
            SentinelAI
          </div>
          <h2 className="text-xl font-bold text-white">Enterprise Security Login</h2>
          <p className="text-xs text-gray-400 mt-1">Adaptive Malicious Insider Threat Detection</p>
        </div>

        {error && <div className="mb-4 text-xs text-red-400 bg-red-950/30 border border-red-800 p-3 rounded">{error}</div>}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs uppercase text-gray-400 mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-xs uppercase text-gray-400 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2 rounded text-sm transition shadow-lg shadow-blue-600/30"
          >
            Authenticate Session
          </button>
        </form>

        <div className="mt-6 text-xs text-gray-500 text-center">
          Default users seeded: <span className="text-gray-300 font-mono">admin</span>, <span className="text-gray-300 font-mono">analyst</span>
        </div>
      </div>
    </div>
  );
}