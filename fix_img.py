import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the Favicon with the 3D Mockup
old_img = r'<img src="images/Favicon Loceryl.png" alt="Premium" style="background:var\(--cream-light\); padding:4px; border:1px solid var\(--amber-gold\);">'
new_img = r'<img src="images/digital_guide_v2_nobg.png" alt="Premium" style="background:var(--beige-chip); padding:2px; border:1px solid var(--amber-gold); object-fit:contain; border-radius:50%; width:40px; height:40px;">'

html = re.sub(old_img, new_img, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done replacing image")
