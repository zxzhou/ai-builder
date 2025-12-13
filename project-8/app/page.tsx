'use client'

import { useState } from 'react'
import JobDescriptionInput from '@/components/JobDescriptionInput'
import ResumeInput from '@/components/ResumeInput'
import ModelSelector from '@/components/ModelSelector'
import RefinementOutput from '@/components/RefinementOutput'
import ChatWindow from '@/components/ChatWindow'

export default function Home() {
  const [jobDescription, setJobDescription] = useState('')
  const [jobDescriptionUrl, setJobDescriptionUrl] = useState('')
  const [resumeBullets, setResumeBullets] = useState('')
  const [selectedModel, setSelectedModel] = useState('gemini-2.5-pro')
  const [optimizedBullets, setOptimizedBullets] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [chatHistory, setChatHistory] = useState<Array<{role: 'user' | 'assistant', content: string}>>([])

  const clearError = () => setError(null)

  const handleGenerate = async () => {
    if (!jobDescription && !jobDescriptionUrl) {
      setError('Please provide a job description or URL')
      return
    }
    if (!resumeBullets.trim()) {
      setError('Please provide your current resume bullet points')
      return
    }

    setIsGenerating(true)
    setError(null)
    setOptimizedBullets('')
    setChatHistory([])

    try {
      const response = await fetch('/api/refine', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jobDescription,
          jobDescriptionUrl,
          resumeBullets,
          model: selectedModel,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to generate optimized resume')
      }

      const data = await response.json()
      setOptimizedBullets(data.optimizedBullets)
      setChatHistory([
        {
          role: 'assistant',
          content: `I've generated optimized resume bullet points based on the job description. You can now refine them further using the chat below.`
        }
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleChatMessage = async (message: string) => {
    if (!optimizedBullets) {
      setError('Please generate optimized bullets first')
      return
    }

    const userMessage = { role: 'user' as const, content: message }
    setChatHistory(prev => [...prev, userMessage])

    try {
      const response = await fetch('/api/chat-refine', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          jobDescription,
          currentBullets: optimizedBullets,
          chatHistory: [...chatHistory, userMessage],
          model: selectedModel,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to refine resume')
      }

      const data = await response.json()
      setOptimizedBullets(data.refinedBullets)
      setChatHistory(prev => [...prev, {
        role: 'assistant' as const,
        content: data.response
      }])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
      setChatHistory(prev => prev.slice(0, -1)) // Remove user message on error
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-2">
            AI-Powered Resume Builder
          </h1>
          <p className="text-lg text-gray-600">
            Optimize your resume bullet points for any job description
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-red-700 flex items-start gap-3">
            <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div className="flex-1">
              <p className="font-medium">Error</p>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Model Selector - Top */}
        <div className="mb-6">
          <ModelSelector
            value={selectedModel}
            onChange={setSelectedModel}
          />
        </div>

        {/* Input Section - Side by Side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <JobDescriptionInput
            value={jobDescription}
            onChange={(val) => { setJobDescription(val); clearError() }}
            urlValue={jobDescriptionUrl}
            onUrlChange={(val) => { setJobDescriptionUrl(val); clearError() }}
          />
          <ResumeInput
            value={resumeBullets}
            onChange={(val) => { setResumeBullets(val); clearError() }}
          />
        </div>

        {/* Generate Button - Prominent */}
        <div className="mb-6">
          <button
            onClick={handleGenerate}
            disabled={isGenerating || (!jobDescription && !jobDescriptionUrl) || !resumeBullets.trim()}
            className="w-full bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 disabled:from-gray-400 disabled:to-gray-500 text-white font-semibold py-4 px-6 rounded-lg transition-all duration-200 flex items-center justify-center shadow-lg hover:shadow-xl disabled:shadow-none transform hover:scale-[1.02] disabled:transform-none"
          >
            {isGenerating ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Analyzing and Optimizing...</span>
              </>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>Generate Optimized Resume</span>
              </>
            )}
          </button>
          {(!jobDescription && !jobDescriptionUrl) || !resumeBullets.trim() ? (
            <p className="mt-2 text-sm text-center text-gray-500">
              Please fill in both the job description and resume bullets to continue
            </p>
          ) : null}
        </div>

        {/* Output Section */}
        {optimizedBullets || isGenerating ? (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div className="lg:col-span-2">
              <RefinementOutput
                content={optimizedBullets}
                isLoading={isGenerating}
              />
            </div>
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-md p-6 h-full">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  💡 Tips
                </h3>
                <ul className="space-y-3 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Use the chat below to refine specific bullets</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Try: "Make it more technical" or "Add metrics"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Click "Copy" to copy bullets to your resume</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-primary-600 mt-1">•</span>
                    <span>Switch models to see different optimization styles</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <div className="mb-6">
            <RefinementOutput
              content={optimizedBullets}
              isLoading={isGenerating}
            />
          </div>
        )}

        {/* Chat Window */}
        {optimizedBullets && (
          <ChatWindow
            chatHistory={chatHistory}
            onSendMessage={handleChatMessage}
          />
        )}
      </div>
    </main>
  )
}

