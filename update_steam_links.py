#!/usr/bin/env python3
"""
Update all Steam links to show Coming Soon popup
"""

import re
from pathlib import Path

def update_steam_links_in_file(file_path):
    """Update Steam links in a single HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace href links to Steam with onclick handlers
    # Pattern 1: Links with Steam URL
    content = re.sub(
        r'href="https://store\.steampowered\.com/app/XXXXX/Gunslingers_Revenge/"[^>]*target="_blank"',
        'href="#" onclick="showComingSoonPopup(); return false;"',
        content
    )
    
    # Pattern 2: window.open calls to Steam
    content = re.sub(
        r"window\.open\('https://store\.steampowered\.com/app/XXXXX/Gunslingers_Revenge/', '_blank'\)",
        "showComingSoonPopup()",
        content
    )
    
    # Add the Coming Soon popup function if not already present
    if 'showComingSoonPopup' not in content and '</body>' in content:
        popup_script = """
    <script>
        function showComingSoonPopup() {
            // Show the newsletter popup with coming soon message
            const popup = document.getElementById('newsletter-popup');
            if (popup) {
                popup.classList.add('active');
                // Update the title to mention Steam coming soon
                const title = popup.querySelector('h3');
                if (title) {
                    title.textContent = 'Steam Launch Coming Soon!';
                }
                const subtitle = popup.querySelector('p');
                if (subtitle) {
                    subtitle.textContent = 'Be the first to know when Gunslinger\\'s Revenge launches on Steam. Join our newsletter for exclusive early access!';
                }
            } else {
                // Fallback alert if popup not found
                alert('Steam launch coming soon! Join our newsletter to be notified when we go live.');
                // Try to focus newsletter form if it exists
                const emailInput = document.querySelector('input[type="email"]');
                if (emailInput) {
                    emailInput.focus();
                }
            }
        }
    </script>
"""
        content = content.replace('</body>', popup_script + '\n</body>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Update all HTML files
html_files = list(Path(".").glob("**/*.html"))
for html_file in html_files:
    if "assets_backup" not in str(html_file) and "venv" not in str(html_file):
        print(f"Updating {html_file}...")
        update_steam_links_in_file(html_file)

print("\nSteam link updates complete!")