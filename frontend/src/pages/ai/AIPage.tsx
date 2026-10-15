import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Send, Loader, AlertCircle, ChevronDown, MessageSquare, Search, Copy, Check } from 'lucide-react';
import { aiService } from '../../services/api/aiService';
import { SemanticSearchPanel } from '../../components/ai/SemanticSearchPanel';
import type { Project } from '../../types/project';
import './AIPage.css';

interface Source {
  file: string;
  startLine: number;
  endLine: number;
  symbol?: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  createdAt?: string;
}

interface Conversation {
  id: number;
  title: string;
  createdAt: string;
}

type TabType = 'chat' | 'search';

// CodeBlock component for rendering code with copy functionality
const CodeBlock: React.FC<{ code: string; language: string }> = ({ code, language }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <div className="code-block-wrapper">
      <div className="code-block-header">
        <span className="code-language">{language || 'text'}</span>
        <button className="copy-button" onClick={copyToClipboard}>
          {copied ? (
            <>
              <Check size={14} />
              Copied!
            </>
          ) : (
            <>
              <Copy size={14} />
              Copy
            </>
          )}
        </button>
      </div>
      <pre className="code-block">
        <code>{code}</code>
      </pre>
    </div>
  );
};

// Helper function to parse message content and render text and code blocks
const renderMessageContent = (content: string): React.ReactNode[] => {
  const nodes: React.ReactNode[] = [];
  const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
  let lastIndex = 0;
  let match;
  let keyCounter = 0;

  while ((match = codeBlockRegex.exec(content)) !== null) {
    const matchStart = match.index;
    const matchEnd = codeBlockRegex.lastIndex;
    
    // Add text before code block
    if (matchStart > lastIndex) {
      const textBefore = content.substring(lastIndex, matchStart);
      textBefore.split('\n').forEach((line) => {
        nodes.push(<p key={`text-${keyCounter++}`}>{line || <br />}</p>);
      });
    }
    
    // Add code block
    const language = match[1] || 'text';
    const code = match[2];
    nodes.push(<CodeBlock key={`code-${keyCounter++}`} code={code} language={language} />);
    
    lastIndex = matchEnd;
  }

  // Add remaining text after last code block
  if (lastIndex < content.length) {
    const remainingText = content.substring(lastIndex);
    remainingText.split('\n').forEach((line) => {
      nodes.push(<p key={`text-${keyCounter++}`}>{line || <br />}</p>);
    });
  }

  return nodes.length > 0 ? nodes : [<p key="empty"><br /></p>];
};

export const AIPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [activeTab, setActiveTab] = useState<TabType>('chat');
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(
    projectId ? parseInt(projectId) : null
  );
  const [projects] = useState<Project[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [showSidebar, setShowSidebar] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const projectIdNum = projectId ? parseInt(projectId) : 0;

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // The backend only returns the latest answer for a conversation (not the
  // full message list), so threads are cached client-side per conversation.
  const threadsRef = useRef<Record<number, Message[]>>({});

  const selectConversation = (id: number) => {
    setConversationId(id);
    setMessages(threadsRef.current[id] ?? []);
    setError(null);
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !projectIdNum) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      createdAt: new Date().toISOString(),
    };

    // Add user message immediately
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const result = await aiService.chat(projectIdNum, {
        question: input,
        conversationId: conversationId || undefined,
        topK: 10,
      });

      // Track the conversation returned by the server
      if (result.conversationId) {
        setConversationId(result.conversationId);
        setConversations((prev) =>
          prev.some((c) => c.id === result.conversationId)
            ? prev
            : [
                ...prev,
                {
                  id: result.conversationId,
                  title: userMessage.content.slice(0, 40),
                  createdAt: new Date().toISOString(),
                },
              ]
        );
      }

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
        createdAt: new Date().toISOString(),
      };

      setMessages((prev) => {
        const next = [...prev, assistantMessage];
        if (result.conversationId) threadsRef.current[result.conversationId] = next;
        return next;
      });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMsg);
      // Remove the user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const handleSourceClick = (source?: Source) => {
    if (source) {
      // TODO: Navigate to file editor with line numbers
      console.log('Opening file:', source.file, 'at lines', source.startLine, '-', source.endLine);
    }
  };

  return (
    <div className="ai-page">
      <div className={`ai-sidebar ${showSidebar ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>
            <MessageSquare size={20} />
            Conversations
          </h2>
          <button
            className="sidebar-toggle"
            onClick={() => setShowSidebar(!showSidebar)}
            aria-label="Toggle sidebar"
          >
            <ChevronDown size={20} />
          </button>
        </div>

        <div className="conversations-list">
          {conversations.length === 0 ? (
            <p className="empty-state">No conversations yet. Start a new chat!</p>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                className={`conversation-item ${
                  conversationId === conv.id ? 'active' : ''
                }`}
                onClick={() => selectConversation(conv.id)}
              >
                <span className="conv-title">{conv.title}</span>
                <span className="conv-date">
                  {new Date(conv.createdAt).toLocaleDateString()}
                </span>
              </button>
            ))
          )}
        </div>

        <button
          className="new-conversation-btn"
          onClick={() => {
            setConversationId(null);
            setMessages([]);
            setInput('');
            setError(null);
          }}
        >
          + New Chat
        </button>
      </div>

      <div className="ai-main">
        {/* Tab Navigation */}
        <div className="ai-tabs">
          <button
            className={`tab-button ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            <MessageSquare size={18} />
            Chat
          </button>
          <button
            className={`tab-button ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => setActiveTab('search')}
          >
            <Search size={18} />
            Code Search
          </button>
        </div>

        {/* Chat Tab Content */}
        {activeTab === 'chat' && (
          <>
        <div className="ai-header">
          <h1>🤖 AI Code Assistant</h1>
          <p>Ask questions about your codebase. Answers are generated from the indexed repository context.</p>
        </div>

        {error && (
          <div className="error-banner">
            <AlertCircle size={20} />
            <span>{error}</span>
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}

        <div className="messages-container">
          {messages.length === 0 && !error ? (
            <div className="empty-messages">
              <MessageSquare size={48} />
              <h2>Start a Conversation</h2>
              <p>Ask questions like:</p>
              <ul>
                <li>"Explain the authentication system"</li>
                <li>"Where is JWT implemented?"</li>
                <li>"How does project creation work?"</li>
                <li>"What are the main dependencies?"</li>
              </ul>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`message-bubble ${message.role}-message`}
              >
                <div className="message-content">
                  {message.role === 'assistant' ? (
                    <div className="markdown-content">
                      {renderMessageContent(message.content)}
                    </div>
                  ) : (
                    <p>{message.content}</p>
                  )}
                </div>

                {message.createdAt && (
                  <div className="message-timestamp">
                    {new Date(message.createdAt).toLocaleTimeString()}
                  </div>
                )}

                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <span className="sources-label">📌 Sources:</span>
                    <div className="sources-list">
                      {message.sources.map((source, i) => (
                        <button
                          key={i}
                          className="source-link"
                          onClick={() => handleSourceClick(source)}
                          title={`${source.file}:${source.startLine}-${source.endLine}`}
                        >
                          <span className="source-file">{source.file}</span>
                          <span className="source-lines">
                            {source.startLine}-{source.endLine}
                          </span>
                          {source.symbol && (
                            <span className="source-symbol">{source.symbol}</span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))
          )}

          {loading && (
            <div className="message-bubble assistant-message loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form className="message-input-form" onSubmit={handleSendMessage}>
          <div className="input-wrapper">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about your code... (e.g., 'Explain the user authentication flow')"
              disabled={loading}
              className="message-input"
              autoFocus
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="send-button"
              title="Send message"
            >
              {loading ? (
                <Loader size={20} className="spinner" />
              ) : (
                <Send size={20} />
              )}
            </button>
          </div>
          <p className="input-hint">
            💡 Tip: Be specific. Ask about files, functions, or architecture.
          </p>
        </form>
          </>
        )}

        {/* Code Search Tab Content */}
        {activeTab === 'search' && (
          <div style={{ padding: '2rem', overflowY: 'auto', flex: 1 }}>
            <SemanticSearchPanel
              projects={projects}
              selectedProjectId={selectedProjectId}
              onProjectChange={setSelectedProjectId}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AIPage;
