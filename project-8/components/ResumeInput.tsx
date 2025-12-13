'use client'

interface ResumeInputProps {
  value: string
  onChange: (value: string) => void
}

export default function ResumeInput({ value, onChange }: ResumeInputProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 h-full flex flex-col">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          📄 Your Resume Bullets
        </h2>
        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded">
          Required
        </span>
      </div>
      <div className="flex-1 flex flex-col">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Enter each bullet point on a new line...&#10;&#10;Example:&#10;• Led a team of 5 developers to deliver a new feature&#10;• Increased user engagement by 30% through A/B testing&#10;• Optimized database queries reducing load time by 50%&#10;&#10;💡 Tip: Include your actual achievements and responsibilities. The AI will enhance them to match the job description."
          rows={12}
          className="flex-1 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none text-sm"
        />
        <div className="mt-2 flex items-center justify-between">
          <p className="text-xs text-gray-500 flex items-center gap-1">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            One bullet per line
          </p>
          <p className="text-xs text-gray-400">
            {value.split('\n').filter(line => line.trim()).length} bullet{value.split('\n').filter(line => line.trim()).length !== 1 ? 's' : ''}
          </p>
        </div>
      </div>
    </div>
  )
}

