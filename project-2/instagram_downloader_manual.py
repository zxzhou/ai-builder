#!/usr/bin/env python3
"""
Alternative Instagram Image Downloader (Manual Method)
Uses requests with anti-bot measures as a fallback option.

WARNING: This method is more likely to be blocked. Use instaloader method if possible.
"""

import requests
import json
import re
import time
import random
from pathlib import Path
from urllib.parse import urlparse
import sys


class InstagramDownloader:
    """Manual Instagram downloader with anti-bot measures."""
    
    def __init__(self, delay_min=2, delay_max=5):
        """
        Initialize downloader with anti-bot settings.
        
        Args:
            delay_min: Minimum delay between requests (seconds)
            delay_max: Maximum delay between requests (seconds)
        """
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.session = requests.Session()
        
        # Set realistic browser headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
    
    def random_delay(self):
        """Add random delay to mimic human behavior."""
        delay = random.uniform(self.delay_min, self.delay_max)
        time.sleep(delay)
    
    def get_profile_page(self, username):
        """Fetch the profile page HTML."""
        url = f"https://www.instagram.com/{username}/"
        print(f"🔍 Fetching profile page: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching profile: {e}")
            return None
    
    def extract_json_data(self, html):
        """Extract JSON data from Instagram page."""
        # Instagram embeds data in a <script> tag
        pattern = r'<script type="application/json" data-react-helmet="true">(.*?)</script>'
        matches = re.findall(pattern, html, re.DOTALL)
        
        for match in matches:
            try:
                data = json.loads(match)
                return data
            except json.JSONDecodeError:
                continue
        
        # Alternative: Look for window._sharedData
        pattern = r'window\._sharedData\s*=\s*({.*?});'
        match = re.search(pattern, html)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        return None
    
    def get_image_urls(self, username):
        """Extract image URLs from Instagram profile."""
        html = self.get_profile_page(username)
        if not html:
            return []
        
        # Try to extract JSON data
        data = self.extract_json_data(html)
        
        image_urls = []
        
        # Method 1: Try to find image URLs in JSON
        if data:
            # Navigate through the JSON structure (Instagram's structure varies)
            # This is a simplified approach
            json_str = json.dumps(data)
            # Look for image URLs
            url_pattern = r'https://[^"]*\.(jpg|jpeg|png|webp)[^"]*'
            urls = re.findall(url_pattern, json_str, re.IGNORECASE)
            image_urls.extend([url for url in urls if 'instagram' in url.lower()])
        
        # Method 2: Direct regex search in HTML
        # Look for img tags or background-image URLs
        img_pattern = r'https://[^"\s]*\.(jpg|jpeg|png|webp)[^"\s]*'
        html_urls = re.findall(img_pattern, html, re.IGNORECASE)
        image_urls.extend([url for url in html_urls if 'instagram' in url.lower()])
        
        # Remove duplicates and filter
        unique_urls = list(set(image_urls))
        # Filter to only include actual image URLs (not thumbnails if possible)
        filtered_urls = [url for url in unique_urls if any(x in url for x in ['/p/', '/scontent-', 'cdninstagram'])]
        
        return filtered_urls[:50]  # Limit to first 50 for safety
    
    def download_image(self, url, output_path):
        """Download a single image."""
        try:
            # Update referer header
            self.session.headers['Referer'] = 'https://www.instagram.com/'
            
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Determine file extension
            parsed = urlparse(url)
            ext = Path(parsed.path).suffix or '.jpg'
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                ext = '.jpg'
            
            # Save image
            filename = output_path / f"image_{hash(url) % 100000}{ext}"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return filename
        except Exception as e:
            print(f"⚠️  Error downloading {url}: {e}")
            return None
    
    def download_all(self, username, output_dir=None):
        """Download all images from a profile."""
        if output_dir is None:
            output_dir = f"./instagram_downloads/{username}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📥 Downloading images from @{username}...")
        print(f"💾 Saving to: {output_path.absolute()}")
        print("⚠️  WARNING: This method may be blocked by Instagram.")
        print("   Consider using instaloader method instead.\n")
        
        # Get image URLs
        image_urls = self.get_image_urls(username)
        
        if not image_urls:
            print("❌ No images found. Instagram may have blocked the request or changed their structure.")
            print("   Try using the instaloader method instead.")
            return
        
        print(f"📸 Found {len(image_urls)} image URLs")
        
        # Download images with delays
        downloaded = 0
        for i, url in enumerate(image_urls, 1):
            print(f"📥 Downloading image {i}/{len(image_urls)}...")
            filename = self.download_image(url, output_path)
            if filename:
                downloaded += 1
                print(f"   ✅ Saved: {filename.name}")
            else:
                print(f"   ❌ Failed to download")
            
            # Random delay between downloads
            if i < len(image_urls):
                self.random_delay()
        
        print(f"\n✅ Download complete! {downloaded}/{len(image_urls)} images saved.")
        print(f"📁 Location: {output_path.absolute()}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python instagram_downloader_manual.py <username> [output_dir]")
        print("\nExample:")
        print("  python instagram_downloader_manual.py grapeot")
        print("\n⚠️  WARNING: This method is more likely to be blocked.")
        print("   Use instagram_downloader.py (instaloader) for better results.")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '').replace('https://www.instagram.com/', '').rstrip('/')
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    downloader = InstagramDownloader(delay_min=3, delay_max=6)
    downloader.download_all(username, output_dir)


if __name__ == "__main__":
    main()

