import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS
new_css = """
    /* --- DOPAMINE ADDITIONS --- */
    #a11y-btn { position: fixed; top: 80px; right: 16px; z-index: 1000; width: 44px; height: 44px; background: rgba(255,255,255,0.95); backdrop-filter: blur(5px); border: 2px solid var(--amber-gold); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-family: var(--font-display); color: var(--brown-primary); font-size: 16px; cursor: pointer; box-shadow: var(--shadow-md); transition: transform 0.2s; }
    #a11y-btn:active { transform: scale(0.9); }
    body.text-large { font-size: 22px !important; }
    body.text-large h1 { font-size: 1.15em; }
    body.text-large h2.section-title { font-size: 1.25em; }
    body.text-large .section-body { font-size: 21px; }
    body.text-large .pain-list li { font-size: 18px; }

    #sticky-cta { position: fixed; bottom: 16px; left: 16px; right: 16px; z-index: 999; display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--amber-gold); color: var(--brown-primary); font-weight: 800; padding: 18px; border-radius: var(--radius-pill); box-shadow: 0 10px 30px rgba(107,50,17,0.4); text-transform: uppercase; font-size: 14px; letter-spacing: 0.05em; transform: translateY(150%); transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1); animation: pulse-glow 2.5s infinite; text-decoration: none; }
    #sticky-cta.visible { transform: translateY(0); }
    @media(min-width: 768px) { #sticky-cta { display: none; } }

    #social-toast { position: fixed; bottom: 90px; left: 16px; z-index: 998; background: white; border: 1px solid var(--beige-border); border-radius: 12px; padding: 12px 16px; display: flex; align-items: center; gap: 12px; box-shadow: var(--shadow-md); transform: translateX(-150%); transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1); max-width: 280px; }
    @media(min-width: 768px) { #social-toast { bottom: 24px; max-width: 320px; } }
    #social-toast.show { transform: translateX(0); }
    #social-toast .st-text { font-size: 12px; line-height: 1.3; color: var(--text-body); }
    #social-toast .st-text strong { color: var(--brown-primary); font-weight: 700; }
    #social-toast .st-time { font-size: 10px; color: var(--text-muted); margin-top: 2px; }

    .offer-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 280px; height: 280px; background: radial-gradient(circle, rgba(212,169,106,0.6) 0%, rgba(212,169,106,0) 70%); filter: blur(20px); z-index: -1; animation: glow-pulse 3s ease-in-out infinite; pointer-events: none; }
    @media(min-width: 768px) { .offer-glow { width: 360px; height: 360px; } }
    @keyframes glow-pulse { 0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); } 50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); } }

    .pain-list.focus-active li { transition: opacity 0.4s ease, transform 0.4s ease; }
    .pain-list.focus-active li.dimmed { opacity: 0.35; transform: scale(0.96); }

    .bonus-unlock-stamp { text-align: center; font-size: 16px; font-weight: 900; color: #2A5A10; letter-spacing: 0.1em; text-transform: uppercase; background: #D8EDCA; border: 2px dashed #2A5A10; padding: 12px; border-radius: 12px; margin-bottom: 20px; transform: scale(0.5); opacity: 0; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.4s; }
    .bonus-unlock-stamp.unlocked { transform: scale(1) rotate(-2deg); opacity: 1; }
"""
content = content.replace("</style>", new_css + "\n  </style>")

# 2. HTML elements
html_overlays = """
  <div id="a11y-btn" title="Aumentar letra">A+</div>
  <a id="sticky-cta" href="#oferta">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
    Garantir Protocolo
  </a>
  <div id="social-toast">
    <div style="font-size:24px">🛒</div>
    <div class="st-text">
      <span id="st-name"><strong>Maria C.</strong> (SP)</span><br>
      Acabou de comprar o protocolo!
      <div class="st-time">Há poucos segundos</div>
    </div>
  </div>
"""
content = content.replace('<div class="noise-bg"></div>', '<div class="noise-bg"></div>\n' + html_overlays)

# 3. Offer glow
content = content.replace('<img src="images/digital_guide_v2_nobg.png" alt="O Protocolo Digital no Celular">', 
                          '<div class="offer-glow"></div>\n        <img src="images/digital_guide_v2_nobg.png" alt="O Protocolo Digital no Celular">')

# 4. Bonus Unlock
content = content.replace('<div class="bonus-cards">', 
                          '<div class="bonus-unlock-stamp" id="bonusStamp">🔓 BÔNUS DESBLOQUEADOS</div>\n        <div class="bonus-cards">')

# 5. JS
new_js = """
  // --- DOPAMINE JS --- //
  function vibrate() {
    if (navigator.vibrate) {
        try { navigator.vibrate(40); } catch(e){}
    }
  }

  document.querySelectorAll('a, button, .ba-slider').forEach(el => {
    el.addEventListener('pointerdown', vibrate, {passive: true});
  });

  const a11yBtn = document.getElementById('a11y-btn');
  if(a11yBtn) {
    a11yBtn.addEventListener('click', () => {
      document.body.classList.toggle('text-large');
      vibrate();
    });
  }

  const pBar = document.getElementById('page-progress-bar');
  const stickyCta = document.getElementById('sticky-cta');
  const heroSec = document.getElementById('hero-sec');

  window.addEventListener('scroll', () => {
    // Progress
    if(pBar) {
      const scrollPx = document.documentElement.scrollTop;
      const winHeightPx = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      pBar.style.width = ${(scrollPx / winHeightPx) * 100}%;
    }
    // Sticky CTA
    if(stickyCta && heroSec) {
      if(window.scrollY > heroSec.offsetHeight) {
        stickyCta.classList.add('visible');
      } else {
        stickyCta.classList.remove('visible');
      }
    }
  }, {passive: true});

  const socialToast = document.getElementById('social-toast');
  const stName = document.getElementById('st-name');
  const names = ["Maria C. (SP)", "Sônia R. (RJ)", "Lúcia T. (MG)", "Aparecida M. (RS)", "Helena S. (PR)", "Fátima V. (SC)", "Neuza B. (GO)"];
  if(socialToast) {
    setInterval(() => {
      stName.innerHTML = <strong></strong>;
      socialToast.classList.add('show');
      if (navigator.vibrate) { try{ navigator.vibrate([30, 50, 30]); } catch(e){} }
      setTimeout(() => { socialToast.classList.remove('show'); }, 6000);
    }, 22000); // 22s interval
  }

  const painList = document.querySelector('.pain-list');
  if(painList) {
    const painItems = painList.querySelectorAll('li');
    const focusObs = new IntersectionObserver(entries => {
      let anyIntersecting = false;
      entries.forEach(e => {
        if(e.isIntersecting) {
          e.target.classList.remove('dimmed');
          anyIntersecting = true;
        } else {
          e.target.classList.add('dimmed');
        }
      });
      if(anyIntersecting) painList.classList.add('focus-active');
      else painList.classList.remove('focus-active');
    }, { rootMargin: "-35% 0px -35% 0px" });
    painItems.forEach(li => focusObs.observe(li));
  }

  const bonusStamp = document.getElementById('bonusStamp');
  if(bonusStamp) {
    const bonusObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if(e.isIntersecting) {
          setTimeout(() => {
            bonusStamp.classList.add('unlocked');
            if(navigator.vibrate) { try{ navigator.vibrate([40, 60, 100]); }catch(e){} }
          }, 300);
          bonusObs.unobserve(bonusStamp);
        }
      });
    }, { threshold: 0.5 });
    bonusObs.observe(bonusStamp);
  }
"""

content = content.replace("</script>\n</body>", new_js + "\n</script>\n</body>")

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modificacoes aplicadas com sucesso.")
