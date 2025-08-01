import React from 'react';
import { CheckCircle, Clock, AlertCircle, Loader2 } from 'lucide-react';
import { ProgressStep } from '../types';

interface ProgressPanelProps {
  steps: ProgressStep[];
}

const ProgressPanel: React.FC<ProgressPanelProps> = ({ steps }) => {
  if (steps.length === 0) {
    return (
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Clock className="w-5 h-5 text-dark-400" />
          <h2 className="text-lg font-semibold text-white">Progress</h2>
        </div>
        <div className="text-center py-8 text-dark-400">
          <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>Waiting for agent to start...</p>
        </div>
      </div>
    );
  }

  const getStepIcon = (status: ProgressStep['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'running':
        return <Loader2 className="w-5 h-5 text-accent-500 animate-spin" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-dark-500" />;
    }
  };

  const getStepColor = (status: ProgressStep['status']) => {
    switch (status) {
      case 'completed':
        return 'text-green-400';
      case 'running':
        return 'text-accent-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-dark-400';
    }
  };

  return (
    <div className="card animate-slide-up">
      <div className="flex items-center space-x-2 mb-6">
        <Loader2 className="w-5 h-5 text-accent-500 animate-spin" />
        <h2 className="text-lg font-semibold text-white">Progress</h2>
      </div>

      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-0.5">
              {getStepIcon(step.status)}
            </div>
            <div className="flex-1 min-w-0">
              <p className={`text-sm font-medium ${getStepColor(step.status)}`}>
                {step.message}
              </p>
              <p className="text-xs text-dark-500 mt-1">
                {step.timestamp.toLocaleTimeString()}
              </p>
            </div>
            {index < steps.length - 1 && (
              <div className="absolute left-[22px] mt-6 w-px h-6 bg-dark-700"></div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-dark-800">
        <div className="flex items-center justify-between text-sm">
          <span className="text-dark-400">
            {steps.filter(s => s.status === 'completed').length} of {steps.length} completed
          </span>
          <div className="w-24 bg-dark-800 rounded-full h-2">
            <div 
              className="bg-accent-500 h-2 rounded-full transition-all duration-300"
              style={{ 
                width: `${(steps.filter(s => s.status === 'completed').length / steps.length) * 100}%` 
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProgressPanel;