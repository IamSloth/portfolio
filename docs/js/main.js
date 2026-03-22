/* ================================================
   PORTFOLIO — Main JS
   Auto-play frame animation + Parallax + Reveal
   ================================================ */

const FRAME_COUNT = 96;
const FRAME_PATH = 'assets/frames/frame_';

/* ── Frame Sequence ── */
class FrameSequence {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.frames = new Array(FRAME_COUNT);
    this.loaded = 0;
    this.current = 0;
  }

  preload(onProgress) {
    return new Promise(resolve => {
      let done = 0;
      for (let i = 0; i < FRAME_COUNT; i++) {
        const img = new Image();
        img.onload = () => {
          this.frames[i] = img;
          done++;
          this.loaded = done;
          if (onProgress) onProgress(done / FRAME_COUNT);
          if (i === 0) this.draw(0);
          if (done === FRAME_COUNT) resolve();
        };
        img.onerror = () => {
          done++;
          if (done === FRAME_COUNT) resolve();
        };
        img.src = `${FRAME_PATH}${String(i).padStart(4, '0')}.webp`;
      }
    });
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    if (this.frames[this.current]) this.draw(this.current);
  }

  draw(index) {
    const img = this.frames[index];
    if (!img) return;
    this.current = index;

    const { canvas, ctx } = this;
    const cw = canvas.width, ch = canvas.height;
    ctx.clearRect(0, 0, cw, ch);

    // object-fit: cover
    const scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
    const dw = img.naturalWidth * scale;
    const dh = img.naturalHeight * scale;
    ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
  }
}

/* ── Hero Text Split ── */
function splitHeroText() {
  const h1 = document.querySelector('.hero-content h1');
  if (!h1) return;
  const parts = h1.innerHTML.split(/(<span[^>]*>.<\/span>)/);
  let html = '', ci = 0;
  parts.forEach(part => {
    if (part.startsWith('<span')) {
      const ch = part.match(/>(.)<\//)[1];
      html += `<span class="accent char" style="--i:${ci}">${ch}</span>`;
      ci++;
    } else {
      for (const c of part) {
        html += `<span class="char" style="--i:${ci}">${c}</span>`;
        ci++;
      }
    }
  });
  h1.innerHTML = html;
  h1.classList.add('split-ready');
}

/* ── Auto-play Hero Animation (Seamless overlap-blend loop) ── */
function initHeroAutoplay(seq) {
  const FPS = 24;
  const interval = 1000 / FPS;
  const BLEND = 24;                        // overlap zone (frames)
  const CYCLE = FRAME_COUNT - BLEND;       // 72 usable frames per cycle
  let frame = 0, last = 0;

  function drawBlend(idxA, idxB, alpha) {
    // Draw frame A, then frame B on top with alpha
    seq.draw(idxA);
    const img = seq.frames[idxB];
    if (!img) return;
    const { canvas, ctx } = seq;
    const cw = canvas.width, ch = canvas.height;
    ctx.globalAlpha = alpha;
    const s = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
    ctx.drawImage(img, (cw - img.naturalWidth * s) / 2, (ch - img.naturalHeight * s) / 2,
      img.naturalWidth * s, img.naturalHeight * s);
    ctx.globalAlpha = 1;
  }

  function tick(now) {
    if (now - last >= interval) {
      const idx = frame % CYCLE;

      if (idx < BLEND) {
        // Blend zone: tail frame fading out, head frame fading in
        const alpha = idx / BLEND;          // 0→1
        const tailIdx = idx + CYCLE;        // overlapping tail frame (72-95)
        drawBlend(tailIdx, idx, alpha);
      } else {
        seq.draw(idx);
      }

      frame++;
      last = now;
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

/* ── Hero Parallax Fade on Scroll ── */
function initHeroParallax() {
  const content = document.querySelector('.hero-content');
  const indicator = document.querySelector('.scroll-indicator');
  const canvas = document.getElementById('hero-canvas');
  const heroH = window.innerHeight;

  window.addEventListener('scroll', () => {
    const ratio = Math.min(window.scrollY / (heroH * 0.6), 1);
    content.style.opacity = 1 - ratio;
    content.style.transform = `translateY(${ratio * -40}px) scale(${1 - ratio * 0.05})`;
    if (indicator) indicator.style.opacity = 1 - Math.min(ratio * 3, 1);

    // Canvas: dim + subtle zoom as user scrolls away
    if (canvas) {
      canvas.style.opacity = 0.38 * (1 - ratio * 0.6);
      canvas.style.transform = `scale(${1 + ratio * 0.08})`;
    }
  }, { passive: true });
}

/* ── Scroll Reveal ── */
function initReveal() {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}

/* ── Count Up ── */
function initCountUp() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return;
      io.unobserve(el);

      const target = parseFloat(el.dataset.count);
      const dec = parseInt(el.dataset.decimals || '0');
      const dur = 1600;
      const start = performance.now();

      (function tick(now) {
        const p = Math.min((now - start) / dur, 1);
        const ease = 1 - Math.pow(1 - p, 4);
        el.textContent = (target * ease).toFixed(dec);
        if (p < 1) requestAnimationFrame(tick);
      })(start);
    }, { threshold: 0.5 });
    io.observe(el);
  });
}

/* ── Nav scroll state + mobile toggle ── */
function initNav() {
  const nav = document.querySelector('.nav');
  const links = nav.querySelectorAll('.nav-links a');
  const sections = document.querySelectorAll('section[id]');
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  // Mobile menu toggle
  if (toggle) {
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('open');
      navLinks.classList.toggle('open');
    });
    // Close menu on link click
    links.forEach(a => a.addEventListener('click', () => {
      toggle.classList.remove('open');
      navLinks.classList.remove('open');
    }));
  }

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 80);

    // Active section highlight
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 200) current = sec.id;
    });

    // Bottom of page → activate last section (Contact)
    const atBottom = (window.innerHeight + window.scrollY) >= document.body.scrollHeight - 50;
    if (atBottom && sections.length) {
      current = sections[sections.length - 1].id;
    }

    links.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === `#${current}`);
    });
  }, { passive: true });
}

/* ── Scroll Progress Bar ── */
function initScrollProgress() {
  const bar = document.getElementById('scroll-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.transform = `scaleX(${h > 0 ? window.scrollY / h : 0})`;
  }, { passive: true });
}

/* ── Main ── */
async function main() {
  const canvas = document.getElementById('hero-canvas');
  const seq = new FrameSequence(canvas);

  // Loader elements
  const loader = document.getElementById('loader');
  const bar = loader.querySelector('.loader-bar');
  const pct = loader.querySelector('.loader-pct');

  seq.resize();
  window.addEventListener('resize', () => seq.resize());

  // Preload with progress
  await seq.preload(progress => {
    const p = Math.round(progress * 100);
    bar.style.width = p + '%';
    pct.textContent = p;
  });

  // Split hero text before reveal (so chars are ready for animation)
  splitHeroText();

  // Reveal site
  loader.classList.add('done');
  document.body.classList.add('loaded');

  // Remove loader from DOM after animation
  setTimeout(() => loader.remove(), 1200);

  // Init modules
  initHeroAutoplay(seq);
  initHeroParallax();
  initReveal();
  initCountUp();
  initNav();
  initScrollProgress();
}

document.addEventListener('DOMContentLoaded', main);
