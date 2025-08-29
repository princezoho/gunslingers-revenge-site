#!/usr/bin/env python3
"""
Quick performance optimizations for Gunslinger's Revenge - No dependencies required
Focus on immediate wins: lazy loading, defer scripts, optimize critical path
"""

import os
import re
from pathlib import Path

def add_lazy_loading():
    """Add lazy loading to images"""
    print("🖼️  Adding lazy loading to images...")
    
    modified = 0
    for html_file in Path(".").glob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Add lazy loading to images (except logo and hero images)
        def add_loading(match):
            img_tag = match.group(0)
            src = match.group(2)
            
            # Skip critical above-fold images
            skip_keywords = ['logo', 'hero', 'revenge-fire', 'your-turn-ui', 'enemy-turn-ui', 'horse-charms']
            if any(keyword in src.lower() for keyword in skip_keywords):
                return img_tag
            
            # Check if loading attribute already exists
            if 'loading=' in img_tag:
                return img_tag
            
            # Add lazy loading
            return img_tag.replace('>', ' loading="lazy">')
        
        content = re.sub(r'(<img\s+[^>]*src="([^"]+)"[^>]*>)', add_loading, content)
        
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            modified += 1
            print(f"  ✓ {html_file.name}")
    
    print(f"✅ Modified {modified} files\n")

def optimize_index_critical_path():
    """Optimize index.html for faster initial load"""
    print("⚡ Optimizing index.html critical rendering path...")
    
    index_path = Path("index.html")
    if not index_path.exists():
        print("  ✗ index.html not found")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add preconnect for external resources
    preconnects = """    <!-- DNS Prefetch and Preconnect for faster loading -->
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
    <link rel="dns-prefetch" href="https://www.google-analytics.com">
    
    <!-- Preload critical resources -->
    <link rel="preload" href="assets/logo-revenge-fire.png" as="image" fetchpriority="high">
    <link rel="preload" href="css/theme.css" as="style">
    """
    
    if 'dns-prefetch' not in content:
        content = content.replace('    <meta charset="UTF-8">', '    <meta charset="UTF-8">\n' + preconnects)
        print("  ✓ Added resource hints")
    
    # 2. Add critical inline CSS for above-the-fold
    critical_css = """
    <style>
        /* Critical inline CSS for faster first paint */
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#1a1a1a;color:#fff}
        .hero{min-height:100vh;display:flex;align-items:center;justify-content:center;position:relative;background:#000}
        .hero-overlay{text-align:center;z-index:2;padding:2rem}
        .hero-logo-title{max-width:90%;width:600px;height:auto}
        .hero-subtitle{font-size:1.5rem;margin:1rem 0 2rem;color:#f5e9dc}
        .btn{display:inline-block;padding:1rem 2rem;text-decoration:none;border-radius:4px;transition:all 0.3s}
        .btn-primary{background:#c87f2f;color:#fff}
        .btn-primary:hover{background:#a86928}
        .site-nav{position:fixed;top:0;width:100%;background:rgba(0,0,0,0.9);z-index:1000;padding:1rem}
        .logo{height:50px}
        @media(max-width:768px){.hero-subtitle{font-size:1.2rem}}
    </style>"""
    
    if '/* Critical inline CSS' not in content:
        content = content.replace('</title>', '</title>' + critical_css)
        print("  ✓ Added critical CSS inline")
    
    # 3. Defer non-critical CSS
    content = re.sub(
        r'<link rel="stylesheet" href="(custom\.css[^"]*)"',
        r'<link rel="preload" href="\1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="\1"></noscript>',
        content
    )
    
    content = re.sub(
        r'<link rel="stylesheet" href="(nav-dropdown\.css[^"]*)"',
        r'<link rel="preload" href="\1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"><noscript><link rel="stylesheet" href="\1"></noscript>',
        content
    )
    
    # 4. Add async/defer to scripts
    content = re.sub(
        r'<script src="optimize\.js"',
        r'<script src="optimize.js" defer',
        content
    )
    
    # 5. Move scripts to bottom if they're in head (except GA)
    # This is more complex, skip for safety
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ Optimized critical rendering path")
    print("✅ index.html optimized\n")

def optimize_all_pages_scripts():
    """Defer non-critical JavaScript on all pages"""
    print("📜 Optimizing JavaScript loading...")
    
    modified = 0
    for html_file in Path(".").glob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Add defer to optimize.js
        content = re.sub(
            r'<script src="optimize\.js"(?![^>]*(?:defer|async))',
            r'<script src="optimize.js" defer',
            content
        )
        
        if content != original:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            modified += 1
            print(f"  ✓ {html_file.name}")
    
    print(f"✅ Optimized {modified} files\n")

def create_image_optimization_script():
    """Create a shell script for image optimization using system tools"""
    print("🛠️  Creating image optimization script...")
    
    script_content = """#!/bin/bash
# Image optimization script for Gunslinger's Revenge
# Uses ImageMagick (convert) or other system tools

echo "🖼️  Optimizing images in assets folder..."

# Create optimized directory
mkdir -p assets/optimized

# Counter
count=0

# Optimize PNGs
for img in assets/*.png; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        echo "Processing $filename..."
        
        # Use ImageMagick if available
        if command -v convert &> /dev/null; then
            convert "$img" -quality 85 -resize '1920>' "assets/optimized/$filename"
            ((count++))
        # Use sips on macOS
        elif command -v sips &> /dev/null; then
            sips -Z 1920 "$img" --out "assets/optimized/$filename" 2>/dev/null
            ((count++))
        else
            echo "No image optimization tool found. Install ImageMagick."
            break
        fi
    fi
done

# Optimize JPGs
for img in assets/*.jpg assets/*.jpeg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        echo "Processing $filename..."
        
        if command -v convert &> /dev/null; then
            convert "$img" -quality 85 -resize '1920>' "assets/optimized/$filename"
            ((count++))
        elif command -v sips &> /dev/null; then
            sips -Z 1920 "$img" --out "assets/optimized/$filename" 2>/dev/null
            ((count++))
        fi
    fi
done

echo "✅ Optimized $count images"
echo "📁 Optimized images saved in assets/optimized/"
echo ""
echo "To use optimized images:"
echo "1. Review images in assets/optimized/"
echo "2. If satisfied: mv assets assets.backup && mv assets/optimized assets"
"""
    
    with open("optimize_images.sh", 'w') as f:
        f.write(script_content)
    
    os.chmod("optimize_images.sh", 0o755)
    print("  ✓ Created optimize_images.sh")
    print("  Run with: ./optimize_images.sh\n")

def add_htaccess_compression():
    """Add compression rules to .htaccess"""
    print("📦 Adding compression rules to .htaccess...")
    
    compression_rules = """
# Enable Gzip Compression
<IfModule mod_deflate.c>
    # Compress HTML, CSS, JavaScript, Text, XML
    AddOutputFilterByType DEFLATE application/javascript
    AddOutputFilterByType DEFLATE application/rss+xml
    AddOutputFilterByType DEFLATE application/vnd.ms-fontobject
    AddOutputFilterByType DEFLATE application/x-font
    AddOutputFilterByType DEFLATE application/x-font-opentype
    AddOutputFilterByType DEFLATE application/x-font-otf
    AddOutputFilterByType DEFLATE application/x-font-truetype
    AddOutputFilterByType DEFLATE application/x-font-ttf
    AddOutputFilterByType DEFLATE application/x-javascript
    AddOutputFilterByType DEFLATE application/xhtml+xml
    AddOutputFilterByType DEFLATE application/xml
    AddOutputFilterByType DEFLATE font/opentype
    AddOutputFilterByType DEFLATE font/otf
    AddOutputFilterByType DEFLATE font/ttf
    AddOutputFilterByType DEFLATE image/svg+xml
    AddOutputFilterByType DEFLATE image/x-icon
    AddOutputFilterByType DEFLATE text/css
    AddOutputFilterByType DEFLATE text/html
    AddOutputFilterByType DEFLATE text/javascript
    AddOutputFilterByType DEFLATE text/plain
    AddOutputFilterByType DEFLATE text/xml
</IfModule>

# Browser Caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType image/jpeg "access plus 1 month"
    ExpiresByType image/gif "access plus 1 month"
    ExpiresByType image/png "access plus 1 month"
    ExpiresByType text/css "access plus 1 week"
    ExpiresByType text/html "access plus 1 hour"
    ExpiresByType text/javascript "access plus 1 week"
    ExpiresByType application/javascript "access plus 1 week"
    ExpiresDefault "access plus 2 days"
</IfModule>
"""
    
    htaccess_path = Path(".htaccess")
    
    if htaccess_path.exists():
        with open(htaccess_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'mod_deflate' not in content:
            with open(htaccess_path, 'a', encoding='utf-8') as f:
                f.write(compression_rules)
            print("  ✓ Added compression rules to .htaccess")
        else:
            print("  ℹ Compression rules already present")
    else:
        print("  ℹ .htaccess not found, skipping")
    
    print()

def main():
    print("🚀 Quick Performance Optimization for Gunslinger's Revenge")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("index.html").exists():
        print("❌ Error: index.html not found.")
        print("Please run from the website root directory.")
        return 1
    
    # Run optimizations
    add_lazy_loading()
    optimize_index_critical_path()
    optimize_all_pages_scripts()
    create_image_optimization_script()
    add_htaccess_compression()
    
    print("=" * 60)
    print("✅ Quick optimizations complete!")
    print("\n📊 What was done:")
    print("  • Added lazy loading to images")
    print("  • Optimized critical rendering path")
    print("  • Deferred non-critical JavaScript")
    print("  • Created image optimization script")
    print("  • Added compression rules")
    
    print("\n🎯 Next steps:")
    print("1. Run image optimization: ./optimize_images.sh")
    print("2. Test locally to ensure everything works")
    print("3. Commit changes: git add -A && git commit -m 'Optimize page performance'")
    print("4. Push to GitHub: git push")
    
    print("\n💡 Your biggest performance wins will come from:")
    print("  • Optimizing the 214MB of images in assets/")
    print("  • Consider using a CDN like Cloudflare (free tier)")
    print("  • Replace large GIFs with videos (MP4/WebM)")
    
    return 0

if __name__ == '__main__':
    exit(main())