#!/usr/bin/env python3
"""
Simple script to add Google Analytics 4 to HTML files without external dependencies
"""

import os
import re
import sys

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
<!-- End Google Analytics 4 -->
"""

def add_analytics_to_html(file_path, measurement_id, dry_run=False):
    """Add Google Analytics to a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if GA is already present
        if 'googletagmanager.com/gtag' in content or measurement_id in content:
            print(f"✓ {file_path} - Already has Google Analytics")
            return False
        
        # Find the </head> tag
        head_close = content.find('</head>')
        if head_close == -1:
            print(f"⚠ {file_path} - No </head> tag found, skipping")
            return False
        
        # Insert GA script before </head>
        ga_script = get_ga4_script(measurement_id)
        new_content = content[:head_close] + ga_script + content[head_close:]
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ {file_path} - Added Google Analytics")
        else:
            print(f"[DRY RUN] Would add GA to {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ {file_path} - Error: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 add_ga_simple.py G-MEASUREMENT-ID [--dry-run]")
        print("Example: python3 add_ga_simple.py G-ABC1234567 --dry-run")
        return 1
    
    measurement_id = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    # Validate measurement ID format
    if not re.match(r'^G-[A-Z0-9]{10}$', measurement_id):
        print(f"Error: Invalid GA4 Measurement ID format: {measurement_id}")
        print("Expected format: G-XXXXXXXXXX (G- followed by 10 alphanumeric characters)")
        print("Using as-is anyway for demo purposes...")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"\nFound {len(html_files)} HTML files")
    print(f"Using GA4 Measurement ID: {measurement_id}")
    if dry_run:
        print("Running in DRY RUN mode - no files will be modified\n")
    else:
        print()
    
    modified_count = 0
    for file_path in sorted(html_files):
        if add_analytics_to_html(file_path, measurement_id, dry_run):
            modified_count += 1
    
    print(f"\n{'Would modify' if dry_run else 'Modified'} {modified_count} files")
    print(f"Skipped {len(html_files) - modified_count} files")
    
    if not dry_run and modified_count > 0:
        print("\n✅ Google Analytics has been added successfully!")
        print("\nNext steps:")
        print("1. Review the changes with: git diff")
        print("2. Commit the changes: git add -A && git commit -m 'Add Google Analytics 4 tracking'")
        print("3. Push to GitHub: git push")
        print("4. Verify in Google Analytics Real-Time reports after deployment")
    
    return 0

if __name__ == '__main__':
    exit(main())