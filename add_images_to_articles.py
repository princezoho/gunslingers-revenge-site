#!/usr/bin/env python3
"""
Add 3 SEO-optimized images to all existing articles
"""

import os
import re
from bs4 import BeautifulSoup

# Curated list of relevant gaming/card game images from Unsplash
image_urls = [
    "https://images.unsplash.com/photo-1570303345338-e1f0eddf4946?w=1200",  # cards
    "https://images.unsplash.com/photo-1611996575749-79a3a250f948?w=1200",  # gaming setup
    "https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?w=1200",  # card hand
    "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?w=1200",  # coins/economy
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200",  # charts/analytics
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200",  # AI/technology
    "https://images.unsplash.com/photo-1598520106830-8c45c2035460?w=1200",  # gaming cards
    "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1200",  # mystical/fantasy
    "https://images.unsplash.com/photo-1535378917042-10a22c95931a?w=1200",  # technology
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200",  # strategy
    "https://images.unsplash.com/photo-1527430253228-e93688616381?w=1200",  # algorithm
    "https://images.unsplash.com/photo-1554244933-d876deb6b2ff?w=1200",  # money/monetization
    "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=1200",  # cards spread
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200",  # analytics dashboard
    "https://images.unsplash.com/photo-1561154464-82e9adf32764?w=1200",  # gaming
    "https://images.unsplash.com/photo-1612198188060-c7c2a3b66eae?w=1200",  # deck of cards
    "https://images.unsplash.com/photo-1529488127-7c86630e8e81?w=1200",  # western/cowboy
    "https://images.unsplash.com/photo-1533720576245-fd35fac12b0a?w=1200",  # wild west
    "https://images.unsplash.com/photo-1509824227185-9c5a654b3629?w=1200",  # saloon/western
    "https://images.unsplash.com/photo-1605629921711-2f6b00c6bbf4?w=1200",  # cards table
]

def add_images_to_article(filepath):
    """Add 3 SEO-optimized images to an article if it doesn't already have enough"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Count existing images (excluding logo and nav images)
    article = soup.find('article', class_='blog-post')
    if not article:
        article = soup.find('main')
    
    if not article:
        return False
    
    existing_images = article.find_all('img')
    # Filter out logo and navigation images
    content_images = [img for img in existing_images if 'logo' not in img.get('src', '').lower() 
                     and 'icon' not in img.get('src', '').lower()]
    
    if len(content_images) >= 3:
        print(f"✓ {filepath} already has {len(content_images)} images")
        return False
    
    # Get article title for context
    title_tag = soup.find('h1')
    title = title_tag.text if title_tag else "Article"
    
    # Find good spots to insert images
    paragraphs = article.find_all('p')
    h2_tags = article.find_all('h2')
    
    images_to_add = 3 - len(content_images)
    images_added = 0
    
    # Try to add images after certain paragraphs or h2 tags
    insertion_points = []
    
    # Add after 3rd paragraph if exists
    if len(paragraphs) > 3:
        insertion_points.append(('after', paragraphs[3]))
    
    # Add after middle h2 if exists
    if len(h2_tags) > 1:
        mid_h2 = h2_tags[len(h2_tags)//2]
        insertion_points.append(('after', mid_h2))
    
    # Add after 7th paragraph if exists
    if len(paragraphs) > 7:
        insertion_points.append(('after', paragraphs[7]))
    
    # Use rotating image URLs
    img_index = hash(filepath) % len(image_urls)
    
    for i in range(min(images_to_add, len(insertion_points))):
        position, element = insertion_points[i]
        
        # Create image tag with SEO attributes
        img_url = image_urls[(img_index + i) % len(image_urls)]
        
        # Generate contextual alt text based on title
        if 'western' in title.lower() or 'gunslinger' in title.lower():
            alt_texts = [
                f"Wild West themed card game illustration for {title}",
                f"Western deckbuilder gameplay concept for {title}",
                f"Frontier card battle visualization supporting {title}"
            ]
        elif 'strategy' in title.lower() or 'guide' in title.lower():
            alt_texts = [
                f"Strategic card game planning diagram for {title}",
                f"Deckbuilding strategy visualization for {title}",
                f"Card game tactics illustration supporting {title}"
            ]
        elif 'review' in title.lower():
            alt_texts = [
                f"Gameplay screenshot example for {title}",
                f"Game interface demonstration for {title}",
                f"Visual gameplay elements discussed in {title}"
            ]
        else:
            alt_texts = [
                f"Card game concept illustration for {title}",
                f"Deckbuilder gameplay visualization for {title}",
                f"Gaming strategy diagram supporting {title}"
            ]
        
        alt_text = alt_texts[i % len(alt_texts)]
        
        new_img = soup.new_tag('img')
        new_img['src'] = img_url
        new_img['alt'] = alt_text
        new_img['title'] = alt_text.replace(' for ', ' - ').replace(' supporting ', ' - ')
        new_img['loading'] = 'lazy'
        new_img['style'] = 'width: 100%; height: auto; margin: 2rem 0; border-radius: 8px;'
        
        # Insert the image
        element.insert_after(new_img)
        images_added += 1
    
    if images_added > 0:
        # Save the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"✓ Added {images_added} images to {filepath}")
        return True
    
    return False

def main():
    print("Adding SEO-optimized images to all articles...")
    print("-" * 50)
    
    articles_updated = 0
    
    # Process all HTML files in posts directory
    for root, dirs, files in os.walk('posts'):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                if add_images_to_article(filepath):
                    articles_updated += 1
    
    print(f"\nTotal articles updated with images: {articles_updated}")

if __name__ == "__main__":
    main()