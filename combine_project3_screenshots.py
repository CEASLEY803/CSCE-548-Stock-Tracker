"""
Combine Project 3 screenshots into a single PDF document.
"""
from PIL import Image
import os

# Configuration
docs_folder = "docs"
output_pdf = "docs/Project3_Web_Client_Screenshots.pdf"

# Get all p3-*.png files and sort them numerically
screenshot_files = [f for f in os.listdir(docs_folder) if f.startswith("p3-") and f.endswith(".png")]
screenshot_files.sort(key=lambda x: int(x.split("-")[1].split(".")[0]))

print(f"Found {len(screenshot_files)} screenshots to combine:")
for i, filename in enumerate(screenshot_files, 1):
    print(f"  {i}. {filename}")

# Load all images
images = []
for filename in screenshot_files:
    filepath = os.path.join(docs_folder, filename)
    print(f"Loading {filename}...")
    img = Image.open(filepath)

    # Convert to RGB if needed (PNG might have alpha channel)
    if img.mode in ('RGBA', 'LA', 'P'):
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = rgb_img
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    images.append(img)

# Save as PDF
print(f"\nCreating PDF: {output_pdf}")
if images:
    images[0].save(
        output_pdf,
        save_all=True,
        append_images=images[1:],
        resolution=100.0,
        quality=95,
        optimize=False
    )

    # Get file size
    file_size = os.path.getsize(output_pdf)
    file_size_kb = file_size / 1024

    print(f"\n✓ SUCCESS!")
    print(f"✓ Created PDF with {len(images)} pages")
    print(f"✓ File: {output_pdf}")
    print(f"✓ Size: {file_size_kb:.1f} KB")
else:
    print("✗ No images found to combine!")
