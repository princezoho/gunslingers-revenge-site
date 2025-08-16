#!/usr/bin/env python3
"""
Compress PNG and JPG images for Gunslinger's Revenge website
© 2025 Jeje Studios
"""

import os
from PIL import Image
import glob

def compress_image(input_path, output_path, quality=85):
    """Compress a single image"""
    try:
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Save with optimization
        if input_path.lower().endswith('.png'):
            img.save(output_path, 'PNG', optimize=True)
        else:
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Get file sizes
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size/original_size) * 100
        
        print(f"✓ {os.path.basename(input_path)}: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB ({reduction:.1f}% reduction)")
        return True
    except Exception as e:
        print(f"✗ Error compressing {input_path}: {e}")
        return False

def main():
    source_dir = "assets/uncompressed"
    output_dir = "assets"
    
    # Images to compress with SEO-friendly names
    images_to_compress = {
        "charms-page.png": "gunslingers-revenge-horse-charms-system.png",
        "horse-trading-edit.png": "gunslingers-revenge-horse-trading-stable.png", 
        "enemy-turn.png": "gunslingers-revenge-enemy-turn-ui.png",
        "your-turn2.png": "gunslingers-revenge-your-turn-ui.png",
        "tonics-shark.png": "gunslingers-revenge-tonics-crafting.png",
        "bounty-captured-chomp.png": "gunslingers-revenge-bounty-captured.png",
        "bounty-longshot-loomis.png": "gunslingers-revenge-bounty-wanted.png",
        "charm-info.png": "gunslingers-revenge-charm-details.png",
        "layout-t.png": "gunslingers-revenge-game-layout.png",
        "relic-animation2.png": "gunslingers-revenge-relic-system.png",
        "jerry-b-dangerous.png": "gunslingers-revenge-jerry-boss.png",
        "apple-beer.png": "gunslingers-revenge-saloon-drinks.png",
        "frothy-beer.png": "gunslingers-revenge-beer-tonic.png"
    }
    
    print("🎯 Compressing Gunslinger's Revenge images...")
    print("=" * 50)
    
    total_original = 0
    total_compressed = 0
    
    for original_name, new_name in images_to_compress.items():
        input_path = os.path.join(source_dir, original_name)
        output_path = os.path.join(output_dir, new_name)
        
        if os.path.exists(input_path):
            original_size = os.path.getsize(input_path)
            total_original += original_size
            
            if compress_image(input_path, output_path):
                compressed_size = os.path.getsize(output_path)
                total_compressed += compressed_size
    
    print("=" * 50)
    print(f"Total: {total_original/1024/1024:.1f}MB → {total_compressed/1024/1024:.1f}MB")
    print(f"Overall reduction: {(1-total_compressed/total_original)*100:.1f}%")
    print("\n✅ Compression complete! Images ready for web.")

if __name__ == "__main__":
    main()