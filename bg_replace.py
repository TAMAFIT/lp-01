import sys
from rembg import remove
from PIL import Image, ImageDraw

def create_gradient_bg(size, color_top, color_bottom):
    base = Image.new('RGB', size, color_top)
    top = color_top
    bottom = color_bottom
    r_diff = bottom[0] - top[0]
    g_diff = bottom[1] - top[1]
    b_diff = bottom[2] - top[2]
    
    draw = ImageDraw.Draw(base)
    for y in range(size[1]):
        r = int(top[0] + (r_diff * y) / size[1])
        g = int(top[1] + (g_diff * y) / size[1])
        b = int(top[2] + (b_diff * y) / size[1])
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    return base

def process_image(input_path, output_path):
    try:
        print(f"Processing {input_path}...")
        input_image = Image.open(input_path).convert("RGBA")
        
        # Remove background using rembg
        transparent_image = remove(input_image)
        
        # Soft natural studio backdrop: warm light-gray/beige gradient
        # Top: very light beige, Bottom: warm medium gray
        bg = create_gradient_bg(transparent_image.size, (250, 248, 244), (225, 222, 215))
        
        # Paste the transparent image over the background
        bg.paste(transparent_image, (0, 0), transparent_image)
        
        # Save the result
        bg.save(output_path, "WEBP", quality=90)
        
        print(f"Successfully saved to {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    process_image("trainer-obayashi-orig.webp", "trainer-obayashi.webp")
    process_image("trainer-tamai-orig.webp", "trainer-tamai.webp")
