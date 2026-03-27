import os
from PIL import Image, ImageEnhance, ImageDraw
from rembg import remove, new_session

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

def enhance_image(img):
    img = ImageEnhance.Brightness(img).enhance(1.15)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = ImageEnhance.Color(img).enhance(1.10)
    return img

def main():
    brain_dir = r'C:\Users\pc1\.gemini\antigravity\brain\3ccd4aba-f3c4-4aad-94c0-f13c8cda931d'
    # The file we found:
    input_path = os.path.join(brain_dir, 'media__1774583661533.jpg')
    output_path = 'trainer-tamai.webp'
    
    obayashi_path = 'trainer-obayashi.webp'
    obayashi = Image.open(obayashi_path)
    target_w, target_h = obayashi.size
    print(f"Target size (from Obayashi): {target_w}x{target_h}")
    
    img = Image.open(input_path).convert("RGBA")
    
    # 1. Enhance
    img = enhance_image(img)
    
    # 2. Crop/Resize to match aspect ratio of target
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    
    if img_ratio > target_ratio:
        # Image is wider, crop the sides
        new_w = int(img.height * target_ratio)
        offset = (img.width - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, img.height))
    else:
        # Image is taller, crop top/bottom
        # For a portrait we usually want to keep the top (head) if possible, but let's do center
        new_h = int(img.width / target_ratio)
        offset = (img.height - new_h) // 2
        img = img.crop((0, offset, img.width, offset + new_h))
        
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 3. Remove Background using u2net_human_seg
    print("Removing background...")
    session = new_session("u2net_human_seg")
    transparent_image = remove(img, session=session)
    
    # 4. Composite over background gradient
    print("Compositing...")
    bg = create_gradient_bg((target_w, target_h), (250, 248, 244), (225, 222, 215))
    bg.paste(transparent_image, (0, 0), transparent_image)
    
    bg.save(output_path, "WEBP", quality=90)
    print("Done!")

if __name__ == '__main__':
    main()
