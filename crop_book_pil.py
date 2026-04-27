from PIL import Image

img = Image.open('images/header - celular + livro.png').convert('RGBA')
width, height = img.size

# Extract alpha channel
alpha = img.split()[3]
pixels = alpha.load()

# Find the column with the minimum alpha sum in the middle 50% of the image
mid_start = width // 4
mid_end = (width * 3) // 4

min_alpha_sum = float('inf')
split_x = width // 2

for x in range(mid_start, mid_end):
    col_sum = sum(pixels[x, y] for y in range(height))
    if col_sum < min_alpha_sum:
        min_alpha_sum = col_sum
        split_x = x

# Now split_x is the gap between the phone and the book.
# The book is usually on the right, phone on the left, or vice versa.
# Let's crop both halves
left_half = img.crop((0, 0, split_x, height))
right_half = img.crop((split_x, 0, width, height))

# We can get the bounding box of each to see its aspect ratio
bbox_left = left_half.getbbox()
bbox_right = right_half.getbbox()

if bbox_left and bbox_right:
    left_w = bbox_left[2] - bbox_left[0]
    left_h = bbox_left[3] - bbox_left[1]
    right_w = bbox_right[2] - bbox_right[0]
    right_h = bbox_right[3] - bbox_right[1]
    
    aspect_left = left_w / left_h
    aspect_right = right_w / right_h
    
    # Book is wider (aspect ratio closer to 1 or > 1), phone is taller (aspect ratio < 0.6)
    if aspect_left > aspect_right:
        # Left is the book
        book = left_half.crop(bbox_left)
        phone = right_half.crop(bbox_right)
    else:
        # Right is the book
        book = right_half.crop(bbox_right)
        phone = left_half.crop(bbox_left)
        
    book.save('images/livro_icone.png')
    print('Successfully cropped the book to images/livro_icone.png')
else:
    print('Failed to get bounding boxes')
