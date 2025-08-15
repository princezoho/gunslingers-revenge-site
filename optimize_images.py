#!/usr/bin/env python3
"""
Image optimization script for Gunslinger's Revenge website
Compresses images, converts to appropriate formats, and generates SEO-friendly names
"""

from PIL import Image
import os
import shutil
from pathlib import Path

def optimize_images():
    """Optimize all images in the assets directory"""
    
    assets_dir = Path("assets")
    backup_dir = Path("assets_backup")
    
    # Create backup directory
    if not backup_dir.exists():
        shutil.copytree(assets_dir, backup_dir)
        print(f"Created backup at {backup_dir}")
    
    # Image optimization settings
    optimizations = {
        # Large PNGs that should be converted to JPG
        "balatro.png": {"new_name": "balatro-card-game-deck-builder", "format": "JPEG", "quality": 85},
        "eternal-card-game.png": {"new_name": "eternal-card-game-ccg", "format": "JPEG", "quality": 85},
        "griftlands.png": {"new_name": "griftlands-roguelike-deck-builder", "format": "JPEG", "quality": 85},
        "inscryption.png": {"new_name": "inscryption-horror-card-game", "format": "JPEG", "quality": 85},
        "magic-the-gathering-arena.png": {"new_name": "magic-gathering-arena-digital", "format": "JPEG", "quality": 85},
        "monster-train.png": {"new_name": "monster-train-roguelike-strategy", "format": "JPEG", "quality": 85},
        "pirates-outlaws.png": {"new_name": "pirates-outlaws-deck-builder", "format": "JPEG", "quality": 85},
        "roguebook.png": {"new_name": "roguebook-tactical-card-game", "format": "JPEG", "quality": 85},
        "slay-the-spire.png": {"new_name": "slay-spire-roguelike-classic", "format": "JPEG", "quality": 85},
        "star-realms-digital.png": {"new_name": "star-realms-digital-card-battle", "format": "JPEG", "quality": 85},
        
        # Regular images - optimize quality
        "balatro-real.jpg": {"new_name": "balatro-poker-roguelike-gameplay", "quality": 80},
        "eternal-card-game-real.jpg": {"new_name": "eternal-card-game-screenshot", "quality": 80},
        "general-store.jpg": {"new_name": "wild-west-general-store-interior", "quality": 85},
        "green-gunslinger.jpg": {"new_name": "green-gunslinger-character-art", "quality": 85},
        "griftlands-real.jpg": {"new_name": "griftlands-sci-fi-gameplay", "quality": 80},
        "inscryption-real.jpg": {"new_name": "inscryption-horror-gameplay", "quality": 80},
        "monster-train-real.jpg": {"new_name": "monster-train-hell-gameplay", "quality": 80},
        "pirates-outlaws-real.jpg": {"new_name": "pirates-outlaws-sea-adventure", "quality": 80},
        "slay-the-spire-real.jpg": {"new_name": "slay-spire-card-combat", "quality": 80},
        "star-realms-digital-real.jpg": {"new_name": "star-realms-space-combat", "quality": 80},
        "sunset-guitarist.jpg": {"new_name": "wild-west-sunset-guitarist", "quality": 85},
        
        # Logo and UI elements - keep PNG for transparency
        "logo-gunslingers.png": {"new_name": "gunslingers-revenge-logo", "quality": 95},
        "stat-sheet.png": {"new_name": "character-stat-sheet-parchment", "quality": 90},
        
        # GIFs - optimize without conversion
        "accessory.gif": {"new_name": "gun-accessory-animation"},
        "doublegun.gif": {"new_name": "dual-wielding-guns-animation"},
        "lasso.gif": {"new_name": "cowboy-lasso-animation"},
        "longScene_wide.gif": {"new_name": "wild-west-panorama-animation"},
        "sfx17.gif": {"new_name": "special-effect-green-animation"},
        "sfx26.gif": {"new_name": "special-effect-tan-animation"},
        "shotgun.gif": {"new_name": "shotgun-blast-animation"},
        "vfx.gif": {"new_name": "visual-effects-animation"},
    }
    
    total_size_before = 0
    total_size_after = 0
    
    for filename, settings in optimizations.items():
        file_path = assets_dir / filename
        
        if not file_path.exists():
            print(f"Warning: {filename} not found")
            continue
            
        # Get original size
        original_size = file_path.stat().st_size
        total_size_before += original_size
        
        # Handle different file types
        if filename.endswith('.gif'):
            # For GIFs, just rename for SEO
            new_name = settings["new_name"] + ".gif"
            new_path = assets_dir / new_name
            if file_path != new_path:
                shutil.copy2(file_path, new_path)
                print(f"Renamed {filename} to {new_name}")
            total_size_after += original_size
            
        else:
            # For static images, optimize
            try:
                img = Image.open(file_path)
                
                # Convert RGBA to RGB if needed for JPEG conversion
                if settings.get("format") == "JPEG" and img.mode in ('RGBA', 'LA', 'P'):
                    # Create a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Determine new filename
                if settings.get("format") == "JPEG":
                    new_name = settings["new_name"] + ".jpg"
                elif filename.endswith('.png'):
                    new_name = settings["new_name"] + ".png"
                else:
                    new_name = settings["new_name"] + ".jpg"
                
                new_path = assets_dir / new_name
                
                # Save optimized image
                save_kwargs = {"optimize": True}
                if "quality" in settings:
                    save_kwargs["quality"] = settings["quality"]
                if settings.get("format"):
                    save_kwargs["format"] = settings["format"]
                    
                img.save(new_path, **save_kwargs)
                
                new_size = new_path.stat().st_size
                total_size_after += new_size
                
                reduction = ((original_size - new_size) / original_size) * 100
                print(f"Optimized {filename} -> {new_name}: {original_size//1024}KB -> {new_size//1024}KB ({reduction:.1f}% reduction)")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                total_size_after += original_size
    
    print(f"\nTotal size reduction: {total_size_before//1024}KB -> {total_size_after//1024}KB ({((total_size_before - total_size_after) / total_size_before) * 100:.1f}% reduction)")

if __name__ == "__main__":
    optimize_images()