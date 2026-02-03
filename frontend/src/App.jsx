import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import MasterHRView from './pages/MasterHRView';
import SyncCenter from './pages/SyncCenter';
import './index.css';

function Navigation() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="glass-card border-0 shadow-glass mb-8">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center shadow-glow float-animation">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                HR Dashboard
              </h2>
              <p className="text-xs text-gray-500">Integrated Management System</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex space-x-2">
            <Link
              to="/"
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-300 ${isActive('/')
                  ? 'bg-gradient-primary text-white shadow-glow'
                  : 'text-gray-700 hover:bg-gray-100'
                }`}
            >
              📊 Master View
            </Link>
            <Link
              to="/sync"
              className={`px-6 py-3 rounded-lg font-medium transition-all duration-300 ${isActive('/sync')
                  ? 'bg-gradient-primary text-white shadow-glow'
                  : 'text-gray-700 hover:bg-gray-100'
                }`}
            >
              🔄 Sync Center
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen animated-gradient">
        <div className="container mx-auto px-4 py-8">
          <Navigation />
          <Routes>
            <Route path="/" element={<MasterHRView />} />
            <Route path="/sync" element={<SyncCenter />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
