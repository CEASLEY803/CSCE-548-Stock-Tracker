"""
Combine Project 2 screenshots into a single PDF
"""
from PIL import Image
import os

# List of screenshots in order
screenshots = [
    'p1.png',  # Live Railway API
    'p2.png',  # CRUD test results
    'p3.png',  # Test summary
    'p4.png',  # Detailed CREATE/READ
    'p5.png',  # DELETE operation
    'p6.png'   # Final summary
]

# Filter to only existing files
existing_files = [f for f in screenshots if os.path.exists(f)]

if not existing_files:
    print("No screenshot files found!")
    exit(1)

print(f"Found {len(existing_files)} screenshots:")
for f in existing_files:
    print(f"  - {f}")

# Open all images and convert to RGB
images = []
for filename in existing_files:
    img = Image.open(filename)
    # Convert to RGB if necessary (removes alpha channel)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    images.append(img)

# Save as PDF
output_file = 'Project2_CRUD_Evidence.pdf'
if images:
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        resolution=100.0,
        quality=95
    )
    print(f"\n✓ PDF created successfully: {output_file}")
    print(f"  Total pages: {len(images)}")
    print("\nThis PDF is ready to submit to Blackboard!")
else:
    print("No valid images to convert!")
