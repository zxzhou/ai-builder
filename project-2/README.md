# Instagram Image Downloader - Project 2

A tool to download all images from a public Instagram account with anti-bot protection measures.

## Overview

This project provides multiple methods to download images from Instagram:

1. **Recommended: `instagram_downloader.py`** - Uses `instaloader` library (best anti-bot protection)
2. **Browser-Based: `instagram_downloader_browser.py`** - Uses Selenium to automate browser (best for existing login)
3. **Alternative: `instagram_downloader_manual.py`** - Manual scraping with requests (fallback option)
4. **HAR Parser: `parse_har_file.py`** - Extract URLs from browser Network tab export

## Features

- ✅ Downloads all images from public Instagram accounts
- ✅ Anti-bot protection (rate limiting, proper headers, delays)
- ✅ Optional login support for better rate limits
- ✅ Automatic directory organization
- ✅ Progress tracking
- ✅ Error handling and resume capability

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **For browser-based method only:** Install ChromeDriver:
```bash
# macOS
brew install chromedriver

# Linux
sudo apt-get install chromium-chromedriver

# Or download from https://chromedriver.chromium.org/
```

## Usage

### Method 1: Using Instaloader (Recommended)

This is the **best method** as it handles anti-bot measures automatically.

#### Basic Usage (No Login)
```bash
python instagram_downloader.py grapeot
```

This will download all images from `https://www.instagram.com/grapeot/` to `./instagram_downloads/grapeot/`

#### With Custom Output Directory
```bash
python instagram_downloader.py grapeot ./my_images
```

#### With Login (Recommended for Better Rate Limits)
```bash
python instagram_downloader.py grapeot --login your_username your_password
```

**Why login?**
- Higher rate limits (less likely to be blocked)
- Access to more content
- More reliable downloads

**Note:** Login credentials are optional. The script works without login for public accounts, but may have stricter rate limits.

### Method 2: Browser-Based (Best for Existing Login) ⭐ NEW

This method uses Selenium to automate a real browser, which is perfect when you're already logged in via web browser.

#### Prerequisites
Install ChromeDriver:
```bash
# macOS
brew install chromedriver

# Or download from https://chromedriver.chromium.org/
```

#### Basic Usage
```bash
python instagram_downloader_browser.py grapeot
```

#### Use Existing Browser Session (Recommended) ⚠️ IMPORTANT
If you're already logged into Instagram in Chrome, use your existing session:
```bash
# IMPORTANT: Close Chrome completely first, then run:
python instagram_downloader_browser.py grapeot --use-existing-profile
```

**Important:** You must close Chrome completely before running with `--use-existing-profile`, otherwise ChromeDriver cannot access the profile.

This will use your logged-in Chrome session, so you don't need to log in again!

**Note:** Instagram may limit the number of posts visible to non-logged-in users. If you're not seeing all images (e.g., only 26-67 out of 86), try using `--use-existing-profile` with Chrome closed to access your logged-in session.

#### Headless Mode (No Browser Window)
```bash
python instagram_downloader_browser.py grapeot --headless
```

#### How It Works
1. Opens a browser (Chrome)
2. Navigates to Instagram profile
3. Automatically scrolls to load all images (handles infinite scroll)
4. Extracts image URLs from DOM and network requests
5. Downloads all images

**Advantages:**
- ✅ Uses real browser (less likely to be blocked)
- ✅ Can use existing logged-in session
- ✅ Handles infinite scroll automatically
- ✅ Captures images from network requests
- ✅ Works with private accounts (if logged in)

### Method 3: Manual HAR Export (Manual Browser Method)

If you prefer to manually export network logs from your browser:

1. Open Instagram profile in Chrome/Firefox
2. Open Developer Tools (F12 or Cmd+Option+I)
3. Go to **Network** tab
4. Filter by "Img" or search for "cdninstagram"
5. **Scroll through the entire profile** to load all images
6. Right-click in Network tab → **"Save all as HAR with content"**
7. Run the parser:
```bash
python parse_har_file.py network_log.har grapeot
```

### Method 4: Manual Scraping (Fallback)

⚠️ **Warning:** This method is more likely to be blocked by Instagram. Use only if other methods don't work.

```bash
python instagram_downloader_manual.py grapeot
```

## Anti-Bot Protection Features

### Instaloader Method
- ✅ Automatic rate limiting
- ✅ Session management
- ✅ Proper HTTP headers
- ✅ Request delays
- ✅ Connection retry logic
- ✅ Handles Instagram's API structure

### Browser-Based Method
- ✅ Uses real browser (Chrome) - looks like human activity
- ✅ Can leverage existing logged-in session
- ✅ Natural scrolling behavior
- ✅ Browser cookies and session management
- ✅ Less likely to be detected as bot

### Manual Method
- ✅ Realistic browser headers
- ✅ Random delays between requests (2-5 seconds)
- ✅ Session management
- ✅ Proper referer headers

## Output Structure

```
instagram_downloads/
└── grapeot/
    ├── image_1.jpg
    ├── image_2.jpg
    ├── image_3.jpg
    └── ...
```

## Best Practices to Avoid Being Blocked

1. **Use the instaloader method** - It's specifically designed for Instagram
2. **Login with your account** - Reduces rate limiting issues
3. **Don't run too frequently** - Space out your downloads
4. **Respect rate limits** - The script includes automatic delays
5. **Use a VPN if needed** - If you're still getting blocked

## Troubleshooting

### "Profile does not exist"
- Check the username is correct (without @)
- Make sure the account is public

### "Login failed" or "Two-factor authentication required"
- Verify your credentials
- If 2FA is enabled, you may need to use an app-specific password
- You can run without login for public accounts

### "Connection error" or Rate Limiting
- Wait a few hours and try again
- Try logging in with your account
- Reduce the number of concurrent requests (if modifying the code)

### "No images found" (Manual method)
- Instagram may have changed their page structure
- Use the instaloader method instead
- The account might be private

### Getting Blocked
- Wait 24-48 hours before trying again
- Use login credentials
- Consider using a VPN
- Use the instaloader method (more reliable)

## Technical Details

### Instaloader Method
- Uses the official `instaloader` library
- Handles Instagram's GraphQL API
- Automatically manages sessions and cookies
- Downloads metadata (optional)

### Manual Method
- Parses HTML and embedded JSON
- Uses regex to extract image URLs
- More fragile but doesn't require external dependencies beyond requests

## Limitations

- **Private accounts**: Require login and following the account
- **Rate limits**: Instagram may temporarily block requests if too aggressive
- **Instagram changes**: If Instagram updates their structure, manual method may break
- **Videos**: Currently only downloads images (can be modified to include videos)

## Legal and Ethical Considerations

- ✅ Only download from **public accounts**
- ✅ Respect copyright and intellectual property
- ✅ Don't use downloaded images for commercial purposes without permission
- ✅ Follow Instagram's Terms of Service
- ✅ Use responsibly and don't abuse the service

## Example

Download all images from Yan's account:

```bash
# Recommended method
python instagram_downloader.py grapeot

# Or with login for better results
python instagram_downloader.py grapeot --login your_username your_password
```

Images will be saved to `./instagram_downloads/grapeot/`

## License

This project is part of the AI Builder collection and is for educational purposes only.

