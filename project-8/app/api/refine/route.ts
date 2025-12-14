import { NextRequest, NextResponse } from 'next/server'
import { getAIBuilderClient, scrapeJobDescription } from '@/lib/ai-builder-client'

/**
 * Deduplicates bullet points by:
 * 1. Extracting all bullet lines
 * 2. Removing exact duplicates
 * 3. Removing near-duplicates (similar content)
 * 4. Limiting to the expected number of bullets
 */
function deduplicateBullets(response: string, originalBullets: string): string {
  // Extract bullet lines (starting with - or *)
  const bulletLines = response
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.startsWith('- ') || line.startsWith('* '))
    .map(line => line.replace(/^[-*]\s*/, '').trim())

  if (bulletLines.length === 0) {
    // Fallback: try to extract any lines that look like bullets
    const fallbackLines = response
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 20 && !line.toLowerCase().includes('optimize') && !line.toLowerCase().includes('bullet'))
    
    if (fallbackLines.length > 0) {
      return fallbackLines
        .slice(0, Math.min(fallbackLines.length, 10))
        .map(line => `- ${line}`)
        .join('\n')
    }
    return response
  }

  // Count original bullets
  const originalCount = originalBullets
    .split('\n')
    .map(line => line.trim())
    .filter(line => line.length > 0)
    .length

  // Remove exact duplicates (case-insensitive)
  const seen = new Set<string>()
  const uniqueBullets: string[] = []

  for (const bullet of bulletLines) {
    const normalized = bullet.toLowerCase().trim()
    
    // Skip if exact duplicate
    if (seen.has(normalized)) {
      continue
    }

    // Skip if very similar to existing bullet (fuzzy match)
    let isDuplicate = false
    for (const existing of Array.from(seen)) {
      // Check if bullets are very similar (more than 80% similar)
      const similarity = calculateSimilarity(normalized, existing)
      if (similarity > 0.8) {
        isDuplicate = true
        break
      }
    }

    if (!isDuplicate) {
      seen.add(normalized)
      uniqueBullets.push(bullet)
    }
  }

  // Limit to original count + 2 (allow slight variation)
  const maxBullets = Math.min(uniqueBullets.length, originalCount + 2)
  const finalBullets = uniqueBullets.slice(0, maxBullets)

  return finalBullets.map(bullet => `- ${bullet}`).join('\n')
}

/**
 * Calculate similarity between two strings (simple Jaccard-like similarity)
 */
function calculateSimilarity(str1: string, str2: string): number {
  const words1 = new Set(str1.split(/\s+/).filter(w => w.length > 3))
  const words2 = new Set(str2.split(/\s+/).filter(w => w.length > 3))
  
  if (words1.size === 0 && words2.size === 0) return 1
  if (words1.size === 0 || words2.size === 0) return 0

  const intersection = new Set(Array.from(words1).filter(w => words2.has(w)))
  const union = new Set([...Array.from(words1), ...Array.from(words2)])
  
  return intersection.size / union.size
}

// Optimized prompt - more concise for faster processing
const REFINEMENT_PROMPT = `Optimize these resume bullets for the job description. Use strong action verbs, quantify achievements, and match JD requirements.

Job Description:
{jobDescription}

Current Bullets:
{resumeBullets}

Return ONLY optimized bullets in markdown format (one per line, starting with "- "). 
- Return exactly the same number of bullets as input (one optimized bullet per input bullet)
- Do NOT repeat bullets
- Do NOT add explanations or reasoning
- Return only the bullet points, nothing else`

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

    let optimizedBullets = completion.choices[0]?.message?.content || ''

    if (!optimizedBullets) {
      return NextResponse.json(
        { error: 'Failed to generate optimized resume bullets' },
        { status: 500 }
      )
    }

    // Post-process to remove duplicates and clean up response
    optimizedBullets = deduplicateBullets(optimizedBullets, resumeBullets)

    return NextResponse.json({ optimizedBullets })
  } catch (error) {
    console.error('Error in refine API:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to refine resume' },
      { status: 500 }
    )
  }
}

