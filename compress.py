import os
from PIL import Image

def optimize_images():
    count = 0
    total_saved = 0
    directory = "."
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(directory, filename)
            original_size = os.path.getsize(filepath)
            
            # Skip fairly small files to strictly avoid quality loss on already optimized ones
            if original_size < 300 * 1024:
                continue

            try:
                with Image.open(filepath) as img:
                    # Convert to RGB if it's not (for JPEG saving)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # Resize if width > 1600
                    if img.width > 1600:
                        ratio = 1600.0 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((1600, new_height), Image.Resampling.LANCZOS)
                    
                    # Save replacing the original
                    img.save(filepath, optimize=True, quality=80)

                new_size = os.path.getsize(filepath)
                if new_size < original_size:
                    print(f"Optimized {filename}: {original_size // 1024}KB -> {new_size // 1024}KB (-{((original_size - new_size) / original_size * 100):.1f}%)")
                    total_saved += (original_size - new_size)
                    count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nDone! Processed {count} images, saved {total_saved // (1024 * 1024)}MB total.")

if __name__ == "__main__":
    optimize_images()
