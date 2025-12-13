import OpenAI from 'openai'

const AI_BUILDER_BASE_URL = 'https://space.ai-builders.com/backend/v1'

export function getAIBuilderClient() {
  // AI_BUILDER_TOKEN is injected by Koyeb at runtime
  // In Next.js, server-side env vars are available via process.env
  const apiKey = process.env.AI_BUILDER_TOKEN
  
  if (!apiKey) {
    // Log available env vars for debugging (but don't expose sensitive data)
    const envKeys = Object.keys(process.env).sort()
    console.error('AI_BUILDER_TOKEN not found. Available env vars:', envKeys.length)
    console.error('Looking for AI_BUILDER_TOKEN in:', envKeys.filter(k => k.toUpperCase().includes('AI') || k.toUpperCase().includes('BUILDER')))
    throw new Error('AI_BUILDER_TOKEN is not set in environment variables. Please ensure it is configured in your deployment environment.')
  }

  return new OpenAI({
    baseURL: AI_BUILDER_BASE_URL,
    apiKey: apiKey,
  })
}

export async function scrapeJobDescription(url: string): Promise<string> {
  try {
    const client = getAIBuilderClient()
    
    // Use the supermind-agent-v1 model which can extract content from URLs
    const completion = await client.chat.completions.create({
      model: 'supermind-agent-v1',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant that extracts job description text from web pages. Extract only the job description content, removing navigation, ads, and other irrelevant content. Return the clean job description text.'
        },
        {
          role: 'user',
          content: `Please extract the job description from this URL: ${url}. Return only the job description text, formatted clearly.`
        }
      ],
      temperature: 0.3,
      max_tokens: 4000,
    })

    return completion.choices[0]?.message?.content || ''
  } catch (error) {
    console.error('Error scraping job description:', error)
    throw new Error('Failed to scrape job description from URL')
  }
}

