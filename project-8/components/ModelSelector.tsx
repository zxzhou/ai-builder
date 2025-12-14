'use client'

interface ModelSelectorProps {
  value: string
  onChange: (value: string) => void
}

const MODELS = [
  { value: 'grok-4-fast', label: 'Grok 4 Fast', description: 'X.AI\'s fast Grok model', speed: 'fast' },
  { value: 'deepseek', label: 'DeepSeek', description: 'Fast and cost-effective', speed: 'fast' },
  { value: 'supermind-agent-v1', label: 'Supermind Agent', description: 'Multi-tool agent with web search', speed: 'slow' },
]

const SPEED_LABELS: Record<string, string> = {
  fast: '⚡ Fast',
  medium: '⚖️ Medium',
  slow: '🐌 Slower',
}

export default function ModelSelector({ value, onChange }: ModelSelectorProps) {
  const selectedModel = MODELS.find(m => m.value === value)
  
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex items-center gap-4 flex-wrap">
        <label htmlFor="model-select" className="text-sm font-semibold text-gray-700 whitespace-nowrap">
          🧠 AI Model:
        </label>
        <select
          id="model-select"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="flex-1 min-w-[200px] px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white text-sm"
        >
          {MODELS.map((model) => (
            <option key={model.value} value={model.value}>
              {model.label} {model.recommended ? '(Recommended)' : ''} - {model.description}
            </option>
          ))}
        </select>
        <div className="flex items-center gap-2">
          {selectedModel?.recommended && (
            <span className="px-2 py-1 bg-primary-100 text-primary-700 text-xs font-medium rounded">
              Recommended
            </span>
          )}
          {selectedModel?.speed && (
            <span className={`px-2 py-1 text-xs font-medium rounded ${
              selectedModel.speed === 'fast' ? 'bg-green-100 text-green-700' :
              selectedModel.speed === 'medium' ? 'bg-yellow-100 text-yellow-700' :
              'bg-gray-100 text-gray-700'
            }`}>
              {SPEED_LABELS[selectedModel.speed]}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

