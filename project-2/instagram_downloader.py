#!/usr/bin/env python3
"""
Instagram Image Downloader
Downloads all images from a public Instagram account with anti-bot protection.

This script uses instaloader, which handles:
- Rate limiting
- Session management
- Proper headers
- Login (optional, for better rate limits)
"""

import instaloader
import os
import sys
import time
import shutil
from pathlib import Path


def download_instagram_images(username, output_dir=None, login_username=None, login_password=None):
    """
    Download all images from a public Instagram account.
    
    Args:
        username: Instagram username (without @)
        output_dir: Directory to save images (default: ./instagram_downloads/{username})
        login_username: Optional Instagram username for login (reduces rate limiting)
        login_password: Optional Instagram password for login
    """
    # Set up output directory
    if output_dir is None:
        output_dir = f"./instagram_downloads/{username}"
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📥 Downloading images from @{username}...")
    print(f"💾 Saving to: {output_path.absolute()}")
    
    # Create Instaloader instance
    # Note: Instaloader will save to ./{username}/ by default
    # We'll move files to output_path after download
    loader = instaloader.Instaloader(
        download_videos=False,  # Only download images
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,  # Set to True if you want JSON metadata
        compress_json=False,
        post_metadata_txt_pattern="",
        storyitem_metadata_txt_pattern="",
        max_connection_attempts=3,
        request_timeout=30.0,
    )
    
    # Optional: Login to reduce rate limiting
    # Note: Login is optional but recommended for better rate limits
    if login_username and login_password:
        try:
            print(f"🔐 Logging in as @{login_username}...")
            loader.login(login_username, login_password)
            print("✅ Login successful!")
        except instaloader.exceptions.BadCredentialsException:
            print("❌ Login failed: Invalid credentials. Continuing without login...")
        except instaloader.exceptions.TwoFactorAuthRequiredException:
            print("❌ Login failed: Two-factor authentication required.")
            print("   Please use the alternative method or disable 2FA temporarily.")
            sys.exit(1)
        except Exception as e:
            print(f"⚠️  Login error: {e}. Continuing without login...")
    else:
        print("ℹ️  Running without login (may have stricter rate limits)")
    
    try:
        # Get profile
        print(f"🔍 Fetching profile @{username}...")
        profile = instaloader.Profile.from_username(loader.context, username)
        
        if not profile.is_private or (login_username and login_password):
            print(f"✅ Found profile: {profile.full_name or username}")
            print(f"📊 Posts: {profile.mediacount}")
            
            # Download posts
            print("\n📥 Starting download...")
            loader.download_profile(username, profile_pic=False, download_stories=False)
            
            # Move files from instaloader's default directory to our output directory
            # Instaloader saves to ./{username}/ by default
            default_dir = Path(username)
            if default_dir.exists() and default_dir.is_dir():
                # Move all image files
                moved_count = 0
                for file in default_dir.iterdir():
                    if file.is_file():
                        # Only move image files
                        if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']:
                            dest = output_path / file.name
                            if not dest.exists():
                                shutil.move(str(file), str(dest))
                                moved_count += 1
                            else:
                                file.unlink()  # Remove duplicate
                
                # Try to remove the directory if empty
                try:
                    if not any(default_dir.iterdir()):
                        default_dir.rmdir()
                except:
                    pass
                
                if moved_count > 0:
                    print(f"📦 Moved {moved_count} images to output directory")
            
            print(f"\n✅ Download complete! Images saved to: {output_path.absolute()}")
            
            # Count downloaded images
            image_count = len(list(output_path.glob("*.jpg"))) + \
                         len(list(output_path.glob("*.jpeg"))) + \
                         len(list(output_path.glob("*.png"))) + \
                         len(list(output_path.glob("*.webp")))
            print(f"📸 Total images downloaded: {image_count}")
            
        else:
            print(f"❌ Profile @{username} is private. Cannot download without login.")
            sys.exit(1)
            
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"❌ Profile @{username} does not exist.")
        sys.exit(1)
    except instaloader.exceptions.ConnectionException as e:
        print(f"❌ Connection error: {e}")
        print("   This might be due to rate limiting. Try again later or use login.")
        sys.exit(1)
    except instaloader.exceptions.LoginRequiredException:
        print(f"❌ Login required to access @{username}")
        print("   Please provide login credentials or the account may be private.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python instagram_downloader.py <username> [output_dir] [--login username password]")
        print("\nExample:")
        print("  python instagram_downloader.py grapeot")
        print("  python instagram_downloader.py grapeot ./my_images")
        print("  python instagram_downloader.py grapeot --login my_username my_password")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '').replace('https://www.instagram.com/', '').rstrip('/')
    
    output_dir = None
    login_username = None
    login_password = None
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--login' and i + 2 < len(sys.argv):
            login_username = sys.argv[i + 1]
            login_password = sys.argv[i + 2]
            i += 3
        elif output_dir is None:
            output_dir = sys.argv[i]
            i += 1
        else:
            i += 1
    
    download_instagram_images(username, output_dir, login_username, login_password)


if __name__ == "__main__":
    main()

