import OpenAI from 'openai'

const AI_BUILDER_BASE_URL = 'https://space.ai-builders.com/backend/v1'

export function getAIBuilderClient() {
  // Try multiple ways to get the token (for different deployment scenarios)
  const apiKey = process.env.AI_BUILDER_TOKEN || 
                 process.env.NEXT_PUBLIC_AI_BUILDER_TOKEN ||
                 process.env['AI_BUILDER_TOKEN']
  
  if (!apiKey) {
    console.error('AI_BUILDER_TOKEN not found in environment variables')
    console.error('Available env vars:', Object.keys(process.env).filter(k => k.includes('AI') || k.includes('BUILDER')))
    throw new Error('AI_BUILDER_TOKEN is not set in environment variables')
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

