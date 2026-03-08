import os
from PIL import Image

def optimize_images():
    count = 0
    total_saved = 0
    directory = "."
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            filepath = os.path.join(directory, filename)
            original_size = os.path.getsize(filepath)
            
            # Skip fairly small WebP files to strictly avoid quality loss on already optimized ones
            if original_size < 100 * 1024 and filename.lower().endswith('.webp'):
                continue

            try:
                base_name = os.path.splitext(filename)[0]
                webp_filepath = os.path.join(directory, f"{base_name}.webp")
                
                with Image.open(filepath) as img:
                    # Resize if width > 1600
                    if img.width > 1600:
                        ratio = 1600.0 / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((1600, new_height), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB/RGBA for WebP saving
                    if img.mode not in ("RGB", "RGBA"):
                        if img.mode in ("P", "LA"):
                            img = img.convert("RGBA")
                        else:
                            img = img.convert("RGB")
                    
                    # Save as WebP
                    img.save(webp_filepath, "webp", optimize=True, quality=80)

                new_size = os.path.getsize(webp_filepath)
                
                if filepath != webp_filepath:
                    os.remove(filepath)
                    print(f"Converted {filename} to WebP: {original_size // 1024}KB -> {new_size // 1024}KB")
                    total_saved += (original_size - new_size)
                    count += 1
                else:
                    if new_size < original_size:
                        print(f"Optimized {filename}: {original_size // 1024}KB -> {new_size // 1024}KB")
                        total_saved += (original_size - new_size)
                        count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nDone! Processed {count} images, saved {total_saved // (1024 * 1024)}MB total.")

if __name__ == "__main__":
    optimize_images()
