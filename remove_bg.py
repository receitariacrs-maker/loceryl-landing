from PIL import Image

def remove_bg():
    img = Image.open('images/digital_guide_v2.png').convert('RGBA')
    data = img.getdata()
    new_data = []
    for item in data:
        avg = (item[0] + item[1] + item[2]) / 3.0
        if avg > 240 and abs(item[0]-item[1]) < 15 and abs(item[1]-item[2]) < 15:
            if avg >= 252:
                new_data.append((255, 255, 255, 0))
            else:
                alpha = int(255 * (252 - avg) / 12)
                new_data.append((item[0], item[1], item[2], max(0, min(255, alpha))))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save('images/digital_guide_v2_nobg.png', 'PNG')

remove_bg()
