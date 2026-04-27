import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the old CSS
old_css = r'    body\.text-large \{ font-size: 22px !important; \}\s*body\.text-large h1 \{ font-size: 1\.15em; \}\s*body\.text-large h2\.section-title \{ font-size: 1\.25em; \}\s*body\.text-large \.section-body \{ font-size: 21px; \}\s*body\.text-large \.pain-list li \{ font-size: 18px; \}'

new_css = r'''    /* A11Y TEXT SCALES */
    body.text-medium { font-size: 18px !important; }
    body.text-medium .hero-sub, body.text-medium .section-body, body.text-medium .pain-list li, body.text-medium .step-how-text, body.text-medium .faq-body-inner, body.text-medium .guarantee-box p, body.text-medium .author-copy p { font-size: 19px !important; line-height: 1.6; }
    body.text-medium h1 { font-size: 42px !important; }
    body.text-medium h2.section-title { font-size: 34px !important; }
    body.text-medium .btn-cta { font-size: 20px !important; }

    body.text-large { font-size: 22px !important; }
    body.text-large .hero-sub, body.text-large .section-body, body.text-large .pain-list li, body.text-large .step-how-text, body.text-large .faq-body-inner, body.text-large .guarantee-box p, body.text-large .author-copy p { font-size: 23px !important; line-height: 1.6; }
    body.text-large h1 { font-size: 48px !important; }
    body.text-large h2.section-title { font-size: 38px !important; }
    body.text-large .btn-cta { font-size: 22px !important; }'''

html = re.sub(old_css, new_css, html)

# 2. Replace the old JS
old_js = r'''  const a11yBtn = document\.getElementById\('a11y-btn'\);\s*if\(a11yBtn\) \{\s*a11yBtn\.addEventListener\('click', \(\) => \{\s*document\.body\.classList\.toggle\('text-large'\);\s*vibrate\(\);\s*\}\);\s*\}'''

new_js = r'''  const a11yBtn = document.getElementById('a11y-btn');
  if(a11yBtn) {
    let sizeState = 0; // 0=normal, 1=medium, 2=large
    a11yBtn.addEventListener('click', () => {
      sizeState = (sizeState + 1) % 3;
      document.body.classList.remove('text-medium', 'text-large');
      
      if(sizeState === 1) {
        document.body.classList.add('text-medium');
        a11yBtn.innerHTML = 'A++'; // visual indicator
      } else if(sizeState === 2) {
        document.body.classList.add('text-large');
        a11yBtn.innerHTML = 'A-'; // reset indicator
      } else {
        a11yBtn.innerHTML = 'A+'; // normal
      }
      if(navigator.vibrate) { try{ navigator.vibrate(50); }catch(e){} }
    });
  }'''

html = re.sub(old_js, new_js, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Text sizes updated")
