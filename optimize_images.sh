#!/bin/bash
# Image optimization script for Gunslinger's Revenge
# Uses ImageMagick (convert) or other system tools

echo "🖼️  Optimizing images in assets folder..."

# Create optimized directory
mkdir -p assets/optimized

# Counter
count=0

# Optimize PNGs
for img in assets/*.png; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        echo "Processing $filename..."
        
        # Use ImageMagick if available
        if command -v convert &> /dev/null; then
            convert "$img" -quality 85 -resize '1920>' "assets/optimized/$filename"
            ((count++))
        # Use sips on macOS
        elif command -v sips &> /dev/null; then
            sips -Z 1920 "$img" --out "assets/optimized/$filename" 2>/dev/null
            ((count++))
        else
            echo "No image optimization tool found. Install ImageMagick."
            break
        fi
    fi
done

# Optimize JPGs
for img in assets/*.jpg assets/*.jpeg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        echo "Processing $filename..."
        
        if command -v convert &> /dev/null; then
            convert "$img" -quality 85 -resize '1920>' "assets/optimized/$filename"
            ((count++))
        elif command -v sips &> /dev/null; then
            sips -Z 1920 "$img" --out "assets/optimized/$filename" 2>/dev/null
            ((count++))
        fi
    fi
done

echo "✅ Optimized $count images"
echo "📁 Optimized images saved in assets/optimized/"
echo ""
echo "To use optimized images:"
echo "1. Review images in assets/optimized/"
echo "2. If satisfied: mv assets assets.backup && mv assets/optimized assets"
