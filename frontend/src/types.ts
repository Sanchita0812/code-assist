export interface ProgressStep {
  id: string;
  message: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  timestamp: Date;
}

export interface ModifiedFile {
  path: string;
  changes: number;
  diff: string;
}

export interface AgentResult {
  modifiedFiles: ModifiedFile[];
  pullRequestUrl: string;
  plan: string;
  summary: string;
}