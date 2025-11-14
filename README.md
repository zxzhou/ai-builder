# AI Builder

A collection of AI and automation projects for web scraping, data extraction, and more.

## Projects

### [Project 1: CVPR 2024 Paper Scraper](./project-1/)

A web scraper to extract paper information from the CVPR 2024 Open Access website. Extracts titles, authors, abstracts, and links to PDFs/supplementary materials.

**Features:**
- Parallel processing for fast extraction
- Incremental saving with resume capability
- Automatic duplicate prevention

### [Project 2: Instagram Image Downloader](./project-2/)

A tool to download all images from public Instagram accounts with anti-bot protection. Uses instaloader library for reliable downloads.

**Features:**
- Anti-bot protection (rate limiting, proper headers)
- Optional login support for better rate limits
- Automatic directory organization
- Progress tracking

### [Project 3: Search Query Redirect Tool](./project-3/)

A JavaScript tool that enhances your web search experience by redirecting search queries to alternative search engines when results are unsatisfactory. Automatically extracts queries from major search engines and redirects to your preferred alternative.

**Features:**
- Automatic query extraction from multiple search engines
- Support for 10+ alternative search engines
- Works as bookmarklet, browser extension, or console script
- Easy one-click redirect functionality

### [Project 4: Image Analyzer](./project-4/)

A desktop application that uses Google's Gemini AI to analyze images based on custom prompts. Built with Python and Tkinter, this tool provides an intuitive graphical interface for image analysis tasks.

**Features:**
- Custom prompts for flexible image analysis
- Easy image selection with file browser
- Real-time AI-powered analysis using Gemini 2.5 Flash Lite
- User-friendly GUI built with Tkinter
- Secure API key management with environment variables

### [Project 5: Pi Day Challenge Circle Drawer](./project-5/)

A Python program that draws a near-perfect circle in the [Pi Day Challenge game](https://yage.ai/genai/pi.html) to achieve a high rank. Uses mathematical precision to calculate optimal center point and radius, then draws perfectly smooth circles using browser automation.

**Features:**
- Two versions: Playwright (recommended) and PyAutoGUI
- Optimal circle calculation (center at canvas center, 85% radius)
- High precision: 1000 points (Playwright) or 720 points (PyAutoGUI)
- Perfect circle closure for accurate Pi calculation
- Smooth drawing with no zigzag artifacts (Playwright version)
- Auto browser control (Playwright version)

## Getting Started

Each project has its own README with specific installation and usage instructions. Navigate to the project folder for details.

## Requirements

- Python 3.9+
- pip
- Git (for version control)

## License

This collection is open source and available for educational purposes.
