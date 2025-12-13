import { NextRequest, NextResponse } from 'next/server'
import { scrapeJobDescription } from '@/lib/ai-builder-client'

export async function POST(request: NextRequest) {
  try {
    const { url } = await request.json()

    if (!url || typeof url !== 'string') {
      return NextResponse.json(
        { error: 'URL is required' },
        { status: 400 }
      )
    }

    const jobDescription = await scrapeJobDescription(url)
    
    return NextResponse.json({ jobDescription })
  } catch (error) {
    console.error('Error in scrape-jd API:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to scrape job description' },
      { status: 500 }
    )
  }
}

