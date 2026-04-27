import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the old A11Y block
html = re.sub(r'    /\* A11Y TEXT SCALES \*/.*?body\.text-large \.btn-cta \{ font-size: 22px !important; \}', 
              r'    /* A11Y TEXT SCALES */\n    body { --text-scale: 1; }\n    body.text-medium { --text-scale: 1.15; }\n    body.text-large { --text-scale: 1.30; }', 
              html, flags=re.DOTALL)

# Safely replace font-size values that are NOT already in a calc()
# We use a negative lookbehind if possible, or just be careful.
# Actually, since we only run this once, we can just replace all plain font-sizes.
# If they already have var(--text-scale, 1), we don't replace them again.

def replacer(match):
    val = match.group(1)
    unit = match.group(2)
    # If it's already a calc, do nothing (though the regex won't match calc(16px))
    return f'font-size: calc({val}{unit} * var(--text-scale, 1))'

# Match font-size: 16px
# Match font-size: 1.2em
# BUT do NOT match if it's already calc(16px * var(--text-scale, 1))
# The regex ont-size:\s*([\d\.]+)(px|em|rem) won't match calc because it doesn't have calc.
html = re.sub(r'font-size:\s*([\d\.]+)(px|em|rem)(?!\s*\*)', replacer, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done font-size variable injection")
