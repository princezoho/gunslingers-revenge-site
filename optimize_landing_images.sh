#!/bin/bash

echo "🚀 Optimizing critical landing page images..."

# Critical images for index.html
critical_images=(
    "logo-revenge-fire.png"
    "gunslingers-revenge-logo.png"
    "gunslingers-revenge-your-turn-ui.png"
    "gunslingers-revenge-enemy-turn-ui.png"
    "gunslingers-revenge-horse-charms-system.png"
    "character-stat-sheet-parchment.png"
    "green-gunslinger-character-art.jpg"
)

mkdir -p assets/optimized

for img in "${critical_images[@]}"; do
    if [ -f "assets/$img" ]; then
        echo "Optimizing $img..."
        
        # Use sips (macOS) to resize and compress
        if [[ "$img" == *.png ]]; then
            # PNG files - resize to max 1200px width
            sips -Z 1200 "assets/$img" --out "assets/optimized/$img" 2>/dev/null
            
            # Further compress with pngquant if available
            if command -v pngquant &> /dev/null; then
                pngquant --quality=70-90 --force --output "assets/optimized/$img" "assets/optimized/$img"
            fi
        else
            # JPG files - resize and compress
            sips -Z 1200 -s format jpeg -s formatOptions 85 "assets/$img" --out "assets/optimized/$img" 2>/dev/null
        fi
        
        # Show size comparison
        original_size=$(ls -lh "assets/$img" | awk '{print $5}')
        new_size=$(ls -lh "assets/optimized/$img" 2>/dev/null | awk '{print $5}')
        echo "  ✓ $img: $original_size → $new_size"
    fi
done

echo ""
echo "✅ Landing page images optimized!"
echo ""
echo "To use optimized images:"
echo "1. Test the site with optimized images"
echo "2. If everything looks good, replace originals:"
echo "   cp assets/optimized/* assets/"
echo ""

# Show total size savings
original_total=$(du -sh assets/*.png assets/*.jpg 2>/dev/null | grep -E "(${critical_images[*]// /|})" | awk '{sum+=$1} END {print sum}')
optimized_total=$(du -sh assets/optimized/* 2>/dev/null | awk '{sum+=$1} END {print sum}')
echo "Total size reduction for critical images"