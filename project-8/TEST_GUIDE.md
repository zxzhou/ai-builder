# Testing Guide

## ✅ Server Status

The development server is running at: **http://localhost:3000**

## 🧪 Manual Testing Steps

### 1. Test the UI Components

1. **Open the application**: Navigate to http://localhost:3000
2. **Verify all components are visible**:
   - ✅ Job Description input (text area + URL field)
   - ✅ Resume Bullet Points input
   - ✅ Model Selector dropdown
   - ✅ Generate button
   - ✅ Output area (initially empty)

### 2. Test Basic Functionality

#### Test Case 1: Text Input Only
1. **Job Description**: Paste this sample JD:
```
We are looking for a Senior Software Engineer with 5+ years of experience in full-stack development. 
The ideal candidate should have:
- Strong experience with React and Node.js
- Experience with cloud platforms (AWS, Azure)
- Leadership experience managing teams
- Excellent problem-solving skills
```

2. **Resume Bullets**: Enter these sample bullets:
```
• Worked on web applications using JavaScript
• Helped improve application performance
• Collaborated with team members on projects
• Used various technologies to build features
```

3. **Model**: Keep default (Gemini 2.5 Pro)
4. **Click "Generate Optimized Resume"**
5. **Expected**: 
   - Loading spinner appears
   - Optimized bullets appear in output area
   - Chat window appears below

#### Test Case 2: URL Input
1. **JD URL**: Try a job posting URL (optional - may not work for all sites)
2. **Resume Bullets**: Same as above
3. **Click Generate**
4. **Expected**: System attempts to scrape URL, falls back to text if needed

#### Test Case 3: Chat Refinement
1. After generating optimized bullets, try these chat commands:
   - "Make the first bullet more technical"
   - "Add more metrics to the second bullet"
   - "Make it sound more leadership-focused"

2. **Expected**: 
   - Bullets update in real-time
   - Chat history shows conversation
   - Assistant provides explanations

### 3. Test Error Handling

#### Test Case 4: Missing Inputs
1. **Leave Job Description empty** → Click Generate
   - Expected: Error message appears

2. **Leave Resume Bullets empty** → Click Generate
   - Expected: Error message appears

3. **Fill both fields** → Error should clear

### 4. Test Model Switching

#### Test Case 5: Different Models
1. Generate with "Gemini 2.5 Pro"
2. Change to "Grok 4 Fast"
3. Generate again with same inputs
4. **Expected**: Different output (may vary slightly)

## 🔍 API Testing

### Test API Endpoints Directly

#### Test `/api/refine` endpoint:

```bash
curl -X POST http://localhost:3000/api/refine \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Software Engineer with React experience",
    "resumeBullets": "• Built web applications\n• Worked with JavaScript",
    "model": "gemini-2.5-pro"
  }'
```

**Expected Response:**
```json
{
  "optimizedBullets": "- Optimized bullet points here..."
}
```

#### Test `/api/chat-refine` endpoint:

```bash
curl -X POST http://localhost:3000/api/chat-refine \
  -H "Content-Type: application/json" \
  -d '{
    "jobDescription": "Software Engineer",
    "currentBullets": "- Built web applications\n- Worked with JavaScript",
    "chatHistory": [
      {"role": "user", "content": "Make it more technical"}
    ],
    "model": "gemini-2.5-pro"
  }'
```

**Expected Response:**
```json
{
  "refinedBullets": "- Updated bullets...",
  "response": "Explanation of changes..."
}
```

## 🐛 Common Issues & Solutions

### Issue: "AI_BUILDER_TOKEN is not set"
**Solution**: Check that `.env.local` exists and contains the token

### Issue: API returns 500 error
**Solution**: 
- Check server logs in terminal
- Verify token is valid
- Check network connectivity

### Issue: URL scraping fails
**Solution**: This is expected for some sites. Use text input instead.

### Issue: Slow response times
**Solution**: 
- Normal for LLM calls (can take 10-30 seconds)
- Try a faster model like "Grok 4 Fast"

## ✅ Success Criteria

The application is working correctly if:
- ✅ All UI components render properly
- ✅ Generate button produces optimized bullets
- ✅ Chat refinement updates bullets in real-time
- ✅ Error messages appear for invalid inputs
- ✅ Model switching works
- ✅ Responsive design works on mobile/desktop

## 📊 Performance Benchmarks

- **Initial generation**: 10-30 seconds (depends on model)
- **Chat refinement**: 5-15 seconds
- **Page load**: < 1 second

