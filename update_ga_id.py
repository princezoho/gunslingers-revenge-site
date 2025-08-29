#!/usr/bin/env python3
"""
Update the Google Analytics Measurement ID in all HTML files
"""

import os
import sys

def update_ga_id(old_id, new_id):
    """Update GA measurement ID in all HTML files"""
    updated_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if old_id in content:
                        new_content = content.replace(old_id, new_id)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        updated_files.append(file_path)
                        print(f"✅ Updated: {file_path}")
                
                except Exception as e:
                    print(f"❌ Error updating {file_path}: {e}")
    
    return updated_files

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 update_ga_id.py G-YOUR_ACTUAL_ID")
        print("Example: python3 update_ga_id.py G-ABC1234567")
        return 1
    
    new_id = sys.argv[1]
    old_id = "G-XXXXXXXXXX"
    
    print(f"Updating GA Measurement ID from {old_id} to {new_id}")
    
    updated = update_ga_id(old_id, new_id)
    
    if updated:
        print(f"\n✅ Successfully updated {len(updated)} files")
        print("\nNext steps:")
        print("1. Review changes: git diff")
        print("2. Commit: git add -A && git commit -m 'Update Google Analytics Measurement ID'")
        print("3. Push: git push")
    else:
        print("\n⚠ No files were updated. The placeholder ID may have already been changed.")
    
    return 0

if __name__ == '__main__':
    exit(main())