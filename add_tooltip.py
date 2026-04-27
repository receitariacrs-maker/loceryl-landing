import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. CSS Injection
css_target = r'#a11y-btn:active \{ transform: scale\(0\.9\); \}'
css_replacement = r'''#a11y-btn:active { transform: scale(0.9); }
    #a11y-tooltip { position: absolute; top: 50%; right: 54px; transform: translateY(-50%) translateX(20px); background: var(--brown-primary); color: white; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-family: var(--font-display); font-weight: 600; white-space: nowrap; opacity: 0; pointer-events: none; transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1); box-shadow: var(--shadow-md); letter-spacing: 0.03em; }
    #a11y-tooltip::after { content: ''; position: absolute; top: 50%; right: -5px; transform: translateY(-50%); border-width: 6px 0 6px 6px; border-style: solid; border-color: transparent transparent transparent var(--brown-primary); }
    #a11y-tooltip.show { opacity: 1; transform: translateY(-50%) translateX(0); }'''

html = re.sub(css_target, css_replacement, html)

# 2. JS Injection
js_target = r'''  const a11yBtn = document\.getElementById\('a11y-btn'\);
  if\(a11yBtn\) \{
    let sizeState = 0; // 0=normal, 1=medium, 2=large
    a11yBtn\.addEventListener\('click', \(\) => \{'''

js_replacement = r'''  const a11yBtn = document.getElementById('a11y-btn');
  if(a11yBtn) {
    const a11yTooltip = document.createElement('div');
    a11yTooltip.id = 'a11y-tooltip';
    a11yTooltip.innerHTML = 'Dificuldade para ler? <br>Clique aqui para aumentar!';
    a11yTooltip.style.textAlign = 'right';
    a11yBtn.appendChild(a11yTooltip);

    let tTimer = setTimeout(() => {
      a11yTooltip.classList.add('show');
      setTimeout(() => a11yTooltip.classList.remove('show'), 8000);
    }, 2500);

    let sizeState = 0; // 0=normal, 1=medium, 2=large
    a11yBtn.addEventListener('click', () => {
      clearTimeout(tTimer);
      a11yTooltip.classList.remove('show');'''

html = re.sub(js_target, js_replacement, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done tooltip injection")
