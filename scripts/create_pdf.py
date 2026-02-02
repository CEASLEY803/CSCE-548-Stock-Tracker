"""
Combine PNG screenshots into a single PDF
"""
from PIL import Image
import os

# Get all PNG files
png_files = [
    'Tables1-4.png',
    'Table5.png',
    'tables.png',
    'Stocks.png'
]

# Filter to only existing files
existing_files = [f for f in png_files if os.path.exists(f)]

if not existing_files:
    print("No PNG files found!")
    exit(1)

print(f"Found {len(existing_files)} images:")
for f in existing_files:
    print(f"  - {f}")

# Open all images and convert to RGB (PDF requires RGB)
images = []
for filename in existing_files:
    img = Image.open(filename)
    # Convert to RGB if necessary (removes alpha channel)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    images.append(img)

# Save as PDF
output_file = 'Stock_Tracker_Screenshots.pdf'
if images:
    # First image is the base, rest are appended
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        resolution=100.0,
        quality=95
    )
    print(f"\n✓ PDF created successfully: {output_file}")
    print(f"  Total pages: {len(images)}")
else:
    print("No valid images to convert!")
