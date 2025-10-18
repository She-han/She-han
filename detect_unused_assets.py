#!/usr/bin/env python3
"""
Detect unused assets in the repository.
This script checks if image files are referenced in the README.md file.
"""

import os
import re
from pathlib import Path


def get_image_files(directory="."):
    """Get all image files in the repository."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico'}
    image_files = []
    
    for root, dirs, files in os.walk(directory):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    
    return image_files


def get_referenced_files(readme_path="README.md"):
    """Get all files referenced in README.md."""
    if not os.path.exists(readme_path):
        return set()
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all file references including GitHub blob URLs for this repo
    # Patterns: ![alt](file.ext), <img src="file.ext", GitHub blob URLs
    patterns = [
        r'!\[.*?\]\(([^http][^)]+)\)',  # Markdown image syntax (local)
        r'src="([^http][^"]+)"',        # HTML img src (local files)
        r'src=\'([^http][^\']+)\'',     # HTML img src with single quotes (local)
        r'github\.com/She-han/She-han/blob/main/([^"\')\s]+)',  # GitHub blob URLs
    ]
    
    referenced_files = set()
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            # Clean up the path
            clean_path = match.strip().lstrip('./')
            referenced_files.add(clean_path)
    
    return referenced_files


def detect_unused_assets():
    """Detect unused assets in the repository."""
    print("🔍 Detecting unused assets...")
    print("=" * 50)
    
    # Get all image files
    image_files = get_image_files()
    if not image_files:
        print("✅ No image files found in the repository.")
        return
    
    print(f"📁 Found {len(image_files)} image file(s):")
    for img in image_files:
        print(f"   • {img}")
    print()
    
    # Get referenced files from README
    referenced_files = get_referenced_files()
    print(f"📝 Found {len(referenced_files)} file reference(s) in README.md:")
    for ref in referenced_files:
        print(f"   • {ref}")
    print()
    
    # Check for unused files
    unused_files = []
    for img_path in image_files:
        # Normalize path for comparison
        img_name = os.path.basename(img_path)
        img_relative = img_path.lstrip('./')
        
        # Check if this image is referenced
        is_used = any(
            img_name in ref or img_relative in ref or img_path in ref
            for ref in referenced_files
        )
        
        if not is_used:
            unused_files.append(img_path)
    
    # Report results
    if unused_files:
        print(f"⚠️  Found {len(unused_files)} unused asset(s):")
        for unused in unused_files:
            print(f"   • {unused}")
        print("\n💡 Consider removing unused assets to keep the repository clean.")
    else:
        print("✅ All assets are being used! No unused files detected.")
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   Total assets: {len(image_files)}")
    print(f"   Used assets: {len(image_files) - len(unused_files)}")
    print(f"   Unused assets: {len(unused_files)}")


if __name__ == "__main__":
    detect_unused_assets()