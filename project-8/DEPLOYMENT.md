# Deployment Guide

## Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **All Changes Committed**: All files must be committed and pushed to GitHub
3. **AI Builder Token**: Your `AI_BUILDER_TOKEN` will be automatically injected during deployment

## Deployment Steps

### Step 1: Prepare Your GitHub Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Resume Builder app"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Create a new public repository
   - Name it something like `resume-builder` or `ai-resume-optimizer`

3. **Push Your Code**:
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Gather Deployment Information

You'll need:
1. **GitHub Repository URL**: `https://github.com/your-username/your-repo-name`
2. **Service Name**: A unique name (e.g., `resume-builder`). This becomes your subdomain: `https://resume-builder.ai-builders.space`
3. **Git Branch**: Usually `main` or `master`

### Step 3: Deploy

Ask the AI assistant: "Please deploy my application" and provide:
- Repository URL
- Service name
- Branch name

The AI will handle the deployment using the AI Builder deployment API.

## What Happens During Deployment

1. **Repository Clone**: The system clones your specified branch from GitHub
2. **Docker Build**: Builds a Docker image using your Dockerfile
3. **Deployment**: Deploys to Koyeb platform
4. **Provisioning**: Takes 5-10 minutes
5. **Live**: Your app will be available at `https://your-service-name.ai-builders.space`

## Important Notes

- **PORT Environment Variable**: Your app must use the `PORT` environment variable (already configured)
- **AI_BUILDER_TOKEN**: Automatically injected - don't include it in your code
- **Public Repository**: Repository must be public
- **Resource Limits**: 256 MB RAM limit - keep dependencies lean

## Troubleshooting

### Check Deployment Status
Use the deployment API or portal to check status:
- Status: `queued` → `deploying` → `HEALTHY` (or `ERROR`)

### Common Issues

1. **Build Fails**: Check Dockerfile syntax and dependencies
2. **App Won't Start**: Verify PORT environment variable is used correctly
3. **Timeout**: Check if build process is too slow (optimize Dockerfile)

### Getting Help

Contact instructors with:
- Service name
- Repository URL
- Timestamp of failed deployment
- Error logs (if available)

## Files Created for Deployment

- ✅ `Dockerfile` - Multi-stage build for Next.js
- ✅ `server.js` - Custom server that honors PORT env var
- ✅ `.dockerignore` - Excludes unnecessary files from Docker build
- ✅ `next.config.js` - Updated with standalone output

## Verification

After deployment, verify:
1. App loads at `https://your-service-name.ai-builders.space`
2. API endpoints work correctly
3. Environment variables are properly set

