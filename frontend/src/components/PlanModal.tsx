import React from 'react';
import { X, FileText, Target, CheckCircle } from 'lucide-react';

interface PlanModalProps {
  plan: string;
  summary: string;
  onClose: () => void;
}

const PlanModal: React.FC<PlanModalProps> = ({ plan, summary, onClose }) => {
  const formatPlan = (planText: string) => {
    const lines = planText.split('\n');
    const formattedLines: JSX.Element[] = [];

    lines.forEach((line, index) => {
      if (line.startsWith('##')) {
        formattedLines.push(
          <h3 key={index} className="text-lg font-semibold text-white mt-6 mb-3 flex items-center">
            <Target className="w-5 h-5 mr-2 text-accent-500" />
            {line.replace('##', '').trim()}
          </h3>
        );
      } else if (line.startsWith('###')) {
        formattedLines.push(
          <h4 key={index} className="text-md font-medium text-accent-300 mt-4 mb-2">
            {line.replace('###', '').trim()}
          </h4>
        );
      } else if (line.startsWith('- ') && line.includes('.')) {
        const [file, ...descParts] = line.substring(2).split(':');
        const description = descParts.join(':').trim();
        formattedLines.push(
          <div key={index} className="mb-3 p-3 bg-dark-800 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <FileText className="w-4 h-4 text-accent-500" />
              <code className="text-accent-300 font-mono text-sm">{file}</code>
            </div>
            {description && (
              <p className="text-dark-200 text-sm ml-6">{description}</p>
            )}
          </div>
        );
      } else if (line.trim().startsWith('- ')) {
        formattedLines.push(
          <div key={index} className="flex items-start space-x-2 mb-2 ml-6">
            <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
            <span className="text-dark-300 text-sm">{line.substring(2).trim()}</span>
          </div>
        );
      } else if (line.trim()) {
        formattedLines.push(
          <p key={index} className="text-dark-300 mb-2">{line}</p>
        );
      }
    });

    return formattedLines;
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-dark-900 border border-dark-700 rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-6 border-b border-dark-700">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-accent-600 rounded-lg flex items-center justify-center">
              <Target className="w-4 h-4 text-white" />
            </div>
            <h2 className="text-xl font-semibold text-white">Implementation Plan</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-dark-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-dark-400" />
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {/* Summary Section */}
          <div className="mb-8 p-4 bg-dark-800 rounded-lg border border-dark-700">
            <h3 className="text-lg font-medium text-white mb-3 flex items-center">
              <CheckCircle className="w-5 h-5 mr-2 text-green-500" />
              Summary
            </h3>
            <p className="text-dark-200 leading-relaxed">{summary}</p>
          </div>

          {/* Detailed Plan */}
          <div className="prose prose-invert max-w-none">
            {formatPlan(plan)}
          </div>
        </div>

        <div className="p-6 border-t border-dark-700 bg-dark-800/50">
          <button
            onClick={onClose}
            className="btn-primary w-full"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default PlanModal;