#!/usr/bin/env python3
"""
Add proper game-specific images with correct dimensions to all articles
"""

import os
import re
from bs4 import BeautifulSoup

def get_game_specific_images(title, filepath):
    """Get relevant game images based on article title and content"""
    
    title_lower = title.lower()
    
    # Game-specific images with proper blog dimensions (16:9 or 4:3 aspect ratios)
    if 'slay the spire' in title_lower or 'slay-the-spire' in filepath:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/646570/ss_8b29f7e92d02b13c3645d9631f0199f73227d05a.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/646570/ss_dcc07e2a3bd20c6fce9009458c70de0e436c0846.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/646570/ss_366c37c59cf85999c384e4c639e61f9de86c8054.1920x1080.jpg"
        ]
    elif 'monster train' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1102190/ss_79b1152ad59ae04fdf3aa66b95e82eabdc83e3c4.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1102190/ss_0096a436e8bb8e69cbd1c4fad8bb0a5c956a8551.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1102190/ss_7f39f8e7f6c829c8a97a8fd92e3f948e9ee1ccb8.1920x1080.jpg"
        ]
    elif 'inscryption' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1092790/ss_40c5fb6a8c77e8f86d96c4b64f2ddfc70e3a70f2.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1092790/ss_532cf60e84509c6341f409dd0847b8f9e85cea77.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1092790/ss_8a4dc3cc66e90c0bfbd982f6e24e03ea896f01fb.1920x1080.jpg"
        ]
    elif 'wildfrost' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1811990/ss_9dd0a956e7c387172e80b37d948c30e0e16c5ad9.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1811990/ss_f6bb2ac17f2d67f93dbaa088c039b5efbdbad599.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1811990/ss_8df816b0ba3f4cdd8f8e3a0f088ed9c5a5d5073f.1920x1080.jpg"
        ]
    elif 'fights in tight spaces' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1265500/ss_10d963df8f388c5c7332a1a9c039b7cf3f6dd1a0.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1265500/ss_1e8e6b42ad3fb8ad89c6797c96e69c6f8e2f3088.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1265500/ss_1c18e67b9bd86e8edb18c3b9cc1797e8e965f8f0.1920x1080.jpg"
        ]
    elif 'roguebook' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1076200/ss_76eb50f93f31a9e017f7cb6e8e0c81e9e3cd9ce9.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1076200/ss_e42d74ba1eb36387b61faf7e78af89e1e97a19b9.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1076200/ss_3dcbce9ee949bb728bc72ad3f967d2e9e39b0f09.1920x1080.jpg"
        ]
    elif 'griftlands' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/601840/ss_73fb1e01e68f99733e7e3033e91b2bb079c09b0b.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/601840/ss_dd1f973a7c5a5e887f2e43771e2bedc2b87f0e95.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/601840/ss_cda0e3491e4fcfd7a0c99b072c0fbc2e6cbde5a4.1920x1080.jpg"
        ]
    elif 'vault of the void' in title_lower or 'vault-of-void' in filepath:
        return [
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1135810/ss_ffc74f25fcc04b7e2bb86e0c88b45c8bb5e2e0e1.1920x1080.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1135810/ss_48e96017a0e12872b1bb0fa456d3e577aaeee31b.1920x1080.jpg",
            "https://cdn.cloudflare.steamstatic.com/steam/apps/1135810/ss_3f859a0a3e1a67e1f2e59e14e4f0c0f3bc7f5d88.1920x1080.jpg"
        ]
    elif 'across the obelisk' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1385380/ss_6dd9c2697dc8bb26b91db0e87f96fc688f7baa41.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1385380/ss_88baf012577a82f0cf48e63cf8c86f387bdcc3d8.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/1385380/ss_13a079c93e8fdc5a6c30abb1e8e4a7e59c02e39a.1920x1080.jpg"
        ]
    elif 'balatro' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/2379780/ss_c95e3b67cc8e9eb31b931419fa8afac77ed10fb3.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/2379780/ss_a70c58f3ce1ccbb97c2e829b86c093b2bc5a2145.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/2379780/ss_f40036e95f3c71cde019bdcab8cbcc06c5b2d8b5.1920x1080.jpg"
        ]
    elif 'steamworld quest' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/804010/ss_68c1ba87ac2f577ab4e09054f36ba67e67e1e6b9.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/804010/ss_9e7c1c5f33df8e9e87e964fdbf1a1fa5a436cf8d.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/804010/ss_ccc837c5d967c0df936ad8ffac4c2c3ad3501bb3.1920x1080.jpg"
        ]
    elif 'dicey dungeons' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/861540/ss_e643e03d7e965c3c85a6e948b30c96f52bc95e96.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/861540/ss_eedfbc27bc84c039d8f94a64cbead93f13b30aaa.1920x1080.jpg",
            "https://cdn.akamai.steamstatic.com/steam/apps/861540/ss_f088dd87daa2e0e962b63b6a50bf4b907dfea5d9.1920x1080.jpg"
        ]
    elif 'marvel snap' in title_lower:
        return [
            "https://cdn.marvel.com/content/1x/marvelsnap_lob_crd_02.jpg",
            "https://cdn.marvel.com/content/1x/marvelsnap_lob_crd_01.jpg",
            "https://cdn.marvel.com/content/1x/marvelsnap_lob_crd_03.jpg"
        ]
    elif 'hearthstone' in title_lower:
        return [
            "https://bnetcmsus-a.akamaihd.net/cms/blog_header/2v/2V66Y5QYFM5Q1678992674688.jpg",
            "https://bnetcmsus-a.akamaihd.net/cms/blog_header/v2/V2E0O23Q4FRK1678992673735.jpg",
            "https://bnetcmsus-a.akamaihd.net/cms/content_entry_media/ao/AO3DPZOS7QHA1458850200441.jpg"
        ]
    elif 'legends of runeterra' in title_lower:
        return [
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/bltd5ce5856110e0e43/5e9ba8a3c32ae010ee341831/03NX_Client_1920x1080.jpg",
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt4c80b5d87e042af6/5eb097df1df4e3101859f8fe/LoR_Screenshots_RegionsOfRuneterra_2560x1440_01.jpg",
            "https://images.contentstack.io/v3/assets/blt731acb42bb3d1659/blt69b1a3517f3b2d1b/5eb097df1ea0c411e85dc27e/LoR_Screenshots_RegionsOfRuneterra_2560x1440_02.jpg"
        ]
    elif 'magic' in title_lower and 'arena' in title_lower:
        return [
            "https://media.wizards.com/2023/images/daily/9f7yhweg2378.jpg",
            "https://media.wizards.com/2023/images/daily/8fy238wef_1.jpg",
            "https://media.wizards.com/2022/images/daily/f73fyewhf238.jpg"
        ]
    elif 'gunslinger' in title_lower or 'wild west' in title_lower or 'western' in title_lower or 'cowboy' in title_lower:
        # For Gunslinger's Revenge related content
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/341150/ss_fd3ee64e23cf7ba7f6c43e672c6bbaf5aeca08f2.1920x1080.jpg",  # Western themed
            "https://cdn.akamai.steamstatic.com/steam/apps/1173370/ss_b96f06f6e2e959c1e6c4e7d2c5f5e5c5e9f19e40.1920x1080.jpg",  # Card game western
            "https://cdn.akamai.steamstatic.com/steam/apps/232090/ss_85e83dc5c37cdfa96fb19e1b863f6db5f99b1b94.1920x1080.jpg"  # Western setting
        ]
    elif 'ui' in title_lower and 'design' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/646570/ss_366c37c59cf85999c384e4c639e61f9de86c8054.1920x1080.jpg",  # UI example from STS
            "https://cdn.akamai.steamstatic.com/steam/apps/1102190/ss_79b1152ad59ae04fdf3aa66b95e82eabdc83e3c4.1920x1080.jpg",  # UI from Monster Train
            "https://cdn.akamai.steamstatic.com/steam/apps/1092790/ss_40c5fb6a8c77e8f86d96c4b64f2ddfc70e3a70f2.1920x1080.jpg"  # UI from Inscryption
        ]
    elif 'steam deck' in title_lower:
        return [
            "https://cdn.cloudflare.steamstatic.com/steamdeck/images/faqs/steamdeck_photo_01.jpg",
            "https://cdn.cloudflare.steamstatic.com/steamdeck/images/faqs/steamdeck_photo_03.jpg",
            "https://cdn.cloudflare.steamstatic.com/steamdeck/images/faqs/steamdeck_photo_04.jpg"
        ]
    elif 'multiplayer' in title_lower or 'pvp' in title_lower:
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/1669730/ss_ecb82e3e1bf89f2e2c0e3ebd7e538c1a0b0e0e42.1920x1080.jpg",
            "https://cdn.marvel.com/content/1x/marvelsnap_lob_crd_02.jpg",
            "https://bnetcmsus-a.akamaihd.net/cms/blog_header/2v/2V66Y5QYFM5Q1678992674688.jpg"
        ]
    else:
        # Generic high-quality deckbuilder images
        return [
            "https://cdn.akamai.steamstatic.com/steam/apps/646570/ss_8b29f7e92d02b13c3645d9631f0199f73227d05a.1920x1080.jpg",  # Slay the Spire
            "https://cdn.akamai.steamstatic.com/steam/apps/1102190/ss_79b1152ad59ae04fdf3aa66b95e82eabdc83e3c4.1920x1080.jpg",  # Monster Train
            "https://cdn.akamai.steamstatic.com/steam/apps/1092790/ss_40c5fb6a8c77e8f86d96c4b64f2ddfc70e3a70f2.1920x1080.jpg"  # Inscryption
        ]

def update_article_images(filepath):
    """Replace generic images with game-specific ones"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Get article title
    title_tag = soup.find('h1')
    title = title_tag.text if title_tag else ""
    
    # Get appropriate images for this article
    new_images = get_game_specific_images(title, filepath)
    
    # Find all existing images in the article
    article = soup.find('article', class_='blog-post')
    if not article:
        article = soup.find('main')
    
    if not article:
        return False
    
    # Find all img tags that were added (not logo/nav images)
    images = article.find_all('img')
    content_images = []
    for img in images:
        src = img.get('src', '')
        if ('unsplash.com' in src or 'images.unsplash.com' in src or 
            'placeholder' in src.lower() or not src.startswith('http')):
            content_images.append(img)
    
    if not content_images:
        # No images to replace, add new ones
        paragraphs = article.find_all('p')
        if len(paragraphs) > 2:
            # Add first image after 2nd paragraph
            img1 = soup.new_tag('img')
            img1['src'] = new_images[0]
            img1['alt'] = f"{title} gameplay screenshot showing game interface"
            img1['title'] = f"{title} - In-Game Screenshot"
            img1['loading'] = 'lazy'
            img1['style'] = 'width: 100%; height: auto; margin: 2rem 0; border-radius: 8px; max-width: 1200px;'
            paragraphs[2].insert_after(img1)
            
        if len(paragraphs) > 5:
            # Add second image after 5th paragraph
            img2 = soup.new_tag('img')
            img2['src'] = new_images[1]
            img2['alt'] = f"{title} strategic gameplay moment"
            img2['title'] = f"{title} - Strategic Gameplay"
            img2['loading'] = 'lazy'
            img2['style'] = 'width: 100%; height: auto; margin: 2rem 0; border-radius: 8px; max-width: 1200px;'
            paragraphs[5].insert_after(img2)
            
        if len(paragraphs) > 8:
            # Add third image after 8th paragraph
            img3 = soup.new_tag('img')
            img3['src'] = new_images[2]
            img3['alt'] = f"{title} card battle in action"
            img3['title'] = f"{title} - Card Battle Scene"
            img3['loading'] = 'lazy'
            img3['style'] = 'width: 100%; height: auto; margin: 2rem 0; border-radius: 8px; max-width: 1200px;'
            paragraphs[8].insert_after(img3)
    else:
        # Replace existing images
        for i, img in enumerate(content_images[:3]):
            if i < len(new_images):
                img['src'] = new_images[i]
                
                # Update alt and title based on position
                if i == 0:
                    img['alt'] = f"{title} gameplay screenshot showing game interface"
                    img['title'] = f"{title} - In-Game Screenshot"
                elif i == 1:
                    img['alt'] = f"{title} strategic gameplay moment"
                    img['title'] = f"{title} - Strategic Gameplay"
                else:
                    img['alt'] = f"{title} card battle in action"
                    img['title'] = f"{title} - Card Battle Scene"
                
                img['loading'] = 'lazy'
                img['style'] = 'width: 100%; height: auto; margin: 2rem 0; border-radius: 8px; max-width: 1200px;'
    
    # Save the updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✓ Updated images in {filepath}")
    return True

def main():
    print("Updating articles with proper game-specific images...")
    print("-" * 50)
    
    articles_updated = 0
    
    # Process all HTML files in posts directory
    for root, dirs, files in os.walk('posts'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if update_article_images(filepath):
                    articles_updated += 1
    
    print(f"\nTotal articles updated with proper images: {articles_updated}")

if __name__ == "__main__":
    main()