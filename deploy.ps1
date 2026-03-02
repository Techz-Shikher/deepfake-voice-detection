# Deployment script for Vercel (PowerShell)
# For Windows users

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
$vercelCheck = vercel --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Vercel CLI is not installed." -ForegroundColor Yellow
    Write-Host "Installing Vercel CLI globally..." -ForegroundColor Yellow
    npm install -g vercel
}

Write-Host "Starting deployment to Vercel..." -ForegroundColor Green
Write-Host ""

# Deploy to Vercel
vercel --prod

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Deployment complete!" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
