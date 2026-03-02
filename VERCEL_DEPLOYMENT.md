# Vercel Deployment Guide

This guide explains how to deploy the Deepfake Voice Detection application to Vercel.

## Prerequisites

1. **Node.js & npm** - Required for Vercel CLI
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify installation: `node --version` and `npm --version`

2. **Vercel Account** - Create one at [vercel.com](https://vercel.com)

3. **Git Repository** - Your project must be in a Git repository
   - Initialize if needed: `git init`

## Installation Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Authenticate with Vercel

```bash
vercel login
```

Follow the prompts to authenticate your Vercel account.

### 3. Link Your Project

```bash
vercel link
```

This creates/links your project to Vercel and generates configuration files.

## Deployment Methods

### Method 1: Using the Deploy Script (Recommended)

**On Windows (PowerShell):**
```powershell
.\deploy.ps1
```

**On Mac/Linux (Bash):**
```bash
bash deploy.sh
```

### Method 2: Manual Deployment

```bash
vercel --prod
```

This deploys your application to production.

### Method 3: Git Integration (Recommended for CI/CD)

1. Push your code to GitHub, GitLab, or Bitbucket
2. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Select your repository
5. Vercel will automatically detect and configure your Flask app
6. Click "Deploy"

Any future pushes to your main branch will auto-deploy.

## Configuration Files

The deployment comes with two key configuration files:

### `vercel.json`
Specifies how Vercel should build and run your Flask application:
- Uses Python 3.11
- Routes all requests to `api.py`
- Runs the Flask app as a serverless function

### `.vercelignore`
Lists files/folders to exclude from deployment:
- Virtual environments
- Cache files
- Git files
- Temporary data files

## Environment Variables

To add environment variables in Vercel:

1. Go to your project settings in [vercel.com/dashboard](https://vercel.com/dashboard)
2. Navigate to "Settings" → "Environment Variables"
3. Add your variables (e.g., API keys, database URLs)
4. Click "Save"
5. Redeploy to apply changes: `vercel --prod`

## Important Notes for Flask on Vercel

- Your Flask app runs as **serverless functions**
- File uploads are temporary (use cloud storage like AWS S3 for persistent storage)
- Cold starts may cause initial requests to be slower
- The `debug=True` setting will be disabled in production (Vercel ignores it)
- Vercel automatically detects and uses `app.run()` from your Flask app

## Troubleshooting

### Access Model File Error
If you get an error about missing model files:
- Include models in Git (if small) or use environment variables to download them
- Or modify `api.py` to handle missing models gracefully

### Memory/Size Limits
- Maximum package size: 250MB
- If your models are too large, consider using cloud storage

### Port Configuration
- Vercel automatically handles port assignment (not 5000)
- Your app must use the `PORT` environment variable provided by Vercel

To check current deployments and console logs:
```bash
vercel logs [project-name]
```

## After Deployment

1. Visit your Vercel project URL (displayed after deployment)
2. Test all endpoints to ensure they work correctly
3. Check the browser console for any errors
4. Monitor logs in the Vercel dashboard

## Rollback to Previous Deployment

If you need to revert to a previous version:
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to "Deployments"
4. Click the three dots next to a previous deployment
5. Select "Promote to Production"

## Getting Help

- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- Flask Documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- Vercel Community: [vercel.com/support](https://vercel.com/support)
