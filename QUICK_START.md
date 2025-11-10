# Quick Start Guide

## Step 1: Configure Git (One-time setup)

Open Terminal and run:

```bash
cd /Users/davidzhou/Desktop/ai-builder
./setup_git.sh
```

Or manually configure:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Important**: Use the same email as your GitHub account.

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-builder`
3. Description: "A collection of AI and automation projects"
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README"
6. Click **Create repository**

## Step 3: Get GitHub Personal Access Token

GitHub requires a token instead of password:

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name: "My Laptop"
4. Check **repo** scope
5. Click **Generate token**
6. **Copy the token** (you won't see it again!)

## Step 4: Push to GitHub

Run these commands (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd /Users/davidzhou/Desktop/ai-builder

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Add project 1 - CVPR 2024 paper scraper"

# Set main branch
git branch -M main

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ai-builder.git

# Push to GitHub
git push -u origin main
```

When prompted:
- **Username**: Your GitHub username
- **Password**: Paste your Personal Access Token

## Done! 🎉

Your code is now on GitHub at: `https://github.com/YOUR_USERNAME/ai-builder`

## Future Updates

To push changes later:

```bash
git add .
git commit -m "Your commit message"
git push
```

## Need Help?

See `GITHUB_SETUP.md` for detailed instructions.

