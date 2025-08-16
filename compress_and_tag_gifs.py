#!/usr/bin/env python3
"""
Compress and add SEO metadata to GIF files for Gunslinger's Revenge
Author: Jeje Studios
Copyright: Gunslinger's Revenge
"""

import os
from PIL import Image, ImageSequence
import json
from datetime import datetime

# SEO metadata for each character/asset
SEO_METADATA = {
    "char-02-idel.gif": {
        "title": "Gunslinger's Revenge - Idle Gunslinger Character Animation",
        "description": "Wild West gunslinger idle stance animation for roguelike deck-building game",
        "keywords": "gunslinger animation, wild west character, roguelike game asset, deck builder sprite"
    },
    "char-08-attack.gif": {
        "title": "Gunslinger's Revenge - Quick Draw Attack Animation",
        "description": "Fast-paced revolver attack animation for Wild West deck-building game",
        "keywords": "attack animation, revolver shot, wild west combat, game animation"
    },
    "char-10-n.gif": {
        "title": "Gunslinger's Revenge - Mysterious Outlaw Character",
        "description": "Animated outlaw character for roguelike deck-builder Gunslinger's Revenge",
        "keywords": "outlaw character, wild west villain, roguelike enemy, deck builder npc"
    },
    "char-12-n.gif": {
        "title": "Gunslinger's Revenge - Frontier Character Animation",
        "description": "Frontier character animation for Wild West roguelike game",
        "keywords": "frontier character, wild west npc, game character animation, roguelike asset"
    },
    "char-14-attack.gif": {
        "title": "Gunslinger's Revenge - Special Attack Animation",
        "description": "Powerful special attack move animation for deck-building combat",
        "keywords": "special attack, combat animation, deck builder ability, wild west game"
    },
    "char-18-n.gif": {
        "title": "Gunslinger's Revenge - Bandit Character Animation",
        "description": "Animated bandit enemy for Wild West roguelike deck-builder",
        "keywords": "bandit enemy, wild west antagonist, roguelike character, deck builder enemy"
    },
    "char-21-attack2.gif": {
        "title": "Gunslinger's Revenge - Dual Wielding Attack Animation",
        "description": "Dual pistol wielding fury attack for roguelike deck-building game",
        "keywords": "dual wielding, double pistols, wild west combat, special ability animation"
    },
    "char-25-n.gif": {
        "title": "Gunslinger's Revenge - Sheriff Character Animation",
        "description": "Animated sheriff character for Wild West deck-building adventure",
        "keywords": "sheriff character, law enforcement, wild west authority, game character"
    },
    "char-26.gif": {
        "title": "Gunslinger's Revenge - Mysterious Stranger Animation",
        "description": "The mysterious stranger character from Gunslinger's Revenge roguelike",
        "keywords": "mysterious stranger, wild west character, roguelike npc, deck builder ally"
    },
    "char-27-n.gif": {
        "title": "Gunslinger's Revenge - Bounty Hunter Animation",
        "description": "Bounty hunter character animation for Wild West deck-builder",
        "keywords": "bounty hunter, wild west mercenary, roguelike character, game animation"
    },
    "char-27-n-color-3.gif": {
        "title": "Gunslinger's Revenge - Colorful Outlaw Animation",
        "description": "Vibrant outlaw character variant for roguelike deck-building game",
        "keywords": "colorful outlaw, character variant, wild west villain, deck builder enemy"
    },
    "char-28-n.gif": {
        "title": "Gunslinger's Revenge - Gunslinger Ally Animation",
        "description": "Allied gunslinger character for Wild West roguelike adventure",
        "keywords": "gunslinger ally, wild west partner, roguelike companion, deck builder character"
    },
    "char-31-n.gif": {
        "title": "Gunslinger's Revenge - Desert Wanderer Animation",
        "description": "Desert wanderer character animation for roguelike deck-builder",
        "keywords": "desert wanderer, wild west nomad, roguelike character, game animation"
    },
    "ghost-coyote.gif": {
        "title": "Gunslinger's Revenge - Ghost Coyote Enemy Animation",
        "description": "Supernatural ghost coyote enemy for Wild West roguelike deck-builder",
        "keywords": "ghost coyote, supernatural enemy, wild west creature, roguelike boss"
    },
    "skelly.gif": {
        "title": "Gunslinger's Revenge - Undead Gunslinger Animation",
        "description": "Skeleton gunslinger enemy animation for roguelike deck-building game",
        "keywords": "skeleton enemy, undead gunslinger, wild west horror, roguelike creature"
    },
    "next-night-bg-menu.gif": {
        "title": "Gunslinger's Revenge - Night Menu Background Animation",
        "description": "Animated night scene menu background for Wild West deck-builder",
        "keywords": "menu background, night scene, wild west atmosphere, game ui animation"
    },
    "out-1.gif": {
        "title": "Gunslinger's Revenge - Victory Animation Effect",
        "description": "Victory celebration animation for roguelike deck-building game",
        "keywords": "victory animation, game effect, celebration animation, deck builder vfx"
    },
    "test-bgs copy.gif": {
        "title": "Gunslinger's Revenge - Desert Background Animation",
        "description": "Animated desert background for Wild West roguelike game",
        "keywords": "desert background, wild west scenery, game background, animated landscape"
    }
}

def compress_gif(input_path, output_path, quality=85, optimize=True):
    """
    Compress GIF while maintaining animation and adding metadata
    """
    try:
        # Open the GIF
        img = Image.open(input_path)
        
        # Get filename for metadata lookup
        filename = os.path.basename(input_path)
        metadata = SEO_METADATA.get(filename, {
            "title": f"Gunslinger's Revenge - {filename.split('.')[0]}",
            "description": "Game asset for Gunslinger's Revenge roguelike deck-building game",
            "keywords": "gunslinger's revenge, wild west game, roguelike, deck builder"
        })
        
        # Prepare frames
        frames = []
        durations = []
        
        for frame in ImageSequence.Iterator(img):
            # Convert to RGBA if needed
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            
            # Reduce colors for better compression
            frame = frame.quantize(colors=128, method=2)
            
            frames.append(frame)
            durations.append(frame.info.get('duration', 100))
        
        # Create metadata info
        info = {
            'title': metadata['title'],
            'description': metadata['description'],
            'keywords': metadata['keywords'],
            'author': 'Jeje Studios',
            'copyright': '© 2025 Gunslinger\'s Revenge - Jeje Studios',
            'software': 'Gunslinger\'s Revenge Asset Pipeline',
            'created': datetime.now().isoformat(),
            'website': 'https://gunslingersrevenge.com'
        }
        
        # Save with optimization
        if frames:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                optimize=optimize,
                quality=quality,
                comment=json.dumps(info)
            )
            
            # Get file sizes
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            reduction = (1 - compressed_size/original_size) * 100
            
            return {
                'original_size': original_size,
                'compressed_size': compressed_size,
                'reduction': reduction,
                'metadata': info
            }
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return None

def main():
    """
    Process all GIFs in the uncompressed folder
    """
    input_dir = "assets/uncompressed"
    output_dir = "assets"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    total_original = 0
    total_compressed = 0
    processed_files = []
    
    print("=" * 60)
    print("GUNSLINGER'S REVENGE - GIF COMPRESSION & SEO TAGGING")
    print("Copyright © 2025 Jeje Studios")
    print("=" * 60)
    print()
    
    # Process each GIF
    for filename in os.listdir(input_dir):
        if filename.endswith('.gif'):
            input_path = os.path.join(input_dir, filename)
            
            # Generate SEO-friendly filename
            seo_filename = filename.replace(' ', '-').lower()
            if not seo_filename.startswith('gunslingers-revenge-'):
                base_name = seo_filename.replace('.gif', '')
                seo_filename = f"gunslingers-revenge-{base_name}.gif"
            
            output_path = os.path.join(output_dir, seo_filename)
            
            print(f"Processing: {filename}")
            print(f"  Output: {seo_filename}")
            
            result = compress_gif(input_path, output_path)
            
            if result:
                total_original += result['original_size']
                total_compressed += result['compressed_size']
                
                print(f"  Original: {result['original_size']/1024:.1f} KB")
                print(f"  Compressed: {result['compressed_size']/1024:.1f} KB")
                print(f"  Reduction: {result['reduction']:.1f}%")
                print(f"  SEO Title: {result['metadata']['title']}")
                print()
                
                processed_files.append({
                    'original': filename,
                    'output': seo_filename,
                    'size_reduction': result['reduction'],
                    'metadata': result['metadata']
                })
    
    # Summary
    print("=" * 60)
    print("COMPRESSION SUMMARY")
    print("=" * 60)
    print(f"Files processed: {len(processed_files)}")
    print(f"Total original size: {total_original/1024/1024:.2f} MB")
    print(f"Total compressed size: {total_compressed/1024/1024:.2f} MB")
    print(f"Overall reduction: {(1-total_compressed/total_original)*100:.1f}%")
    print()
    
    # Save metadata report
    report_path = "gif_compression_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'author': 'Jeje Studios',
            'copyright': '© 2025 Gunslinger\'s Revenge',
            'files_processed': processed_files,
            'summary': {
                'total_files': len(processed_files),
                'original_size_mb': total_original/1024/1024,
                'compressed_size_mb': total_compressed/1024/1024,
                'reduction_percent': (1-total_compressed/total_original)*100
            }
        }, f, indent=2)
    
    print(f"Metadata report saved to: {report_path}")
    print()
    print("All assets tagged with Jeje Studios / Gunslinger's Revenge credits")
    print("SEO metadata embedded in all files")
    print("Ready for deployment!")

if __name__ == "__main__":
    main()