'use client'

import { useState, useRef, useEffect } from 'react'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

interface ChatWindowProps {
  chatHistory: ChatMessage[]
  onSendMessage: (message: string) => void
}

export default function ChatWindow({ chatHistory, onSendMessage }: ChatWindowProps) {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const message = input.trim()
    setInput('')
    setIsLoading(true)
    
    try {
      await onSendMessage(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">
          💬 Refine Your Resume
        </h2>
        <p className="text-sm text-gray-600">
          Ask for specific changes to your optimized bullets. Examples:
        </p>
        <div className="mt-2 flex flex-wrap gap-2">
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">"Make it more technical"</span>
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">"Add metrics"</span>
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">"More leadership-focused"</span>
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">"Simplify bullet 2"</span>
        </div>
      </div>
      
      <div className="border border-gray-300 rounded-lg p-4 mb-4 min-h-[300px] max-h-[400px] overflow-y-auto bg-gray-50">
        {chatHistory.length === 0 ? (
          <div className="text-center text-gray-400 py-8">
            <p>Start a conversation to refine your resume bullets</p>
          </div>
        ) : (
          <div className="space-y-4">
            {chatHistory.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-200 rounded-lg px-4 py-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your refinement request..."
          disabled={isLoading}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-semibold py-2 px-6 rounded-lg transition-colors duration-200"
        >
          Send
        </button>
      </form>
    </div>
  )
}

