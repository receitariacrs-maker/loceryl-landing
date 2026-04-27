
    // ── SCROLL REVEAL com Anime.js ──
    const revealObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const delay = el.classList.contains('reveal-delay-1') ? 40
          : el.classList.contains('reveal-delay-2') ? 80
            : el.classList.contains('reveal-delay-3') ? 120
              : el.classList.contains('reveal-delay-4') ? 160
                : el.classList.contains('reveal-delay-5') ? 200
                  : el.classList.contains('reveal-delay-6') ? 240 : 0;
        anime({ targets: el, opacity: [0, 1], translateY: [16, 0], duration: 420, delay, easing: 'cubicBezier(0.22,1,0.36,1)' });
        revealObs.unobserve(el);
      });
    }, { threshold: 0.04, rootMargin: '0px 0px 0px 0px' });
    document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

    // ── SPOTLIGHT reveal com Anime.js ──
    document.querySelectorAll('.spotlight').forEach((el, i) => {
      anime({ targets: el, opacity: [0, 1], translateX: ['-8%', '0%'], duration: 2200, delay: i * 120, easing: 'easeOutQuart' });
    });

    // ── STAT NUMBERS com Anime.js ──
    const statObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseFloat(el.dataset.target);
        const decimals = parseInt(el.dataset.decimals || '0');
        const suffix = el.dataset.suffix || '';
        const obj = { val: 0 };
        anime({
          targets: obj, val: target, duration: 1800, easing: 'easeOutExpo',
          update() { el.textContent = obj.val.toFixed(decimals) + suffix; }
        });
        statObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    document.querySelectorAll('.stat-number[data-target]').forEach(el => statObs.observe(el));

    // ── 3 PASSOS — sticky desktop / swipe mobile ──
    (function () {
      const outer = document.getElementById('stepsOuter');
      const track = document.getElementById('stepsTrack');
      if (!outer || !track) return;

      const items = track.querySelectorAll('.step-how-item');
      const total = items.length;
      const dots = [0, 1, 2].map(i => document.getElementById('dot-' + i));
      const isDesktop = () => window.innerWidth >= 768;

      let currentStep = 0;
      let shift = 0;

      function getItemWidth() { return items[0].getBoundingClientRect().width + (isDesktop() ? 24 : 16); }

      function applyTransform(s) {
        shift = Math.max(0, Math.min(s, getItemWidth() * (total - 1)));
        track.style.transform = `translateX(-${shift}px)`;
        const active = Math.min(total - 1, Math.round(shift / getItemWidth()));
        currentStep = active;
        dots.forEach((d, i) => d && d.classList.toggle('active', i === active));
      }

      // ── DESKTOP: sticky scroll ──
      function onScrollDesktop() {
        const rect = outer.getBoundingClientRect();
        const outerH = outer.offsetHeight;
        const vh = window.innerHeight;
        const progress = Math.max(0, Math.min(1, -rect.top / (outerH - vh)));
        applyTransform(progress * getItemWidth() * (total - 1));
      }

      // ── MOBILE: swipe livre ──
      let swipeActive = false;
      let swipeStartX = 0;
      let swipeStartShift = 0;

      function snapToStep(step) {
        step = Math.max(0, Math.min(total - 1, step));
        const target = step * getItemWidth();
        const from = shift;
        anime({
          duration: 380, easing: 'cubicBezier(0.22,1,0.36,1)',
          update: a => applyTransform(from + (target - from) * a.progress / 100)
        });
      }

      let swipeStartY = 0;

      track.addEventListener('touchstart', e => {
        if (isDesktop()) return;
        swipeActive = true;
        swipeStartX = e.touches[0].clientX;
        swipeStartY = e.touches[0].clientY;
        swipeStartShift = shift;
      }, { passive: true });

      track.addEventListener('touchmove', e => {
        if (!swipeActive || isDesktop()) return;
        const dx = e.touches[0].clientX - swipeStartX;
        const dy = e.touches[0].clientY - swipeStartY;

        // Se for um movimento horizontal, evitamos que a tela role para baixo
        if (Math.abs(dx) > Math.abs(dy) && e.cancelable) {
          e.preventDefault();
        }

        applyTransform(swipeStartShift - dx);
      }, { passive: false });

      track.addEventListener('touchend', e => {
        if (!swipeActive || isDesktop()) return;
        swipeActive = false;
        const dx = e.changedTouches[0].clientX - swipeStartX;
        if (Math.abs(dx) > 30) snapToStep(currentStep + (dx < 0 ? 1 : -1));
        else snapToStep(currentStep);
      }, { passive: false });

      track.addEventListener('touchcancel', () => { swipeActive = false; }, { passive: true });

      window.addEventListener('scroll', () => { if (isDesktop()) onScrollDesktop(); }, { passive: true });
      if (isDesktop()) onScrollDesktop();
      else applyTransform(0);
    })();

    // ── ÍCONES DOS PASSOS — animação ao toque (mobile) ──
    document.querySelectorAll('.step-how-num').forEach(num => {
      num.addEventListener('pointerdown', () => {
        anime({ targets: num, translateY: -6, scale: 1.1, duration: 200, easing: 'easeOutQuad' });
      }, { passive: true });
      num.addEventListener('pointerup', () => {
        anime({ targets: num, translateY: 0, scale: 1, duration: 300, easing: 'easeOutQuad' });
      }, { passive: true });
      num.addEventListener('pointerleave', () => {
        anime({ targets: num, translateY: 0, scale: 1, duration: 300, easing: 'easeOutQuad' });
      }, { passive: true });
    });

    // ── BOTÃO CTA — feedback tátil + evento Pixel ──
    document.querySelectorAll('.btn-cta').forEach(btn => {
      btn.addEventListener('pointerdown', () => anime({ targets: btn, scale: 0.97, duration: 80, easing: 'easeOutQuad' }));
      btn.addEventListener('pointerup', () => anime({ targets: btn, scale: 1, duration: 180, easing: 'easeOutQuad' }));
      btn.addEventListener('pointerleave', () => anime({ targets: btn, scale: 1, duration: 180, easing: 'easeOutQuad' }));
      btn.addEventListener('click', () => {
        if (typeof fbq !== 'undefined') fbq('track', 'InitiateCheckout');
      });
    });

    // ── WHATSAPP — evento Pixel ──
    const waFloat = document.getElementById('wa-float');
    if (waFloat) {
      waFloat.addEventListener('click', () => {
        if (typeof fbq !== 'undefined') fbq('track', 'Contact');
      });
    }

    // ── HERO: animar elementos na entrada ──
    anime.timeline({ easing: 'cubicBezier(0.22,1,0.36,1)' })
      .add({ targets: '.hero-badge', opacity: [0, 1], translateY: [12, 0], duration: 320 })
      .add({ targets: '.hero h1', opacity: [0, 1], translateY: [16, 0], duration: 360 }, '-=200')
      .add({ targets: '.hero-sub', opacity: [0, 1], translateY: [12, 0], duration: 300 }, '-=220')
      .add({ targets: '.btn-cta', opacity: [0, 1], translateY: [10, 0], duration: 300 }, '-=200')
      .add({ targets: '.btn-micro', opacity: [0, 1], translateY: [8, 0], duration: 260 }, '-=180')
      .add({ targets: '.hero-img-wrap', opacity: [0, 1], translateY: [20, 0], duration: 400 }, '-=200');

    // FAQ
    document.querySelectorAll('.faq-q').forEach(q => {
      q.addEventListener('click', () => {
        const item = q.parentElement;
        const open = item.classList.contains('open');
        document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
        if (!open) item.classList.add('open');
      });
    });

    // Tweaks
    const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
      "primaryColor": "#6B3211",
      "fontDisplay": "'Lora', Georgia, serif",
      "animations": true,
      "compact": true
    }/*EDITMODE-END*/;

    let T = { ...TWEAK_DEFAULTS };

    function applyTweaks() {
      document.documentElement.style.setProperty('--brown-primary', T.primaryColor);
      document.documentElement.style.setProperty('--font-display', T.fontDisplay);
      if (!T.animations) document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
      const pad = T.compact ? '32px 0' : '';
      document.querySelectorAll('.section,.hero,.final-cta,.urgency-bar,.stats-bar,.showcase-section').forEach(el => el.style.padding = pad ? pad : '');
    }

    window.addEventListener('message', e => {
      if (e.data?.type === '__activate_edit_mode') document.getElementById('tweaks-panel').style.display = 'block';
      if (e.data?.type === '__deactivate_edit_mode') document.getElementById('tweaks-panel').style.display = 'none';
    });
    window.parent.postMessage({ type: '__edit_mode_available' }, '*');

    document.getElementById('tw-primary').addEventListener('input', e => {
      T.primaryColor = e.target.value; applyTweaks();
      window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { primaryColor: T.primaryColor } }, '*');
    });
    document.getElementById('tw-font-display').addEventListener('change', e => {
      T.fontDisplay = e.target.value; applyTweaks();
      window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { fontDisplay: T.fontDisplay } }, '*');
    });

    const animSw = document.getElementById('tw-anim');
    animSw.addEventListener('click', () => { T.animations = !T.animations; animSw.classList.toggle('on', T.animations); applyTweaks(); window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { animations: T.animations } }, '*'); });

    const compSw = document.getElementById('tw-compact');
    compSw.addEventListener('click', () => { T.compact = !T.compact; compSw.classList.toggle('on', T.compact); applyTweaks(); window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { compact: T.compact } }, '*'); });

    document.getElementById('tw-close').addEventListener('click', () => { document.getElementById('tweaks-panel').style.display = 'none'; window.parent.postMessage({ type: '__edit_mode_dismissed' }, '*'); });

    applyTweaks();

    // Countdown — 2h session timer, resets each visit
    (function () {
      const KEY = 'lv_cd_end';
      let end = parseInt(sessionStorage.getItem(KEY) || '0');
      if (!end || end < Date.now()) { end = Date.now() + 2 * 60 * 60 * 1000; sessionStorage.setItem(KEY, end); }
      function tick() {
        const diff = Math.max(0, end - Date.now());
        const h = String(Math.floor(diff / 3600000)).padStart(2, '0');
        const m = String(Math.floor((diff % 3600000) / 60000)).padStart(2, '0');
        const s = String(Math.floor((diff % 60000) / 1000)).padStart(2, '0');
        document.getElementById('cd-h').textContent = h;
        document.getElementById('cd-m').textContent = m;
        document.getElementById('cd-s').textContent = s;
      }
      tick(); setInterval(tick, 1000);
    })();
    // PARALLAX ANIMATION NOS ÍCONES DE DOR
    const painIcons = document.querySelectorAll('.pain-img');
    window.addEventListener('scroll', () => {
      painIcons.forEach((img, index) => {
        const rect = img.parentElement.getBoundingClientRect();
        // Anima apenas se o elemento estiver na tela
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          const scrollPercent = (window.innerHeight - rect.top) / window.innerHeight;
          // Distância de movimento do scroll (mais suave no translateY)
          const yMove = (scrollPercent * 30) - 15;
          const rotate = index % 2 === 0 ? (scrollPercent * 15 - 7.5) : (scrollPercent * -15 + 7.5);
          img.style.transform = `translateY(${yMove}px) rotate(${rotate}deg) scale(1.15)`;
        }
      });
    }, { passive: true });

    // BA SLIDER
    const baSlider = document.getElementById('baSlider');
    if (baSlider) {
      const baAfter = document.getElementById('baAfterImg');
      const baHandle = document.getElementById('baHandle');
      baSlider.addEventListener('input', (e) => {
        const val = e.target.value;
        baAfter.style.clipPath = `inset(0 0 0 ${val}%)`;
        baHandle.style.left = `${val}%`;
      });
    }

    // HIGHLIGHT MARKERS
    const hlObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('active');
        }
      });
    }, { threshold: 1 });
    document.querySelectorAll('.highlight-marker').forEach(el => hlObs.observe(el));

    // WA REACTIONS
    const reactions = ['❤️', '👍', '😍', '🔥'];
    const waBox = document.getElementById('waReactions');
    if (waBox) {
      const waObs = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
          let count = 0;
          const interval = setInterval(() => {
            if (count > 6) { clearInterval(interval); return; }
            const el = document.createElement('div');
            el.className = 'wa-reaction';
            el.textContent = reactions[Math.floor(Math.random() * reactions.length)];
            el.style.left = `${Math.random() * 30 - 15}px`;
            waBox.appendChild(el);
            setTimeout(() => el.remove(), 2500);
            count++;
          }, 800);
          waObs.disconnect();
        }
      }, { threshold: 0.5 });
      waObs.observe(waBox);
    }

    // GUARANTEE PARTICLES
    const gb = document.querySelector('.guarantee-box');
    if (gb) {
      for (let i = 0; i < 12; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.width = Math.random() * 5 + 3 + 'px';
        p.style.height = p.style.width;
        p.style.left = Math.random() * 100 + '%';
        p.style.bottom = Math.random() * 20 - 10 + '%';
        p.style.animationDuration = Math.random() * 3 + 3 + 's';
        p.style.animationDelay = Math.random() * 2 + 's';
        gb.appendChild(p);
      }
    }

    // STEPS PROGRESS BAR
    const pBar = document.getElementById('stepsProgressBar');
    if (pBar) {
      const outer = document.getElementById('stepsOuter');
      window.addEventListener('scroll', () => {
        const rect = outer.getBoundingClientRect();
        const outerH = outer.offsetHeight;
        const vh = window.innerHeight;
        const progress = Math.max(0, Math.min(1, -rect.top / (outerH - vh)));
        pBar.style.width = (progress * 100) + '%';
      }, { passive: true });
    }

    // TOP PAGE PROGRESS
    const topBar = document.getElementById('page-progress-bar');
    window.addEventListener('scroll', () => {
      const scrollPos = window.scrollY;
      const height = document.body.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollPos / height) * 100;
      if (topBar) topBar.style.width = scrollPercent + '%';
    }, { passive: true });

    // HERO PARALLAX ASSETS
    const hl = document.querySelector('.hero-lemon');
    const hg = document.querySelector('.hero-garlic');
    window.addEventListener('scroll', () => {
      const s = window.scrollY;
      if (hl) hl.style.transform = `translateY(${s * -0.2}px) rotate(${25 + (s * 0.05)}deg)`;
      if (hg) hg.style.transform = `translateY(${s * -0.15}px) rotate(${-15 - (s * 0.03)}deg)`;
    }, { passive: true });

    // DRAW SVG CHECKMARKS
    const drawObs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          setTimeout(() => e.target.classList.add('active'), 200);
        }
      });
    }, { threshold: 1 });
    document.querySelectorAll('.draw-check').forEach(el => drawObs.observe(el));

    // BONUS CARD 3D TILT
    document.querySelectorAll('.bonus-card').forEach(card => {
      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const midX = rect.width / 2;
        const midY = rect.height / 2;
        const rotateX = ((y - midY) / midY) * -8;
        const rotateY = ((x - midX) / midX) * 8;
        card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = `perspective(800px) rotateX(0) rotateY(0) scale(1)`;
      });
    });
  
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

  const stickyCta = document.getElementById('sticky-cta');
  const heroSec = document.getElementById('hero-sec');

  window.addEventListener('scroll', () => {
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
      stName.innerHTML = `<strong>${names[Math.floor(Math.random()*names.length)]}</strong>`;
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

