import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { 
  MessageSquare, Send, Plus, Trash2, BookOpen, Sparkles, 
  Bot, User, Check, Copy 
} from 'lucide-react';
import { type Language, translations } from '../i18n/translations';

interface KhetGPTChatProps {
  language: Language;
}

interface Citation {
  citation_id: number;
  document_name: string;
  page_number: number;
  category: string;
  similarity: number;
}

interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  language?: string;
  citations?: Citation[];
  created_at?: string;
}

interface ConversationItem {
  id: string;
  title: string;
  language: string;
  created_at: string;
  message_count: number;
}

const API_BASE = import.meta.env.VITE_API_URL || (typeof window !== 'undefined' && window.location.origin.includes('localhost') ? 'http://localhost:8000' : '');

export const KhetGPTChat: React.FC<KhetGPTChatProps> = ({ language }) => {
  const t = translations[language];
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const [conversations, setConversations] = useState<ConversationItem[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  // Fetch conversations on mount
  useEffect(() => {
    fetchConversations();
  }, []);

  // Fetch messages when active conversation changes
  useEffect(() => {
    if (activeConversationId) {
      fetchMessages(activeConversationId);
    } else {
      setMessages([]);
    }
  }, [activeConversationId]);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const fetchConversations = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/conversations`);
      if (res.ok) {
        const data: ConversationItem[] = await res.json();
        setConversations(data);
      }
    } catch (e) {
      console.error('Error fetching conversations:', e);
    }
  };

  const fetchMessages = async (convId: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/conversations/${convId}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || []);
      }
    } catch (e) {
      console.error('Error loading messages:', e);
    }
  };

  const handleStartNewChat = () => {
    setActiveConversationId(null);
    setMessages([]);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleDeleteConversation = async (e: React.MouseEvent, convId: string) => {
    e.stopPropagation();
    try {
      const res = await fetch(`${API_BASE}/api/conversations/${convId}`, { method: 'DELETE' });
      if (res.ok) {
        setConversations(prev => prev.filter(c => c.id !== convId));
        if (activeConversationId === convId) {
          handleStartNewChat();
        }
      }
    } catch (e) {
      console.error('Failed to delete conversation:', e);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputText).trim();
    if (!text || loading) return;

    // Add user message to state optimistically
    const userMsg: ChatMessage = {
      role: 'user',
      content: text,
      language: language
    };
    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: text,
          conversation_id: activeConversationId || undefined,
          language: language
        })
      });

      if (!res.ok) {
        throw new Error('Failed to get answer from AI server.');
      }

      const data = await res.json();
      
      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content: data.content,
        language: data.language,
        citations: data.citations
      };

      setMessages(prev => [...prev, assistantMsg]);

      // If new conversation, update active id and refresh list
      if (!activeConversationId && data.conversation_id) {
        setActiveConversationId(data.conversation_id);
        fetchConversations();
      }
    } catch (err: any) {
      console.error('Chat error:', err);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: t.errorGeneric,
          language: language
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="h-[calc(100vh-8.5rem)] flex flex-col md:flex-row gap-4 max-w-7xl mx-auto">
      {/* Sidebar: Conversation History */}
      <aside className="w-full md:w-72 lg:w-80 bg-white rounded-3xl border border-gray-200 shadow-sm flex flex-col overflow-hidden">
        <div className="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 className="font-bold text-gray-900 text-sm flex items-center">
            <MessageSquare className="w-4 h-4 text-green-700 mr-2" />
            {t.chatHistoryTitle}
          </h2>
          <button
            onClick={handleStartNewChat}
            className="flex items-center space-x-1 px-3 py-1.5 bg-green-50 hover:bg-green-100 text-green-800 rounded-xl text-xs font-bold border border-green-200 transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>{t.chatNewBtn}</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-1.5">
          {conversations.length === 0 ? (
            <div className="text-center py-8 text-xs text-gray-400">
              No conversations yet
            </div>
          ) : (
            conversations.map(conv => (
              <div
                key={conv.id}
                onClick={() => setActiveConversationId(conv.id)}
                className={`group flex items-center justify-between p-3 rounded-xl cursor-pointer text-xs font-medium transition-all ${
                  activeConversationId === conv.id
                    ? 'bg-green-50 text-green-900 font-bold border border-green-200 shadow-xs'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <div className="flex-1 truncate mr-2">
                  <p className="truncate text-gray-900">{conv.title}</p>
                  <span className="text-[10px] text-gray-400">
                    {new Date(conv.created_at).toLocaleDateString()}
                  </span>
                </div>
                <button
                  onClick={(e) => handleDeleteConversation(e, conv.id)}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-red-600 transition-opacity text-gray-400"
                  title="Delete chat"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))
          )}
        </div>
      </aside>

      {/* Main Chat Conversation Container */}
      <main className="flex-1 bg-white rounded-3xl border border-gray-200 shadow-sm flex flex-col overflow-hidden">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="max-w-xl mx-auto py-12 text-center space-y-6">
              <div className="w-16 h-16 rounded-3xl bg-gradient-to-br from-green-500 to-emerald-700 text-white flex items-center justify-center mx-auto shadow-lg shadow-green-600/20">
                <Sparkles className="w-8 h-8" />
              </div>
              <div>
                <h3 className="text-xl sm:text-2xl font-extrabold text-gray-900 mb-2">
                  {t.chatEmptyTitle}
                </h3>
                <p className="text-sm text-gray-600">
                  {t.chatEmptyDesc}
                </p>
              </div>

              {/* Starter Prompts */}
              <div className="grid grid-cols-1 gap-2.5 text-left text-xs sm:text-sm">
                <button
                  onClick={() => handleSendMessage(t.chatPrompt1)}
                  className="p-3.5 rounded-2xl bg-gray-50 hover:bg-green-50/80 border border-gray-200 hover:border-green-300 text-gray-800 font-medium transition-all text-left flex items-center justify-between group"
                >
                  <span>{t.chatPrompt1}</span>
                  <Plus className="w-4 h-4 text-gray-400 group-hover:text-green-600 flex-shrink-0 ml-2" />
                </button>
                <button
                  onClick={() => handleSendMessage(t.chatPrompt2)}
                  className="p-3.5 rounded-2xl bg-gray-50 hover:bg-green-50/80 border border-gray-200 hover:border-green-300 text-gray-800 font-medium transition-all text-left flex items-center justify-between group"
                >
                  <span>{t.chatPrompt2}</span>
                  <Plus className="w-4 h-4 text-gray-400 group-hover:text-green-600 flex-shrink-0 ml-2" />
                </button>
                <button
                  onClick={() => handleSendMessage(t.chatPrompt3)}
                  className="p-3.5 rounded-2xl bg-gray-50 hover:bg-green-50/80 border border-gray-200 hover:border-green-300 text-gray-800 font-medium transition-all text-left flex items-center justify-between group"
                >
                  <span>{t.chatPrompt3}</span>
                  <Plus className="w-4 h-4 text-gray-400 group-hover:text-green-600 flex-shrink-0 ml-2" />
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-3 sm:gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-green-600 to-emerald-700 text-white flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                    <Bot className="w-5 h-5" />
                  </div>
                )}

                <div className={`max-w-2xl rounded-2xl p-4 sm:p-5 text-sm ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-br from-green-600 to-emerald-700 text-white shadow-md rounded-tr-xs'
                    : 'bg-gray-50/90 text-gray-900 border border-gray-200 shadow-sm rounded-tl-xs space-y-4'
                }`}>
                  {msg.role === 'user' ? (
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {msg.content}
                    </div>
                  ) : (
                    <div className="prose prose-sm max-w-none text-gray-900 leading-relaxed">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                          h1: ({ children }) => (
                            <h1 className="text-lg font-bold text-gray-900 mt-4 mb-2 pb-1 border-b border-gray-200">{children}</h1>
                          ),
                          h2: ({ children }) => (
                            <h2 className="text-base font-bold text-gray-900 mt-3 mb-1.5">{children}</h2>
                          ),
                          h3: ({ children }) => (
                            <h3 className="text-sm font-bold text-gray-900 mt-2 mb-1">{children}</h3>
                          ),
                          p: ({ children }) => (
                            <p className="mb-2 leading-relaxed text-gray-800 last:mb-0">{children}</p>
                          ),
                          strong: ({ children }) => (
                            <strong className="font-bold text-gray-900">{children}</strong>
                          ),
                          em: ({ children }) => (
                            <em className="italic text-gray-800">{children}</em>
                          ),
                          ul: ({ children }) => (
                            <ul className="list-disc list-outside pl-5 mb-2.5 space-y-1 text-gray-800">{children}</ul>
                          ),
                          ol: ({ children }) => (
                            <ol className="list-decimal list-outside pl-5 mb-2.5 space-y-1 text-gray-800">{children}</ol>
                          ),
                          li: ({ children }) => (
                            <li className="leading-relaxed pl-0.5">{children}</li>
                          ),
                          blockquote: ({ children }) => (
                            <blockquote className="border-l-4 border-green-600 pl-3 py-1 my-2 italic bg-green-50/60 rounded-r text-gray-700">{children}</blockquote>
                          ),
                          table: ({ children }) => (
                            <div className="overflow-x-auto my-3 rounded-xl border border-gray-200">
                              <table className="min-w-full divide-y divide-gray-200 text-xs text-left bg-white">{children}</table>
                            </div>
                          ),
                          thead: ({ children }) => (
                            <thead className="bg-gray-100 font-semibold text-gray-800">{children}</thead>
                          ),
                          th: ({ children }) => (
                            <th className="px-3 py-2 border-b border-gray-200 font-semibold">{children}</th>
                          ),
                          td: ({ children }) => (
                            <td className="px-3 py-2 border-b border-gray-100 text-gray-700">{children}</td>
                          ),
                          a: ({ href, children }) => (
                            <a
                              href={href}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-green-700 hover:text-green-900 font-semibold underline underline-offset-2"
                            >
                              {children}
                            </a>
                          ),
                          code: ({ className, children, ...props }) => {
                            const isInline = !className && typeof children === 'string' && !children.includes('\n');
                            return isInline ? (
                              <code className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-1.5 py-0.5 rounded text-xs font-mono font-medium">
                                {children}
                              </code>
                            ) : (
                              <pre className="bg-gray-900 text-gray-100 p-3 rounded-xl overflow-x-auto text-xs font-mono my-2.5">
                                <code className={className} {...props}>{children}</code>
                              </pre>
                            );
                          }
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  )}

                  {/* Grounded Citations Display */}
                  {msg.role === 'assistant' && msg.citations && msg.citations.length > 0 && (
                    <div className="pt-3 border-t border-gray-200/80">
                      <div className="flex items-center text-xs font-bold text-gray-700 mb-2">
                        <BookOpen className="w-3.5 h-3.5 text-green-700 mr-1.5" />
                        <span>{t.chatSourcesLabel}</span>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {msg.citations.map((c, cIdx) => (
                          <div
                            key={cIdx}
                            className="inline-flex items-center px-2.5 py-1 rounded-lg bg-white border border-gray-300 text-[11px] font-medium text-gray-800 shadow-xs"
                          >
                            <span className="font-semibold text-green-800 mr-1.5">
                              📄 {c.document_name}
                            </span>
                            <span className="text-gray-500">
                              (p. {c.page_number})
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Copy Button */}
                  {msg.role === 'assistant' && (
                    <div className="flex justify-end pt-1">
                      <button
                        onClick={() => copyToClipboard(msg.content, idx)}
                        className="inline-flex items-center text-xs text-gray-400 hover:text-gray-700 transition-colors"
                        title="Copy message"
                      >
                        {copiedIndex === idx ? (
                          <>
                            <Check className="w-3.5 h-3.5 text-green-600 mr-1" />
                            <span className="text-green-600 font-semibold">Copied!</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5 mr-1" />
                            <span>Copy</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>

                {msg.role === 'user' && (
                  <div className="w-9 h-9 rounded-xl bg-gray-200 text-gray-700 flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </div>
            ))
          )}

          {/* Typing Loading Indicator */}
          {loading && (
            <div className="flex gap-3 sm:gap-4 items-start">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-green-600 to-emerald-700 text-white flex items-center justify-center flex-shrink-0 shadow-sm mt-1">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-gray-50 rounded-2xl p-4 border border-gray-200 shadow-sm flex items-center space-x-2 text-xs font-semibold text-gray-600">
                <div className="w-2 h-2 rounded-full bg-green-600 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-green-600 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-green-600 animate-bounce [animation-delay:0.4s]" />
                <span className="ml-2">{t.chatThinking}</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-3 sm:p-4 border-t border-gray-200 bg-gray-50/50">
          <div className="relative flex items-end bg-white rounded-2xl border border-gray-300 focus-within:border-green-600 focus-within:ring-2 focus-within:ring-green-500/20 shadow-sm transition-all p-2">
            <textarea
              ref={textareaRef}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={t.chatPlaceholder}
              rows={1}
              className="w-full resize-none bg-transparent px-3 py-2 text-sm text-gray-900 placeholder-gray-400 focus:outline-none max-h-32 min-h-[44px]"
            />
            <button
              onClick={() => handleSendMessage()}
              disabled={!inputText.trim() || loading}
              className="p-2.5 rounded-xl bg-green-600 hover:bg-green-700 text-white disabled:opacity-40 disabled:hover:bg-green-600 transition-colors shadow-sm flex-shrink-0"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
          <div className="mt-2 text-center text-[11px] text-gray-500">
            {t.chatDisclaimer}
          </div>
        </div>
      </main>
    </div>
  );
};
