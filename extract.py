import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    with open('check.js', 'w', encoding='utf-8') as f:
        f.write(scripts[-1])
    print("Extracted JS to check.js")
