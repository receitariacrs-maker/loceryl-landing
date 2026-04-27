import cv2
import numpy as np
from PIL import Image

# Read image with alpha channel
img_path = 'images/header - celular + livro.png'
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

if img is None:
    print('Failed to load image')
else:
    # Extract alpha channel
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        
        # Threshold to get a binary mask of opaque objects
        _, thresh = cv2.threshold(alpha, 10, 255, cv2.THRESH_BINARY)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort by area, keep top 2
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        
        best_aspect = 0
        best_rect = None
        
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            aspect = w / h
            # The phone is tall (w/h < 1), the book is wider (w/h > phone)
            # Or the book could be just a different shape.
            if aspect > best_aspect:
                best_aspect = aspect
                best_rect = (x, y, w, h)
                
        if best_rect:
            x, y, w, h = best_rect
            # Add a small padding
            pad = 10
            H, W = alpha.shape
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(W, x + w + pad)
            y2 = min(H, y + h + pad)
            
            book_img = img[y1:y2, x1:x2]
            cv2.imwrite('images/livro_notificacao.png', book_img)
            print(f'Cropped book with aspect ratio {best_aspect:.2f}')
        else:
            print('Could not find objects')
    else:
        print('Image has no alpha channel')
