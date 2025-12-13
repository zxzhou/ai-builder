'use client'

interface JobDescriptionInputProps {
  value: string
  onChange: (value: string) => void
  urlValue: string
  onUrlChange: (value: string) => void
}

export default function JobDescriptionInput({
  value,
  onChange,
  urlValue,
  onUrlChange,
}: JobDescriptionInputProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 h-full flex flex-col">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          📂 Job Description
        </h2>
        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
          Required
        </span>
      </div>
      
      <div className="mb-4">
        <label htmlFor="jd-url" className="block text-sm font-medium text-gray-700 mb-2">
          <span className="flex items-center gap-1">
            Job Posting URL
            <span className="text-gray-400 font-normal">(Optional)</span>
          </span>
        </label>
        <div className="flex items-center gap-2">
          <input
            id="jd-url"
            type="url"
            value={urlValue}
            onChange={(e) => onUrlChange(e.target.value)}
            placeholder="https://example.com/job-posting"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
          />
          {urlValue && (
            <button
              onClick={() => onUrlChange('')}
              className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              title="Clear URL"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        <p className="mt-1 text-xs text-gray-500">
          Paste a job posting URL to automatically extract the description
        </p>
      </div>

      <div className="flex-1 flex flex-col">
        <label htmlFor="jd-text" className="block text-sm font-medium text-gray-700 mb-2">
          Or Paste Job Description Here
        </label>
        <textarea
          id="jd-text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Paste the full job description here...&#10;&#10;Include:&#10;• Job title and requirements&#10;• Required skills and qualifications&#10;• Responsibilities and expectations"
          rows={12}
          className="flex-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-sm"
        />
        <p className="mt-2 text-xs text-gray-500 flex items-center gap-1">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          More details = better optimization
        </p>
      </div>
    </div>
  )
}

