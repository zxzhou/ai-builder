import { NextRequest, NextResponse } from 'next/server'
import { getAIBuilderClient } from '@/lib/ai-builder-client'

export async function POST(request: NextRequest) {
  try {
    const { jobDescription, currentBullets, chatHistory, model } = await request.json()

    if (!currentBullets || typeof currentBullets !== 'string') {
      return NextResponse.json(
        { error: 'Current bullets are required' },
        { status: 400 }
      )
    }

    if (!chatHistory || !Array.isArray(chatHistory) || chatHistory.length === 0) {
      return NextResponse.json(
        { error: 'Chat history is required' },
        { status: 400 }
      )
    }

    const selectedModel = model || 'gemini-2.5-pro'
    const client = getAIBuilderClient()

    // Build the system message with context
    const systemMessage = `You are an expert resume writer helping to refine resume bullet points. 

**Context:**
- Original Job Description: ${jobDescription || 'Not provided'}
- Current Optimized Bullet Points:
${currentBullets}

**Your Task:**
The user will provide refinement requests (e.g., "Make the first bullet more sales-focused", "Add a bullet about project management", "Make it more technical"). 

You should:
1. Understand the user's request
2. Modify the resume bullet points accordingly
3. Return BOTH:
   - The updated bullet points (formatted as markdown with "- " for each bullet)
   - A brief response explaining what you changed

**Output Format:**
Your response should be in this format:
<BULLETS>
[Updated bullet points in markdown format]
</BULLETS>

<RESPONSE>
[Brief explanation of changes made]
</RESPONSE>`

    // Convert chat history to OpenAI format
    const messages = [
      { role: 'system' as const, content: systemMessage },
      ...chatHistory.map((msg: { role: string; content: string }) => ({
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
      })),
    ]

    const completion = await client.chat.completions.create({
      model: selectedModel,
      messages,
      temperature: 0.7,
      max_tokens: 1500, // Reduced for faster response
    })

    const response = completion.choices[0]?.message?.content || ''

    if (!response) {
      return NextResponse.json(
        { error: 'Failed to generate refinement' },
        { status: 500 }
      )
    }

    // Parse the response to extract bullets and explanation
    const bulletsMatch = response.match(/<BULLETS>([\s\S]*?)<\/BULLETS>/)
    const responseMatch = response.match(/<RESPONSE>([\s\S]*?)<\/RESPONSE>/)

    let refinedBullets = currentBullets
    let explanation = 'I\'ve updated the resume bullets based on your request.'

    if (bulletsMatch) {
      refinedBullets = bulletsMatch[1].trim()
    } else {
      // Fallback: try to extract bullets if format is different
      // Look for markdown bullets
      const bulletLines = response
        .split('\n')
        .filter(line => line.trim().startsWith('- ') || line.trim().startsWith('* '))
        .map(line => line.trim())
      
      if (bulletLines.length > 0) {
        refinedBullets = bulletLines.join('\n')
      }
    }

    if (responseMatch) {
      explanation = responseMatch[1].trim()
    }

    return NextResponse.json({
      refinedBullets,
      response: explanation,
    })
  } catch (error) {
    console.error('Error in chat-refine API:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to refine resume' },
      { status: 500 }
    )
  }
}

