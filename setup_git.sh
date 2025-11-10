#!/bin/bash
# Git and GitHub Setup Script for AI Builder Project

echo "=========================================="
echo "AI Builder - Git & GitHub Setup"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   On macOS: xcode-select --install"
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Configure Git (if not already configured)
read -p "Enter your name for Git commits: " git_name
read -p "Enter your email for Git commits: " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"

echo ""
echo "✓ Git configured:"
echo "   Name: $(git config --global user.name)"
echo "   Email: $(git config --global user.email)"
echo ""

# Check if repository is already initialized
if [ -d ".git" ]; then
    echo "✓ Git repository already initialized"
else
    echo "Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Create a repository on GitHub.com:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: ai-builder"
echo "   - Choose Public or Private"
echo "   - DO NOT initialize with README"
echo ""
echo "2. After creating the repository, run:"
echo "   git add ."
echo "   git commit -m 'Initial commit: Add project 1 - CVPR 2024 paper scraper'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-builder.git"
echo "   git push -u origin main"
echo ""
echo "3. When prompted for credentials:"
echo "   - Username: Your GitHub username"
echo "   - Password: Your Personal Access Token (not your GitHub password)"
echo ""
echo "For detailed instructions, see GITHUB_SETUP.md"
echo ""

