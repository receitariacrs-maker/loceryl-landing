import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix WhatsApp CSS
html = re.sub(r'#wa-float\s*\{\s*position:\s*fixed;\s*bottom:\s*24px;', 
              r'#wa-float {\n      position: fixed;\n      bottom: 96px;', html)

# 2. Fix Social Toast HTML (Replacing the 🛒 or ?? emoji)
html = re.sub(r'<div id="social-toast">\s*<div style="font-size:24px">.*?</div>',
              r'<div id="social-toast">\n    <img src="images/Favicon Loceryl.png" alt="Premium" style="background:var(--cream-light); padding:4px; border:1px solid var(--amber-gold);">', html)

# 3. Fix Social Toast JS logic (Replacing setInterval with random timeouts)
js_target = r'''    setInterval\(\(\) => \{
      stName\.innerHTML = <strong>\$\{names\[Math\.floor\(Math\.random\(\)\*names\.length\)\]\}<\/strong>;
      socialToast\.classList\.add\('show'\);
      if \(navigator\.vibrate\) \{ try\{ navigator\.vibrate\(\[30, 50, 30\]\); \} catch\(e\)\{\} \}
      setTimeout\(\(\) => \{ socialToast\.classList\.remove\('show'\); \}, 6000\);
    \}, 22000\); // 22s interval'''

js_replacement = r'''    function showToast() {
      stName.innerHTML = <strong></strong>;
      socialToast.classList.add('show');
      if (navigator.vibrate) { try{ navigator.vibrate([30, 50, 30]); } catch(e){} }
      setTimeout(() => { 
        socialToast.classList.remove('show'); 
        setTimeout(showToast, Math.floor(Math.random() * 25000) + 12000); // 12s to 37s
      }, 6000);
    }
    setTimeout(showToast, Math.floor(Math.random() * 10000) + 5000);'''

html = re.sub(js_target, js_replacement, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done")
