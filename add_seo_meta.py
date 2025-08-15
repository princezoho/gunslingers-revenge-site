#!/usr/bin/env python3
"""
Add comprehensive SEO metadata to all HTML files
"""

import re
from pathlib import Path

def add_seo_to_html(file_path, seo_data):
    """Add SEO metadata to an HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the closing </head> tag
    head_close_index = content.find('</head>')
    
    if head_close_index == -1:
        print(f"Warning: No </head> tag found in {file_path}")
        return
    
    # Build the SEO tags
    seo_tags = []
    
    # Basic meta tags
    if 'keywords' in seo_data:
        seo_tags.append(f'    <meta name="keywords" content="{seo_data["keywords"]}">')
    if 'author' in seo_data:
        seo_tags.append(f'    <meta name="author" content="{seo_data["author"]}">')
    
    # Open Graph tags
    seo_tags.append(f'    <!-- Open Graph / Facebook -->')
    seo_tags.append(f'    <meta property="og:type" content="website">')
    seo_tags.append(f'    <meta property="og:url" content="{seo_data.get("url", "https://gunslingersrevenge.com/")}">')
    seo_tags.append(f'    <meta property="og:title" content="{seo_data.get("title", "Gunslinger\'s Revenge")}">')
    seo_tags.append(f'    <meta property="og:description" content="{seo_data.get("description", "")}">')
    seo_tags.append(f'    <meta property="og:image" content="{seo_data.get("image", "https://gunslingersrevenge.com/assets/gunslingers-revenge-logo.png")}">')
    
    # Twitter Card tags
    seo_tags.append(f'    <!-- Twitter -->')
    seo_tags.append(f'    <meta property="twitter:card" content="summary_large_image">')
    seo_tags.append(f'    <meta property="twitter:url" content="{seo_data.get("url", "https://gunslingersrevenge.com/")}">')
    seo_tags.append(f'    <meta property="twitter:title" content="{seo_data.get("title", "Gunslinger\'s Revenge")}">')
    seo_tags.append(f'    <meta property="twitter:description" content="{seo_data.get("description", "")}">')
    seo_tags.append(f'    <meta property="twitter:image" content="{seo_data.get("image", "https://gunslingersrevenge.com/assets/gunslingers-revenge-logo.png")}">')
    
    # Canonical URL
    seo_tags.append(f'    <link rel="canonical" href="{seo_data.get("url", "https://gunslingersrevenge.com/")}">')
    
    # Favicon
    seo_tags.append(f'    <link rel="icon" type="image/png" href="/assets/gunslingers-revenge-logo.png">')
    
    # Join all tags with newlines
    seo_block = '\n'.join(seo_tags) + '\n'
    
    # Insert the SEO block before </head>
    new_content = content[:head_close_index] + seo_block + content[head_close_index:]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added SEO metadata to {file_path}")

# Define SEO data for each page
pages_seo = {
    "index.html": {
        "title": "Gunslinger's Revenge - Roguelike Deck-Building Wild West Game",
        "description": "Play Gunslinger's Revenge, a fast-paced roguelike deck-builder set in the Wild West. Build powerful decks, duel outlaws, and become a legend. Wishlist on Steam now!",
        "keywords": "roguelike deck builder, wild west game, card game, deck building game, roguelike game, indie game, steam wishlist, gunslinger game, western card game",
        "url": "https://gunslingersrevenge.com/",
        "author": "Gunslinger's Revenge Team",
        "image": "https://gunslingersrevenge.com/assets/green-gunslinger-character-art.jpg"
    },
    "features.html": {
        "title": "Game Features - Gunslinger's Revenge Deck-Builder",
        "description": "Discover unique features: dual-wielding mechanics, lasso system, 100+ cards, procedural generation, and stunning Wild West animations in Gunslinger's Revenge.",
        "keywords": "game features, deck building mechanics, roguelike features, dual wielding, card synergies, procedural generation, wild west gameplay",
        "url": "https://gunslingersrevenge.com/features.html",
        "author": "Gunslinger's Revenge Team",
        "image": "https://gunslingersrevenge.com/assets/shotgun-blast-animation.gif"
    },
    "gallery.html": {
        "title": "Screenshots & Artwork - Gunslinger's Revenge",
        "description": "View stunning screenshots, character art, and animated effects from Gunslinger's Revenge. Experience the Wild West atmosphere before you play.",
        "keywords": "game screenshots, wild west artwork, game gallery, character art, visual effects, game animations, indie game art",
        "url": "https://gunslingersrevenge.com/gallery.html",
        "author": "Gunslinger's Revenge Team",
        "image": "https://gunslingersrevenge.com/assets/wild-west-panorama-animation.gif"
    },
    "blog.html": {
        "title": "Blog - Gunslinger's Revenge Dev Updates & Strategy Guides",
        "description": "Read development updates, strategy guides, and deck-building tips. Learn about roguelike mechanics and Wild West game design from the developers.",
        "keywords": "game development blog, roguelike strategy, deck building tips, indie game dev, wild west games, card game strategy",
        "url": "https://gunslingersrevenge.com/blog.html",
        "author": "Gunslinger's Revenge Team",
        "image": "https://gunslingersrevenge.com/assets/wild-west-sunset-guitarist.jpg"
    },
    "contact.html": {
        "title": "Contact Us - Gunslinger's Revenge Support & Feedback",
        "description": "Contact the Gunslinger's Revenge team for support, feedback, or partnership opportunities. Join our community and get exclusive updates.",
        "keywords": "contact game developers, indie game support, feedback, partnership, newsletter signup, community",
        "url": "https://gunslingersrevenge.com/contact.html",
        "author": "Gunslinger's Revenge Team",
        "image": "https://gunslingersrevenge.com/assets/gunslingers-revenge-logo.png"
    }
}

# Process each page
for page_name, seo_data in pages_seo.items():
    page_path = Path(page_name)
    if page_path.exists():
        add_seo_to_html(page_path, seo_data)
    else:
        print(f"Warning: {page_name} not found")

print("\nSEO metadata addition complete!")