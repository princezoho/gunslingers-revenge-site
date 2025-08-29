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
