import React from 'react';
import { Code2, Zap } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <div className="w-8 h-8 bg-gradient-to-br from-accent-500 to-accent-700 rounded-lg flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-accent-400 rounded-full animate-pulse-slow">
                <Zap className="w-2 h-2 text-dark-950 absolute top-0.5 left-0.5" />
              </div>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Backspace</h1>
              <p className="text-sm text-dark-400">AI Coding Assistant</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2 text-sm text-dark-400">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Ready</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;