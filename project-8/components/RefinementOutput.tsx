'use client'

import { useEffect, useRef, useState } from 'react'

interface RefinementOutputProps {
  content: string
  isLoading: boolean
}

export default function RefinementOutput({ content, isLoading }: RefinementOutputProps) {
  const contentRef = useRef<HTMLDivElement>(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight
    }
  }, [content])

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          ✨ Optimized Resume Bullets
        </h2>
        {content && !isLoading && (
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 text-sm bg-primary-50 text-primary-700 rounded-lg hover:bg-primary-100 transition-colors flex items-center gap-2"
            title="Copy to clipboard"
          >
            {copied ? (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Copied!
              </>
            ) : (
              <>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy
              </>
            )}
          </button>
        )}
      </div>
      <div
        ref={contentRef}
        className="flex-1 border border-gray-300 rounded-lg p-4 min-h-[400px] max-h-[600px] overflow-y-auto bg-gray-50"
      >
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <svg className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p className="text-gray-600">Analyzing your resume and job description...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
            </div>
          </div>
        ) : content ? (
          <div className="prose prose-sm max-w-none">
            <div className="whitespace-pre-wrap text-gray-800">{content}</div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            <p>Generated optimized bullet points will appear here</p>
          </div>
        )}
      </div>
    </div>
  )
}

