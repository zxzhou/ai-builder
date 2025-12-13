#!/bin/bash

# Test script for Resume Builder API
# Make sure the dev server is running: npm run dev

echo "🧪 Testing Resume Builder API"
echo "================================"
echo ""

# Test 1: Basic refinement
echo "Test 1: Basic Resume Refinement"
echo "--------------------------------"
RESPONSE=$(curl -s -X POST http://localhost:3000/api/refine \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Software Engineer with React and Node.js experience. Looking for someone with 3+ years of experience building scalable web applications.",
    "resumeBullets": "• Built web applications using JavaScript\n• Worked on improving application performance\n• Collaborated with team members",
    "model": "gemini-2.5-pro"
  }')

if echo "$RESPONSE" | grep -q "optimizedBullets"; then
  echo "✅ Test 1 PASSED"
  echo "$RESPONSE" | jq -r '.optimizedBullets' | head -5
else
  echo "❌ Test 1 FAILED"
  echo "$RESPONSE"
fi

echo ""
echo ""

# Test 2: Chat refinement
echo "Test 2: Chat-based Refinement"
echo "--------------------------------"
RESPONSE2=$(curl -s -X POST http://localhost:3000/api/chat-refine \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Software Engineer",
    "currentBullets": "- Built web applications\n- Worked with JavaScript",
    "chatHistory": [
      {"role": "user", "content": "Make the first bullet more technical and add specific technologies"}
    ],
    "model": "gemini-2.5-pro"
  }')

if echo "$RESPONSE2" | grep -q "refinedBullets"; then
  echo "✅ Test 2 PASSED"
  echo "Refined Bullets:"
  echo "$RESPONSE2" | jq -r '.refinedBullets' | head -3
  echo ""
  echo "Response:"
  echo "$RESPONSE2" | jq -r '.response'
else
  echo "❌ Test 2 FAILED"
  echo "$RESPONSE2"
fi

echo ""
echo ""
echo "================================"
echo "✅ API Testing Complete!"
echo ""
echo "Next steps:"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Test the UI manually"
echo "3. Try different models and inputs"

