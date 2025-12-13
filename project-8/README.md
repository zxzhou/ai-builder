# AI-Powered Resume Builder & Refiner

A complete, full-stack web application that uses AI to optimize resume bullet points for specific job descriptions. Built with Next.js, TypeScript, Tailwind CSS, and integrated with the AI Builder API.

## 🎯 Features

- **Job Description Input**: Support for both text input and URL scraping
- **Resume Optimization**: AI-powered refinement of resume bullet points
- **Multiple LLM Models**: Choose from Gemini, Grok, DeepSeek, and Supermind Agent
- **Interactive Chat Refinement**: Continuously refine your resume with natural language requests
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Updates**: See your optimized resume bullets update in real-time

## 🛠️ Technology Stack

- **Frontend**: Next.js 14 with React and TypeScript
- **Styling**: Tailwind CSS
- **Backend**: Next.js API Routes
- **LLM Integration**: AI Builder API (OpenAI-compatible)
- **Deployment Ready**: Configured for production deployment

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- AI Builder API token (provided via environment variable)

## 🚀 Getting Started

### 1. Install Dependencies

```bash
npm install
# or
yarn install
```

### 2. Set Up Environment Variables

Create a `.env.local` file in the project root:

```bash
AI_BUILDER_TOKEN=your_token_here
```

**Note**: The AI Builder token should be obtained from your AI Builder account. If you're using the MCP server, you can retrieve it using the `get_auth_token` tool.

### 3. Run the Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Build for Production

```bash
npm run build
npm start
```

## 📖 Usage Guide

### Step 1: Input Job Description

You can provide the job description in two ways:
- **Text Input**: Paste the job description directly into the text area
- **URL Input**: Provide a URL to a job posting (the system will attempt to scrape it)

**Note**: If both are provided, the URL takes priority. If URL scraping fails, it falls back to the text input.

### Step 2: Input Current Resume Bullets

Enter your current resume bullet points, one per line. For example:
```
• Led a team of 5 developers to deliver a new feature
• Increased user engagement by 30% through A/B testing
• Optimized database queries reducing load time by 50%
```

### Step 3: Select AI Model

Choose from available models:
- **Gemini 2.5 Pro**: Google's advanced Gemini model (recommended)
- **Grok 4 Fast**: X.AI's fast Grok model
- **DeepSeek**: Fast and cost-effective
- **Supermind Agent**: Multi-tool agent with web search capabilities

### Step 4: Generate Optimized Resume

Click "Generate Optimized Resume" to get AI-optimized bullet points tailored to the job description.

### Step 5: Refine with Chat

Use the interactive chat window to further refine your resume. Try commands like:
- "Make the first bullet more sales-focused"
- "Add a bullet about project management"
- "Make it more technical"
- "Quantify the achievements in bullet 2"

## 🏗️ Project Structure

```
project-8/
├── app/
│   ├── api/
│   │   ├── refine/          # Initial resume refinement endpoint
│   │   ├── chat-refine/     # Chat-based refinement endpoint
│   │   └── scrape-jd/       # Job description URL scraping endpoint
│   ├── globals.css          # Global styles with Tailwind
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Main page component
├── components/
│   ├── JobDescriptionInput.tsx
│   ├── ResumeInput.tsx
│   ├── ModelSelector.tsx
│   ├── RefinementOutput.tsx
│   └── ChatWindow.tsx
├── lib/
│   └── ai-builder-client.ts # AI Builder API client
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── README.md
```

## 🔧 API Endpoints

### POST `/api/refine`

Refines resume bullet points based on job description.

**Request Body:**
```json
{
  "jobDescription": "string (optional)",
  "jobDescriptionUrl": "string (optional)",
  "resumeBullets": "string (required)",
  "model": "string (optional, default: 'gemini-2.5-pro')"
}
```

**Response:**
```json
{
  "optimizedBullets": "string"
}
```

### POST `/api/chat-refine`

Refines resume bullets based on chat conversation.

**Request Body:**
```json
{
  "jobDescription": "string",
  "currentBullets": "string",
  "chatHistory": [{"role": "user|assistant", "content": "string"}],
  "model": "string"
}
```

**Response:**
```json
{
  "refinedBullets": "string",
  "response": "string"
}
```

### POST `/api/scrape-jd`

Scrapes job description from a URL.

**Request Body:**
```json
{
  "url": "string"
}
```

**Response:**
```json
{
  "jobDescription": "string"
}
```

## 🎨 Customization

### Styling

The application uses Tailwind CSS. Customize colors and styles in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
      },
    },
  },
}
```

### AI Models

Available models are defined in `components/ModelSelector.tsx`. You can add or modify models there.

## 🐛 Troubleshooting

### Environment Variable Issues

If you see errors about `AI_BUILDER_TOKEN`:
1. Ensure `.env.local` exists in the project root
2. Verify the token is correct and has proper permissions
3. Restart the development server after adding/changing environment variables

### URL Scraping Fails

If URL scraping doesn't work:
1. Ensure the URL is publicly accessible
2. Try providing the job description text directly
3. Some websites may block automated scraping

### API Errors

If you encounter API errors:
1. Check your AI Builder token is valid
2. Verify you have sufficient API credits/quota
3. Check the browser console and server logs for detailed error messages

## 📝 License

This project is part of the AI Builder course materials.

## 🤝 Contributing

This is a course project. For questions or issues, please contact your instructor.

## 🔗 Related Resources

- [AI Builder API Documentation](https://www.ai-builders.com/resources/students-backend/openapi.json)
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

