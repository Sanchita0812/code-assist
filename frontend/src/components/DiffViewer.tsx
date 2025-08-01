import React from 'react';

interface DiffViewerProps {
  diff: string;
}

const DiffViewer: React.FC<DiffViewerProps> = ({ diff }) => {
  const lines = diff.split('\n');

  const getLineType = (line: string) => {
    if (line.startsWith('+')) return 'added';
    if (line.startsWith('-')) return 'removed';
    if (line.startsWith('@@')) return 'header';
    return 'context';
  };

  const getLineClass = (type: string) => {
    switch (type) {
      case 'added':
        return 'bg-green-900/30 text-green-300 border-l-2 border-green-500';
      case 'removed':
        return 'bg-red-900/30 text-red-300 border-l-2 border-red-500';
      case 'header':
        return 'bg-accent-900/30 text-accent-300 font-semibold';
      default:
        return 'text-dark-400';
    }
  };

  const formatLine = (line: string, type: string) => {
    if (type === 'header') {
      return line;
    }
    // Remove the +/- prefix for display but keep the indentation
    return line.substring(1);
  };

  return (
    <div className="bg-dark-950 font-mono text-sm overflow-x-auto">
      <div className="p-4">
        {lines.map((line, index) => {
          const type = getLineType(line);
          return (
            <div
              key={index}
              className={`px-3 py-1 ${getLineClass(type)} whitespace-pre`}
            >
              <span className="select-none text-dark-500 mr-4 inline-block w-8 text-right">
                {type !== 'header' ? index + 1 : ''}
              </span>
              {formatLine(line, type)}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DiffViewer;