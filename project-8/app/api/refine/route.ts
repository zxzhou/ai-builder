import { NextRequest, NextResponse } from 'next/server'
import { getAIBuilderClient, scrapeJobDescription } from '@/lib/ai-builder-client'

// Optimized prompt - more concise for faster processing
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
      return NextResponse.json(
        { error: 'Resume bullet points are required' },
        { status: 400 }
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
          return NextResponse.json(
            { error: 'Failed to scrape job description from URL. Please provide the job description text directly.' },
            { status: 400 }
          )
        }
      } catch (error) {
        console.error('Error scraping URL:', error)
        // Fall back to text input if scraping fails
        if (!jobDescription) {
          return NextResponse.json(
            { error: 'Failed to scrape job description from URL. Please provide the job description text directly.' },
            { status: 400 }
          )
        }
      }
    }

    if (!finalJobDescription || !finalJobDescription.trim()) {
      return NextResponse.json(
        { error: 'Job description is required (either text or URL)' },
        { status: 400 }
      )
    }

    const selectedModel = model || 'gemini-2.5-pro'
    const client = getAIBuilderClient()

    const prompt = REFINEMENT_PROMPT
      .replace('{jobDescription}', finalJobDescription)
      .replace('{resumeBullets}', resumeBullets)

    const completion = await client.chat.completions.create({
      model: selectedModel,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.7,
      max_tokens: 1500, // Reduced for faster response
    })

    const optimizedBullets = completion.choices[0]?.message?.content || ''

    if (!optimizedBullets) {
      return NextResponse.json(
        { error: 'Failed to generate optimized resume bullets' },
        { status: 500 }
      )
    }

    return NextResponse.json({ optimizedBullets })
  } catch (error) {
    console.error('Error in refine API:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to refine resume' },
      { status: 500 }
    )
  }
}

