#!/bin/bash
# Compress remaining images for Gunslinger's Revenge
# © 2025 Jeje Studios

echo "🎯 Compressing remaining Gunslinger's Revenge images..."
echo "=================================================="

# Process remaining PNG files
for file in assets/uncompressed/*.png; do
    filename=$(basename "$file")
    
    # Skip already processed files
    case "$filename" in
        "charms-page.png"|"horse-trading-edit.png"|"enemy-turn.png"|"your-turn2.png"|"tonics-shark.png"|"bounty-captured-chomp.png"|"bounty-longshot-loomis.png"|"charm-info.png"|"layout-t.png"|"relic-animation2.png"|"jerry-b-dangerous.png"|"apple-beer.png"|"frothy-beer.png")
            continue;;
    esac
    
    # Generate SEO-friendly names for remaining files
    case "$filename" in
        "charm-info2.png") output="gunslingers-revenge-charm-info-detailed.png";;
        "charms-page1.png") output="gunslingers-revenge-charms-collection.png";;
        "gunslinger-logo-plaque.png") output="gunslingers-revenge-logo-plaque.png";;
        "horse-trading-edit-horse.png") output="gunslingers-revenge-horse-selection.png";;
        "out-3-1.png") output="gunslingers-revenge-character-out.png";;
        "rip.mock.png") output="gunslingers-revenge-death-screen.png";;
        *) continue;;
    esac
    
    echo "Compressing $filename → $output"
    sips -s format png --setProperty formatOptions 85 "$file" --out "assets/$output" 2>/dev/null
    # Add metadata
    exiftool -overwrite_original -quiet \
        -Artist="Jeje Studios" \
        -Copyright="© 2025 Gunslinger's Revenge - Jeje Studios" \
        -Description="Gunslinger's Revenge roguelike deckbuilder game" \
        "assets/$output" 2>/dev/null
done

# Process JPG files
for file in assets/uncompressed/*.{jpg,JPG}; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")
    
    case "$filename" in
        "AAB888D9-2F42-415D-8430-D447C3161511.jpg") output="gunslingers-revenge-concept-art-1.jpg";;
        "D9E6612F-96B3-46BC-8BFF-8DFBB7F0CE64.jpg") output="gunslingers-revenge-concept-art-2.jpg";;
        "IMG_2691.JPG") output="gunslingers-revenge-gameplay-screenshot.jpg";;
        *) continue;;
    esac
    
    echo "Compressing $filename → $output"
    sips -s format jpeg --setProperty formatOptions 85 "$file" --out "assets/$output" 2>/dev/null
    # Add metadata
    exiftool -overwrite_original -quiet \
        -Artist="Jeje Studios" \
        -Copyright="© 2025 Gunslinger's Revenge - Jeje Studios" \
        -Description="Gunslinger's Revenge Wild West roguelike deckbuilder" \
        "assets/$output" 2>/dev/null
done

# Process GIF files that haven't been compressed yet
echo ""
echo "Processing GIF animations..."
for file in assets/uncompressed/*.gif; do
    filename=$(basename "$file")
    
    # Skip already processed GIFs
    if [ -f "assets/gunslingers-revenge-$filename" ]; then
        continue
    fi
    
    output="gunslingers-revenge-$filename"
    echo "Compressing GIF: $filename → $output"
    
    # Use gifsicle if available, otherwise just copy with metadata
    if command -v gifsicle &> /dev/null; then
        gifsicle -O3 --colors 128 --lossy=80 \
            --comment "© 2025 Gunslinger's Revenge - Jeje Studios | Wild West Roguelike Deck-Builder" \
            "$file" > "assets/$output" 2>/dev/null
    else
        cp "$file" "assets/$output"
    fi
done

echo "=================================================="
echo "✅ Compression complete!"
echo ""
echo "New compressed files added to assets folder:"
ls -lh assets/gunslingers-revenge-* | tail -10