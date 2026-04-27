from rembg import remove
from PIL import Image

input_path = 'images/digital_guide_v2.png'
output_path = 'images/digital_guide_v2_nobg.png'

print("Removing background...")
with open(input_path, 'rb') as i:
    input_bytes = i.read()
    output_bytes = remove(input_bytes)
with open(output_path, 'wb') as o:
    o.write(output_bytes)

print("Cropping bounding box...")
img = Image.open(output_path)
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)
    img.save(output_path, "PNG")
print("Done!")
