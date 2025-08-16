#!/bin/bash

# Gunslinger's Revenge GIF Compression Script
# Copyright © 2025 Jeje Studios
# Author: Gunslinger's Revenge Development Team
# Website: https://gunslingersrevenge.com

echo "============================================================"
echo "GUNSLINGER'S REVENGE - GIF COMPRESSION & SEO OPTIMIZATION"
echo "Copyright © 2025 Jeje Studios"
echo "============================================================"
echo ""

# Create compressed directory if it doesn't exist
mkdir -p assets/compressed

# Counter for statistics
TOTAL_ORIGINAL=0
TOTAL_COMPRESSED=0
FILE_COUNT=0

# Process each GIF file
for gif in assets/uncompressed/*.gif; do
    if [ -f "$gif" ]; then
        filename=$(basename "$gif")
        base_name="${filename%.gif}"
        
        # Create SEO-friendly filename
        seo_name="gunslingers-revenge-${base_name}"
        output_file="assets/${seo_name}.gif"
        
        echo "Processing: $filename"
        
        # Get original size
        original_size=$(stat -f%z "$gif" 2>/dev/null || stat -c%s "$gif" 2>/dev/null)
        
        # Compress with gifsicle
        # -O3: maximum optimization
        # --colors 128: reduce to 128 colors
        # --lossy=80: lossy compression
        # --comment: add metadata
        gifsicle -O3 --colors 128 --lossy=80 \
            --comment "© 2025 Gunslinger's Revenge - Jeje Studios | Wild West Roguelike Deck-Builder | https://gunslingersrevenge.com" \
            "$gif" -o "$output_file"
        
        # Get compressed size
        compressed_size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null)
        
        # Calculate reduction
        reduction=$(echo "scale=1; (1 - $compressed_size/$original_size) * 100" | bc)
        
        # Convert sizes to KB for display
        original_kb=$(echo "scale=1; $original_size/1024" | bc)
        compressed_kb=$(echo "scale=1; $compressed_size/1024" | bc)
        
        echo "  Original: ${original_kb} KB"
        echo "  Compressed: ${compressed_kb} KB"
        echo "  Reduction: ${reduction}%"
        echo "  Output: $output_file"
        echo ""
        
        # Update totals
        TOTAL_ORIGINAL=$((TOTAL_ORIGINAL + original_size))
        TOTAL_COMPRESSED=$((TOTAL_COMPRESSED + compressed_size))
        FILE_COUNT=$((FILE_COUNT + 1))
    fi
done

# Calculate total statistics
if [ $FILE_COUNT -gt 0 ]; then
    TOTAL_REDUCTION=$(echo "scale=1; (1 - $TOTAL_COMPRESSED/$TOTAL_ORIGINAL) * 100" | bc)
    TOTAL_ORIGINAL_MB=$(echo "scale=2; $TOTAL_ORIGINAL/1024/1024" | bc)
    TOTAL_COMPRESSED_MB=$(echo "scale=2; $TOTAL_COMPRESSED/1024/1024" | bc)
    
    echo "============================================================"
    echo "COMPRESSION SUMMARY"
    echo "============================================================"
    echo "Files processed: $FILE_COUNT"
    echo "Total original size: ${TOTAL_ORIGINAL_MB} MB"
    echo "Total compressed size: ${TOTAL_COMPRESSED_MB} MB"
    echo "Overall reduction: ${TOTAL_REDUCTION}%"
    echo ""
    echo "All files tagged with:"
    echo "  Author: Jeje Studios"
    echo "  Copyright: © 2025 Gunslinger's Revenge"
    echo "  Website: https://gunslingersrevenge.com"
    echo ""
    echo "SEO-optimized filenames created with 'gunslingers-revenge-' prefix"
    echo "Ready for local testing!"
fi