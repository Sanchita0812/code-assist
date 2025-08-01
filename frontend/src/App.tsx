import React, { useState } from 'react';
import Header from './components/Header';
import InputSection from './components/InputSection';
import ProgressPanel from './components/ProgressPanel';
import ResultsPanel from './components/ResultsPanel';
import PlanModal from './components/PlanModal';
import { AgentResult, ProgressStep } from './types';

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState<ProgressStep[]>([]);
  const [result, setResult] = useState<AgentResult | null>(null);
  const [showPlanModal, setShowPlanModal] = useState(false);

  const handleRunAgent = async (repoUrl: string, prompt: string) => {
    setIsRunning(true);
    setProgress([]);
    setResult(null);

    // Simulate progress steps
    const steps: ProgressStep[] = [
      { id: '1', message: 'Cloning repository...', status: 'running', timestamp: new Date() },
      { id: '2', message: 'Analyzing codebase...', status: 'pending', timestamp: new Date() },
      { id: '3', message: 'Planning changes...', status: 'pending', timestamp: new Date() },
      { id: '4', message: 'Applying edits...', status: 'pending', timestamp: new Date() },
      { id: '5', message: 'Creating pull request...', status: 'pending', timestamp: new Date() },
    ];

    setProgress(steps);

    try {
      // Simulate API call
      for (let i = 0; i < steps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        setProgress(prev => prev.map((step, index) => {
          if (index === i) {
            return { ...step, status: 'completed' };
          } else if (index === i + 1) {
            return { ...step, status: 'running' };
          }
          return step;
        }));
      }

      // Mock result
      const mockResult: AgentResult = {
        modifiedFiles: [
          {
            path: 'src/components/UserAuth.tsx',
            changes: 15,
            diff: `@@ -1,10 +1,15 @@
 import React, { useState } from 'react';
+import { logger } from '../utils/logger';
 
 export const UserAuth: React.FC = () => {
   const [loading, setLoading] = useState(false);
 
-  const handleLogin = async (credentials: LoginCredentials) => {
+  const handleLogin = async (credentials: LoginCredentials) => {
+    logger.info('Login attempt started', { email: credentials.email });
     setLoading(true);
     try {
       const result = await authService.login(credentials);
+      logger.info('Login successful', { userId: result.userId });
       return result;
     } catch (error) {
+      logger.error('Login failed', { error: error.message });
       throw error;
     } finally {
       setLoading(false);`
          },
          {
            path: 'src/services/authService.ts',
            changes: 8,
            diff: `@@ -5,6 +5,7 @@
 import { ApiClient } from './apiClient';
+import { logger } from '../utils/logger';
 
 class AuthService {
   async login(credentials: LoginCredentials): Promise<AuthResult> {
+    logger.debug('AuthService.login called');
     const response = await ApiClient.post('/auth/login', credentials);
     return response.data;
   }`
          },
          {
            path: 'src/utils/logger.ts',
            changes: 25,
            diff: `@@ -0,0 +1,25 @@
+export enum LogLevel {
+  DEBUG = 0,
+  INFO = 1,
+  WARN = 2,
+  ERROR = 3,
+}
+
+class Logger {
+  private level: LogLevel = LogLevel.INFO;
+
+  debug(message: string, meta?: any) {
+    if (this.level <= LogLevel.DEBUG) {
+      console.debug('[DEBUG]', message, meta);
+    }
+  }
+
+  info(message: string, meta?: any) {
+    if (this.level <= LogLevel.INFO) {
+      console.info('[INFO]', message, meta);
+    }
+  }
+
+  error(message: string, meta?: any) {
+    console.error('[ERROR]', message, meta);
+  }
+}
+
+export const logger = new Logger();`
          }
        ],
        pullRequestUrl: 'https://github.com/user/repo/pull/123',
        plan: `## Implementation Plan

### Files to Modify:
- src/components/UserAuth.tsx: Add logging to authentication flow
  - Import logger utility
  - Add info log for login attempts
  - Add success/error logging
  
- src/services/authService.ts: Add debug logging to service calls
  - Import logger utility  
  - Add debug log for service method calls
  
### Files to Create:
- src/utils/logger.ts: Create centralized logging utility
  - Define log levels (DEBUG, INFO, WARN, ERROR)
  - Implement Logger class with level-based filtering
  - Export singleton logger instance

### Summary:
This implementation adds comprehensive logging to all authentication-related async functions as requested. The logger utility provides different log levels and can be easily configured for different environments.`,
        summary: 'Successfully analyzed 15 files and identified 3 files that needed logging improvements. Created a centralized logger utility and integrated it into all async authentication functions.'
      };

      setResult(mockResult);
    } catch (error) {
      setProgress(prev => prev.map(step => 
        step.status === 'running' ? { ...step, status: 'error' } : step
      ));
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-950">
      <Header />
      
      <main className="container mx-auto px-6 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column */}
          <div className="space-y-6">
            <InputSection onRunAgent={handleRunAgent} isRunning={isRunning} />
            <ProgressPanel steps={progress} />
          </div>
          
          {/* Right Column */}
          <div className="space-y-6">
            {result && (
              <ResultsPanel 
                result={result} 
                onShowPlan={() => setShowPlanModal(true)}
              />
            )}
          </div>
        </div>
      </main>

      {showPlanModal && result && (
        <PlanModal 
          plan={result.plan}
          summary={result.summary}
          onClose={() => setShowPlanModal(false)}
        />
      )}
    </div>
  );
}

export default App;