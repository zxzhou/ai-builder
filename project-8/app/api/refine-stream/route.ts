import { NextRequest } from 'next/server'
import { getAIBuilderClient, scrapeJobDescription } from '@/lib/ai-builder-client'

// Optimized, more concise prompt for faster processing
const REFINEMENT_PROMPT = `Optimize these resume bullets for the job description. Use strong action verbs, quantify achievements, and match JD requirements.

Job Description:
{jobDescription}

Current Bullets:
{resumeBullets}

Return ONLY optimized bullets in markdown format (one per line, starting with "- "). No explanations.`

export async function POST(request: NextRequest) {
  try {
    const { jobDescription, jobDescriptionUrl, resumeBullets, model } = await request.json()

    if (!resumeBullets || typeof resumeBullets !== 'string' || !resumeBullets.trim()) {
      return new Response(
        JSON.stringify({ error: 'Resume bullet points are required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      )
    }

    let finalJobDescription = jobDescription || ''

    // If URL is provided, try to scrape it first
    if (jobDescriptionUrl && typeof jobDescriptionUrl === 'string' && jobDescriptionUrl.trim()) {
      try {
        const scrapedJD = await scrapeJobDescription(jobDescriptionUrl)
        if (scrapedJD && scrapedJD.trim()) {
          finalJobDescription = scrapedJD
        } else if (!jobDescription) {
          return new Response(
            JSON.stringify({ error: 'Failed to scrape job description from URL. Please provide the job description text directly.' }),
            { status: 400, headers: { 'Content-Type': 'application/json' } }
          )
        }
      } catch (error) {
        console.error('Error scraping URL:', error)
        if (!jobDescription) {
          return new Response(
            JSON.stringify({ error: 'Failed to scrape job description from URL. Please provide the job description text directly.' }),
            { status: 400, headers: { 'Content-Type': 'application/json' } }
          )
        }
      }
    }

    if (!finalJobDescription || !finalJobDescription.trim()) {
      return new Response(
        JSON.stringify({ error: 'Job description is required (either text or URL)' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      )
    }

    const selectedModel = model || 'gemini-2.5-pro'
    const client = getAIBuilderClient()

    const prompt = REFINEMENT_PROMPT
      .replace('{jobDescription}', finalJobDescription)
      .replace('{resumeBullets}', resumeBullets)

    // Create a streaming response
    const stream = await client.chat.completions.create({
      model: selectedModel,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 1500, // Reduced from 2000 for faster response
      stream: true,
    })

    // Create a ReadableStream to send chunks to the client
    const encoder = new TextEncoder()
    const readable = new ReadableStream({
      async start(controller) {
        try {
          let fullContent = ''
          for await (const chunk of stream) {
            const content = chunk.choices[0]?.delta?.content || ''
            if (content) {
              fullContent += content
              // Send chunk to client
              controller.enqueue(encoder.encode(`data: ${JSON.stringify({ content, done: false })}\n\n`))
            }
          }
          // Send final message
          controller.enqueue(encoder.encode(`data: ${JSON.stringify({ content: '', done: true, fullContent })}\n\n`))
          controller.close()
        } catch (error) {
          controller.error(error)
        }
      },
    })

    return new Response(readable, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    })
  } catch (error) {
    console.error('Error in refine-stream API:', error)
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : 'Failed to refine resume' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    )
  }
}

