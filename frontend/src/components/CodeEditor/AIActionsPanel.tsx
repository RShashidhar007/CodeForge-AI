import React, { useState } from 'react';
import {
  Zap,
  BookOpen,
  AlertCircle,
  Lightbulb,
  TestTube,
  Loader,
  X,
} from 'lucide-react';
import { aiService } from '../../services/api/aiService';
import './AIActionsPanel.css';

interface AIActionsPanelProps {
  projectId: number;
  selectedCode: string;
  filepath: string;
  startLine: number;
  endLine: number;
  language: string;
  onClose: () => void;
}

type ActionType = 'explain' | 'bugs' | 'improve' | 'tests' | null;

export const AIActionsPanel: React.FC<AIActionsPanelProps> = ({
  projectId,
  selectedCode,
  filepath,
  startLine,
  endLine,
  language,
  onClose,
}) => {
  const [activeAction, setActiveAction] = useState<ActionType>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async (action: ActionType) => {
    if (action === activeAction) {
      setActiveAction(null);
      setResult(null);
      return;
    }

    setActiveAction(action);
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      let response: any;

      switch (action) {
        case 'explain':
          response = await aiService.explainCode(projectId, {
            code: selectedCode,
            filepath,
            start_line: startLine,
            end_line: endLine,
            language,
          });
          setResult(response.explanation);
          break;

        case 'bugs':
          response = await aiService.detectBugs(projectId, {
            code: selectedCode,
            filepath,
            start_line: startLine,
            end_line: endLine,
            language,
          });
          setResult(response.analysis);
          break;

        case 'improve':
          response = await aiService.improveCode(projectId, {
            code: selectedCode,
            filepath,
            start_line: startLine,
            end_line: endLine,
            language,
          });
          setResult(response.suggestions);
          break;

        case 'tests':
          response = await aiService.generateTests(projectId, {
            code: selectedCode,
            filepath,
            start_line: startLine,
            end_line: endLine,
            language,
          });
          setResult(response.tests);
          break;
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMsg);
      setActiveAction(null);
    } finally {
      setLoading(false);
    }
  };

  const actions = [
    {
      id: 'explain',
      label: 'Explain',
      icon: BookOpen,
      description: 'Understand what this code does',
    },
    {
      id: 'bugs',
      label: 'Find Bugs',
      icon: AlertCircle,
      description: 'Detect potential issues',
    },
    {
      id: 'improve',
      label: 'Improve',
      icon: Lightbulb,
      description: 'Get improvement suggestions',
    },
    {
      id: 'tests',
      label: 'Generate Tests',
      icon: TestTube,
      description: 'Create unit tests',
    },
  ] as const;

  return (
    <div className="ai-actions-panel">
      <div className="panel-header">
        <div className="header-content">
          <Zap size={18} className="header-icon" />
          <div>
            <h3>AI Code Assistant</h3>
            <p className="selected-info">
              {filepath}:{startLine}-{endLine}
            </p>
          </div>
        </div>
        <button
          className="close-button"
          onClick={onClose}
          aria-label="Close panel"
        >
          <X size={20} />
        </button>
      </div>

      <div className="panel-content">
        {!result && !error && (
          <div className="actions-grid">
            {actions.map((action) => (
              <button
                key={action.id}
                className={`action-button ${
                  activeAction === action.id ? 'active' : ''
                } ${loading && activeAction === action.id ? 'loading' : ''}`}
                onClick={() => handleAction(action.id as ActionType)}
                disabled={loading && activeAction !== action.id}
              >
                <action.icon size={24} className="action-icon" />
                <span className="action-label">{action.label}</span>
                <span className="action-description">{action.description}</span>
                {loading && activeAction === action.id && (
                  <Loader size={16} className="spinner" />
                )}
              </button>
            ))}
          </div>
        )}

        {loading && (
          <div className="loading-state">
            <Loader size={32} className="spinner-large" />
            <p>Analyzing code...</p>
          </div>
        )}

        {error && (
          <div className="error-state">
            <AlertCircle size={24} />
            <p className="error-message">{error}</p>
            <button
              className="retry-button"
              onClick={() => handleAction(activeAction)}
            >
              Try Again
            </button>
          </div>
        )}

        {result && !loading && (
          <div className="result-state">
            <div className="result-header">
              <h4>
                {activeAction === 'explain' && '📝 Explanation'}
                {activeAction === 'bugs' && '🐛 Bug Analysis'}
                {activeAction === 'improve' && '💡 Improvement Suggestions'}
                {activeAction === 'tests' && '✅ Generated Tests'}
              </h4>
              <button
                className="back-button"
                onClick={() => {
                  setActiveAction(null);
                  setResult(null);
                }}
              >
                ← Back
              </button>
            </div>

            <div className="result-content">
              {/* Simple markdown-like rendering */}
              {result.split('\n').map((line, i) => {
                if (!line.trim()) {
                  return <br key={i} />;
                }

                // Code blocks
                if (line.startsWith('```')) {
                  return null;
                }

                // Headers
                if (line.startsWith('##')) {
                  return (
                    <h5 key={i}>{line.replace(/^#+\s?/, '')}</h5>
                  );
                }

                // Lists
                if (line.match(/^[\d\-\*]\.\s/) || line.startsWith('- ')) {
                  return (
                    <li key={i} className="result-list-item">
                      {line.replace(/^[\d\-\*\.\s]+/, '')}
                    </li>
                  );
                }

                // Bold text
                let renderedLine = line.replace(
                  /\*\*(.*?)\*\*/g,
                  '<strong>$1</strong>'
                );

                // Italic text
                renderedLine = renderedLine.replace(
                  /\*(.*?)\*/g,
                  '<em>$1</em>'
                );

                return (
                  <p key={i} dangerouslySetInnerHTML={{ __html: renderedLine }} />
                );
              })}
            </div>

            <button
              className="copy-button"
              onClick={() => {
                navigator.clipboard.writeText(result);
                alert('Copied to clipboard!');
              }}
            >
              📋 Copy Result
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default AIActionsPanel;
