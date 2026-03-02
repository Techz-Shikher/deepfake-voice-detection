# Quick Start: Deploy to Vercel

## One-Time Setup

```powershell
# 1. Install Node.js from https://nodejs.org/
# 2. Install Vercel CLI
npm install -g vercel

# 3. Login to Vercel
vercel login

# 4. Link project to Vercel (from project root)
vercel link
```

## Deploy to Production

**Option A - Using PowerShell (Windows):**
```powershell
.\deploy.ps1
```

**Option B - Using Command Line:**
```bash
vercel --prod
```

**Option C - Using Git Integration (Recommended):**
1. Push to GitHub: `git push origin main`
2. Vercel automatically deploys on push

## View Your Site

After deployment, you'll get a URL like:
```
https://your-project-name.vercel.app
```

## Useful Commands

```bash
# Check deployment status
vercel status

# View logs
vercel logs

# Set environment variable
vercel env add API_KEY

# View active deployments
vercel deployments

# Remove a deployment
vercel remove [project-name] --yes
```

## Key Files

- **vercel.json** - Deployment configuration
- **.vercelignore** - Files to exclude from deployment
- **api.py** - Your Flask application (entry point)
- **requirements.txt** - Python dependencies

## Notes

✅ Flask automatically converts to serverless functions
✅ All routes in api.py become available
✅ Uploads go to temporary storage (use cloud storage for persistence)
✅ Free tier includes: 1,000 serverless function invocations/day
✅ Auto-deploys on every Git push (with GitHub integration)

## For Full Instructions

See: **VERCEL_DEPLOYMENT.md**
