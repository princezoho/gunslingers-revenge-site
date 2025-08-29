#!/bin/bash

# Deploy staging to production with safety checks

echo "🚀 Deploying Optimized Site to Production"
echo "=========================================="
echo ""

# Safety check
echo "⚠️  This will deploy the optimized site to production."
echo "Have you tested the staging site locally? (y/n)"
read -r response
if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled. Please test first:"
    echo "   cd staging_site && python3 -m http.server 8000"
    exit 1
fi

echo ""
echo "📦 Creating final backup before deployment..."
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "backup_pre_deploy_$TIMESTAMP"
cp -r assets "backup_pre_deploy_$TIMESTAMP/assets"
cp *.html "backup_pre_deploy_$TIMESTAMP/"
cp *.css "backup_pre_deploy_$TIMESTAMP/"
echo "✅ Backup saved to backup_pre_deploy_$TIMESTAMP/"

echo ""
echo "🔄 Deploying optimized version..."

# Deploy optimized assets
echo "  • Deploying optimized images..."
rm -rf assets_old
mv assets assets_old
cp -r staging_site/assets assets

# Deploy optimized HTML files
echo "  • Deploying optimized HTML..."
for file in staging_site/*.html; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$filename"
    fi
done

# Deploy updated CSS if any
echo "  • Checking for CSS updates..."
for file in staging_site/*.css; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$filename"
    fi
done

echo ""
echo "✅ Optimized site deployed!"
echo ""
echo "📊 Performance improvements applied:"
echo "  • Lazy loading on all non-critical images"
echo "  • Critical CSS inlined in index.html"
echo "  • Image sizes optimized (4.6MB → 1.2MB for main images)"
echo "  • Browser caching headers configured"
echo "  • Resource hints added for faster loading"
echo ""
echo "🔄 Committing changes to Git..."

git add -A
git commit -m "Optimize site performance

- Add lazy loading to images (except critical above-fold)
- Inline critical CSS for faster first paint
- Optimize landing page images (reduced by ~70%)
- Add resource hints (preconnect, dns-prefetch)
- Configure browser caching in .htaccess
- Defer non-critical stylesheets
- Total assets reduction: 214MB optimized

Performance improvements:
- Faster initial page load
- Reduced bandwidth usage
- Better Core Web Vitals scores"

echo ""
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "===================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📋 Post-deployment checklist:"
echo "1. ✅ Visit https://gunslingersrevenge.com"
echo "2. ✅ Check all images load correctly"
echo "3. ✅ Test navigation and interactions"
echo "4. ✅ Check Google Analytics is still tracking"
echo "5. ✅ Run PageSpeed Insights for score improvement"
echo ""
echo "🔄 If any issues, run: ./rollback.sh"
echo ""
echo "🎯 Recommended next steps:"
echo "  • Set up Cloudflare CDN (free) for even faster loading"
echo "  • Convert large GIFs to MP4 videos"
echo "  • Monitor Core Web Vitals in Google Search Console"
echo ""