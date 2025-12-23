# Unused Asset Detection

This repository includes a Python script to detect unused image assets.

## Usage

Run the script from the repository root:

```bash
python3 detect_unused_assets.py
```

## What it does

The script:
- Scans for all image files (png, jpg, gif, svg, etc.) in the repository
- Checks if each image is referenced in README.md
- Supports both local file paths and GitHub blob URLs
- Reports which assets are unused and could be safely removed

## Example Output

```
🔍 Detecting unused assets...
==================================================
📁 Found 3 image file(s):
   • ./Right_Side.gif
   • ./logo-white.png
   • ./about_me.gif

📝 Found 3 file reference(s) in README.md:
   • Right_Side.gif
   • logo-white.png
   • about_me.gif

✅ All assets are being used! No unused files detected.

==================================================
📊 Summary:
   Total assets: 3
   Used assets: 3
   Unused assets: 0
```

## Security Note

This script helps maintain a clean repository and was created after removing an exposed GitHub personal access token that was found in the README.md file.