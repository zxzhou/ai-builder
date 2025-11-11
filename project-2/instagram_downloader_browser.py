#!/usr/bin/env python3
"""
Instagram Image Downloader - Browser-Based Method
Uses Selenium to automate browser, scroll through Instagram profile, and capture image URLs.

This method:
1. Opens a browser (can use existing logged-in session)
2. Navigates to Instagram profile
3. Scrolls to load all images (handles infinite scroll)
4. Captures image URLs from network requests or DOM
5. Downloads all images

Best for: When you're already logged in via browser
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import requests
import re
from pathlib import Path
import json
import sys
from urllib.parse import urlparse
from typing import Set, List


class InstagramBrowserDownloader:
    """Browser-based Instagram image downloader using Selenium."""
    
    def __init__(self, headless=False, use_existing_profile=False, profile_path=None):
        """
        Initialize the browser downloader.
        
        Args:
            headless: Run browser in headless mode (no GUI)
            use_existing_profile: Use existing Chrome profile (to use logged-in session)
            profile_path: Path to Chrome user profile (default: ~/.config/google-chrome/Default)
        """
        self.headless = headless
        self.use_existing_profile = use_existing_profile
        self.profile_path = profile_path
        self.driver = None
        self.image_urls: Set[str] = set()
        
    def setup_driver(self):
        """Set up Chrome driver with appropriate options."""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Use existing profile if specified (to leverage logged-in session)
        if self.use_existing_profile:
            if self.profile_path:
                chrome_options.add_argument(f'--user-data-dir={self.profile_path}')
            else:
                # Default Chrome profile location (macOS)
                import os
                home = os.path.expanduser("~")
                default_profile = os.path.join(home, "Library/Application Support/Google/Chrome/Default")
                if os.path.exists(default_profile):
                    chrome_options.add_argument(f'--user-data-dir={os.path.dirname(default_profile)}')
                    chrome_options.add_argument(f'--profile-directory=Default')
                else:
                    print("⚠️  Default Chrome profile not found. Continuing without existing session...")
        
        # Additional options for better stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Enable performance logging to capture network requests
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        # Set user agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            # Hide webdriver property
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
            print("✅ Browser initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Error setting up browser: {e}")
            print("   Make sure ChromeDriver is installed:")
            print("   brew install chromedriver  # macOS")
            print("   or download from https://chromedriver.chromium.org/")
            return False
    
    def scroll_to_load_all(self, max_scrolls=200, scroll_delay=2.5):
        """
        Scroll through the Instagram profile to load all images.
        Uses incremental scrolling to trigger lazy loading.
        
        Args:
            max_scrolls: Maximum number of scroll attempts
            scroll_delay: Delay between scrolls (seconds)
        """
        print("📜 Scrolling to load all images (this may take a few minutes)...")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_count = 0
        no_change_count = 0
        last_image_count = 0
        consecutive_no_change = 0
        
        while scroll_count < max_scrolls:
            # Scroll incrementally (not all the way to bottom at once)
            # This helps trigger lazy loading better
            current_scroll = self.driver.execute_script("return window.pageYOffset;")
            window_height = self.driver.execute_script("return window.innerHeight;")
            
            # Scroll down by 80% of window height (more gradual)
            scroll_amount = int(window_height * 0.8)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(scroll_delay)
            
            # Also scroll to bottom every 5 scrolls to ensure we reach the end
            if scroll_count % 5 == 0:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_delay + 1)  # Extra wait when scrolling to bottom
            
            # Wait for images to load
            time.sleep(1.5)
            
            # Check if new content loaded
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            current_scroll_pos = self.driver.execute_script("return window.pageYOffset;")
            max_scroll = self.driver.execute_script("return document.body.scrollHeight - window.innerHeight;")
            
            # Count images from network logs to see progress
            try:
                # Try to count visible post containers
                articles = self.driver.find_elements(By.TAG_NAME, "article")
                current_images = len(articles)
            except:
                current_images = 0
            
            # Check if we're at the bottom
            at_bottom = current_scroll_pos >= max_scroll - 100  # Within 100px of bottom
            
            if new_height == last_height:
                no_change_count += 1
                consecutive_no_change += 1
                
                # If we're at bottom AND no new content for several scrolls, we're done
                if at_bottom and consecutive_no_change >= 8:
                    print(f"   ✅ Reached end of page after {scroll_count + 1} scrolls")
                    break
            else:
                consecutive_no_change = 0
                no_change_count = 0
                if current_images > last_image_count:
                    print(f"   📜 Scrolled {scroll_count + 1} times, found {current_images} posts so far...")
                    last_image_count = current_images
                elif scroll_count % 15 == 0:
                    print(f"   📜 Scrolled {scroll_count + 1} times, page height: {new_height}px...")
            
            last_height = new_height
            scroll_count += 1
        
        # Final comprehensive scroll to ensure everything is loaded
        print("   🔄 Final scroll to ensure all content is loaded...")
        for i in range(3):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            # Scroll back up a bit and down again to trigger lazy loads
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
            time.sleep(2)
        
        # One final scroll to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        print(f"✅ Finished scrolling ({scroll_count} scrolls, final page height: {self.driver.execute_script('return document.body.scrollHeight')}px)")
    
    def extract_image_urls_from_dom(self):
        """Extract image URLs from the page DOM using multiple methods."""
        print("🔍 Extracting image URLs from page...")
        
        image_urls = set()
        
        try:
            # Method 1: Find all img tags (most comprehensive)
            img_elements = self.driver.find_elements(By.TAG_NAME, "img")
            print(f"   Found {len(img_elements)} img elements")
            
            for img in img_elements:
                # Try multiple attributes
                for attr in ['src', 'srcset', 'data-src', 'data-srcset']:
                    value = img.get_attribute(attr)
                    if value:
                        # Handle srcset (multiple URLs)
                        if ',' in value:
                            urls = [u.strip().split()[0] for u in value.split(',')]
                        else:
                            urls = [value]
                        
                        for url in urls:
                            if url and ("instagram.com" in url or "cdninstagram.com" in url):
                                # Skip thumbnails and avatars
                                if any(skip in url.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar', 'profile_pic', 'icon']):
                                    continue
                                image_urls.add(url)
            
            # Method 2: Find images in article containers (Instagram posts)
            try:
                articles = self.driver.find_elements(By.TAG_NAME, "article")
                print(f"   Found {len(articles)} article containers")
                for article in articles:
                    imgs = article.find_elements(By.TAG_NAME, "img")
                    for img in imgs:
                        src = img.get_attribute("src") or img.get_attribute("data-src")
                        if src and ("instagram.com" in src or "cdninstagram.com" in src):
                            if not any(skip in src.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar']):
                                image_urls.add(src)
            except Exception as e:
                print(f"   ⚠️  Error extracting from articles: {e}")
            
            # Method 3: Find background images in style attributes
            try:
                elements_with_bg = self.driver.find_elements(By.XPATH, "//*[@style]")
                for elem in elements_with_bg:
                    style = elem.get_attribute("style")
                    if style:
                        # Extract URL from background-image: url(...)
                        urls = re.findall(r'url\(["\']?([^"\']+)["\']?\)', style)
                        for url in urls:
                            if "instagram.com" in url or "cdninstagram.com" in url:
                                if not any(skip in url.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar']):
                                    image_urls.add(url)
            except Exception as e:
                print(f"   ⚠️  Error extracting background images: {e}")
            
            # Method 4: Extract from Instagram's data structures (if available in page source)
            try:
                page_source = self.driver.page_source
                # Look for image URLs in the page source
                url_pattern = r'https://[^"\s]*cdninstagram\.com[^"\s]*\.(jpg|jpeg|png|webp)[^"\s]*'
                found_urls = re.findall(url_pattern, page_source, re.IGNORECASE)
                for match in found_urls:
                    # Reconstruct full URL (pattern might have captured partial)
                    # This is a fallback, so we'll be lenient
                    pass  # Skip this method as it's unreliable
            except:
                pass
            
            # Normalize URLs and get high-resolution versions
            normalized_urls = set()
            for url in image_urls:
                # Skip obvious non-post images
                if any(skip in url.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar', 'profile_pic', 'icon', 'logo']):
                    continue
                
                # Try to get higher resolution version
                # Instagram URLs often have size parameters like s640x640, s1080x1080
                if '/s640x640/' in url:
                    # Try 1080p version
                    high_res = url.replace('/s640x640/', '/s1080x1080/')
                    normalized_urls.add(high_res)
                elif '/s480x480/' in url:
                    high_res = url.replace('/s480x480/', '/s1080x1080/')
                    normalized_urls.add(high_res)
                elif '/s320x320/' in url:
                    high_res = url.replace('/s320x320/', '/s1080x1080/')
                    normalized_urls.add(high_res)
                
                # Also keep original
                normalized_urls.add(url)
            
            self.image_urls.update(normalized_urls)
            print(f"   ✅ Found {len(normalized_urls)} unique image URLs from DOM")
            
        except Exception as e:
            print(f"   ⚠️  Error extracting URLs from DOM: {e}")
            import traceback
            traceback.print_exc()
    
    def extract_image_urls_from_network(self):
        """Extract image URLs from browser network logs (requires performance logging)."""
        print("🔍 Extracting image URLs from network requests...")
        
        try:
            # Get performance logs (requires ChromeOptions with logging)
            logs = self.driver.get_log('performance')
            image_urls = set()
            
            print(f"   Analyzing {len(logs)} network log entries...")
            
            for log in logs:
                try:
                    message = json.loads(log['message'])
                    if message['message']['method'] == 'Network.responseReceived':
                        response = message['message']['params']['response']
                        url = response.get('url', '')
                        mime_type = response.get('mimeType', '')
                        
                        # Check if it's an image from Instagram
                        if url and ('instagram.com' in url or 'cdninstagram.com' in url):
                            # Check mime type or URL pattern
                            is_image = 'image' in mime_type.lower() if mime_type else False
                            looks_like_image = any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) or '/s' in url
                            
                            if is_image or looks_like_image:
                                # Skip small images (thumbnails, icons, avatars)
                                if not any(skip in url.lower() for skip in ['/s150x150/', '/s50x50/', 'avatar', 'profile_pic', 'icon', 'logo']):
                                    image_urls.add(url)
                except (json.JSONDecodeError, KeyError) as e:
                    continue  # Skip malformed logs
            
            self.image_urls.update(image_urls)
            print(f"   ✅ Found {len(image_urls)} image URLs from network")
            
        except Exception as e:
            print(f"   ⚠️  Could not extract from network logs: {e}")
            print("   (This is optional - DOM extraction should work)")
    
    def download_images(self, output_dir: Path):
        """Download all collected image URLs."""
        if not self.image_urls:
            print("❌ No image URLs found to download")
            return 0
        
        print(f"\n📥 Downloading {len(self.image_urls)} images...")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        downloaded = 0
        failed = 0
        
        # Get cookies from browser session
        cookies = self.driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Set headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.instagram.com/',
        })
        
        for i, url in enumerate(self.image_urls, 1):
            try:
                print(f"   📥 [{i}/{len(self.image_urls)}] Downloading...", end='\r')
                
                # Determine file extension
                parsed = urlparse(url)
                path = parsed.path
                ext = Path(path).suffix
                if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                    ext = '.jpg'
                
                # Download image
                response = session.get(url, timeout=30, stream=True)
                response.raise_for_status()
                
                # Save with unique filename
                filename = output_dir / f"image_{i:04d}{ext}"
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                downloaded += 1
                time.sleep(0.5)  # Small delay between downloads
                
            except Exception as e:
                failed += 1
                print(f"\n   ⚠️  Failed to download {url}: {e}")
        
        print(f"\n✅ Download complete: {downloaded} successful, {failed} failed")
        return downloaded
    
    def download_profile(self, username: str, output_dir: str = None):
        """
        Main method to download all images from an Instagram profile.
        
        Args:
            username: Instagram username (without @)
            output_dir: Output directory for images
        """
        if output_dir is None:
            output_dir = f"./instagram_downloads/{username}"
        
        output_path = Path(output_dir)
        
        if not self.setup_driver():
            return False
        
        try:
            # Navigate to profile
            url = f"https://www.instagram.com/{username}/"
            print(f"🌐 Navigating to {url}...")
            self.driver.get(url)
            
            # Wait for page to load
            print("⏳ Waiting for page to load...")
            time.sleep(5)
            
            # Wait for main content to appear
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
                print("✅ Page loaded successfully")
            except TimeoutException:
                print("⚠️  Timeout waiting for content, continuing anyway...")
                # Check if we're being asked to log in
                try:
                    login_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Log in') or contains(text(), 'Sign up')]")
                    if login_elements:
                        print("⚠️  Instagram may be asking for login. Try using --use-existing-profile")
                        print("   (Make sure Chrome is closed first)")
                except:
                    pass
            
            # Check if page loaded successfully
            if "instagram.com" not in self.driver.current_url:
                print("❌ Failed to load Instagram page")
                return False
            
            # Check page height - if it's very small, we might not be seeing all content
            page_height = self.driver.execute_script("return document.body.scrollHeight")
            if page_height < 2000:
                print(f"⚠️  Page height is only {page_height}px - Instagram may be limiting content.")
                print("   Try using --use-existing-profile with Chrome closed to use your logged-in session.")
            
            # Scroll to load all images (use more scrolls to ensure we get everything)
            self.scroll_to_load_all(max_scrolls=200, scroll_delay=2.5)
            
            # Extract image URLs
            self.extract_image_urls_from_dom()
            # Try network extraction (optional)
            try:
                self.extract_image_urls_from_network()
            except:
                pass  # Network extraction is optional
            
            if not self.image_urls:
                print("❌ No images found. The account might be private or the page structure changed.")
                return False
            
            print(f"\n📸 Found {len(self.image_urls)} unique image URLs")
            
            # Download images
            downloaded = self.download_images(output_path)
            
            print(f"\n✅ Complete! Images saved to: {output_path.absolute()}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python instagram_downloader_browser.py <username> [options]")
        print("\nOptions:")
        print("  --headless              Run browser in headless mode (no GUI)")
        print("  --use-existing-profile  Use existing Chrome profile (for logged-in session)")
        print("  --profile-path PATH      Path to Chrome user profile")
        print("  --output-dir DIR         Output directory for images")
        print("\nExample:")
        print("  python instagram_downloader_browser.py grapeot")
        print("  python instagram_downloader_browser.py grapeot --use-existing-profile")
        print("  python instagram_downloader_browser.py grapeot --headless --output-dir ./images")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '').replace('https://www.instagram.com/', '').rstrip('/')
    
    # Parse arguments
    headless = '--headless' in sys.argv
    use_existing_profile = '--use-existing-profile' in sys.argv
    output_dir = None
    profile_path = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output-dir' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--profile-path' and i + 1 < len(sys.argv):
            profile_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    downloader = InstagramBrowserDownloader(
        headless=headless,
        use_existing_profile=use_existing_profile,
        profile_path=profile_path
    )
    
    downloader.download_profile(username, output_dir)


if __name__ == "__main__":
    main()

