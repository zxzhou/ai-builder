# Deployment Checklist

## ✅ Pre-Deployment Checklist

### Files Created/Updated:
- ✅ `Dockerfile` - Multi-stage build for Next.js
- ✅ `server.js` - Custom server (honors PORT env var)
- ✅ `.dockerignore` - Excludes unnecessary files
- ✅ `next.config.js` - Updated with standalone output
- ✅ `package.json` - Updated start script
- ✅ `DEPLOYMENT.md` - Deployment guide

### Ready for Deployment:
- ✅ Application code complete
- ✅ Dockerfile configured
- ✅ PORT environment variable support
- ✅ AI_BUILDER_TOKEN will be auto-injected

## 📋 Deployment Steps

### Step 1: GitHub Repository Setup

**If you don't have a GitHub repo yet:**

1. Go to https://github.com/new
2. Create a new **public** repository
3. Name it (e.g., `resume-builder` or `ai-resume-optimizer`)
4. **Don't** initialize with README, .gitignore, or license (we already have these)

**Initialize and push your code:**

```bash
cd /Users/davidzhou/Desktop/ai-builder/project-8

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI-Powered Resume Builder"

# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Gather Deployment Information

You'll need to provide:

1. **GitHub Repository URL**
   - Format: `https://github.com/your-username/your-repo-name`
   - Example: `https://github.com/johndoe/resume-builder`

2. **Service Name**
   - A unique identifier (lowercase, hyphens allowed)
   - This becomes your subdomain: `https://your-service-name.ai-builders.space`
   - Example: `resume-builder` or `my-resume-optimizer`

3. **Git Branch**
   - Usually `main` or `master`
   - The branch containing your code

### Step 3: Deploy

Once you have:
- ✅ Code pushed to GitHub
- ✅ Repository URL
- ✅ Service name
- ✅ Branch name

**Ask me to deploy** by saying:
> "Please deploy my application. Repository: [URL], Service name: [name], Branch: [branch]"

Or I can help you deploy using the AI Builder deployment API.

## 🔍 Verification

After deployment (takes 5-10 minutes):

1. Check status via deployment API or portal
2. Visit your app at: `https://your-service-name.ai-builders.space`
3. Test the application:
   - Enter a job description
   - Enter resume bullets
   - Generate optimized bullets
   - Test chat refinement

## ⚠️ Important Notes

- **Public Repository Required**: Your GitHub repo must be public
- **All Changes Must Be Pushed**: Uncommitted changes won't be deployed
- **AI_BUILDER_TOKEN**: Automatically injected - don't include in code
- **Resource Limit**: 256 MB RAM - keep dependencies lean
- **Provisioning Time**: 5-10 minutes for initial deployment

## 🐛 Troubleshooting

### If deployment fails:

1. **Check Dockerfile**: Ensure it's correct
2. **Verify PORT**: Make sure app uses PORT environment variable
3. **Check Logs**: Review deployment logs for errors
4. **Contact Support**: Share service name, repo URL, and error details

### Common Issues:

- **Build fails**: Check dependencies in package.json
- **App won't start**: Verify PORT is used correctly
- **Timeout**: Optimize Dockerfile for faster builds

## 📞 Need Help?

Contact instructors with:
- Service name
- Repository URL  
- Timestamp of deployment
- Error messages (if any)

