#!/usr/bin/env python3
"""
Add Google Analytics 4 (GA4) tracking code to all HTML files in the Gunslinger's Revenge website
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

def get_ga4_script(measurement_id):
    """Generate the GA4 tracking script"""
    return f"""<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{measurement_id}');
</script>
<!-- End Google Analytics 4 -->"""

def add_analytics_to_html(file_path, measurement_id, dry_run=False):
    """Add Google Analytics to a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if GA is already present
        if 'googletagmanager.com/gtag' in content or measurement_id in content:
            print(f"✓ {file_path} - Already has Google Analytics")
            return False
        
        soup = BeautifulSoup(content, 'html.parser')
        head = soup.find('head')
        
        if not head:
            print(f"⚠ {file_path} - No <head> tag found, skipping")
            return False
        
        # Create the GA script as a BeautifulSoup object
        ga_script = BeautifulSoup(get_ga4_script(measurement_id), 'html.parser')
        
        # Find the best position (after meta charset or at the beginning)
        charset_meta = head.find('meta', charset=True)
        if charset_meta:
            # Insert after charset meta tag
            for element in reversed(ga_script.contents):
                if element != '\n':
                    charset_meta.insert_after(element)
        else:
            # Insert at the beginning of head
            for element in reversed(ga_script.contents):
                if element != '\n':
                    head.insert(0, element)
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            print(f"✅ {file_path} - Added Google Analytics")
        else:
            print(f"[DRY RUN] Would add GA to {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ {file_path} - Error: {e}")
        return False

def process_repository(repo_path, measurement_id, dry_run=False):
    """Process all HTML files in the repository"""
    
    # Files to process
    html_files = []
    
    # Check if it's a local directory
    if os.path.exists(repo_path):
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and node_modules
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
    else:
        # Fetch from GitHub
        print(f"Fetching file list from GitHub repository...")
        
        # List of known HTML files from the repository
        known_files = [
            'index.html', 'blog.html', 'blog-index.html', 'blog-index-complete.html',
            'cards.html', 'characters.html', 'contact.html', 'downloads.html',
            'faq.html', 'game-guide.html', 'gallery.html', 'game-mechanics.html',
            'history.html', 'news.html', 'play-now.html', 'privacy-policy.html',
            'rules.html', 'social.html', 'story.html', 'support.html',
            'terms-of-service.html', 'tournaments.html'
        ]
        
        for file in known_files:
            html_files.append(file)
    
    print(f"\nFound {len(html_files)} HTML files to process")
    print(f"Using GA4 Measurement ID: {measurement_id}")
    if dry_run:
        print("Running in DRY RUN mode - no files will be modified\n")
    else:
        print()
    
    modified_count = 0
    for file_path in html_files:
        if add_analytics_to_html(file_path, measurement_id, dry_run):
            modified_count += 1
    
    print(f"\n{'Would modify' if dry_run else 'Modified'} {modified_count} files")
    print(f"Skipped {len(html_files) - modified_count} files (already have GA or errors)")
    
    return modified_count

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Add Google Analytics 4 to Gunslinger\'s Revenge website')
    parser.add_argument('measurement_id', help='GA4 Measurement ID (e.g., G-XXXXXXXXXX)')
    parser.add_argument('--path', default='.', help='Path to repository (default: current directory)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without modifying files')
    
    args = parser.parse_args()
    
    # Validate measurement ID format
    if not re.match(r'^G-[A-Z0-9]{10}$', args.measurement_id):
        print(f"Error: Invalid GA4 Measurement ID format: {args.measurement_id}")
        print("Expected format: G-XXXXXXXXXX (G- followed by 10 alphanumeric characters)")
        return 1
    
    # Process the repository
    modified = process_repository(args.path, args.measurement_id, args.dry_run)
    
    if not args.dry_run and modified > 0:
        print("\n✅ Google Analytics has been added successfully!")
        print("\nNext steps:")
        print("1. Review the changes with: git diff")
        print("2. Commit the changes: git add -A && git commit -m 'Add Google Analytics 4 tracking'")
        print("3. Push to GitHub: git push")
        print("4. Verify in Google Analytics Real-Time reports after deployment")
    
    return 0

if __name__ == '__main__':
    exit(main())