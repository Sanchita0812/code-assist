import React, { useState } from 'react';
import { FileText, ExternalLink, Eye, EyeOff, GitPullRequest, Info } from 'lucide-react';
import { AgentResult } from '../types';
import DiffViewer from './DiffViewer';

interface ResultsPanelProps {
  result: AgentResult;
  onShowPlan: () => void;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({ result, onShowPlan }) => {
  const [expandedFiles, setExpandedFiles] = useState<Set<string>>(new Set());

  const toggleFileExpansion = (filePath: string) => {
    const newExpanded = new Set(expandedFiles);
    if (newExpanded.has(filePath)) {
      newExpanded.delete(filePath);
    } else {
      newExpanded.add(filePath);
    }
    setExpandedFiles(newExpanded);
  };

  const totalChanges = result.modifiedFiles.reduce((sum, file) => sum + file.changes, 0);

  return (
    <div className="space-y-6">
      {/* Summary Card */}
      <div className="card animate-fade-in">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <FileText className="w-4 h-4 text-white" />
            </div>
            <h2 className="text-lg font-semibold text-white">Results</h2>
          </div>
          <button
            onClick={onShowPlan}
            className="btn-secondary text-sm flex items-center space-x-1"
          >
            <Info className="w-4 h-4" />
            <span>Explain Plan</span>
          </button>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-dark-800 rounded-lg p-3">
            <div className="text-2xl font-bold text-accent-400">{result.modifiedFiles.length}</div>
            <div className="text-sm text-dark-400">Files Modified</div>
          </div>
          <div className="bg-dark-800 rounded-lg p-3">
            <div className="text-2xl font-bold text-green-400">{totalChanges}</div>
            <div className="text-sm text-dark-400">Total Changes</div>
          </div>
        </div>

        <div className="flex space-x-3">
          <a
            href={result.pullRequestUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary flex items-center space-x-2 flex-1 justify-center"
          >
            <GitPullRequest className="w-4 h-4" />
            <span>View Pull Request</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>

      {/* Modified Files */}
      <div className="card animate-slide-up">
        <div className="flex items-center space-x-2 mb-6">
          <FileText className="w-5 h-5 text-accent-500" />
          <h3 className="text-lg font-semibold text-white">Modified Files</h3>
        </div>

        <div className="space-y-3">
          {result.modifiedFiles.map((file) => (
            <div key={file.path} className="border border-dark-700 rounded-lg overflow-hidden">
              <div 
                className="flex items-center justify-between p-4 bg-dark-800 cursor-pointer hover:bg-dark-750 transition-colors"
                onClick={() => toggleFileExpansion(file.path)}
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-accent-600 rounded-lg flex items-center justify-center">
                    <FileText className="w-4 h-4 text-white" />
                  </div>
                  <div>
                    <div className="font-mono text-sm text-white">{file.path}</div>
                    <div className="text-xs text-dark-400">
                      {file.changes} change{file.changes !== 1 ? 's' : ''}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs bg-green-900 text-green-300 px-2 py-1 rounded">
                    +{file.changes}
                  </span>
                  {expandedFiles.has(file.path) ? (
                    <EyeOff className="w-4 h-4 text-dark-400" />
                  ) : (
                    <Eye className="w-4 h-4 text-dark-400" />
                  )}
                </div>
              </div>
              
              {expandedFiles.has(file.path) && (
                <div className="border-t border-dark-700">
                  <DiffViewer diff={file.diff} />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ResultsPanel;