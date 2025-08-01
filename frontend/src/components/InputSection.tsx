import React, { useState } from 'react';
import { Play, Github, MessageSquare } from 'lucide-react';

interface InputSectionProps {
  onRunAgent: (repoUrl: string, prompt: string) => void;
  isRunning: boolean;
}

const InputSection: React.FC<InputSectionProps> = ({ onRunAgent, isRunning }) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoUrl.trim() && prompt.trim() && !isRunning) {
      onRunAgent(repoUrl.trim(), prompt.trim());
    }
  };

  const isValidGithubUrl = (url: string) => {
    return url.includes('github.com') && url.includes('/');
  };

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center space-x-2 mb-6">
        <div className="w-8 h-8 bg-accent-600 rounded-lg flex items-center justify-center">
          <Play className="w-4 h-4 text-white" />
        </div>
        <h2 className="text-lg font-semibold text-white">Start New Task</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-dark-200 mb-2">
            <Github className="w-4 h-4 inline mr-2" />
            GitHub Repository URL
          </label>
          <input
            type="url"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className={`input-field w-full ${
              repoUrl && !isValidGithubUrl(repoUrl) 
                ? 'border-red-500 focus:ring-red-500' 
                : ''
            }`}
            disabled={isRunning}
          />
          {repoUrl && !isValidGithubUrl(repoUrl) && (
            <p className="text-red-400 text-sm mt-1">Please enter a valid GitHub URL</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-dark-200 mb-2">
            <MessageSquare className="w-4 h-4 inline mr-2" />
            Describe Your Changes
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Add logging to all async functions, refactor the authentication system, implement error handling..."
            rows={4}
            className="input-field w-full resize-none"
            disabled={isRunning}
          />
          <p className="text-dark-400 text-xs mt-1">
            Be specific about what you want to change or improve
          </p>
        </div>

        <button
          type="submit"
          disabled={!repoUrl.trim() || !prompt.trim() || !isValidGithubUrl(repoUrl) || isRunning}
          className="btn-primary w-full flex items-center justify-center space-x-2 py-3"
        >
          {isRunning ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Running Agent...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4" />
              <span>Run Agent</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-6 p-4 bg-dark-800 rounded-lg">
        <h3 className="text-sm font-medium text-dark-200 mb-2">Example Prompts:</h3>
        <div className="space-y-1 text-sm text-dark-400">
          <p>• "Add TypeScript types to all components"</p>
          <p>• "Implement error boundaries in React components"</p>
          <p>• "Add input validation to all forms"</p>
          <p>• "Convert class components to functional components"</p>
        </div>
      </div>
    </div>
  );
};

export default InputSection;