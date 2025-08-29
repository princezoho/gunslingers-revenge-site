#!/bin/bash

# Safe deployment script for Gunslinger's Revenge performance optimizations
# This script backs up everything before making changes

echo "🛡️  Safe Deployment Script for Gunslinger's Revenge"
echo "===================================================="
echo ""

# Create timestamp for backup
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="backup_$TIMESTAMP"

# Step 1: Create full backup
echo "📦 Step 1: Creating full backup..."
mkdir -p "$BACKUP_DIR"
cp -r assets "$BACKUP_DIR/assets_original"
cp -r *.html "$BACKUP_DIR/"
cp -r *.css "$BACKUP_DIR/"
cp .htaccess "$BACKUP_DIR/" 2>/dev/null
echo "✅ Backup created in $BACKUP_DIR/"
echo ""

# Step 2: Create optimized assets while keeping originals
echo "🖼️  Step 2: Preparing optimized assets..."
mkdir -p assets_optimized_staging

# Copy all original assets first
cp -r assets/* assets_optimized_staging/

# Replace with optimized versions where they exist
if [ -d "assets/optimized" ]; then
    echo "  Copying optimized images..."
    cp -f assets/optimized/* assets_optimized_staging/ 2>/dev/null
    echo "  ✅ Optimized images prepared"
fi
echo ""

# Step 3: Create staging directory with all changes
echo "🔧 Step 3: Creating staging version..."
mkdir -p staging_site

# Copy all files to staging
cp -r *.html staging_site/
cp -r *.css staging_site/
cp -r css staging_site/ 2>/dev/null
cp -r posts staging_site/ 2>/dev/null
cp .htaccess staging_site/ 2>/dev/null
cp -r assets_optimized_staging staging_site/assets

echo "✅ Staging site created in staging_site/"
echo ""

# Step 4: Create rollback script
echo "↩️  Step 4: Creating rollback script..."
cat > rollback.sh << 'EOF'
#!/bin/bash
echo "🔄 Rolling back to previous version..."
if [ -d "backup_latest" ]; then
    rm -rf assets
    rm -f *.html
    cp -r backup_latest/assets_original assets
    cp backup_latest/*.html .
    cp backup_latest/*.css .
    cp backup_latest/.htaccess . 2>/dev/null
    echo "✅ Rollback complete!"
else
    echo "❌ No backup found! Please specify backup directory."
fi
EOF
chmod +x rollback.sh
ln -sf "$BACKUP_DIR" backup_latest
echo "✅ Rollback script created (./rollback.sh)"
echo ""

# Step 5: Show what changed
echo "📊 Step 5: Summary of changes..."
echo "--------------------------------"
echo "Original assets size: $(du -sh "$BACKUP_DIR/assets_original" | cut -f1)"
echo "Optimized assets size: $(du -sh assets_optimized_staging | cut -f1)"

# Count lazy loading additions
LAZY_COUNT=$(grep -c 'loading="lazy"' staging_site/*.html 2>/dev/null | awk -F: '{sum+=$2} END {print sum}')
echo "Lazy loading added to: $LAZY_COUNT images"

# Check for critical CSS
if grep -q "Critical inline CSS" staging_site/index.html; then
    echo "Critical CSS: ✅ Added to index.html"
fi

echo ""
echo "===================================================="
echo "✅ STAGING READY!"
echo ""
echo "📋 Next steps:"
echo "1. TEST LOCALLY:"
echo "   cd staging_site && python3 -m http.server 8000"
echo "   Open http://localhost:8000 in browser"
echo ""
echo "2. IF EVERYTHING WORKS, DEPLOY:"
echo "   ./deploy_to_production.sh"
echo ""
echo "3. IF ISSUES, ROLLBACK:"
echo "   ./rollback.sh"
echo ""