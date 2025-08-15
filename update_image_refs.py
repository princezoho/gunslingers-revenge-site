#!/usr/bin/env python3
"""
Update image references in HTML files to use new optimized image names
"""

import os
from pathlib import Path
import re

# Mapping of old image names to new SEO-optimized names
image_mappings = {
    # PNGs converted to JPGs
    "balatro.png": "balatro-card-game-deck-builder.jpg",
    "eternal-card-game.png": "eternal-card-game-ccg.jpg",
    "griftlands.png": "griftlands-roguelike-deck-builder.jpg",
    "inscryption.png": "inscryption-horror-card-game.jpg",
    "magic-the-gathering-arena.png": "magic-gathering-arena-digital.jpg",
    "monster-train.png": "monster-train-roguelike-strategy.jpg",
    "pirates-outlaws.png": "pirates-outlaws-deck-builder.jpg",
    "roguebook.png": "roguebook-tactical-card-game.jpg",
    "slay-the-spire.png": "slay-spire-roguelike-classic.jpg",
    "star-realms-digital.png": "star-realms-digital-card-battle.jpg",
    
    # Renamed JPGs
    "balatro-real.jpg": "balatro-poker-roguelike-gameplay.jpg",
    "eternal-card-game-real.jpg": "eternal-card-game-screenshot.jpg",
    "general-store.jpg": "wild-west-general-store-interior.jpg",
    "green-gunslinger.jpg": "green-gunslinger-character-art.jpg",
    "griftlands-real.jpg": "griftlands-sci-fi-gameplay.jpg",
    "inscryption-real.jpg": "inscryption-horror-gameplay.jpg",
    "monster-train-real.jpg": "monster-train-hell-gameplay.jpg",
    "pirates-outlaws-real.jpg": "pirates-outlaws-sea-adventure.jpg",
    "slay-the-spire-real.jpg": "slay-spire-card-combat.jpg",
    "star-realms-digital-real.jpg": "star-realms-space-combat.jpg",
    "sunset-guitarist.jpg": "wild-west-sunset-guitarist.jpg",
    
    # PNGs kept as PNG
    "logo-gunslingers.png": "gunslingers-revenge-logo.png",
    "stat-sheet.png": "character-stat-sheet-parchment.png",
    
    # GIFs renamed
    "accessory.gif": "gun-accessory-animation.gif",
    "doublegun.gif": "dual-wielding-guns-animation.gif",
    "lasso.gif": "cowboy-lasso-animation.gif",
    "longScene_wide.gif": "wild-west-panorama-animation.gif",
    "sfx17.gif": "special-effect-green-animation.gif",
    "sfx26.gif": "special-effect-tan-animation.gif",
    "shotgun.gif": "shotgun-blast-animation.gif",
    "vfx.gif": "visual-effects-animation.gif",
}

# Better alt texts for SEO
alt_texts = {
    "balatro-card-game-deck-builder.jpg": "Balatro poker roguelike deck-building card game gameplay screenshot",
    "eternal-card-game-ccg.jpg": "Eternal Card Game digital collectible card game interface",
    "griftlands-roguelike-deck-builder.jpg": "Griftlands sci-fi roguelike deck-builder game screenshot",
    "inscryption-horror-card-game.jpg": "Inscryption psychological horror card game dark atmosphere",
    "magic-gathering-arena-digital.jpg": "Magic The Gathering Arena digital card game battlefield",
    "monster-train-roguelike-strategy.jpg": "Monster Train vertical roguelike strategy card game",
    "pirates-outlaws-deck-builder.jpg": "Pirates Outlaws seafaring roguelike deck-builder adventure",
    "roguebook-tactical-card-game.jpg": "Roguebook hex-based tactical roguelike card battler",
    "slay-spire-roguelike-classic.jpg": "Slay the Spire classic roguelike deck-builder gameplay",
    "star-realms-digital-card-battle.jpg": "Star Realms digital space combat deck-building game",
    
    "balatro-poker-roguelike-gameplay.jpg": "Balatro poker-themed roguelike with joker cards gameplay",
    "eternal-card-game-screenshot.jpg": "Eternal Card Game battle screenshot with spell effects",
    "wild-west-general-store-interior.jpg": "Wild West general store interior with vintage goods and supplies",
    "green-gunslinger-character-art.jpg": "Green Gunslinger mysterious Wild West character artwork",
    "griftlands-sci-fi-gameplay.jpg": "Griftlands narrative sci-fi card game combat scene",
    "inscryption-horror-gameplay.jpg": "Inscryption creepy card game with escape room elements",
    "monster-train-hell-gameplay.jpg": "Monster Train hell train defense strategy gameplay",
    "pirates-outlaws-sea-adventure.jpg": "Pirates Outlaws papercraft style pirate adventure",
    "slay-spire-card-combat.jpg": "Slay the Spire strategic card combat encounter",
    "star-realms-space-combat.jpg": "Star Realms epic space fleet battles card game",
    "wild-west-sunset-guitarist.jpg": "Wild West sunset scene with lone guitarist silhouette",
    
    "gunslingers-revenge-logo.png": "Gunslinger's Revenge official game logo Wild West style",
    "character-stat-sheet-parchment.png": "Gunslinger's Revenge character stats parchment interface",
    
    "gun-accessory-animation.gif": "Animated gun accessory upgrade effect for Gunslinger's Revenge",
    "dual-wielding-guns-animation.gif": "Dual-wielding revolvers animation Wild West gunfight",
    "cowboy-lasso-animation.gif": "Cowboy lasso capture animation special ability",
    "wild-west-panorama-animation.gif": "Wild West panoramic scene animated background",
    "special-effect-green-animation.gif": "Green special effect animation for card abilities",
    "special-effect-tan-animation.gif": "Tan special effect animation for desert magic",
    "shotgun-blast-animation.gif": "Shotgun blast animation powerful attack effect",
    "visual-effects-animation.gif": "Visual effects animation for special card combos",
}

def update_html_files():
    """Update all HTML files with new image references"""
    
    # Find all HTML files
    html_files = list(Path(".").glob("**/*.html"))
    
    for html_file in html_files:
        if "assets_backup" in str(html_file):
            continue
            
        print(f"Processing {html_file}...")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update image references
        for old_name, new_name in image_mappings.items():
            # Update src attributes
            content = content.replace(f'src="assets/{old_name}"', f'src="assets/{new_name}"')
            content = content.replace(f"src='assets/{old_name}'", f"src='assets/{new_name}'")
            content = content.replace(f'url(\'assets/{old_name}\')', f'url(\'assets/{new_name}\')')
            content = content.replace(f'url("assets/{old_name}")', f'url("assets/{new_name}")')
            
            # Update any standalone references
            content = content.replace(f'assets/{old_name}', f'assets/{new_name}')
        
        # Update alt texts for better SEO
        for new_name, alt_text in alt_texts.items():
            # Find img tags with this source and update alt text
            pattern = r'(<img[^>]*src=["\']assets/' + re.escape(new_name) + r'["\'][^>]*alt=)["\'][^"\']*["\']'
            replacement = r'\1"' + alt_text + '"'
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {html_file}")
        else:
            print(f"  No changes needed for {html_file}")
    
    print("\nImage reference update complete!")

if __name__ == "__main__":
    update_html_files()