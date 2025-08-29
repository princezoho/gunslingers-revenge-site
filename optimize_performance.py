#!/usr/bin/env python3
"""
Performance optimization script for Gunslinger's Revenge website
Optimizes images, adds lazy loading, minifies code, and improves page speed
"""

import os
import re
import json
import subprocess
from pathlib import Path
from PIL import Image
import shutil

def optimize_images():
    """Optimize all images in assets folder"""
    print("\n🖼️  Optimizing Images...")
    
    optimized_count = 0
    total_saved = 0
    
    assets_dir = Path("assets")
    
    # Create optimized directory
    optimized_dir = assets_dir / "optimized"
    optimized_dir.mkdir(exist_ok=True)
    
    for img_path in assets_dir.glob("*"):
        if img_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            try:
                original_size = img_path.stat().st_size
                
                # Open and optimize image
                img = Image.open(img_path)
                
                # Convert RGBA to RGB if saving as JPEG
                if img_path.suffix.lower() in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                    img = rgb_img
                
                # Resize if too large (max 1920px width for web)
                if img.width > 1920:
                    ratio = 1920 / img.width
                    new_size = (1920, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save optimized version
                output_path = optimized_dir / img_path.name
                
                if img_path.suffix.lower() == '.png':
                    img.save(output_path, 'PNG', optimize=True, quality=85)
                else:
                    img.save(output_path, 'JPEG', optimize=True, quality=85, progressive=True)
                
                new_size = output_path.stat().st_size
                saved = original_size - new_size
                
                if saved > 0:
                    total_saved += saved
                    optimized_count += 1
                    print(f"  ✓ {img_path.name}: {original_size//1024}KB → {new_size//1024}KB (saved {saved//1024}KB)")
                
            except Exception as e:
                print(f"  ✗ Error optimizing {img_path.name}: {e}")
    
    print(f"\n✅ Optimized {optimized_count} images, saved {total_saved//1024//1024}MB total")
    return optimized_count

def add_lazy_loading_to_html():
    """Add lazy loading to all images in HTML files"""
    print("\n🔄 Adding Lazy Loading to Images...")
    
    modified_files = 0
    
    for html_file in Path(".").glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Add lazy loading to img tags (except hero/above-fold images)
            # Skip logo and hero images
            content = re.sub(
                r'<img\s+([^>]*?)src="(assets/[^"]+)"([^>]*?)(?<!loading="[^"]+")([^>]*?)>',
                lambda m: f'<img {m.group(1)}src="{m.group(2)}"{m.group(3)}{m.group(4)}>' 
                if 'logo' in m.group(2).lower() or 'hero' in m.group(2).lower() or 'revenge-fire' in m.group(2).lower()
                else f'<img {m.group(1)}src="{m.group(2)}"{m.group(3)} loading="lazy"{m.group(4)}>',
                content
            )
            
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_files += 1
                print(f"  ✓ {html_file.name}")
        
        except Exception as e:
            print(f"  ✗ Error processing {html_file.name}: {e}")
    
    print(f"✅ Added lazy loading to {modified_files} HTML files")
    return modified_files

def minify_css():
    """Minify CSS files"""
    print("\n📦 Minifying CSS Files...")
    
    css_files = list(Path(".").glob("*.css")) + list(Path("css").glob("*.css"))
    minified_count = 0
    
    for css_file in css_files:
        try:
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            original_size = len(css_content)
            
            # Basic CSS minification
            # Remove comments
            css_content = re.sub(r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/', '', css_content)
            # Remove unnecessary whitespace
            css_content = re.sub(r'\s+', ' ', css_content)
            css_content = re.sub(r'\s*([{}:;,])\s*', r'\1', css_content)
            
            # Save minified version
            minified_path = css_file.parent / f"{css_file.stem}.min.css"
            with open(minified_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            new_size = len(css_content)
            saved_percent = ((original_size - new_size) / original_size) * 100
            
            print(f"  ✓ {css_file.name} → {minified_path.name} (reduced {saved_percent:.1f}%)")
            minified_count += 1
            
        except Exception as e:
            print(f"  ✗ Error minifying {css_file.name}: {e}")
    
    print(f"✅ Minified {minified_count} CSS files")
    return minified_count

def add_preconnect_and_prefetch():
    """Add preconnect and prefetch tags for better performance"""
    print("\n🔗 Adding Performance Hints to HTML...")
    
    performance_hints = """    <!-- Performance optimizations -->
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.google-analytics.com">
    <link rel="preload" href="css/theme.css" as="style">
    <link rel="preload" href="style.css?v=3" as="style">
    <link rel="preload" href="assets/logo-revenge-fire.png" as="image" fetchpriority="high">
"""
    
    for html_file in Path(".").glob("*.html"):
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add performance hints after <head> tag if not already present
            if 'rel="preconnect"' not in content:
                content = content.replace('<head>', '<head>\n' + performance_hints)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ {html_file.name}")
        
        except Exception as e:
            print(f"  ✗ Error processing {html_file.name}: {e}")
    
    print("✅ Added performance hints")

def optimize_index_html():
    """Special optimizations for index.html landing page"""
    print("\n🏠 Optimizing Landing Page (index.html)...")
    
    index_path = Path("index.html")
    if not index_path.exists():
        print("  ✗ index.html not found")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add critical CSS inline for above-the-fold content
    critical_css = """
    <style>
        /* Critical CSS for above-the-fold content */
        body{margin:0;font-family:system-ui,-apple-system,sans-serif}
        .hero{position:relative;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#1a1a1a}
        .hero-overlay{text-align:center;color:#fff;z-index:1}
        .site-nav{position:fixed;top:0;width:100%;background:#000;z-index:1000;padding:1rem}
        .btn-primary{display:inline-block;padding:1rem 2rem;background:#c87f2f;color:#fff;text-decoration:none;border-radius:4px}
        .logo{height:50px}
    </style>
    """
    
    # Add critical CSS right after <head>
    if '/* Critical CSS' not in content:
        content = content.replace('<head>', '<head>\n' + critical_css)
    
    # Defer non-critical CSS
    content = re.sub(
        r'<link rel="stylesheet" href="(custom\.css[^"]*)"',
        r'<link rel="preload" href="\1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"',
        content
    )
    
    # Add async to non-critical scripts
    content = re.sub(
        r'<script src="optimize\.js"',
        r'<script src="optimize.js" defer',
        content
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("  ✓ Added critical CSS inline")
    print("  ✓ Deferred non-critical styles")
    print("  ✓ Made scripts async/defer")
    print("✅ Landing page optimized")

def create_htaccess_caching():
    """Create .htaccess file with caching rules"""
    print("\n⚡ Creating .htaccess caching rules...")
    
    htaccess_content = """# Compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Browser Caching
<IfModule mod_expires.c>
    ExpiresActive On
    
    # Images
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType image/webp "access plus 1 year"
    ExpiresByType image/svg+xml "access plus 1 year"
    ExpiresByType image/x-icon "access plus 1 year"
    
    # CSS and JavaScript
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType text/javascript "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
    
    # Others
    ExpiresByType application/pdf "access plus 1 month"
    ExpiresByType application/x-shockwave-flash "access plus 1 month"
</IfModule>

# Enable Gzip compression
<IfModule mod_deflate.c>
    <FilesMatch "\\.(js|css|html|htm|php|xml|txt|ttf|otf|eot|svg)$">
        SetOutputFilter DEFLATE
    </FilesMatch>
</IfModule>

# Prevent hotlinking
RewriteEngine on
RewriteCond %{HTTP_REFERER} !^$
RewriteCond %{HTTP_REFERER} !^http(s)?://(www\\.)?gunslingersrevenge.com [NC]
RewriteRule \\.(jpg|jpeg|png|gif)$ - [NC,F,L]
"""
    
    htaccess_path = Path(".htaccess")
    
    # Append to existing .htaccess if it exists
    if htaccess_path.exists():
        with open(htaccess_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        if "Browser Caching" not in existing_content:
            with open(htaccess_path, 'a', encoding='utf-8') as f:
                f.write("\n\n" + htaccess_content)
            print("  ✓ Added caching rules to existing .htaccess")
    else:
        with open(htaccess_path, 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
        print("  ✓ Created new .htaccess with caching rules")
    
    print("✅ Caching rules configured")

def create_webp_versions():
    """Create WebP versions of images for modern browsers"""
    print("\n🎨 Creating WebP versions for modern browsers...")
    
    try:
        from PIL import Image
        webp_count = 0
        
        assets_dir = Path("assets")
        webp_dir = assets_dir / "webp"
        webp_dir.mkdir(exist_ok=True)
        
        for img_path in assets_dir.glob("*.png"):
            try:
                img = Image.open(img_path)
                webp_path = webp_dir / f"{img_path.stem}.webp"
                img.save(webp_path, 'WEBP', quality=85, method=6)
                webp_count += 1
                
                original_size = img_path.stat().st_size
                webp_size = webp_path.stat().st_size
                saved_percent = ((original_size - webp_size) / original_size) * 100
                
                if saved_percent > 0:
                    print(f"  ✓ {img_path.name} → WebP (saved {saved_percent:.1f}%)")
            
            except Exception as e:
                print(f"  ✗ Error converting {img_path.name}: {e}")
        
        print(f"✅ Created {webp_count} WebP images")
    
    except ImportError:
        print("  ⚠ Pillow not installed, skipping WebP conversion")

def main():
    print("🚀 Starting Performance Optimization for Gunslinger's Revenge")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("index.html").exists():
        print("❌ Error: index.html not found. Please run this script from the website root directory.")
        return 1
    
    # Run optimizations
    try:
        # 1. Optimize images (most important for your 214MB assets folder!)
        # Note: Requires PIL/Pillow: pip install Pillow
        try:
            optimize_images()
        except ImportError:
            print("⚠ Pillow not installed. Install with: pip install Pillow")
        
        # 2. Add lazy loading
        add_lazy_loading_to_html()
        
        # 3. Minify CSS
        minify_css()
        
        # 4. Add performance hints
        add_preconnect_and_prefetch()
        
        # 5. Optimize landing page specifically
        optimize_index_html()
        
        # 6. Create caching rules
        create_htaccess_caching()
        
        # 7. Create WebP versions (optional, for modern browsers)
        create_webp_versions()
        
        print("\n" + "=" * 60)
        print("✅ Performance optimization complete!")
        print("\n📊 Next Steps:")
        print("1. Review the changes: git diff")
        print("2. Test locally to ensure everything works")
        print("3. Commit: git add -A && git commit -m 'Optimize page performance'")
        print("4. Push: git push")
        print("5. Test with PageSpeed Insights after deployment")
        print("\n💡 Additional recommendations:")
        print("- Consider using a CDN (CloudFlare, etc.) for assets")
        print("- Enable server-side compression (gzip/brotli)")
        print("- Consider replacing large GIFs with videos (MP4/WebM)")
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())