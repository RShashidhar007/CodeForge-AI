import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Send, Loader, AlertCircle, ChevronDown, MessageSquare } from 'lucide-react';
import { aiService } from '../../services/api/aiService';
import './AIPage.css';

<<<<<<< HEAD
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
=======
interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    file: string;
    start_line: number;
    end_line: number;
    symbol?: string;
  }>;
  created_at?: string;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
}

interface Conversation {
  id: number;
  title: string;
<<<<<<< HEAD
  createdAt: string;
=======
  created_at: string;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
}

export const AIPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
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

<<<<<<< HEAD
  // The backend only returns the latest answer for a conversation (not the
  // full message list), so threads are cached client-side per conversation.
  const threadsRef = useRef<Record<number, Message[]>>({});

  const selectConversation = (id: number) => {
    setConversationId(id);
    setMessages(threadsRef.current[id] ?? []);
    setError(null);
=======
  // Load conversation history when conversation changes
  useEffect(() => {
    if (conversationId) {
      loadConversationHistory();
    }
  }, [conversationId]);

  const loadConversationHistory = async () => {
    if (!conversationId || !projectIdNum) return;

    try {
      const response = await aiService.getConversationHistory(
        projectIdNum,
        conversationId
      );
      setMessages(response.messages || []);
      setError(null);
    } catch (err) {
      console.error('Failed to load conversation:', err);
      setError('Failed to load conversation history');
    }
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !projectIdNum) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    // Add user message immediately
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const result = await aiService.chat(projectIdNum, {
        question: input,
<<<<<<< HEAD
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
=======
        conversation_id: conversationId || undefined,
        top_k: 10,
      });

      // Set conversation ID from response
      if (result.conversation_id) {
        setConversationId(result.conversation_id);
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
      }

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: result.answer,
        sources: result.sources,
<<<<<<< HEAD
        createdAt: new Date().toISOString(),
      };

      setMessages((prev) => {
        const next = [...prev, assistantMessage];
        if (result.conversationId) threadsRef.current[result.conversationId] = next;
        return next;
      });
=======
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMsg);
      // Remove the user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

<<<<<<< HEAD
  const handleSourceClick = (source?: Source) => {
    if (source) {
      // TODO: Navigate to file editor with line numbers
      console.log('Opening file:', source.file, 'at lines', source.startLine, '-', source.endLine);
=======
  const handleSourceClick = (source: Message['sources']?.[0]) => {
    if (source) {
      // TODO: Navigate to file editor with line numbers
      console.log('Opening file:', source.file, 'at lines', source.start_line, '-', source.end_line);
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
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
<<<<<<< HEAD
                onClick={() => selectConversation(conv.id)}
              >
                <span className="conv-title">{conv.title}</span>
                <span className="conv-date">
                  {new Date(conv.createdAt).toLocaleDateString()}
=======
                onClick={() => setConversationId(conv.id)}
              >
                <span className="conv-title">{conv.title}</span>
                <span className="conv-date">
                  {new Date(conv.created_at).toLocaleDateString()}
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
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
        <div className="ai-header">
          <h1>🤖 AI Code Assistant</h1>
<<<<<<< HEAD
          <p>Ask questions about your codebase. Answers are generated from the indexed repository context.</p>
=======
          <p>Ask questions about your codebase. Answers are grounded in your actual code.</p>
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
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
                      {/* Simple markdown rendering */}
                      {message.content.split('\n').map((line, i) => (
                        <p key={i}>{line || <br />}</p>
                      ))}
                    </div>
                  ) : (
                    <p>{message.content}</p>
                  )}
                </div>

                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <span className="sources-label">📌 Sources:</span>
                    <div className="sources-list">
                      {message.sources.map((source, i) => (
                        <button
                          key={i}
                          className="source-link"
                          onClick={() => handleSourceClick(source)}
<<<<<<< HEAD
                          title={`${source.file}:${source.startLine}-${source.endLine}`}
                        >
                          <span className="source-file">{source.file}</span>
                          <span className="source-lines">
                            {source.startLine}-{source.endLine}
=======
                          title={`${source.file}:${source.start_line}-${source.end_line}`}
                        >
                          <span className="source-file">{source.file}</span>
                          <span className="source-lines">
                            {source.start_line}-{source.end_line}
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
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
      </div>
    </div>
  );
};

export default AIPage;
