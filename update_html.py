import re
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace .jpg, .jpeg, .png with .webp for image sources
html = re.sub(r'src="([^"]+?)\.(jpg|jpeg|png)"', r'src="\1.webp"', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.html image sources to webp")
