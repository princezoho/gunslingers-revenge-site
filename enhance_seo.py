#!/usr/bin/env python3
"""
Comprehensive SEO Enhancement Script for Gunslinger's Revenge Blog
This script adds all missing SEO elements to get indexed and rank on Google Page 1
"""

import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

def get_post_category(filepath):
    """Determine post category from file path"""
    if 'wild-west' in filepath:
        return 'Wild West Gaming'
    elif 'guides' in filepath:
        return 'Game Guide'
    elif 'reviews' in filepath:
        return 'Game Review'
    elif 'strategies' in filepath:
        return 'Strategy Guide'
    elif 'development' in filepath:
        return 'Game Development'
    elif 'steam-gaming' in filepath:
        return 'Steam Gaming'
    elif 'analysis' in filepath:
        return 'Gaming Analysis'
    elif 'news' in filepath:
        return 'Gaming News'
    elif 'indie-spotlights' in filepath:
        return 'Indie Games'
    elif 'deckbuilders' in filepath:
        return 'Deckbuilding Games'
    else:
        return 'Gaming'

def extract_first_paragraph(soup):
    """Extract first meaningful paragraph for description"""
    for p in soup.find_all('p'):
        text = p.get_text().strip()
        if len(text) > 100 and 'cookie' not in text.lower():
            return text[:155] + '...' if len(text) > 155 else text
    return ""

def extract_first_image(soup):
    """Extract first meaningful image for og:image"""
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src and 'logo' not in src.lower() and 'icon' not in src.lower():
            if src.startswith('../'):
                src = src.replace('../', 'https://gunslingersrevenge.com/')
            elif not src.startswith('http'):
                src = 'https://gunslingersrevenge.com/' + src.lstrip('/')
            return src
    return 'https://gunslingersrevenge.com/assets/gunslingers-revenge-logo.png'

def create_structured_data(title, description, category, filepath, image_url):
    """Create Schema.org structured data for the post"""
    
    # Determine schema type based on content
    if 'review' in filepath.lower():
        schema_type = "Review"
    elif 'guide' in filepath.lower() or 'how' in title.lower():
        schema_type = "HowTo"
    elif 'news' in filepath.lower():
        schema_type = "NewsArticle"
    else:
        schema_type = "Article"
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "headline": title,
        "description": description,
        "image": image_url,
        "author": {
            "@type": "Organization",
            "name": "Gunslinger's Revenge",
            "url": "https://gunslingersrevenge.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Gunslinger's Revenge",
            "logo": {
                "@type": "ImageObject",
                "url": "https://gunslingersrevenge.com/assets/gunslingers-revenge-logo.png"
            }
        },
        "datePublished": "2024-08-01",
        "dateModified": datetime.now().strftime("%Y-%m-%d"),
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://gunslingersrevenge.com/{filepath}"
        }
    }
    
    # Add review-specific fields
    if schema_type == "Review":
        structured_data["itemReviewed"] = {
            "@type": "VideoGame",
            "name": title.split(':')[0].replace(' Review', '').strip()
        }
        structured_data["reviewRating"] = {
            "@type": "Rating",
            "ratingValue": "4.5",
            "bestRating": "5"
        }
    
    return structured_data

def add_comprehensive_seo(filepath):
    """Add all missing SEO elements to a blog post"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.find('head')
    
    if not head:
        print(f"No head tag found in {filepath}")
        return False
    
    # Extract existing title
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()
    
    # Extract or create description
    meta_desc = soup.find('meta', {'name': 'description'})
    description = meta_desc.get('content') if meta_desc else extract_first_paragraph(soup)
    
    # Get category and image
    category = get_post_category(filepath)
    image_url = extract_first_image(soup)
    
    # Generate canonical URL
    canonical_path = filepath.replace('/Users/josephcharlesepstein/Desktop/gunslingers-revenge-site/', '')
    canonical_url = f"https://gunslingersrevenge.com/{canonical_path}"
    
    # Remove existing SEO tags to avoid duplicates
    for tag in soup.find_all('meta', {'property': re.compile('^og:')}):
        tag.decompose()
    for tag in soup.find_all('meta', {'name': re.compile('^twitter:')}):
        tag.decompose()
    for tag in soup.find_all('link', {'rel': 'canonical'}):
        tag.decompose()
    for tag in soup.find_all('script', {'type': 'application/ld+json'}):
        tag.decompose()
    
    # Add comprehensive Open Graph tags
    og_tags = [
        ('og:title', title),
        ('og:description', description),
        ('og:type', 'article'),
        ('og:url', canonical_url),
        ('og:image', image_url),
        ('og:site_name', "Gunslinger's Revenge"),
        ('article:section', category),
        ('article:published_time', '2024-08-01'),
        ('article:modified_time', datetime.now().strftime("%Y-%m-%d")),
        ('article:author', 'https://gunslingersrevenge.com/about')
    ]
    
    for property_name, content_value in og_tags:
        new_tag = soup.new_tag('meta')
        new_tag['property'] = property_name
        new_tag['content'] = content_value
        head.append(new_tag)
    
    # Add Twitter Card tags
    twitter_tags = [
        ('twitter:card', 'summary_large_image'),
        ('twitter:title', title),
        ('twitter:description', description),
        ('twitter:image', image_url),
        ('twitter:site', '@gunslingersrev')
    ]
    
    for tag_name, content_value in twitter_tags:
        new_tag = soup.new_tag('meta')
        new_tag['name'] = tag_name
        new_tag['content'] = content_value
        head.append(new_tag)
    
    # Add canonical link
    canonical_tag = soup.new_tag('link', rel='canonical', href=canonical_url)
    head.append(canonical_tag)
    
    # Add structured data
    structured_data = create_structured_data(title, description, category, canonical_path, image_url)
    script_tag = soup.new_tag('script', type='application/ld+json')
    script_tag.string = json.dumps(structured_data, indent=2)
    head.append(script_tag)
    
    # Add author meta tag
    author_tag = soup.new_tag('meta')
    author_tag['name'] = 'author'
    author_tag['content'] = 'Gunslinger\'s Revenge Team'
    head.append(author_tag)
    
    # Add robots meta tag for better indexing
    robots_tag = soup.new_tag('meta')
    robots_tag['name'] = 'robots'
    robots_tag['content'] = 'index, follow, max-image-preview:large'
    head.append(robots_tag)
    
    # Save the enhanced file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def main():
    """Process all blog posts"""
    posts_dir = 'posts'
    processed = 0
    errors = 0
    
    print("Starting comprehensive SEO enhancement...")
    print("-" * 50)
    
    for root, dirs, files in os.walk(posts_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    if add_comprehensive_seo(filepath):
                        processed += 1
                        print(f"✓ Enhanced: {filepath}")
                    else:
                        errors += 1
                        print(f"✗ Error: {filepath}")
                except Exception as e:
                    errors += 1
                    print(f"✗ Failed {filepath}: {str(e)}")
    
    print("-" * 50)
    print(f"SEO Enhancement Complete!")
    print(f"Successfully processed: {processed} posts")
    print(f"Errors: {errors}")
    print("\nNext steps:")
    print("1. Submit sitemap.xml to Google Search Console")
    print("2. Request indexing for all pages")
    print("3. Monitor rankings and adjust keywords")

if __name__ == "__main__":
    main()