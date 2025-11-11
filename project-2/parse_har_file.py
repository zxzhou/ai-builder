#!/usr/bin/env python3
"""
Parse HAR (HTTP Archive) file exported from browser Network tab
and extract Instagram image URLs, then download them.

Usage:
1. Open Instagram profile in browser
2. Open Developer Tools → Network tab
3. Scroll through entire profile
4. Right-click in Network tab → "Save all as HAR with content"
5. Run: python parse_har_file.py <har_file> <username> [output_dir]
"""

import json
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import Set


def extract_image_urls_from_har(har_file: str) -> Set[str]:
    """Extract Instagram image URLs from HAR file."""
    print(f"📖 Reading HAR file: {har_file}")
    
    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)
    
    image_urls = set()
    
    # HAR structure: har -> log -> entries -> request/response
    entries = har_data.get('log', {}).get('entries', [])
    
    print(f"🔍 Analyzing {len(entries)} network entries...")
    
    for entry in entries:
        request = entry.get('request', {})
        response = entry.get('response', {})
        url = request.get('url', '')
        
        # Check if it's an image from Instagram
        if not url:
            continue
        
        mime_type = response.get('content', {}).get('mimeType', '')
        headers = response.get('headers', [])
        
        # Get content type from headers if not in content
        if not mime_type:
            for header in headers:
                if header.get('name', '').lower() == 'content-type':
                    mime_type = header.get('value', '')
                    break
        
        # Check if it's an image
        is_image = 'image' in mime_type.lower() if mime_type else False
        is_instagram = 'instagram.com' in url or 'cdninstagram.com' in url
        
        if is_image and is_instagram:
            # Skip thumbnails, avatars, icons
            if any(skip in url.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar', 'profile_pic', 'icon']):
                continue
            
            # Prefer high-resolution images
            # Try to get original resolution
            if '/s640x640/' in url:
                original = url.replace('/s640x640/', '/s1080x1080/')
                image_urls.add(original)
            elif '/s480x480/' in url:
                original = url.replace('/s480x480/', '/s1080x1080/')
                image_urls.add(original)
            
            image_urls.add(url)
    
    print(f"✅ Found {len(image_urls)} unique image URLs")
    return image_urls


def download_images(image_urls: Set[str], output_dir: Path):
    """Download images from URLs."""
    print(f"\n📥 Downloading {len(image_urls)} images to {output_dir}...")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.instagram.com/',
    })
    
    downloaded = 0
    failed = 0
    
    for i, url in enumerate(image_urls, 1):
        try:
            print(f"   📥 [{i}/{len(image_urls)}] Downloading...", end='\r')
            
            # Determine file extension
            parsed = urlparse(url)
            path = parsed.path
            ext = Path(path).suffix
            if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                ext = '.jpg'
            
            # Download
            response = session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save
            filename = output_dir / f"image_{i:04d}{ext}"
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            downloaded += 1
            
        except Exception as e:
            failed += 1
            print(f"\n   ⚠️  Failed to download {url}: {e}")
    
    print(f"\n✅ Download complete: {downloaded} successful, {failed} failed")
    return downloaded


def main():
    if len(sys.argv) < 3:
        print("Usage: python parse_har_file.py <har_file> <username> [output_dir]")
        print("\nSteps:")
        print("1. Open Instagram profile in browser")
        print("2. Open Developer Tools (F12) → Network tab")
        print("3. Filter by 'Img' or search for 'cdninstagram'")
        print("4. Scroll through entire profile to load all images")
        print("5. Right-click in Network tab → 'Save all as HAR with content'")
        print("6. Run this script with the HAR file")
        print("\nExample:")
        print("  python parse_har_file.py network_log.har grapeot")
        sys.exit(1)
    
    har_file = sys.argv[1]
    username = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else f"./instagram_downloads/{username}"
    
    if not Path(har_file).exists():
        print(f"❌ HAR file not found: {har_file}")
        sys.exit(1)
    
    # Extract URLs
    image_urls = extract_image_urls_from_har(har_file)
    
    if not image_urls:
        print("❌ No image URLs found in HAR file")
        sys.exit(1)
    
    # Download
    output_path = Path(output_dir)
    download_images(image_urls, output_path)
    
    print(f"\n✅ Complete! Images saved to: {output_path.absolute()}")


if __name__ == "__main__":
    main()

