# CTI Dashboard Deployment Script
# This script helps you deploy to GitHub and Render

Write-Host "🚀 CTI Dashboard Deployment Helper" -ForegroundColor Cyan
Write-Host ""

# Check if git is configured
$gitUser = git config user.name
$gitEmail = git config user.email

if (-not $gitUser -or -not $gitEmail) {
    Write-Host "⚠️  Git is not configured. Please set up:" -ForegroundColor Yellow
    Write-Host "   git config --global user.name 'Your Name'" -ForegroundColor Yellow
    Write-Host "   git config --global user.email 'your.email@example.com'" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Git configured: $gitUser <$gitEmail>" -ForegroundColor Green
Write-Host ""

# Check if remote exists
$remote = git remote get-url origin 2>$null

if ($remote) {
    Write-Host "📦 Remote repository: $remote" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push your code:" -ForegroundColor Cyan
    Write-Host "   git push -u origin main" -ForegroundColor White
} else {
    Write-Host "📦 No remote repository configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📝 Steps to deploy:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Create a new repository on GitHub:" -ForegroundColor White
    Write-Host "   - Go to: https://github.com/new" -ForegroundColor Gray
    Write-Host "   - Name it: cti-dashboard (or your choice)" -ForegroundColor Gray
    Write-Host "   - Don't initialize with README" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Connect your local repository:" -ForegroundColor White
    Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/cti-dashboard.git" -ForegroundColor Gray
    Write-Host "   git branch -M main" -ForegroundColor Gray
    Write-Host "   git push -u origin main" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""
Write-Host "🌐 Next Steps for Deployment:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Push to GitHub (see commands above)" -ForegroundColor White
Write-Host ""
Write-Host "2. Set up MongoDB Atlas (FREE):" -ForegroundColor White
Write-Host "   - Go to: https://www.mongodb.com/cloud/atlas" -ForegroundColor Gray
Write-Host "   - Create free cluster" -ForegroundColor Gray
Write-Host "   - Get connection string" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Deploy to Render (FREE):" -ForegroundColor White
Write-Host "   - Go to: https://render.com" -ForegroundColor Gray
Write-Host "   - Sign up with GitHub" -ForegroundColor Gray
Write-Host "   - New Web Service → Connect GitHub repo" -ForegroundColor Gray
Write-Host "   - Add environment variables:" -ForegroundColor Gray
Write-Host "     * MONGO_URI (from MongoDB Atlas)" -ForegroundColor Gray
Write-Host "     * SECRET_KEY (generate with: python -c 'import secrets; print(secrets.token_hex(32))')" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 For detailed instructions, see DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""

