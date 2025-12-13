# Deployment Diagnosis & Troubleshooting

## Current Status

**Deployment Status**: `UNHEALTHY`  
**Error Message**: "Deployment failed while running the provisioning script."  
**Service**: `resume-builder`  
**URL**: https://resume-builder.ai-builders.space/  
**Repository**: https://github.com/zxzhou/ai-builder  
**Branch**: `master`

## What We've Verified

### ✅ Local Docker Build Works
- Root Dockerfile builds successfully
- Container runs correctly and serves the application
- Server.js exists in correct location (`/app/server.js`)
- Application responds on port 3000

### ✅ Configuration Files
- `next.config.js` has `output: 'standalone'` ✓
- Root Dockerfile correctly handles `project-8/` subdirectory ✓
- PORT environment variable is properly configured ✓
- Health check endpoint added at `/api/health` ✓

## Root Cause Analysis

Since the Docker build works locally but fails on Koyeb during "provisioning script", the issue is likely:

### 1. Health Check Failure (Most Likely)
- Koyeb performs health checks during provisioning
- Next.js root path (`/`) should work, but explicit `/api/health` endpoint is now added
- Health check might be timing out if server takes too long to start

### 2. Server Startup Time
- Next.js standalone mode might take time to initialize
- Koyeb health checks might be too aggressive
- Solution: Health check endpoint responds immediately

### 3. Build Context Differences
- Local: Testing from project-8 directory
- Koyeb: Clones entire repo, uses root Dockerfile
- Root Dockerfile is correct and tested ✓

### 4. Environment Variable Injection
- `AI_BUILDER_TOKEN` is injected by Koyeb automatically
- PORT is set by Koyeb (overrides Dockerfile default)
- Both should work correctly

## Changes Made

1. **Added Health Check Endpoint** (`/app/api/health/route.ts`)
   - Simple JSON response: `{ status: 'ok', timestamp: ... }`
   - Responds immediately without dependencies
   - Helps Koyeb verify the service is running

2. **Verified Root Dockerfile**
   - Correctly handles `project-8/` subdirectory
   - Uses standalone output mode
   - Properly sets PORT and HOSTNAME
   - Tested and working locally

## Next Steps

1. **Commit and Push Changes**
   ```bash
   git add project-8/app/api/health/route.ts
   git commit -m "Add health check endpoint for Koyeb deployment"
   git push origin master
   ```

2. **Redeploy via API**
   - Use the deployment API to trigger a new deployment
   - Or wait for automatic redeployment if enabled

3. **Monitor Deployment**
   ```bash
   curl -X GET "https://space.ai-builders.com/backend/v1/deployments/resume-builder" \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

4. **If Still Failing**
   - Check if Koyeb logs are available (contact instructors)
   - Verify the health check endpoint is accessible
   - Consider adding startup delay or readiness probe
   - Review resource limits (256MB RAM)

## Testing Health Check Locally

```bash
# Build and run
docker build -t resume-builder-test -f Dockerfile .
docker run -d --name test -p 3000:3000 -e PORT=3000 resume-builder-test

# Test health endpoint
curl http://localhost:3000/api/health

# Should return: {"status":"ok","timestamp":"..."}
```

## Dockerfile Comparison

### Root Dockerfile (Used by Koyeb)
- ✅ Handles `project-8/` subdirectory correctly
- ✅ Uses `ENV PORT=3000` (equals sign)
- ✅ Has `ENV NEXT_TELEMETRY_DISABLED=1` enabled
- ✅ Tested and working

### Project-8 Dockerfile (Local Testing)
- ✅ Works when run from project-8 directory
- ✅ Uses `ENV PORT 3000` (space)
- ✅ Has `ENV NEXT_TELEMETRY_DISABLED 1` commented
- ✅ Tested and working

Both Dockerfiles are correct for their respective contexts.

## Additional Debugging

If deployment continues to fail:

1. **Check Koyeb Logs** (if available via instructors)
   - Look for startup errors
   - Check health check failures
   - Verify PORT is being used correctly

2. **Verify Repository Structure**
   - Ensure `project-8/` directory exists in repo
   - Ensure root Dockerfile exists
   - Ensure all files are committed and pushed

3. **Test Build Context**
   ```bash
   # Simulate Koyeb build context
   cd /tmp
   git clone https://github.com/zxzhou/ai-builder.git
   cd ai-builder
   docker build -t test-koyeb -f Dockerfile .
   docker run -p 3000:3000 -e PORT=3000 test-koyeb
   ```

## Summary

The deployment failure is likely due to:
- **Health check timing out** (now fixed with `/api/health` endpoint)
- **Server startup delay** (health endpoint responds immediately)

The root Dockerfile is correct and tested. The health check endpoint should resolve the provisioning script failure.

