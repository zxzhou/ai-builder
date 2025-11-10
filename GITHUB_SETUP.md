# GitHub Setup Guide

This guide will help you configure Git and GitHub on your laptop.

## Step 1: Configure Git

First, you need to set up your Git identity. Run these commands in your terminal (replace with your actual name and email):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Important**: Use the same email address that you use for your GitHub account.

## Step 2: Check Your Configuration

Verify your settings:

```bash
git config --global user.name
git config --global user.email
```

## Step 3: Set Up GitHub Authentication

GitHub no longer accepts passwords for Git operations. You need to use a Personal Access Token (PAT) or SSH keys.

### Option A: Personal Access Token (Recommended for beginners)

1. Go to GitHub.com and sign in
2. Click your profile picture → **Settings**
3. Scroll down to **Developer settings** (left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name (e.g., "My Laptop")
7. Select scopes: Check **repo** (this gives full control of private repositories)
8. Click **Generate token**
9. **Copy the token immediately** (you won't see it again!)

When you push to GitHub, use your token as the password:
- Username: Your GitHub username
- Password: The token you just created

### Option B: SSH Keys (More secure, recommended for advanced users)

1. Generate an SSH key:
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```
(Press Enter to accept default file location, optionally set a passphrase)

2. Start the ssh-agent:
```bash
eval "$(ssh-agent -s)"
```

3. Add your SSH key to the ssh-agent:
```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your public key:
```bash
cat ~/.ssh/id_ed25519.pub
```

5. Add it to GitHub:
   - Go to GitHub.com → Settings → SSH and GPG keys
   - Click **New SSH key**
   - Paste your public key
   - Click **Add SSH key**

## Step 4: Create a GitHub Repository

1. Go to GitHub.com and click the **+** icon → **New repository**
2. Repository name: `ai-builder`
3. Description: "A collection of AI and automation projects"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 5: Push Your Code

After creating the repository, GitHub will show you commands. Use these (replace `YOUR_USERNAME` with your GitHub username):

```bash
cd /Users/davidzhou/Desktop/ai-builder
git init
git add .
git commit -m "Initial commit: Add project 1 - CVPR 2024 paper scraper"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-builder.git
git push -u origin main
```

When prompted for credentials:
- **Username**: Your GitHub username
- **Password**: Your Personal Access Token (if using HTTPS) or nothing (if using SSH)

## Troubleshooting

### "Permission denied" error
- Make sure you're using a Personal Access Token, not your GitHub password
- Or set up SSH keys as described above

### "Repository not found" error
- Check that the repository name matches exactly
- Verify you have access to the repository

### Need to change remote URL
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/ai-builder.git
```

## Next Steps

After pushing, your code will be on GitHub! You can:
- View it at: `https://github.com/YOUR_USERNAME/ai-builder`
- Clone it on other machines
- Share it with others
- Continue making commits and pushing updates

